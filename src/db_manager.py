import psycopg2
from courswork.config import config


class DBManager:
    def __init__(self, database_name):
        self.database_name = database_name
        self.params = config()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employer_name, COUNT(vacancy_name) FROM vacancies JOIN employers
                USING (employer_id) GROUP BY employer_name
                ORDER BY COUNT(vacancy_name) DESC;
                """)

            data = cur.fetchall()
        conn.close()
        return data

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employer_name, vacancy_name, salary, url FROM vacancies
                JOIN employers USING (employer_id)
                """)

            data = cur.fetchall()
        conn.close()
        return data

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name, ROUND(AVG(salary)) as avg_salary 
                FROM vacancies GROUP BY vacancy_name;
                """)

            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                ORDER BY salary DESC;
                """)

            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{keyword}%'")

            data = cur.fetchall()
        conn.close()
        return data
