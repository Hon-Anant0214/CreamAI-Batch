
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def smart_search(records, query, top_n=5):

    if not query.strip():
        return []

    # Prepare searchable text from each record
    documents = []

    for record in records:
        text = (
            record["paper_code"] + " " +
            record["paper_name"] + " " +
            " ".join(record["syllabus_sections"])
        )
        documents.append(text)

    # Convert text into numerical vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents + [query])

    # Compare query with every record
    scores = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    ).flatten()

    # Sort records by similarity score
    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_n]:
        if scores[index] > 0:
            results.append(records[index])

    return results
