from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

from app.chunking import chunk_pdf
from app.embed import generate_embeddings


def load_all_chunks():

    raw_folder = Path(__file__).resolve().parent.parent / "Data" / "Raw"

    all_chunks = []

    for pdf_file in raw_folder.glob("*.pdf"):
        chunks = chunk_pdf(pdf_file)
        all_chunks.extend(chunks)

    return all_chunks


def semantic_search(question, chunks, chunk_embeddings, top_k=5):

    # Generate embedding for the user question
    question_embedding = generate_embeddings([question])

    # Calculate cosine similarity
    similarities = cosine_similarity(question_embedding, chunk_embeddings)[0]

    # Get indices of the most relevant chunks
    top_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append(
            {
                "text": chunks[index]["text"],
                "metadata": chunks[index]["metadata"],
                "similarity": float(similarities[index]),
            }
        )

    return results


if __name__ == "__main__":
    print("Loading PDF documents...")

    chunks = load_all_chunks()

    print("Total chunks:", len(chunks))

    texts = [chunk["text"] for chunk in chunks]

    print("\nGenerating document embeddings...")

    chunk_embeddings = generate_embeddings(texts)

    question = "What topics are included in the Computer Science syllabus?"

    print("\nSearching for:", question)

    results = semantic_search(question, chunks, chunk_embeddings, top_k=5)

    print("\nTop 5 Search Results:")

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}")
        print("Similarity:", round(result["similarity"], 4))
        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Title:", result["metadata"]["title"])
        print("Text:", result["text"][:250])
