
import json
from pathlib import Path

# Find the project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of the generated JSON file
DATA_FILE = BASE_DIR / "Data" / "records.json"


def load_records():
    """Load all GATE paper records from records.json."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    return records


def search(records, keyword):
    """Search records using paper code, name, and syllabus sections."""
    results = []

    for record in records:
        text = (
            record["paper_code"] + " " +
            record["paper_name"] + " " +
            " ".join(record["syllabus_sections"])
        )

        if keyword.lower() in text.lower():
            results.append(record)

    return results


def count_by(records, field):
    """Count records based on a selected field."""
    counts = {}

    for record in records:
        value = record.get(field)

        if value:
            counts[value] = counts.get(value, 0) + 1

    return counts


def get_by_id(records, paper_code):
    """Find a paper using its paper code."""
    for record in records:
        if record["paper_code"].lower() == paper_code.lower():
            return record

    return None
