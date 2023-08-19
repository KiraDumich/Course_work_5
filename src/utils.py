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


def fill_db(data, database_name, params):
    connection = psycopg2.connect(database=database_name, **params)
    for company in data:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO companies (company_name, description, link)'
                           'VALUES (%s, %s, %s)',
                           (company["company"].get("name"),
                            company["company"].get("description"),
                            company["company"].get("alternate_url"),
                            ))

        for vacancy in company["vacancies"]:
            salary = (vacancy["salary"])
            cursor.execute('INSERT INTO vacancies'
                           '(vacancy_id, company_id, vacancy_name, salary, link, description, experience)'
                           'VALUES (%s, %s, %s, %s, %s, %s)',
                           (vacancy["id"], company["company"].get("id"), vacancy["name"], salary,
                            vacancy["alternate_url"], vacancy["snippet"].get("responsibility"),
                            vacancy["experience"].get("name")))

        connection.commit()
        connection.close()
