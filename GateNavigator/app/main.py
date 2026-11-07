
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.smart_search import smart_search

from app.records import load_records, search, get_by_id

app = FastAPI(title="GATENavigator API")


class QuestionRequest(BaseModel):
    question: str


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
