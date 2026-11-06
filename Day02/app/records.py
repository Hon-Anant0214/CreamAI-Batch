
from Data.Sample_record import RECORDS
def load_records():
    return RECORDS
def search(keyword):
    results = []
    for record in RECORDS:
        text = (
            record["paper_code"] + " " +
            record["paper_name"] + " " +
            " ".join(record["syllabus_sections"])
        )
        if keyword.lower() in text.lower():
            results.append(record)
    return results
def count_by(field):
    counts = {}
    for record in RECORDS:
        value = record.get(field)
        if value:
            counts[value] = counts.get(value, 0) + 1
    return counts
def get_by_id(paper_code):
    for record in RECORDS:
        if record["paper_code"].lower() == paper_code.lower():
            return record

    
    return None
