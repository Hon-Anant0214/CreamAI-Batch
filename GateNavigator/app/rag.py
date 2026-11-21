from app.llm import generate_response
from app.vectorstore import search_documents

SYSTEM_PROMPT = """
You are GATENavigator, an AI assistant that helps students
prepare for the GATE examination.

Answer questions using ONLY the retrieved document context.

Instructions:
1. Use the provided context to answer the question.
2. Do not invent facts or information.
3. If the context does not contain the answer, respond exactly:
   I don't know
4. Keep explanations clear and student-friendly.
5. Cite your sources using the document filename and page number.
6. Use this citation format: [Source: filename, Page: number]
7. Include citations for factual information.
"""


def retrieve_context(question, top_k=5):
    """Retrieve relevant chunks and prioritize the matching syllabus."""

    # First search using the original question.
    initial_results = search_documents(question, top_k=10)

    # Identify the paper code from a matching paper record.
    paper_code = None

    for result in initial_results:
        metadata = result["metadata"]

        if metadata.get("source") == "records.json":
            paper_code = metadata.get("paper_code")
            if paper_code:
                break

    # If a paper code is found, perform an expanded search.
    if paper_code:
        expanded_query = (
            f"GATE {paper_code} Computer Science Information Technology syllabus topics"
            if paper_code == "CS"
            else f"GATE {paper_code} syllabus topics"
        )

        expanded_results = search_documents(expanded_query, top_k=10)

        # Put the matching syllabus PDF first.
        matching_pdf = [
            r
            for r in expanded_results
            if r["metadata"].get("source", "").startswith(f"{paper_code}_")
        ]

        other_results = [r for r in expanded_results if r not in matching_pdf]

        results = matching_pdf + other_results

    else:
        results = initial_results

    results = results[:top_k]

    context_parts = []
    citations = []

    for result in results:
        metadata = result["metadata"]

        source = metadata.get("source", "Unknown")
        page = metadata.get("page", "Unknown")
        title = metadata.get("title", "Unknown")

        context_parts.append(
            f"Document: {source}\n"
            f"Title: {title}\n"
            f"Page: {page}\n"
            f"Content: {result['text']}"
        )

        citation = {"source": source, "page": page, "title": title}

        if citation not in citations:
            citations.append(citation)

    context = "\n\n".join(context_parts)

    return context, citations, len(results)


def answer_question(question, top_k=5):
    """Generate a grounded answer with document citations."""

    context, citations, retrieved_count = retrieve_context(question, top_k=top_k)

    user_prompt = f"""
Retrieved document context:

{context}

Student question:
{question}

Answer using the retrieved context.
If the answer is unavailable, respond exactly:
I don't know
"""

    answer = generate_response(SYSTEM_PROMPT, user_prompt).strip()

    # Do not attach citations to an unanswerable response.
    if answer.lower() == "i don't know":
        answer = "I don't know"
        citations = []

    return {
        "question": question,
        "answer": answer,
        "citations": citations,
        "retrieved_chunks": retrieved_count,
    }


if __name__ == "__main__":
    question = "What topics are included in the Computer Science syllabus?"

    print("Question:", question)

    result = answer_question(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nCitations:")

    for citation in result["citations"]:
        print(f"- {citation['source']}, Page {citation['page']}")

    print("\nRetrieved chunks:", result["retrieved_chunks"])
