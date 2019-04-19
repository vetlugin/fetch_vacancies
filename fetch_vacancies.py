import os
import time
import requests
from dotenv import load_dotenv
from terminaltables import SingleTable

langs = [
    'JavaScript',
    'Java',
    'Python',
    'Ruby',
    'PHP',
    'C++',
    'Go',
    'Objective-C',
    'Scala',
    'Swift',
    'C#'
]

langs = [
    'JavaScript',
    'Java',
    'Python',
    'Ruby',
    'PHP',
    'C++',
    'Go',
    'Objective-C',
    'Scala',
    'Swift',
    'C#'
]


def search_dict_in_list(list_for_searching, key_item, value_item):
    '''
    The function searches an entry with the key 'key_dict' equal in value to
    'key_search' in a list of dictionaries.

    Keywords arguments:
    list_for_searching -- list of dictionaries for searching
    key_item -- key in dictionary we want to find
    value_item -- value we want to find

    '''
    for item_of_list in list_for_searching:
        if str(item_of_list[key_item]) == str(value_item):
            return item_of_list
    return None


def calculate_expected_salary(salary_currency, salary_to, salary_from):
    # Если валюта не равна рублям - возвращаем None
    if salary_currency != 'rub' and salary_currency != 'RUR':
        return None
    elif salary_from == None or salary_from == 0:
        return salary_to * 0.8
    elif salary_to == None or salary_to == 0:
        return salary_from * 1.2
    else:
        return (salary_from+salary_to)/2


def get_vacancies_hh(lang):
    '''
    The function accesses to HeadHunter website and returned JSON data of
    all vacancies of programmers by language 'lang'.

    Keywords arguments:
    lang -- language for searching vacancies of programmers

    '''
    page = pages_number = 0
    all_vacancies = []
    vac_path = 'https://api.hh.ru/vacancies/'

    # Перебираем все страницы
    while page <= pages_number:
        payload = {
            'text': 'программист',
            'text': lang,
            'area': '1',
            'period': '30',
            'per_page': '100',
            'page': page,
        }
        response = requests.get(vac_path, params=payload).json()
        try:
            page_data = response['items']
            pages_number = response['pages']
            vac_found = response['found']
        except KeyError:
            break

        page += 1
        all_vacancies += page_data
    return all_vacancies


def get_vacancies_sj(lang):
    '''
    The function accesses to HeadHunter website and returned JSON data of
    all vacancies of programmers by language 'lang'.

    Keywords arguments:
    lang -- language for searching vacancies of programmers

    '''

    load_dotenv()  # Загружаем переменные окружения, где хранится токен
    token = os.getenv("TOKEN")

    head = {
        'X-Api-App-Id': token,
    }

    page = pages_number = 0
    all_vacancies = []
    vac_path = 'https://api.superjob.ru/2.0/vacancies/'

    while page <= pages_number:
        payload = {
            'town': '4',
            'keyword': lang,
            'page': page,
            'count': 100,
        }
        response = requests.get(vac_path, headers=head, params=payload).json()
        try:
            page_data = response['objects']
            vac_found = response['total']
            pages_number = int(vac_found/100) + 1
        except KeyError:
            break
        page += 1
        all_vacancies = all_vacancies + page_data

    return all_vacancies


def get_lang_rating_hh(count=0):
    '''
    The function returns a dictionary
    is conteined {language: count of vacancies} pair.

    Keywords arguments:
    count -- The minimum number of vacancies to take part in calculate
    Default parameter value is 0.

    '''

    lang_rating = {}
    for lang in langs:
        vacancies = len(get_vacancies_hh(lang))
        if vacancies >= count:
            lang_rating[lang] = vacancies
    return lang_rating


def get_lang_rating_sj(count=0):
    '''
    The function returns a dictionary
    is conteined {language: count of vacancies} pair.

    Keywords arguments:
    count -- The minimum number of vacancies to take part in calculate
    Default parameter value is 0.

    '''

    lang_rating = {}
    for lang in langs:
        vacancies = len(get_vacancies_sj(lang))
        if vacancies >= count:
            lang_rating[lang] = vacancies
    return lang_rating


def predict_rub_salary_hh(vacancy_id, vacancies):
    '''
    The function predicts vacancie's salary in rubles.

    Keywords arguments:
    vacancy_id -- ID of vacancie on HeadHunter site.
    vacancies -- list of all vacancies with parameters.

    If key 'currency' is None function return None.
    If key 'salary_to' is None function return salary_from * 1.2
    If key 'salary_from' is None function return salary_to * 0.8
    If key 'salary_to' and 'salary_from' is not None
    function return (salary_from + salary_to) / 2
    '''
    for vacancie_item in vacancies:
        if int(vacancie_item['id']) == vacancy_id:
            salary = vacancie_item['salary']
            if salary == None:
                return None

            salary_currency = vacancie_item['salary']['currency']
            salary_from = vacancie_item['salary']['from']
            salary_to = vacancie_item['salary']['to']

    return calculate_expected_salary(salary_currency, salary_to, salary_from)


def predict_rub_salary_sj(vacancy_id, vacancies=None):
    '''
    The function predicts vacancie's salary in rubles.

    Keywords arguments:
    vacancy_id -- ID of vacancie on SuperJob site.
    vacancies -- list of all vacancies with parameters.
    If vacancies is None function get vacancie data on SuperJob site.

    If key 'currency' is None function return None.
    If key 'salary_to' is None function return salary_from * 1.2
    If key 'salary_from' is None function return salary_to * 0.8
    If key 'salary_to' and 'salary_from' is not None
    function return (salary_from + salary_to) / 2
    '''

    # Если в функцию не передали список вакансий, то делаем прямой запрос
    # на SuperJob и ищем вакансию там
    if vacancies == None:
        load_dotenv()  # Загружаем переменные окружения, где хранится токен
        token = os.getenv("TOKEN")
        head = {
            'X-Api-App-Id': token,
        }
        vac_path = 'https://api.superjob.ru/2.0/vacancies/{}/'.format(vacancy_id)
        response = requests.get(vac_path, headers=head).json()
    # Если на вход функции принят список вакансий, то ищем в нём нужную вакасию
    else:
        response = search_dict_in_list(vacancies, 'id', vacancy_id)
    # Используем try: на случай если в словаре не будет необходимых ключей
    try:
        salary_currency = response['currency']
        salary_to = response['payment_to']
        salary_from = response['payment_from']
    except KeyError:
        return

    return calculate_expected_salary(salary_currency, salary_to, salary_from)


def get_salary_by_lang_hh(lang):
    '''
    The function get dictionary with salary by languages.

    Keywords arguments:
    lang -- language for searching vacancies of programmers

    Function return dictionary like this:
        {
        "vacancies_found": 1000,    # - Количество найденых вакансий
        "vacancies_processed": 10,  # - Количество вакансий в расчёте
        "average_salary": 100000    # - Средняя зарплата
        }
    '''
    vacancies = get_vacancies_hh(lang)
    vacancies_found = len(vacancies)

    vacancies_processed = 0
    sum_salary_by_lang = 0

    for vacancie_item in vacancies:
        predicted_salary_by_id = predict_rub_salary_hh(int(vacancie_item['id']), vacancies)
        if predicted_salary_by_id is not None:
            vacancies_processed += 1
            sum_salary_by_lang += predicted_salary_by_id

    try:
        average_salary = sum_salary_by_lang / vacancies_processed
    except ZeroDivisionError:
        average_salary = 0

    return {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(sum_of_lang_salary//500*500)
            }


def get_salary_by_lang_sj(lang):
    '''
    The function get dictionary with salary by languages.

    Keywords arguments:
    lang -- language for searching vacancies of programmers

    Function return dictionary like this:
        {
        "vacancies_found": 1000,    # - Количество найденых вакансий
        "vacancies_processed": 10,  # - Количество вакансий в расчёте
        "average_salary": 100000    # - Средняя зарплата
        }
    '''
    vacancies = get_vacancies_sj(lang)
    vacancies_found = len(vacancies)

    vacancies_processed = 0
    sum_salary_by_lang = 0

    for vacancie_item in vacancies:
        predicted_salary_by_id = predict_rub_salary_sj(int(vacancie_item['id']), vacancies)
        if predicted_salary_by_id is not None:
            vacancies_processed += 1
            sum_salary_by_lang += predicted_salary_by_id

    try:
        average_salary = sum_salary_by_lang / vacancies_processed
    except ZeroDivisionError:
        average_salary = 0

    return {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(average_salary //500*500)
            }


def print_table(salary_date, title):
    '''
    The function print data in terminaltable styleself.

    Keywords arguments:
    salary_date -- list of data for printing
    title -- title of table

    '''
    TABLE_DATA = [(
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    )]

    for item in salary_date:
        TABLE_DATA.append((
            item,
            salary_date[item]['vacancies_found'],
            salary_date[item]['vacancies_processed'],
            salary_date[item]['average_salary']
        ))

    # SingleTable.
    table_instance = SingleTable(TABLE_DATA, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()


if __name__ == '__main__':
    start_time = time.time()

    data_hh = {lang:get_salary_by_lang_hh(lang) for lang in langs}
    print_table(data_hh, ' HeadHunter Moscow ')

    data_sj = {lang: get_salary_by_lang_sj(lang) for lang in langs}
    print_table(data_sj, ' SuperJob Moscow ')

    print("--- %s seconds ---" % (time.time() - start_time))
