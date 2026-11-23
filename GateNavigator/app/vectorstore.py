
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.chunking import chunk_pdf

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FOLDER = BASE_DIR / "Data" / "Raw"
RECORDS_FILE = BASE_DIR / "Data" / "records.json"

# Cached document chunks and TF-IDF matrix
_chunks = []
_vectorizer = None
_tfidf_matrix = None


def load_all_chunks():
    """Load PDF chunks and GATE paper records."""

    all_chunks = []

    # Load PDF documents
    for pdf_file in RAW_FOLDER.glob("*.pdf"):
        all_chunks.extend(chunk_pdf(pdf_file))

    # Load GATE paper records
    if RECORDS_FILE.exists():
        with open(RECORDS_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)

        for record in records:
            text = (
                f"Paper Code: {record.get('paper_code', '')}\n"
                f"Paper Name: {record.get('paper_name', '')}\n"
                f"General Aptitude Marks: {record.get('ga_marks', '')}\n"
                f"Subject Marks: {record.get('subject_marks', '')}\n"
                f"Syllabus Sections: {record.get('syllabus_sections', '')}\n"
                f"Syllabus URL: {record.get('syllabus_url', '')}"
            )

            all_chunks.append(
                {
                    "text": text,
                    "metadata": {
                        "source": "records.json",
                        "page": "N/A",
                        "title": "GATE Paper Records",
                        "paper_code": str(record.get("paper_code", "")),
                    },
                }
            )

    return all_chunks


def build_index():
    """Build the TF-IDF index once and cache it."""

    global _chunks, _vectorizer, _tfidf_matrix

    if _tfidf_matrix is not None:
        return

    print("Loading PDF documents and GATE records...")

    _chunks = load_all_chunks()

    if not _chunks:
        print("No document chunks found.")
        _vectorizer = None
        _tfidf_matrix = None
        return

    documents = [chunk["text"] for chunk in _chunks]

    print("Building TF-IDF index...")

    _vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=20000,
    )

    _tfidf_matrix = _vectorizer.fit_transform(documents)

    print("Indexing completed!")
    print("Total indexed chunks:", len(_chunks))


def search_documents(question, top_k=5):
    """Retrieve relevant chunks using TF-IDF and cosine similarity."""

    build_index()

    if _tfidf_matrix is None or not question.strip():
        return []

    question_vector = _vectorizer.transform([question])

    scores = cosine_similarity(
        question_vector,
        _tfidf_matrix,
    ).flatten()

    top_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:
        if scores[index] <= 0:
            continue

        results.append(
            {
                "text": _chunks[index]["text"],
                "metadata": _chunks[index]["metadata"],
                "similarity": float(scores[index]),
            }
        )

    return results


if __name__ == "__main__":
    question = (
        "What is the paper code for Computer Science "
        "and Information Technology?"
    )

    print("\nSearching:", question)

    results = search_documents(question)

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}")
        print("Similarity:", round(result["similarity"], 4))
        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Title:", result["metadata"]["title"])
        print("Text:", result["text"][:250])
