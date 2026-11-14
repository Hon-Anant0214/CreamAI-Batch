import json
from pathlib import Path
from app.llm import generate_response
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.smart_search import smart_search
from typing import Literal

from app.records import load_records, search, get_by_id

app = FastAPI(title="GATENavigator API")


class QuestionRequest(BaseModel):
    question: str
class ChatRequest(BaseModel):
    question: str
    task: Literal["explain", "syllabus"] = "syllabus"
    prompt_version: Literal["v1", "v2"] = "v2"
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = BASE_DIR / "prompts"


def load_prompt(filename):
    prompt_path = PROMPT_DIR / filename

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()
        
@app.get("/health")
def health():
    return {"status": "ok", "message": "GATENavigator API is running"}


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


@app.get("/search")
def search_records(q: str):
    records = load_records()
    results = smart_search(records, q)
    return results


@app.post("/questions")
def ask_question(request: QuestionRequest):
    return {
        "status": "received",
        "question": request.question,
        "message": "Your question has been received."
    }

@app.post("/chat")
def chat(request: ChatRequest):

    # Load the main GATENavigator system prompt
    # Select system prompt based on prompt version
    if request.prompt_version == "v1":
        system_prompt = load_prompt("system_prompt_v1.txt")
    else:
        system_prompt = load_prompt("system_prompt.txt")

    # Select the appropriate task prompt
    if request.task == "explain":

        task_prompt = load_prompt("explain_topic.txt")

        user_prompt = task_prompt.format(
            topic=request.question
        )

    else:

        task_prompt = load_prompt("syllabus_help.txt")

        # Load available GATE paper records
        records = load_records()

        # Prepare records as context for the LLM
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

        user_prompt = task_prompt.format(
            question=request.question,
            context=context
        )

    # Generate response using Groq
    response = generate_response(
        system_prompt,
        user_prompt
    )

    # Convert LLM response into JSON
    try:
        result = json.loads(response)

        return {
            "answer": result["answer"],
            "confidence": result["confidence"],
            "follow_up": result["follow_up"]
        }

    except (json.JSONDecodeError, KeyError, TypeError):
        return {
            "answer": response,
            "confidence": 0.5,
            "follow_up": None
        }
