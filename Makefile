.PHONY: run clean initdb showdb

run:
	python3 main.py

initdb:
	python3 -c "from src import database; database.init_db()"

showdb:
	python3 -m src.show_db

analyze:
	python3 src/analytics.py	

clean:
	rm -f data/vacancies.db data/vacancies.csv