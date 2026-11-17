product_name = GATENavigator
User = Students preparing for the GATE examination.
Problem:-Students struggle to find organized study materials, previous-year questions and preparation guidance.
Data Source:-GATE previous-year question papers, syllabus, study materials and other educational resources.


    what it does?
--->Answers GATE 2027 questions on eligibility, papers, two-paper combinations, syllabus topics and marking scheme straight from IIT Madras's official brochure and syllabus PDFs.

    
    Day01 Task = Create public repo 'CreamAi-Batch' and clone it. README.md = your GATENavigator project card (product, user, problem, data source). day01_intro.py prints the card with variables + f-strings and asks the user's name and question with input(). day01_menu.py: while-loop menu (1 about GATENavigator, 2 sample questions, 3 one if/elif rule check from your domain, 0 exit). Push.




    ## Day 4 – FastAPI, Pandas and Smart Search

### Features

- FastAPI service with five endpoints.
- Health check using `/health`.
- Fetch GATE records using `/records`.
- Fetch an individual paper using `/records/{id}`.
- Search papers using TF-IDF and Cosine Similarity.
- Accept student questions using `/questions`.
- Explore GATE records using Pandas.

### How to Run

1. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Start the FastAPI server:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. Open API documentation:

   `http://127.0.0.1:8000/docs`

### Run Data Analysis

```bash
python -m analysis.explore
```

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API status |
| GET | `/records?limit=5` | Get records |
| GET | `/records/CS` | Get a specific paper |
| GET | `/search?q=computer` | Smart search |
| POST | `/questions` | Submit a question |

### Technologies Used

- Python
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
- TF-IDF
- Cosine Similarity


## Day 6 – LLM Integration and Prompt Engineering

### Features Implemented

- Integrated Groq Cloud LLM API.
- Created an LLM provider wrapper in `app/llm.py`.
- Added the `POST /chat` API endpoint.
- Implemented two system prompt versions (V1 and V2).
- Created separate task prompts for:
  - Explaining technical topics.
  - Answering GATE syllabus and paper-related questions.
- Implemented structured JSON responses containing:
  - `answer`
  - `confidence`
  - `follow_up`
- Stored API configuration using `.env`.
- Added `.env.example` for environment configuration.

### Prompt Evaluation

Created an automated evaluation script to test 10 GATENavigator questions using both prompt versions.

Evaluation files:
- `eval/run_prompt_eval.py`
- `eval/prompt_compare.md`
- `eval/prompt_eval_results.json`
- `eval/prompt_eval_results.csv`

### Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Use the `POST /chat` endpoint to ask questions.

### Environment Configuration

Create a `.env` file in the project root and configure:

```text
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Never commit the actual `.env` file to GitHub.

## Day 7: Semantic Search and Vector Database

### Features Implemented

- PDF document extraction and text chunking using PyPDF.
- Document chunks store source, page number, and title metadata.
- Text embeddings generated using Sentence Transformers.
- Semantic search implemented using cosine similarity.
- Evaluated semantic search using 10 GATE questions.
- Evaluation results saved in `eval/search_results.md`.
- Persistent vector storage implemented using ChromaDB.
- FastAPI endpoint added: `GET /search/semantic?q=`.
- ChromaDB database stored locally in `chroma_db/`.

### Technologies Used

- Python
- PyPDF
- Sentence Transformers
- all-MiniLM-L6-v2
- Scikit-learn
- ChromaDB
- FastAPI

### How to Run

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Use `GET /search/semantic` to search the indexed documents.

To rebuild the vector database:

```bash
python -m app.vectorstore

Day 8 – RAG Pipeline and Evaluation

### RAG Implementation
- Created `app/rag.py`.
- Implemented question answering using retrieved document chunks.
- Integrated Groq LLM with retrieved context.
- Added source citations with document names and page numbers.
- Implemented "I don't know" behavior for unanswerable questions.
- Added POST `/ask` API endpoint.

### Evaluation
- Created `eval/eval_set.json` with 15 questions.
- Created `eval/run_eval.py` to compare two configurations.

### Configuration Comparison

| Metric | Configuration A | Configuration B |
|---|---:|---:|
| Chunk Size | 500 | 800 |
| Overlap | 100 | 150 |
| Top-K | 3 | 5 |
| Keyword Coverage | 82.7% | 80.4% |
| Source Hit Rate | 78.6% | 78.6% |
| Unanswerable Accuracy | 100% | 100% |
| Combined Score | 87.1% | 86.3% |

### Winning Configuration
Configuration A was selected.

- Chunk Size: 500
- Overlap: 100
- Top-K: 3
- Indexed Chunks: 1065

Note: The combined score is a custom average of the three evaluation metrics, not a general RAG accuracy score.

### Known Limitations
- Some questions about aggregate record counts are not answered correctly.
- Retrieval can occasionally select unrelated document sections.
- Further improvements to retrieval and context ranking are needed.

# Day 9 – AI Agent and LangGraph Integration

## Overview

Day 9 focuses on building an AI agent that can use multiple tools to answer GATE-related questions and perform marks calculations.

Two implementations were developed:

- S1: Hand-written agent with tool calling.
- S2: LangGraph-based agent with memory and human approval.

## 1. S1 – Hand-Written Agent

### Files Created

- `app/tools.py`
- `app/agent_loop.py`

### GATE Marks Calculator

Implemented `gate_marks_calculator()` to calculate marks for a mock GATE attempt.

GATE negative marking rules:

- 1-mark MCQ wrong answer: -1/3 mark.
- 2-mark MCQ wrong answer: -2/3 mark.
- MSQ: No negative marking.
- NAT: No negative marking.

The calculator returns:

- Correct marks
- Marks lost to negative marking
- Final score
- Maximum marks (100)

### Agent Tool Selection

The hand-written agent supports two operations:

1. Marks Calculator – Calculates marks using the calculator tool.
2. RAG Search – Retrieves information from indexed GATE syllabus documents.

## 2. S2 – LangGraph Agent

### File Created

- `app/graph.py`

### LangGraph Features

Implemented an agent workflow using LangGraph.

Main components:

- StateGraph – Defines the agent workflow.
- Routing Node – Selects the appropriate tool.
- RAG Node – Answers GATE-related questions.
- Marks Node – Executes the marks calculator.
- Approval Node – Requests user approval before calculating marks.
- Memory Node – Maintains conversation history.
- MemorySaver – Stores workflow checkpoints during execution.

### Workflow

1. User submits a question.
2. Agent identifies the required operation.
3. RAG questions are sent to the RAG search node.
4. Marks calculation requests go to the approval node.
5. The workflow pauses until the user approves or declines.
6. After approval, the marks calculator executes.
7. The result is saved in conversation history.

## 3. FastAPI Integration

Integrated the LangGraph agent into `app/main.py`.

### New Endpoint

`POST /agent`

The endpoint supports:

- RAG-based question answering.
- GATE marks calculation.
- Human approval.
- Conversation threads using thread IDs.
- Returning agent results and conversation history.

### Example RAG Request

```json
{
  "question": "What topics are included in the Computer Science syllabus?",
  "thread_id": "student-api-1"
}
```

### Example Marks Calculation Request

```json
{
  "question": "calculate marks",
  "thread_id": "student-api-2",
  "marks_data": {
    "mcq_1_correct": 5,
    "mcq_1_wrong": 3,
    "mcq_2_correct": 4,
    "mcq_2_wrong": 2,
    "msq_correct": 3,
    "msq_wrong": 1,
    "nat_correct": 5,
    "nat_wrong": 2
  }
}
```

The agent requests approval before executing the calculation.

## 4. Testing Results

| Test | Result |
|---|---|
| Hand-written agent | Passed |
| RAG tool execution | Passed |
| Marks calculator | Passed |
| LangGraph routing | Passed |
| Human approval interrupt | Passed |
| Approval and resume | Passed |
| Conversation memory | Passed |
| FastAPI `/agent` endpoint | Passed |

### Sample Marks Calculator Output

```json
{
  "correct_marks": 29,
  "marks_lost_to_negatives": 2.33,
  "total_marks": 26.67,
  "maximum_marks": 100
}
```

## 5. Important Learning Outcomes

- Understanding AI agent architecture.
- Building and integrating custom tools.
- Implementing tool selection and routing.
- Understanding LangGraph StateGraph.
- Implementing human-in-the-loop approval.
- Managing conversation state and memory.
- Connecting LangGraph workflows with FastAPI.

## Conclusion

Day 9 successfully integrated a hand-written AI agent and a LangGraph-based agent into GATENavigator. The system can answer GATE syllabus questions through RAG, calculate mock-test marks, request user approval, and maintain conversation history.
