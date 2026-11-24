import re
from datetime import date
from pathlib import Path


def extract_document_metadata(pdf_path):
    """Extract basic document identity and revision metadata."""

    pdf_path = Path(pdf_path)
    filename = pdf_path.stem

    version_match = re.search(
        r"(?:v|version|rev)[\s_-]*(\d+(?:\.\d+)*)",
        filename,
        re.IGNORECASE,
    )

    date_match = re.search(
        r"(20\d{2})[-_](\d{1,2})[-_](\d{1,2})",
        filename,
    )

    revision_date = None

    if date_match:
        try:
            revision_date = date(
                int(date_match.group(1)),
                int(date_match.group(2)),
                int(date_match.group(3)),
            ).isoformat()
        except ValueError:
            revision_date = None

    return {
        "document_name": filename,
        "version": version_match.group(1) if version_match else "unknown",
        "revision_date": revision_date or "unknown",
        "source": pdf_path.name,
    }


if __name__ == "__main__":
    sample = Path("Data/Raw/CS_syllabus.pdf")
    print(extract_document_metadata(sample))
