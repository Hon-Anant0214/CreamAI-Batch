[![GATENavigator CI](https://github.com/Hon-Anant0214/CreamAI-Batch/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Hon-Anant0214/CreamAI-Batch/actions/workflows/ci.yml)


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
```
