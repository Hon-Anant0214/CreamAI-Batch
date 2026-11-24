import re
from pathlib import Path

from pypdf import PdfReader

from app.document_metadata import extract_document_metadata


def split_into_chunks(text, chunk_size=500, overlap=100):
    """Split text while trying to preserve sentence boundaries."""

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(paragraph) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            start = 0
            while start < len(paragraph):
                end = min(start + chunk_size, len(paragraph))

                if end < len(paragraph):
                    boundary = paragraph.rfind(" ", start, end)
                    if boundary > start:
                        end = boundary

                chunks.append(paragraph[start:end].strip())
                start = max(end - overlap, start + 1)

            continue

        if len(current_chunk) + len(paragraph) + 1 <= chunk_size:
            current_chunk = f"{current_chunk}\n{paragraph}".strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def chunk_pdf(pdf_path, chunk_size=500, overlap=100):
    """
    Extract PDF text and create chunks with source metadata.

    Attempts to keep syllabus units and their nested content together.
    """

    pdf_path = Path(pdf_path)
    reader = PdfReader(str(pdf_path))
    document_metadata = extract_document_metadata(pdf_path)
    chunks = []

    title = (
        reader.metadata.title
        if reader.metadata and reader.metadata.title
        else pdf_path.stem
    )

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        # Preserve line breaks to identify headings and bullet points.
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        grouped_text = []
        current_group = []
        current_unit = "General"

        for line in lines:
            is_unit_heading = bool(
                re.match(
                    r"^(unit|section|chapter)\s*[\dIVX]+",
                    line,
                    re.IGNORECASE,
                )
            )

            if is_unit_heading and current_group:
                grouped_text.append(
                    (current_unit, "\n".join(current_group))
                )
                current_group = []

            if is_unit_heading:
                current_unit = line

            current_group.append(line)

        if current_group:
            grouped_text.append(
                (current_unit, "\n".join(current_group))
            )

        for unit_name, group_text in grouped_text:
            text_chunks = split_into_chunks(
                group_text,
                chunk_size=chunk_size,
                overlap=overlap,
            )

            for chunk_text in text_chunks:
                chunks.append(
                    {
                        "text": chunk_text,
                        "metadata": {
                            "source": pdf_path.name,
                            "page": page_number,
                            "title": title,
                            "unit": unit_name,
                            **document_metadata,
                    },
                    }
                )

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
