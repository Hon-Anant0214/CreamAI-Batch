
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "Data" / "records.json"

df = pd.read_json(DATA_FILE)

print("\n--- GATENavigator Data Analysis ---")

# Fact 1: Total number of papers
print("\n1. Total number of papers:", len(df))

# Fact 2: Number of unique paper codes
print("2. Unique paper codes:", df["paper_code"].nunique())

# Fact 3: Papers with syllabus sections available
available = df["syllabus_sections"].apply(
    lambda sections: len(sections) > 0
).sum()

print("3. Papers with syllabus sections:", available)
