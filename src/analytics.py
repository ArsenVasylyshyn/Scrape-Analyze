import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from tabulate import tabulate 

DB_PATH = Path("data/vacancies.db")

def analyze_top_technologies(top_n=10):  # 🔧 Change only here
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT t.name AS technology, COUNT(vt.technology_id) AS frequency
    FROM vacancy_technologies vt
    JOIN technologies t ON vt.technology_id = t.id
    GROUP BY vt.technology_id
    ORDER BY frequency DESC
    LIMIT ?;
    """

    df = pd.read_sql_query(query, conn, params=(top_n,))
    conn.close()    


    # 🧾 Table in terminal
    print(f"\n📊 Top {top_n} Technologies:\n")
    print(tabulate(df, headers="keys", tablefmt="pretty", showindex=True))

    # 📊 Diagram
    plt.figure(figsize=(max(8, top_n * 0.6), 6))  # Dynamic width
    plt.bar(df["technology"], df["frequency"], color="cornflowerblue")
    plt.title(f"Top {top_n} Technologies in Job Listings")
    plt.xlabel("Technology")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("data/top_techs.png")
    plt.show()
    
if __name__ == "__main__":
    analyze_top_technologies(top_n=25)  