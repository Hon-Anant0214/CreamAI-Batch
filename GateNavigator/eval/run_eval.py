
import json
import re
from pathlib import Path

from app.vectorstore import index_documents
from app.rag import answer_question


BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_FILE = BASE_DIR / "eval" / "eval_set.json"
OUTPUT_FILE = BASE_DIR / "eval" / "eval_results.json"

CONFIGS = [
    {
        "name": "Configuration A",
        "chunk_size": 500,
        "overlap": 100,
        "top_k": 3
    },
    {
        "name": "Configuration B",
        "chunk_size": 800,
        "overlap": 150,
        "top_k": 5
    }
]

STOP_WORDS = {
    "the", "is", "a", "an", "and", "or", "to", "of",
    "in", "for", "on", "are", "what", "which", "that",
    "has", "have", "with", "currently", "does", "do",
    "me", "show", "stored", "paper", "record"
}


def get_keywords(text):
    """Extract meaningful keywords from expected answers."""

    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    }


def calculate_keyword_coverage(expected, actual):
    """Measure how many expected keywords appear in the answer."""

    expected_keywords = get_keywords(expected)

    if not expected_keywords:
        return 0.0

    actual_keywords = get_keywords(actual)

    matched = expected_keywords.intersection(actual_keywords)

    return round(len(matched) / len(expected_keywords), 2)


def run_configuration(config, questions):

    print("\n" + "=" * 60)
    print("Running:", config["name"])
    print("Chunk size:", config["chunk_size"])
    print("Overlap:", config["overlap"])
    print("Top-K:", config["top_k"])
    print("=" * 60)

    # Rebuild the vector database for this configuration.
    index_documents(
        chunk_size=config["chunk_size"],
        overlap=config["overlap"]
    )

    question_results = []

    for item in questions:

        question_id = item["id"]
        question = item["question"]

        print(f"\nTesting Q{question_id}: {question}")

        try:
            result = answer_question(
                question,
                top_k=config["top_k"]
            )

            answer = result["answer"]

            citations = result["citations"]

            if item["answerable"]:

                keyword_coverage = calculate_keyword_coverage(
                    item["expected_answer"],
                    answer
                )

                expected_source = item["expected_source"]

                source_hit = any(
                    citation["source"] == expected_source
                    for citation in citations
                ) if expected_source else None

                exact_unknown = None

            else:

                keyword_coverage = None
                source_hit = None

                exact_unknown = (
                    answer.strip() == "I don't know"
                )

            question_result = {
                "id": question_id,
                "question": question,
                "expected_answer": item["expected_answer"],
                "actual_answer": answer,
                "citations": citations,
                "retrieved_chunks": result["retrieved_chunks"],
                "keyword_coverage": keyword_coverage,
                "source_hit": source_hit,
                "exact_unknown": exact_unknown
            }

            print("Answer:", answer[:200])
            print("Citations:", citations)

        except Exception as error:

            print("Evaluation error:", str(error))

            question_result = {
                "id": question_id,
                "question": question,
                "error": str(error)
            }

        question_results.append(question_result)

        # Save progress after every question.
        save_progress(config, question_results)

    return question_results


def calculate_metrics(results, questions):

    answerable_results = [
        r for r in results
        if r.get("keyword_coverage") is not None
    ]

    source_results = [
        r for r in results
        if r.get("source_hit") is not None
    ]

    unknown_results = [
        r for r in results
        if r.get("exact_unknown") is not None
    ]

    avg_keyword_coverage = (
        sum(r["keyword_coverage"] for r in answerable_results)
        / len(answerable_results)
        if answerable_results else 0
    )

    source_hit_rate = (
        sum(r["source_hit"] for r in source_results)
        / len(source_results)
        if source_results else 0
    )

    unknown_accuracy = (
        sum(r["exact_unknown"] for r in unknown_results)
        / len(unknown_results)
        if unknown_results else 0
    )

    combined_score = (
        avg_keyword_coverage
        + source_hit_rate
        + unknown_accuracy
    ) / 3

    return {
        "average_keyword_coverage": round(avg_keyword_coverage, 3),
        "source_hit_rate": round(source_hit_rate, 3),
        "unanswerable_accuracy": round(unknown_accuracy, 3),
        "combined_score": round(combined_score, 3),
        "questions_completed": len(results),
        "total_questions": len(questions)
    }


def save_progress(config, results):

    output = {
        "configuration": config,
        "results": results
    }

    progress_file = (
        BASE_DIR / "eval" /
        f"{config['name'].replace(' ', '_').lower()}_progress.json"
    )

    with open(progress_file, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)


def main():

    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    print("GATENavigator RAG Evaluation")
    print("Total evaluation questions:", len(questions))

    all_results = []

    for config in CONFIGS:

        results = run_configuration(config, questions)

        metrics = calculate_metrics(results, questions)

        all_results.append({
            "configuration": config,
            "metrics": metrics,
            "results": results
        })

        print("\nConfiguration metrics:")
        print(json.dumps(metrics, indent=4))

    # Save final evaluation results.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_results, file, indent=4, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("FINAL CONFIGURATION COMPARISON")
    print("=" * 60)

    for result in all_results:

        config = result["configuration"]
        metrics = result["metrics"]

        print("\n", config["name"])
        print("Chunk size:", config["chunk_size"])
        print("Top-K:", config["top_k"])
        print("Keyword coverage:", metrics["average_keyword_coverage"])
        print("Source hit rate:", metrics["source_hit_rate"])
        print("Unanswerable accuracy:", metrics["unanswerable_accuracy"])
        print("Combined score:", metrics["combined_score"])

    winner = max(
        all_results,
        key=lambda x: x["metrics"]["combined_score"]
    )

    print("\nWinning configuration:", winner["configuration"]["name"])
    print("Results saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
