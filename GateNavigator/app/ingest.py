
import json
import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pypdf import PdfReader

from app.models import Record


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "Data" / "Raw"
OUTPUT_FILE = BASE_DIR / "Data" / "records.json"

BASE_URL = "https://gate2027.iitm.ac.in/"


def extract_syllabus_sections(pdf_path):

    sections = []

    try:
        reader = PdfReader(str(pdf_path))

        for page in reader.pages:

            text = page.extract_text() or ""

            for line in text.splitlines():

                line = line.strip()

                if not line:
                    continue

                # Find numbered syllabus headings
                if re.match(r"^\d+(\.\d+)*\.?\s+[A-Z]", line):
                    sections.append(line)

        return list(dict.fromkeys(sections))

    except Exception as error:

        print("PDF extraction error:", error)
        return []


def ingest_records():

    html_file = RAW_DIR / "exam_papers.html"

    records = []

    if not html_file.exists():

        print("HTML file not found!")
        return

    try:

        with open(html_file, "r", encoding="utf-8") as file:

            soup = BeautifulSoup(file.read(), "html.parser")

    except Exception as error:

        print("HTML reading error:", error)
        return

    # Store links grouped by PDF URL
    syllabus_links = {}

    for link in soup.find_all("a", href=True):

        try:

            href = link["href"]

            if "GATE2027_Syllabus.pdf" not in href:
                continue

            pdf_url = urljoin(BASE_URL, href)

            paper_code = re.search(
                r"/([A-Z]{2})_GATE2027_Syllabus\.pdf",
                href
            )

            if not paper_code:
                continue

            code = paper_code.group(1)

            paper_name = link.get_text(" ", strip=True)

            if code not in syllabus_links:

                syllabus_links[code] = {
                    "paper_name": "",
                    "syllabus_url": pdf_url
                }

            # Ignore code-only links
            if paper_name.upper() != code:

                syllabus_links[code]["paper_name"] = paper_name

        except Exception as error:

            print("Bad link skipped:", error)
            continue

    # Create records
    for code, details in syllabus_links.items():

        try:

            name = details["paper_name"]

            if not name:
                print("Paper name missing:", code)
                continue

            pdf_path = RAW_DIR / f"{code}_syllabus.pdf"

            if pdf_path.exists():

                sections = extract_syllabus_sections(pdf_path)

            else:

                sections = []

            record = Record(
                paper_code=code,
                paper_name=name,
                ga_marks=15,
                subject_marks=85,
                syllabus_sections=sections,
                syllabus_url=details["syllabus_url"]
            )

            records.append(record)

        except Exception as error:

            print("Bad record skipped:", code, error)
            continue

    # Convert records into dictionaries
    records_data = [

        {
            "paper_code": record.paper_code,
            "paper_name": record.paper_name,
            "ga_marks": record.ga_marks,
            "subject_marks": record.subject_marks,
            "syllabus_sections": record.syllabus_sections,
            "syllabus_url": record.syllabus_url
        }

        for record in records
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            records_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nData ingestion completed!")
    print("Total records created:", len(records))
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":

    ingest_records()
