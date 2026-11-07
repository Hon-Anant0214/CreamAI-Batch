
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# Official GATE website
PAGE_URL = "https://gate2027.iitm.ac.in/exam_papers_and_syllabus"
BROCHURE_URL = "https://gate2027.iitm.ac.in/static/doc/IB/GATE2027-IB.pdf"

# Papers to download
PAPER_CODES = ["CS", "DA", "RA"]


def download_file(url, filename):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        file_path = RAW_DIR / filename

        with open(file_path, "wb") as file:
            file.write(response.content)

        print("Downloaded:", filename)
        return True

    except requests.exceptions.RequestException as error:
        print("Download failed:", url)
        print("Error:", error)
        return False


def fetch_documents():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Download the main webpage
    if not download_file(PAGE_URL, "exam_papers.html"):
        return

    # Download the information brochure
    download_file(BROCHURE_URL, "GATE2027-IB.pdf")

    # Read webpage to find official syllabus PDF links
    try:
        response = requests.get(PAGE_URL, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for code in PAPER_CODES:
            pdf_url = None

            for link in soup.find_all("a", href=True):
                href = link["href"]

                if f"{code}_GATE2027_Syllabus.pdf" in href:
                    pdf_url = urljoin(PAGE_URL, href)
                    break

            if pdf_url:
                filename = f"{code}_syllabus.pdf"
                download_file(pdf_url, filename)
            else:
                print("Syllabus link not found for:", code)

    except requests.exceptions.RequestException as error:
        print("Could not read syllabus webpage:", error)


if __name__ == "__main__":
    fetch_documents()
