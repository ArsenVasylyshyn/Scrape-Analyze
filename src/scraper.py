import re, time, requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 🔍 Tech keywords
from src.tech_keywords import TECH_KEYWORDS

# 🔍 Extract keywords from text
def extract_keywords(text: str):
    found_keywords = set()
    text_lower = text.lower()

    for category, keywords in TECH_KEYWORDS.items():
        for word in keywords:
            if re.search(rf"\b{re.escape(word)}\b", text_lower):
                found_keywords.add(category)
                break
    return found_keywords

# 🔍 Parse each vacancy
def parse_each_vacancy(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"❌ Error request: {url}")
        return []   

    soup = BeautifulSoup(res.text, "lxml")
    vacancy_text = soup.get_text()
    keywords = extract_keywords(vacancy_text)

    print("🔍 Technologies:", sorted(keywords))
    return sorted(keywords)

# 🔍 Get all vacancies from HTML
def get_all_vacancies_html_selenium(limit=40, max_clicks=10):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://jobs.dou.ua/vacancies/?search=Data+Engineer")
    time.sleep(3)

    clicks = 0
    while clicks < max_clicks:
        try:
            vacancies = driver.find_elements("css selector", "li.l-vacancy")
            print(f"📄 Vacancies on page: {len(vacancies)}")

            if len(vacancies) >= limit:
                print(f"✅ Reached the limit of vacancies: {limit}")
                break

            more_button = driver.find_element("css selector", "div.more-btn a")
            if more_button.is_displayed():
                print("🔘 Click 'More vacancies' button...")
                more_button.click()
                clicks += 1
                time.sleep(3)
            else:
                print("🚫 'More vacancies' button is not displayed.")
                break
        except Exception as e:
            print(f"⚠️ Error loading vacancies or button is missing: {e}")
            break

    html = driver.page_source
    driver.quit()
    return html

# 🔍 Parse vacancies from HTML
def parse_vacancies_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    vacancies = soup.find_all("li", class_=["l-vacancy", "l-vacancy -hot"])

    results = []
    for vacancy in vacancies:
        a_tag = vacancy.find("a", class_="vt")  # link to vacancy
        company_tag = vacancy.find("a", class_="company")  # company name

        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            link = a_tag.get("href")
            company = company_tag.text.strip() if company_tag else "N/A"
            results.append((title, company, link))
    return results