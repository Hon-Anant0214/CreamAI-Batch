
from pathlib import Path
import chromadb

from app.chunking import chunk_pdf
from app.embed import generate_embeddings


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FOLDER = BASE_DIR / "Data" / "Raw"
DB_FOLDER = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_FOLDER))

collection = client.get_or_create_collection(
    name="gatenavigator_documents",
    metadata={"hnsw:space": "cosine"}
)


def load_all_chunks():
    all_chunks = []

    for pdf_file in RAW_FOLDER.glob("*.pdf"):
        all_chunks.extend(chunk_pdf(pdf_file))

    return all_chunks


def index_documents():
    print("Loading PDF documents...")
    chunks = load_all_chunks()

    if not chunks:
        print("No document chunks found.")
        return

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = generate_embeddings(texts)

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

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
        n_results=top_k,
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

    question = "What topics are included in the Computer Science syllabus?"

    print("\nSearching:", question)

    results = search_documents(question)

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}")
        print("Similarity:", round(result["similarity"], 4))
        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Title:", result["metadata"]["title"])
        print("Text:", result["text"][:250])
