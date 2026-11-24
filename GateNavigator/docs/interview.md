# GATENavigator – Project Interview Preparation

## 1. 60-Second Project Pitch

GATENavigator is an AI-powered educational assistant designed to help students prepare for the GATE examination.

The main problem it solves is that students often need to search through multiple syllabus PDFs, examination documents and paper details to find relevant information.

I developed a Retrieval-Augmented Generation system. It loads PDF documents, splits them into smaller chunks and indexes the content using TF-IDF. When a student asks a question, the system uses cosine similarity to retrieve relevant information and sends that context to a Groq-hosted large language model to generate an answer.

The project uses FastAPI for backend APIs and Streamlit for the user interface. It also includes a LangGraph-based agent, input validation, prompt-injection protection, response caching and LLM monitoring.

My goal was to build a practical educational assistant that provides answers grounded in GATE-related documents rather than relying only on the model's general knowledge.

## 2. Ten Likely Interview Questions and Answers

### Q1. What problem does GATENavigator solve?

GATENavigator helps GATE aspirants find information from examination documents, syllabus PDFs and paper records. Instead of manually searching through multiple files, students can ask questions in natural language and receive relevant answers.

### Q2. How does the system work from question to answer?

First, the student enters a question through the Streamlit interface. The frontend sends it to the FastAPI backend. The retrieval component searches indexed document chunks using TF-IDF and cosine similarity. The relevant context is passed to the Groq LLM along with the system instructions. The generated answer is then returned to the frontend.

### Q3. Why did you use RAG instead of only an LLM?

An LLM may generate answers from its general training knowledge and may not know the exact information in a particular GATE document. RAG retrieves relevant information from the project's documents and provides it as context to the LLM. This helps make answers more relevant and grounded in the available sources.

### Q4. How do you retrieve relevant information?

I use TF-IDF vectorization and cosine similarity. TF-IDF represents documents based on the importance of their terms. When a user asks a question, the question is transformed using the same vectorizer. Cosine similarity compares the question vector with document vectors, and the most relevant chunks are selected.

This is a lightweight retrieval approach. It does not require an external vector database or a separate embedding model.

### Q5. How are documents and GATE paper records indexed?

PDF documents are processed through the chunking module. The resulting chunks are collected and indexed. GATE paper details are also loaded from `Data/records.json` and converted into searchable text records. The TF-IDF index is built once and cached in memory.

### Q6. How would you handle multiple versions of the same brochure or a revised syllabus?

This is an important document-management challenge. I would store metadata such as document name, version number, publication date and revision date during ingestion. When multiple versions contain similar information, the retrieval process should prefer the latest valid version.

For syllabus PDFs with nested bullet points, I would use unit-based chunking instead of splitting at arbitrary character limits. This helps keep a complete topic and its subtopics together, preserving their meaning during retrieval.

### Q7. Why did you choose Groq for the LLM?

I used Groq to access a hosted large language model through an API. This avoids the need to run a large language model locally and reduces local hardware requirements. The model is configured through environment variables, so the model can be changed without rewriting the application logic.

### Q8. What is the purpose of FastAPI, Streamlit and LangGraph?

FastAPI provides the backend API endpoints and handles requests. Streamlit provides the interactive user interface. LangGraph is used for agent-based workflow orchestration, allowing the application to organize processing into steps rather than treating every interaction as a single direct LLM call.

### Q9. What steps did you take to make the application more reliable and secure?

I added input validation with Pydantic, including a maximum question length of 2,000 characters. I added response caching to avoid repeated LLM calls for identical prompts. I also added logging for LLM latency and token usage.

For prompt-injection protection, the system prompt instructs the model to treat retrieved document content as untrusted data and not follow instructions found inside documents. I also added an automated test for this behavior.

### Q10. What are the current limitations and future improvements?

The current TF-IDF approach mainly matches terms and may miss relevant information when a question uses different wording. A future improvement would be to add semantic retrieval or a hybrid retrieval approach.

Other improvements could include stronger document version management, unit-aware syllabus chunking, persistent caching, better evaluation datasets and more detailed monitoring of retrieval quality.

## 3. My Hardest Technical Challenge

One of the hardest challenges was thinking about how to handle changing source documents.

For example, an organization may publish multiple revisions of the same brochure, or a syllabus may be updated. If all versions are indexed without tracking their revision information, the system could retrieve outdated information.

The solution is to preserve version and date metadata during document ingestion and use it during retrieval so that the latest valid document is preferred.

Another challenge is preserving the structure of syllabus PDFs. A topic may contain nested bullet points and subtopics. Splitting the document at arbitrary positions can separate a heading from its explanation. Unit-based chunking helps preserve the complete topic structure.

## 4. Important Technical Terms to Remember

| Term | Simple explanation |
|---|---|
| RAG | Retrieves document information before generating an answer |
| TF-IDF | Represents text using term importance |
| Cosine similarity | Measures similarity between two vectors |
| Chunking | Splits large documents into smaller meaningful sections |
| FastAPI | Python framework for building backend APIs |
| Streamlit | Python framework for creating interactive web interfaces |
| Groq | Cloud platform used to access an LLM |
| LangGraph | Framework for building stateful LLM workflows |
| Caching | Reuses previous results to reduce repeated work |
| Prompt injection | An attempt to manipulate an AI system through malicious instructions |

## 5. Interview Reminder

Be honest about what is implemented and what is planned. In particular, describe document version filtering and unit-based syllabus chunking as design improvements unless they have been implemented and tested in the code.

When explaining the project, follow this order:

1. Problem being solved.
2. How documents are processed.
3. How retrieval works.
4. How the LLM generates answers.
5. Technologies used.
6. Challenges, limitations and future improvements.
