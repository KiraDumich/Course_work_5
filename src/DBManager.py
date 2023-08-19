import psycopg2
from config import config


class DBManager:
    def __init__(self, database_name, params=config()):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        connection = psycopg2.connect(database=self.database_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute('SELECT company_name, COUNT(vacancy_id) '
                           'FROM companies '
                           'JOIN vacancies USING(company_id) '
                           'GROUP BY company_name;')

            data = cursor.fetchall()

        connection.close()
        return data

    def get_all_vacancies(self):
        connection = psycopg2.connect(database=self.database_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute('SELECT title_vacancy, company_name, salary'
                           'FROM vacancies'
                           'JOIN companies USING (company_id);')

            data = cursor.fetchall()

        connection.close()
        return data

    def get_avg_salary(self):
        connection = psycopg2.connect(database=self.database_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute('SELECT company_name, round(AVG(salary)) AS average_salary '
                           'FROM companies '
                           'JOIN vacancies USING (company_id) '
                           'GROUP BY company_name;')

            data = cursor.fetchall()

        connection.close()
        return data

    def get_vacancies_wth_highest_salary(self):
        connection = psycopg2.connect(database=self.database_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute('SELECT * '
                           'FROM vacancies '
                           'WHERE salary > (SELECT AVG(salary) FROM vacancies);')

            data = cursor.fetchall()

        connection.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        connection = psycopg2.connect(database=self.database_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT * 
                FROM vacancies
                WHERE lower(vacancy_name) LIKE '%{keyword}%'
                OR lower(vacancy_name) LIKE '%{keyword}'
                OR lower(vacancy_name) LIKE '{keyword}%'""")

            data = cursor.fetchall()

        connection.close()
        return data
