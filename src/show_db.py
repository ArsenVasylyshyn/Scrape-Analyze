import sqlite3
from pathlib import Path
from tabulate import tabulate

# 📋 Database path
DB_PATH = Path("data/vacancies.db")

# 📋 Output vacancies and technologies with limit
def show_vacancies_and_technologies(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 📋 Output vacancies with limit
    cursor.execute("SELECT id, title, company, link FROM vacancies LIMIT ?", (limit,))
    vacancies = cursor.fetchall()
    print("📋 Vacancies:")
    print(tabulate(vacancies, headers=["ID", "Title", "Company", "Link"], tablefmt="grid"))

    # 🧪 Output technologies with limit
    print("\n🧪 Technologies:")
    cursor.execute("SELECT id, name FROM technologies LIMIT ?", (limit,))
    technologies = cursor.fetchall()
    print(tabulate(technologies, headers=["ID", "Technology"], tablefmt="grid"))

    conn.close()

if __name__ == "__main__":
    show_vacancies_and_technologies(limit=5)