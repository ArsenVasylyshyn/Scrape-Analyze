from src.scraper import get_all_vacancies_html_selenium, parse_vacancies_from_html, parse_each_vacancy
from src.sqlite_db import init_db, insert_vacancy_with_technologies
from src.export import save_to_csv
import time    

if __name__ == "__main__":
    LIMIT_ENABLED = False  # 🔁 Enable False to process all vacancies
    LIMIT = 40             # 🔢 How many to process, if enabled limit

    init_db() # Initialize the database

    html = get_all_vacancies_html_selenium(limit=LIMIT if LIMIT_ENABLED else float('inf'))
    results = parse_vacancies_from_html(html)
    print(f"🔗 Total found vacancies after loading: {len(results)}") 

    all_data = []
    for i, (title, company, link) in enumerate(results):
        if LIMIT_ENABLED and i >= LIMIT:
            break

        print(f"🔍 Company: {company}")
        print(f"📌 Vacancy title: {title}")
        print(f"🔗 Link: {link}")

        keywords = parse_each_vacancy(link)
        insert_vacancy_with_technologies(title, company, link, keywords)

        all_data.append((title, company, link, keywords))

        print("💾 Saved to database")    
        print("-" * 50)
        time.sleep(1)

    # Save to CSV after parsing
    save_to_csv(all_data)