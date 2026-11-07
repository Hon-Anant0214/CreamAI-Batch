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