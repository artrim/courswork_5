import requests
import psycopg2


def get_hh_data(employers: list):
    """
    Получение данных о компаниях и вакансиях
    """
    data = []
    employers_list = []
    vacancies_list = []
    for employer in employers:
        company_data = requests.get('https://api.hh.ru/employers/', params={'per_page': 10,
                                                                            'sort_by': 'by_vacancies_open',
                                                                            'text': employer
                                                                            }).json()

        employers_list.extend(company_data['items'])
        for i in company_data['items']:
            vacancy_data = requests.get('https://api.hh.ru/vacancies/', params={"per_page": 20,
                                                                                "employer_id": i[
                                                                                    'id'],
                                                                                'only_with_salary': "true"
                                                                                }).json()

            vacancies_list.extend(vacancy_data['items'])

    data.append({
        'employers': employers_list,
        'vacancies': vacancies_list
    })

    return data


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    employer_name VARCHAR(255)
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy_name VARCHAR NOT NULL,
                    city VARCHAR(50),
                    salary INTEGER,
                    url TEXT
                )
            """)

    conn.commit()
    conn.close()


def save_data_to_database(data, database_name, params):
    """Сохранение данных о компаниях и вакансиях в базу данных. """

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            employer_data = employer['employers']
            for i in employer_data:
                cur.execute(
                    """
                    INSERT INTO employers (employer_id, employer_name) VALUES (%s, %s)
                    """, (i['id'], i['name'])
                )
            vacancies_data = employer['vacancies']
            for vacancy in vacancies_data:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, vacancy_name, city, salary, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy['employer']['id'], vacancy['name'], vacancy['area']['name'],
                     vacancy['salary']['from'], vacancy['alternate_url'])
                )

    conn.commit()
    conn.close()
