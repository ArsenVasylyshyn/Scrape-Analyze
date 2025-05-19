import sqlite3
from pathlib import Path

# 📋 Database path
DB_PATH = Path("data/vacancies.db")

# 📋 Initialize database
def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        link TEXT UNIQUE NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technologies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy_technologies (
        vacancy_id INTEGER NOT NULL,
        technology_id INTEGER NOT NULL,
        FOREIGN KEY (vacancy_id) REFERENCES vacancies(id),
        FOREIGN KEY (technology_id) REFERENCES technologies(id),
        UNIQUE (vacancy_id, technology_id)
    )""")

    conn.commit()
    conn.close()

# 📋 Insert vacancy with technologies
def insert_vacancy_with_technologies(title, company, link, tech_list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT OR IGNORE INTO vacancies (title, company, link) VALUES (?, ?, ?)",
            (title, company, link)
        )
        conn.commit()

        cursor.execute("SELECT id FROM vacancies WHERE link = ?", (link,))
        vacancy_id = cursor.fetchone()[0]

        for tech in tech_list:
            cursor.execute("INSERT OR IGNORE INTO technologies (name) VALUES (?)", (tech,))
            cursor.execute("SELECT id FROM technologies WHERE name = ?", (tech,))
            tech_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT OR IGNORE INTO vacancy_technologies (vacancy_id, technology_id) VALUES (?, ?)",
                (vacancy_id, tech_id)
            )

        conn.commit()

    finally:
        conn.close()