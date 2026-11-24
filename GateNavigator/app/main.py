import json
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from langgraph.types import Command
from pydantic import BaseModel, Field

from app.graph import agent_graph
from app.llm import generate_response
from app.rag import answer_question
from app.records import get_by_id, load_records
from app.smart_search import smart_search
from app.vectorstore import search_documents

app = FastAPI(title="GATENavigator API")

# ---------------------------------
# Request Models
# ---------------------------------


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Student question (maximum 2000 characters)",
    )


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Student question (maximum 2000 characters)",
    )
    task: Literal["explain", "syllabus"] = "syllabus"
    prompt_version: Literal["v1", "v2"] = "v2"


class AgentRequest(BaseModel):
    question: str | None = Field(default=None, max_length=2000)
    marks_data: dict[str, int] | None = None
    thread_id: str = "gate-api-session-1"
    approval: bool | None = None
# ---------------------------------
# Paths and Prompt Loading
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = BASE_DIR / "prompts"


def load_prompt(filename):
    prompt_path = PROMPT_DIR / filename

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


# ---------------------------------
# Health Endpoint
# ---------------------------------


@app.get("/health")
def health():
    return {"status": "ok", "message": "GATENavigator API is running"}


# ---------------------------------
# Records Endpoints
# ---------------------------------


@app.get("/records")
def get_records(limit: int = 28):
    records = load_records()
    return records[:limit]


@app.get("/records/{id}")
def get_record(id: str):
    records = load_records()
    record = get_by_id(records, id)

    if record is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return record


# ---------------------------------
# Search Endpoints
# ---------------------------------


@app.get("/search")
def search_records(q: str):
    records = load_records()
    results = smart_search(records, q)
    return results


@app.get("/search/semantic")
def semantic_search_api(q: str):
    try:
        results = search_documents(q)

        return {"question": q, "total_results": len(results), "results": results}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {e!s}",
        ) from e


# ---------------------------------
# Questions Endpoint
# ---------------------------------


@app.post("/questions")
def ask_question(request: QuestionRequest):
    return {
        "status": "received",
        "question": request.question,
        "message": "Your question has been received.",
    }


# ---------------------------------
# Chat Endpoint
# ---------------------------------


@app.post("/chat")
def chat(request: ChatRequest):

    if request.prompt_version == "v1":
        system_prompt = load_prompt("system_prompt_v1.txt")
    else:
        system_prompt = load_prompt("system_prompt.txt")

    if request.task == "explain":
        task_prompt = load_prompt("explain_topic.txt")

        user_prompt = task_prompt.format(topic=request.question)

    else:
        task_prompt = load_prompt("syllabus_help.txt")

        records = load_records()

        context = "\n".join(
            [
                f"Paper Code: {r['paper_code']}, "
                f"Paper Name: {r['paper_name']}, "
                f"GA Marks: {r['ga_marks']}, "
                f"Subject Marks: {r['subject_marks']}, "
                f"Syllabus Sections: {r['syllabus_sections']}, "
                f"Syllabus URL: {r['syllabus_url']}"
                for r in records
            ]
        )

        user_prompt = task_prompt.format(question=request.question, context=context)

    response = generate_response(system_prompt, user_prompt)

    try:
        result = json.loads(response)

        return {
            "answer": result["answer"],
            "confidence": result["confidence"],
            "follow_up": result["follow_up"],
        }

    except (json.JSONDecodeError, KeyError, TypeError):
        return {"answer": response, "confidence": 0.5, "follow_up": None}


# ---------------------------------
# RAG Endpoint
# ---------------------------------


@app.post("/ask")
def ask_rag_question(request: QuestionRequest):
    try:
        result = answer_question(request.question)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG question answering failed: {e!s}",
        ) from e


# ---------------------------------
# LangGraph Agent Endpoint
# ---------------------------------


@app.post("/agent")
def run_agent(request: AgentRequest):

    config = {"configurable": {"thread_id": request.thread_id}}

    try:
        # Resume after student approval or rejection
        if request.approval is not None:
            response = agent_graph.invoke(
                Command(resume=request.approval), config=config
            )

        else:
            if not request.question:
                raise HTTPException(
                    status_code=400,
                    detail="Question is required for a new agent request.",
                )

            response = agent_graph.invoke(
                {"question": request.question, "marks_data": request.marks_data or {}},
                config=config,
            )

        # Check whether the graph is waiting for approval
        if "__interrupt__" in response:
            approval_request = response["__interrupt__"][0].value

            return {
                "status": "approval_required",
                "thread_id": request.thread_id,
                "approval_request": approval_request,
            }

        return {
            "status": "completed",
            "thread_id": request.thread_id,
            "result": response.get("result"),
            "history": response.get("history", []),
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {e!s}",
        ) from e
