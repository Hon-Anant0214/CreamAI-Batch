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

                if re.match(r"^Section\s+\d+\s*:", line, re.IGNORECASE):
                    sections.append(line)

        return list(dict.fromkeys(sections))

    except Exception as error:
        print("PDF extraction error:", error)
        return []