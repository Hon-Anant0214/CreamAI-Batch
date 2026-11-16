
from sentence_transformers import SentenceTransformer


# Load a lightweight embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts):
    """
    Convert a list of text chunks into numerical embeddings.
    """

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings


if __name__ == "__main__":

    sample_texts = [
        "Computer Science and Information Technology syllabus",
        "Data Science and Artificial Intelligence syllabus",
        "General Aptitude marks in GATE examination"
    ]

    embeddings = generate_embeddings(sample_texts)

    print("\nEmbedding generation successful!")

    print("Number of texts:", len(sample_texts))
    print("Embedding shape:", embeddings.shape)

    print("\nFirst embedding sample:")
    print(embeddings[0][:10])
