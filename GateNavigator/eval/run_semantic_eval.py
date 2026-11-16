
from pathlib import Path

from app.semantic_search import load_all_chunks, semantic_search
from app.embed import generate_embeddings


QUESTIONS = [
    "What GATE 2027 papers are available in GATENavigator?",
    "What is the paper code for Computer Science and Information Technology?",
    "How many marks are allocated to General Aptitude and the subject section in GATE?",
    "Show me the details of the Computer Science (CS) paper.",
    "What is the syllabus PDF link for Data Science and Artificial Intelligence (DA)?",
    "What was the official GATE 2027 cutoff score for Computer Science and Information Technology?",
    "Find the GATE paper with the code AE.",
    "How many GATE papers are currently stored in GATENavigator?",
    "What is the paper code for Electronics and Communication Engineering?",
    "Can you show me the syllabus URL for Aerospace Engineering?"
]


def main():
    print("Loading documents...")
    chunks = load_all_chunks()
    print("Total chunks:", len(chunks))

    print("\nGenerating document embeddings...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    output = [
        "# GATENavigator Semantic Search Evaluation",
        "",
        "Evaluation of semantic search using 10 GATE questions.",
        ""
    ]

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nTesting Q{number}: {question}")

        results = semantic_search(
            question, chunks, embeddings, top_k=3
        )

        output.extend([
            f"## Q{number}: {question}",
            ""
        ])

        for rank, result in enumerate(results, start=1):
            metadata = result["metadata"]

            output.extend([
                f"### Result {rank}",
                f"- Similarity: {result['similarity']:.4f}",
                f"- Source: {metadata['source']}",
                f"- Page: {metadata['page']}",
                f"- Title: {metadata['title']}",
                f"- Text: {result['text'][:300]}",
                ""
            ])

    project_root = Path(__file__).resolve().parent.parent
    output_file = project_root / "eval" / "search_results.md"
    output_file.write_text("\n".join(output), encoding="utf-8")

    print("\nEvaluation completed!")
    print("Results saved to:", output_file)


if __name__ == "__main__":
    main()
