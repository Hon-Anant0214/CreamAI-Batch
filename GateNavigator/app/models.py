
from dataclasses import dataclass


@dataclass
class Record:
    paper_code: str
    paper_name: str
    ga_marks: int
    subject_marks: int
    syllabus_sections: list
    syllabus_url: str
