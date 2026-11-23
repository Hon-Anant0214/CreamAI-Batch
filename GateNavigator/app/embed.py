
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Model will be loaded only when embeddings are requested.
_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")

        # Import only when needed, not when FastAPI starts.
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(MODEL_NAME, device="cpu")

        print("Embedding model loaded successfully.")

    return _model


def generate_embeddings(texts):
    """
    Convert a list of text chunks into numerical embeddings.
    """

    model = get_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        batch_size=16,
    )

    return embeddings


if __name__ == "__main__":
    sample_texts = [
        "Computer Science and Information Technology syllabus",
        "Data Science and Artificial Intelligence syllabus",
        "General Aptitude marks in GATE examination",
    ]

    embeddings = generate_embeddings(sample_texts)

    print("\nEmbedding generation successful!")
    print("Number of texts:", len(sample_texts))
    print("Embedding shape:", embeddings.shape)
    print("\nFirst embedding sample:")
    print(embeddings[0][:10])
