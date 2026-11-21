from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_records_endpoint():
    response = client.get("/records")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_records_limit():
    response = client.get("/records?limit=3")

    assert response.status_code == 200
    assert len(response.json()) <= 3


def test_get_existing_record():
    response = client.get("/records/CS")

    assert response.status_code == 200
    assert response.json()["paper_code"] == "CS"


def test_get_missing_record():
    response = client.get("/records/INVALID")

    assert response.status_code == 404


def test_search_endpoint():
    response = client.get("/search?q=Computer")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ask_endpoint_with_fake_llm(monkeypatch):
    fake_result = {
        "question": "What is GATE CS?",
        "answer": "GATE CS is a Computer Science paper.",
        "citations": [
            {
                "source": "CS_syllabus.pdf",
                "page": 1,
                "title": "Computer Science Syllabus",
            }
        ],
        "retrieved_chunks": 2,
    }

    def fake_answer_question(question):
        return fake_result

    monkeypatch.setattr(main, "answer_question", fake_answer_question)

    response = client.post("/ask", json={"question": "What is GATE CS?"})

    assert response.status_code == 200
    assert response.json()["answer"] == ("GATE CS is a Computer Science paper.")
    assert response.json()["retrieved_chunks"] == 2
    assert len(response.json()["citations"]) == 1
