
# How Large Language Models (LLMs) Work

## 1. What is an LLM?

A Large Language Model (LLM) is an artificial intelligence model
trained on a large amount of text and other language data.

It learns patterns in language, understands relationships between
words, and generates responses based on the input it receives.

Examples of LLMs include GPT, Gemini, and Llama.

## 2. How does an LLM work?

An LLM processes the user's input, breaks the text into smaller
units called tokens, and converts those tokens into numerical
representations.

It uses its learned patterns and neural network architecture
to predict which tokens should come next.

By repeatedly predicting tokens, it generates a meaningful
response to the user's question.

## 3. Basic Working Process

1. The user enters a question.
2. The input text is converted into tokens.
3. The model processes the tokens using its neural network.
4. The model predicts the next tokens.
5. The predicted tokens are converted into readable text.
6. The generated answer is shown to the user.

## 4. LLM Working Diagram

```mermaid
flowchart TD
    A[User Question] --> B[Tokenization]
    B --> C[Neural Network Processing]
    C --> D[Next Token Prediction]
    D --> E[Response Generation]
    E --> F[Final Answer]
```

## 5. What are LLMs used for?

- Answering questions
- Explaining technical concepts
- Summarizing documents
- Generating text and code
- Supporting educational applications
- Helping users understand complex topics

## 6. LLMs in GATENavigator

GATENavigator is designed to help students prepare for GATE.

An LLM can help GATENavigator by:

- Explaining engineering concepts.
- Answering student questions.
- Simplifying difficult topics.
- Providing study guidance.
- Helping students understand GATE syllabus information.

An important limitation is that an LLM can sometimes generate
incorrect information. Therefore, GATENavigator should use
reliable GATE documents and data when answering questions.

## 7. Initial API Testing

### Test 1: Topic Explanation

Question: Explain supervised learning with a simple example.

Task: explain

Result: API returned a valid JSON response containing
answer, confidence, and follow_up.

Status: API working. Further evaluation of answer quality is pending.

### Test 2: Syllabus Help

Question: What is the paper code and syllabus URL for Computer Science?

Task: syllabus

Result:
- Paper Code: CS
- Paper Name: Computer Science & Information Technology
- Syllabus URL: https://gate2027.iitm.ac.in/static/doc/GATE2027_Syllabus/CS_GATE2027_Syllabus.pdf

Status: Correct response based on available records.


## 8. Detailed Comparison Testing

Both prompt versions will be tested using the same 10 questions.

### Testing Method

1. Send each question using Prompt Version 1.
2. Record the generated answer.
3. Send the same question using Prompt Version 2.
4. Record the generated answer.
5. Compare accuracy, relevance, clarity, missing-data handling, and JSON formatting.

### Expected Behaviour

| Test | Expected Behaviour |
|---|---|
| Q1 | Correctly identify available GATE papers |
| Q2 | Identify the CS paper code |
| Q3 | Report GA and subject marks |
| Q4 | Provide CS paper details |
| Q5 | Provide the DA syllabus URL |
| Q6 | Clearly state that unavailable cutoff information is not present |
| Q7 | Identify the AE paper |
| Q8 | Report the number of stored papers |
| Q9 | Identify the EC paper code |
| Q10 | Provide the AE syllabus URL |

### Final Comparison

Actual results and scores will be added after completing all 20 tests.

No evaluation score will be assigned without testing the corresponding response.
