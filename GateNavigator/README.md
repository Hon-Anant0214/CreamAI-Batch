# GATENavigator – AI-Powered GATE Preparation Assistant

GATENavigator is an AI-powered educational assistant designed to help students preparing for the Graduate Aptitude Test in Engineering (GATE).

It allows students to explore GATE examination information, ask questions about eligibility and marking schemes, search syllabus topics, retrieve information from official documents, compare syllabus revisions, and calculate mock examination marks.

The application combines **Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), AI Agents, and document retrieval** to provide an interactive GATE preparation experience.

---

## 1. Project Overview

| Category | Description |
|---|---|
| Product Name | GATENavigator |
| Target Users | Students preparing for the GATE examination |
| Problem | Students struggle to find organized study materials, previous-year questions and preparation guidance |
| Data Sources | GATE question papers, official brochures, syllabus PDFs and educational resources |
| Primary Goal | Provide an AI-powered assistant for GATE examination preparation |

### What Does GATENavigator Do?

GATENavigator answers GATE 2027 questions about:

- Examination eligibility.
- Available GATE papers.
- Two-paper combinations.
- Syllabus topics.
- Examination pattern and marking scheme.
- General Aptitude and subject marks.
- GATE preparation-related questions.

It retrieves information from official IIT Madras examination brochures and syllabus documents where available.

---

## 2. Key Features

- AI-powered conversational interface.
- Retrieval-Augmented Generation (RAG).
- PDF document ingestion and text extraction.
- TF-IDF-based document retrieval.
- Cosine similarity-based search.
- Groq Cloud LLM integration.
- FastAPI backend.
- Streamlit frontend.
- LangGraph-based AI agent.
- GATE marks calculation tool.
- Human-in-the-loop approval.
- Conversation memory.
- GATE syllabus comparison.
- Source citations with document names and page numbers.
- User feedback collection.
- Response caching.
- LLM latency and token monitoring.
- Input validation and prompt-injection protection.
- Docker-based application deployment.

---

## 3. System Architecture

```text
                  STUDENT
                     |
                     v
              STREAMLIT FRONTEND
                     |
                     v
               FASTAPI BACKEND
                     |
          +----------+----------+
          |          |          |
          v          v          v
       RAG       AI AGENT    GATE TOOLS
          |          |          |
          v          v          v
      DOCUMENT    LANGGRAPH   MARKS
      RETRIEVAL   WORKFLOW   CALCULATOR
          |
          v
    TF-IDF + COSINE
      SIMILARITY
          |
          v
    RETRIEVED DOCUMENT
        CHUNKS
          |
          v
      GROQ CLOUD LLM
          |
          v
    GENERATED ANSWER
          |
          v
    SOURCE CITATIONS
          |
          v
       STUDENT
```

### Main Components

| Component | Responsibility |
|---|---|
| Streamlit | User interface and conversational interaction |
| FastAPI | Backend APIs and request handling |
| TF-IDF | Text representation for retrieval |
| Cosine Similarity | Finds relevant document chunks |
| RAG | Combines retrieved information with LLM generation |
| Groq | Provides cloud-based LLM inference |
| LangGraph | Manages agent workflows and state |
| PyPDF | Extracts text from PDF documents |
| Pydantic | Validates API request data |
| Docker | Containerizes the application |

---

## 4. Document Processing and Retrieval

### Document Ingestion

The application processes PDF documents using PyPDF.

The document processing pipeline:

1. Loads PDF documents from `Data/Raw/`.
2. Extracts text from PDF pages.
3. Splits extracted text into smaller chunks.
4. Stores document metadata.
5. Builds a TF-IDF index for retrieval.

### Document Metadata

Each PDF chunk can contain:

- Source filename.
- Page number.
- Document title.
- Unit or section name.
- Document version.
- Revision date.

Document version and revision-date information is extracted from filenames when available.

### Chunking Strategy

The chunking module uses:

- Default chunk size: 500 characters.
- Default overlap: 100 characters.
- Section-aware grouping for headings such as Unit, Section and Chapter.

The goal is to preserve syllabus structure and keep related content together during retrieval.

### Retrieval Method

GATENavigator currently uses:

**TF-IDF + Cosine Similarity**

TF-IDF converts text into numerical representations based on term importance.

Cosine similarity compares the user's question with indexed document chunks and retrieves the most relevant results.

This lightweight retrieval approach does not require an external vector database or a separate embedding model.

### Document Version Handling

The application extracts document version and revision-date metadata when the filename contains this information.

Revision dates are also considered during retrieval ranking as a tie-breaker when similarity scores are equal.

Full document-version filtering and guaranteed latest-version selection are future improvements.

---

## 5. Retrieval-Augmented Generation (RAG)

The RAG pipeline combines document retrieval with LLM-based answer generation.

### RAG Workflow

1. Student submits a question.
2. The backend receives the question.
3. The retrieval component searches indexed documents.
4. Relevant document chunks are selected.
5. Retrieved context is passed to the Groq LLM.
6. The LLM generates a context-grounded answer.
7. The response and available source citations are returned.

### RAG Features

- Context-based question answering.
- Source filename and page citations.
- Grounded responses using retrieved documents.
- Fallback response for questions without sufficient context.
- Prompt instructions to treat retrieved document content as untrusted data.

---

## 6. LLM Integration and Prompt Engineering

GATENavigator integrates the Groq Cloud API to access a hosted large language model.

### Implemented Features

- Groq API integration.
- Centralized LLM provider wrapper in `app/llm.py`.
- Configurable model through environment variables.
- System prompts for GATE-related questions.
- Task-specific prompt instructions.
- Structured response handling.
- Response caching.

### Environment Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=your_supported_groq_model
```

Never commit your actual `.env` file or API keys to GitHub.

An example configuration is provided in `.env.example`.

---

## 7. FastAPI Backend

The backend is implemented using FastAPI.

### Main API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/records` | Retrieve GATE paper records |
| GET | `/records/{id}` | Retrieve an individual paper |
| GET | `/search?q=computer` | Search GATE information |
| POST | `/questions` | Submit a student question |
| POST | `/chat` | LLM-based chat interaction |
| POST | `/ask` | RAG-based question answering |
| POST | `/agent` | Interact with the LangGraph agent |

The exact request and response schemas can be explored through the Swagger documentation.

### Start the Backend

```bash
python -m pip install -r requirements.txt
```

```bash
python -m uvicorn app.main:app --reload
```

Open the API documentation:

`http://127.0.0.1:8000/docs`

---

## 8. GATE Data Analysis and Smart Search

The project includes structured GATE paper records.

### Features

- GATE paper code and paper name retrieval.
- General Aptitude marks.
- Subject marks.
- Syllabus section information.
- Syllabus URL references.
- Record searching.
- Pandas-based data exploration.

### Run Data Analysis

```bash
python -m analysis.explore
```

### Smart Search

The application uses Scikit-learn's TF-IDF vectorizer and cosine similarity to identify relevant records and document content.

---

## 9. AI Agent and LangGraph Integration

GATENavigator includes two agent implementations.

### Hand-Written Agent

Files:

- `app/tools.py`
- `app/agent_loop.py`

Features:

- Tool selection.
- RAG-based document search.
- GATE marks calculation.

### LangGraph Agent

File:

- `app/graph.py`

Features:

- StateGraph-based workflow.
- Routing between operations.
- RAG question-answering node.
- Marks calculation node.
- Human approval workflow.
- Conversation memory.
- Workflow checkpointing.

### Human-in-the-Loop Approval

For marks calculation, the agent can request user approval before executing the action.

This demonstrates how human approval can be incorporated into an AI workflow for actions that require confirmation.

### Example Agent Request

```json
{
  "question": "What topics are included in the Computer Science syllabus?",
  "thread_id": "student-api-1"
}
```

---

## 10. GATE Marks Calculator

The project includes a tool to calculate mock GATE examination marks.

### Negative Marking Rules

- Incorrect 1-mark MCQ: 1/3 mark deducted.
- Incorrect 2-mark MCQ: 2/3 mark deducted.
- MSQ: No negative marking.
- NAT: No negative marking.

### Calculator Output

The tool calculates:

- Correct marks.
- Marks lost due to negative marking.
- Final score.
- Maximum marks.

Input validation prevents invalid negative values and Boolean values from being accepted as numeric marks.

---

## 11. Streamlit Frontend

The frontend is implemented using Streamlit.

### Features

- Interactive chat interface.
- RAG and Agent chat modes.
- AI-generated answers.
- Source citations.
- Human approval for agent actions.
- User feedback using thumbs-up and thumbs-down.
- GATE 2026 and GATE 2027 syllabus comparison.
- Added and removed topic identification.
- Direct PDF page links for syllabus topics.

### Start the Frontend

```bash
streamlit run ui/app.py
```

Open:

`http://localhost:8501`

---

## 12. Evaluation

The project includes evaluation scripts for prompt engineering and retrieval configurations.

### Prompt Evaluation

The evaluation compares different prompt versions using GATENavigator questions.

Relevant files include:

- `eval/run_prompt_eval.py`
- `eval/prompt_compare.md`
- `eval/prompt_eval_results.json`
- `eval/prompt_eval_results.csv`

### Retrieval Evaluation

Two retrieval configurations were compared.

| Metric | Configuration A | Configuration B |
|---|---:|---:|
| Chunk Size | 500 | 800 |
| Overlap | 100 | 150 |
| Top-K | 3 | 5 |
| Keyword Coverage | 82.7% | 80.4% |
| Source Hit Rate | 78.6% | 78.6% |
| Unanswerable Accuracy | 100% | 100% |
| Combined Score | 87.1% | 86.3% |

**Selected Configuration: Configuration A**

- Chunk size: 500.
- Overlap: 100.
- Top-K: 3.
- Indexed chunks in the recorded evaluation: 1,065.

The combined score is a custom average of the three evaluation metrics, not a general RAG accuracy score.

These are results from the recorded evaluation, not a guarantee of accuracy for every question.

---

## 13. Production Hardening

Production-focused improvements were added to make the application more reliable.

### LLM Monitoring

- Logs LLM request latency.
- Tracks prompt tokens.
- Tracks completion tokens.
- Tracks total token usage.
- Logs successful and failed requests.

### Response Caching

Implemented using Python's `lru_cache`.

- Maximum cache capacity: 100 entries.
- Identical prompts reuse cached responses.
- Reduces unnecessary repeated LLM API calls.
- Cache is stored in memory and resets when the application restarts.

### Input Validation

Implemented using Pydantic.

- Maximum question length: 2,000 characters.
- Empty questions are rejected where a question is required.
- Invalid inputs return HTTP 422 responses.

### Prompt-Injection Protection

The RAG system prompt includes security instructions.

- Retrieved document content is treated as untrusted data.
- Instructions inside retrieved documents are not to be followed.
- The model is instructed not to reveal system prompts or credentials.
- An automated prompt-injection test is included.

These instructions provide a defensive layer but cannot guarantee complete protection against every prompt-injection attack.

---

## 14. Docker and Deployment

GATENavigator supports Docker-based application execution.

### Prerequisites

- Docker Desktop.
- Docker Compose.
- Groq API key.

### Build and Start

From the project root:

```bash
docker compose up --build -d
```

### Access Local Services

- Streamlit UI: `http://localhost:8501`
- FastAPI API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Useful Docker Commands

View running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop containers:

```bash
docker compose down
```

Rebuild and restart:

```bash
docker compose up --build -d
```

### Deployment

The FastAPI backend has been containerized and prepared for cloud deployment.

The application uses environment variables for cloud LLM configuration. API credentials should be configured through the deployment platform's environment-variable settings rather than committed to source control.

---

## 15. Testing

Automated tests are maintained in the `tests/` directory.

### Test Coverage

- FastAPI health endpoint.
- GATE record retrieval.
- Record limits.
- Individual record lookup.
- Missing record handling.
- Search endpoint.
- Question-answering endpoint.
- Prompt-injection protection.
- Record search and filtering.
- GATE marks calculation.
- Input validation.

### Run Tests

```bash
python -m pytest -v
```

Or use the concise output:

```bash
python -m pytest -q
```

### Latest Recorded Test Result

**21 passed, 2 warnings**

The two warnings are dependency deprecation warnings and did not cause test failures.

---

## 16. Project Structure

```text
GateNavigator/
│
├── agent/
│
├── analysis/
│   └── explore.py
│
├── app/
│   ├── main.py
│   ├── llm.py
│   ├── rag.py
│   ├── chunking.py
│   ├── document_metadata.py
│   ├── vectorstore.py
│   ├── semantic_search.py
│   ├── embed.py
│   ├── smart_search.py
│   ├── records.py
│   ├── models.py
│   ├── ingest.py
│   ├── fetch.py
│   ├── tools.py
│   ├── agent_loop.py
│   └── graph.py
│
├── Data/
│   ├── Raw/
│   ├── records.json
│   └── Sample_record.py
│
├── docs/
│   ├── interview.md
│   ├── how_llms_work.md
│   └── day10_comparison.png
│
├── eval/
│
├── prompts/
│
├── tests/
│
├── ui/
│   └── app.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── requirements-ui.txt
├── .dockerignore
├── .env.example
├── .gitignore
├── PROGRESS.md
└── README.md
```

---

## 17. Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI, Uvicorn |
| Frontend | Streamlit |
| LLM Provider | Groq Cloud |
| LLM Framework | LangGraph |
| Retrieval | TF-IDF, Cosine Similarity |
| Machine Learning | Scikit-learn |
| Document Processing | PyPDF |
| Data Analysis | Pandas |
| Data Validation | Pydantic |
| Configuration | Python dotenv |
| Testing | Pytest |
| Code Quality | Ruff |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |

---

## 18. Current Limitations and Future Improvements

### Current Limitations

- TF-IDF primarily relies on keyword matching and may miss semantically related questions.
- Document version filtering is not yet a complete latest-version selection mechanism.
- Unit-aware chunking depends on recognizable section headings.
- In-memory caching resets when the application restarts.
- Retrieval quality can vary depending on PDF extraction and document formatting.

### Future Improvements

- Implement hybrid keyword and semantic retrieval.
- Improve document version management and latest-version selection.
- Improve syllabus-aware chunking for nested topics.
- Add persistent caching.
- Expand the retrieval evaluation dataset.
- Improve retrieval ranking and source relevance.
- Add more GATE preparation resources.
- Improve deployment monitoring and scalability.

---

## 19. Interview Preparation

Interview preparation material is available in:

`docs/interview.md`

It includes:

- A 60-second project pitch.
- Ten likely interview questions and answers.
- System architecture explanations.
- RAG and TF-IDF explanations.
- The hardest technical challenge.
- Current limitations and future improvements.

---

## 20. Conclusion

GATENavigator demonstrates the development of an AI-powered educational assistant using document retrieval, Retrieval-Augmented Generation, cloud LLM integration and AI agent workflows.

The project brings together document processing, intelligent search, question answering, examination tools, a conversational interface and production-oriented engineering practices.

Its main objective is to make GATE examination information easier for students to access through a practical and interactive AI assistant.

---

**Project:** GATENavigator  
**Repository:** CreamAI-Batch  
**Branch:** main
