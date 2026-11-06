import argparse
from app.records import load_records, search, count_by, get_by_id

def show(r):
    print(f"{r['paper_code']} | {r['paper_name']} | GA {r['ga_marks']} + Subject {r['subject_marks']}")
    print(f"   Sections: {', '.join(r['syllabus_sections']) or 'N/A'}")
    print(f"   Syllabus: {r['syllabus_url']}\n")

def main():
    p = argparse.ArgumentParser(description="GATE 2027 papers explorer")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    s = sub.add_parser("search"); s.add_argument("keyword")
    c = sub.add_parser("count"); c.add_argument("field", nargs="?", default="category")
    g = sub.add_parser("get"); g.add_argument("code")
    a = p.parse_args()

    records = load_records()
    if a.cmd == "list":
        for r in records: show(r)
    elif a.cmd == "search":
        results = search(records, a.keyword)
        print(f"{len(results)} result(s)\n")
        for r in results: show(r)
    elif a.cmd == "count":
        for k, v in count_by(records, a.field).items(): print(f"{k}: {v}")
    elif a.cmd == "get":
        r = get_by_id(records, a.code)
        show(r) if r else print("Not found")

if __name__ == "__main__":
    main()