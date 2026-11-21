import pytest

from app.records import count_by, get_by_id, load_records, search


# Sample records for testing
@pytest.fixture
def sample_records():
    return [
        {
            "paper_code": "CS",
            "paper_name": "Computer Science",
            "syllabus_sections": ["Programming", "Data Structures", "Algorithms"],
        },
        {
            "paper_code": "DA",
            "paper_name": "Data Science and Artificial Intelligence",
            "syllabus_sections": ["Machine Learning", "Artificial Intelligence"],
        },
        {
            "paper_code": "EC",
            "paper_name": "Electronics and Communication",
            "syllabus_sections": ["Digital Circuits", "Communication Systems"],
        },
    ]


def test_load_records():
    records = load_records()

    assert isinstance(records, list)
    assert len(records) > 0
    assert "paper_code" in records[0]


def test_search_by_paper_code(sample_records):
    results = search(sample_records, "CS Computer Science")

    assert len(results) == 1
    assert results[0]["paper_code"] == "CS"


def test_search_is_case_insensitive(sample_records):
    results = search(sample_records, "machine learning")

    assert len(results) == 1
    assert results[0]["paper_code"] == "DA"


def test_search_by_syllabus_section(sample_records):
    results = search(sample_records, "Algorithms")

    assert len(results) == 1
    assert results[0]["paper_code"] == "CS"


def test_count_by_field(sample_records):
    counts = count_by(sample_records, "paper_code")

    assert counts == {"CS": 1, "DA": 1, "EC": 1}


def test_get_by_id(sample_records):
    record = get_by_id(sample_records, "CS")

    assert record is not None
    assert record["paper_name"] == "Computer Science"


def test_get_by_id_is_case_insensitive(sample_records):
    record = get_by_id(sample_records, "cs")

    assert record is not None
    assert record["paper_code"] == "CS"


def test_get_by_id_not_found(sample_records):
    record = get_by_id(sample_records, "XYZ")

    assert record is None
