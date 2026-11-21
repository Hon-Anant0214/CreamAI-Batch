print("GATENavigator evaluation script started!")
import csv
import json

import requests

# GATENavigator API endpoint
API_URL = "http://127.0.0.1:8000/chat"

# The exact 10 questions from Data/user_questions.md
questions = [
    "What GATE 2027 papers are available in GATENavigator?",
    "What is the paper code for Computer Science and Information Technology?",
    "How many marks are allocated to General Aptitude and the subject section in GATE?",
    "Show me the details of the Computer Science (CS) paper.",
    "What is the syllabus PDF link for Data Science and Artificial Intelligence (DA)?",
    "What was the official GATE 2027 cutoff score for Computer Science and Information Technology?",
    "Find the GATE paper with the code AE.",
    "How many GATE papers are currently stored in GATENavigator?",
    "What is the paper code for Electronics and Communication Engineering?",
    "Can you show me the syllabus URL for Aerospace Engineering?",
]

results = []

print("\nStarting GATENavigator Prompt Evaluation...\n")

# Test all questions with both prompt versions
for index, question in enumerate(questions, start=1):
    print(f"\nTesting Q{index}: {question}")

    for version in ["v1", "v2"]:
        payload = {"question": question, "task": "syllabus", "prompt_version": version}

        try:
            response = requests.post(API_URL, json=payload, timeout=120)

            response.raise_for_status()
            data = response.json()

            result = {
                "question_id": f"Q{index}",
                "question": question,
                "prompt_version": version,
                "answer": data.get("answer", ""),
                "confidence": data.get("confidence", ""),
                "follow_up": data.get("follow_up", ""),
                "status": "Success",
            }

        except requests.RequestException as error:
            result = {
                "question_id": f"Q{index}",
                "question": question,
                "prompt_version": version,
                "answer": "",
                "confidence": "",
                "follow_up": "",
                "status": f"Failed: {error}",
            }

        except (ValueError, TypeError) as error:
            result = {
                "question_id": f"Q{index}",
                "question": question,
                "prompt_version": version,
                "answer": "",
                "confidence": "",
                "follow_up": "",
                "status": f"Invalid response: {error}",
            }

        results.append(result)

        print(f"  Version {version}: {result['status']}")

# Save complete results as JSON
with open("eval/prompt_eval_results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

# Save results as CSV
with open(
    "eval/prompt_eval_results.csv", "w", newline="", encoding="utf-8-sig"
) as file:
    fieldnames = [
        "question_id",
        "question",
        "prompt_version",
        "answer",
        "confidence",
        "follow_up",
        "status",
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("\nEvaluation completed!")
print(f"Total requests: {len(results)}")
print("Results saved in:")
print("1. eval/prompt_eval_results.json")
print("2. eval/prompt_eval_results.csv")
