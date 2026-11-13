import json
from pathlib import Path
from app.llm import generate_response
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.smart_search import smart_search

from app.records import load_records, search, get_by_id

app = FastAPI(title="GATENavigator API")


class QuestionRequest(BaseModel):
    question: str
class ChatRequest(BaseModel):
    question: str
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

    system_prompt = load_prompt("system_prompt.txt")

    user_prompt = f"""
    Student question: {request.question}

    Answer the student as GATENavigator.
    Return only valid JSON with answer, confidence, and follow_up.
    """

    response = generate_response(system_prompt, user_prompt)

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