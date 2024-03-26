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
