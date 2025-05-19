import csv
from pathlib import Path

CSV_PATH = Path("data/vacancies.csv")

def save_to_csv(data):
    CSV_PATH.parent.mkdir(exist_ok=True)
    with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        # Add header
        writer.writerow(["ID", "Title", "Company", "Link", "Technologies"])
        
        for idx, (title, company, link, keywords) in enumerate(data, start=1):
            keywords_str = ", ".join(keywords)
            writer.writerow([idx, title, company, link, keywords_str])
    
    print(f"✅ Data saved to {CSV_PATH}")