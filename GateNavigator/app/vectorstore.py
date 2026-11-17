
import json
from pathlib import Path
import chromadb

from app.chunking import chunk_pdf
from app.embed import generate_embeddings


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FOLDER = BASE_DIR / "Data" / "Raw"
RECORDS_FILE = BASE_DIR / "Data" / "records.json"
DB_FOLDER = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_FOLDER))

collection = client.get_or_create_collection(
    name="gatenavigator_documents",
    metadata={"hnsw:space": "cosine"}
)


def load_all_chunks(chunk_size=500, overlap=100):
    all_chunks = []

    # Load PDF documents
    for pdf_file in RAW_FOLDER.glob("*.pdf"):
        all_chunks.extend(
            chunk_pdf(
                pdf_file,
                chunk_size=chunk_size,
                overlap=overlap
            )
        )

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

            all_chunks.append({
                "text": text,
                "metadata": {
                    "source": "records.json",
                    "page": "N/A",
                    "title": "GATE Paper Records",
                    "paper_code": str(record.get("paper_code", ""))
                }
            })

    return all_chunks


def index_documents(chunk_size=500, overlap=100):
    global collection

    print("Loading PDF documents and paper records...")

    chunks = load_all_chunks(
        chunk_size=chunk_size,
        overlap=overlap
    )

    if not chunks:
        print("No document chunks found.")
        return

    texts = [chunk["text"] for chunk in chunks]
    documents = texts
    metadatas = [chunk["metadata"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = generate_embeddings(texts)

    ids = []

    for i, chunk in enumerate(chunks):
        if chunk["metadata"]["source"] == "records.json":
            paper_code = chunk["metadata"]["paper_code"]
            ids.append(f"record_{paper_code}")
        else:
            ids.append(f"pdf_chunk_{i}")

    # Recreate the collection
    client.delete_collection(
        name="gatenavigator_documents"
    )

    collection = client.get_or_create_collection(
        name="gatenavigator_documents",
        metadata={"hnsw:space": "cosine"}
    )

    print("Saving documents to ChromaDB...")

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist()
    )

    print("Indexing completed!")
    print("Total indexed chunks:", collection.count())


def search_documents(question, top_k=5):
    question_embedding = generate_embeddings([question])

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    search_results = []

    for i in range(len(results["ids"][0])):
        search_results.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "similarity": 1 - results["distances"][0][i]
        })

    return search_results


if __name__ == "__main__":
    index_documents()

    question = "What is the paper code for Computer Science and Information Technology?"

    print("\nSearching:", question)

    results = search_documents(question)

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}")
        print("Similarity:", round(result["similarity"], 4))
        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Title:", result["metadata"]["title"])
        print("Text:", result["text"][:250])
