from pathlib import Path

from pypdf import PdfReader


def chunk_pdf(pdf_path, chunk_size=500, overlap=100):
    """
    Extract text from a PDF and split it into chunks.

    Each chunk stores:
    - source: PDF filename
    - page: PDF page number
    - title: PDF document title
    """

    pdf_path = Path(pdf_path)
    reader = PdfReader(str(pdf_path))

    chunks = []

    # Read document title
    title = (
        reader.metadata.title
        if reader.metadata and reader.metadata.title
        else pdf_path.stem
    )

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        # Clean extracted text
        text = " ".join(text.split())

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append(
                    {
                        "text": chunk_text,
                        "metadata": {
                            "source": pdf_path.name,
                            "page": page_number,
                            "title": title,
                        },
                    }
                )

            if end >= len(text):
                break

            start = end - overlap

    return chunks


if __name__ == "__main__":
    raw_folder = Path(__file__).resolve().parent.parent / "Data" / "Raw"

    pdf_files = list(raw_folder.glob("*.pdf"))

    all_chunks = []

    for pdf_file in pdf_files:
        document_chunks = chunk_pdf(pdf_file)

        all_chunks.extend(document_chunks)

        print(f"\nDocument: {pdf_file.name}")
        print(f"Chunks created: {len(document_chunks)}")

    print("\nTotal chunks created:", len(all_chunks))

    if all_chunks:
        print("\nSample chunk:")
        print(all_chunks[0]["text"][:300])
        print("\nSample metadata:")
        print(all_chunks[0]["metadata"])
