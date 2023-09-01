import requests
import psycopg2


def get_data(companies_id):
    """Возвращает список словарей"""
    data = []
    for id in companies_id:
        url = f'https://api.hh.ru/employers/{id}'
        company_response = requests.get(url)
        data_company = company_response.json()
        vacancy_response = requests.get(data_company["vacancies_url"])
        vacancy_data = vacancy_response.json()
        data.append({
            'company': data_company,
            'vacancies': vacancy_data['items']
        })

    return data


def filter_salary(salary):
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return round((salary['from'] + salary['to']) / 2)
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return 0


def fill_db(data, database_name, **params):
    connection = psycopg2.connect(database=database_name, **params)
    for company in data:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO companies (company_id, company_name, description, link)'
                           'VALUES (%s, %s, %s, %s)'
                            'ON CONFLICT (company_id) DO NOTHING',
                           (company["company"].get("id"), company["company"].get("name"),
                            company["company"].get("description"),
                            company["company"].get("alternate_url"),
                            ))

    connection.commit()
    connection.close()


def create_tables(database_name, params):
    connection = psycopg2.connect(database=database_name, **params)
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS companies(
                       company_id int PRIMARY KEY,
                       company_name VARCHAR,
                       description VARCHAR,
                       link VARCHAR)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS vacancies(
                               vacancy_id int PRIMARY KEY,
                               company_id int REFERENCES companies(company_id),
                               vacancy_name VARCHAR,
                               salary INTEGER,
                               link VARCHAR,
                               description VARCHAR,
                               experience VARCHAR
                               )""")
    connection.commit()
    connection.close()


def fill_db_vacancies(data, database_name, **params):
    connection = psycopg2.connect(database=database_name, **params)
    for company in data:
        with connection.cursor() as cursor:
            for vacancy in company['vacancies']:
                salary = filter_salary(vacancy["salary"])
                cursor.execute('INSERT INTO vacancies'
                               '(vacancy_id, company_id, vacancy_name, salary, link, description, experience)'
                               'VALUES (%s, %s, %s, %s, %s, %s, %s)'
                               'ON CONFLICT (vacancy_id) DO NOTHING',
                               (str(vacancy["id"]), str(company["company"].get("id")), str(vacancy["name"]), str(salary),
                                str(vacancy["alternate_url"]), str(vacancy["snippet"].get("responsibility")),
                                str(vacancy["experience"].get("name"))))

    connection.commit()
    connection.close()
