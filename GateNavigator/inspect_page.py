
from bs4 import BeautifulSoup
from pathlib import Path

file_path = Path("Data/Raw/exam_papers.html")

with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

print("PAGE TITLE:")
print(soup.title.get_text(strip=True) if soup.title else "No title")

print("\nNUMBER OF TABLES:")
print(len(soup.find_all("table")))

print("\nNUMBER OF LINKS:")
print(len(soup.find_all("a", href=True)))

print("\nFIRST 3000 CHARACTERS OF PAGE TEXT:")
print(soup.get_text(" ", strip=True)[:3000])

print("\nFIRST 15 PDF LINKS:")
count = 0

for link in soup.find_all("a", href=True):
    href = link["href"]

    if ".pdf" in href.lower():
        print(link.get_text(" ", strip=True), "->", href)
        count += 1

    if count == 15:
        break
