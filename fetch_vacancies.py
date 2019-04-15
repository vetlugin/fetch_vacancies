import requests
import pprint
import time

def search_dict_in_list(list_for_searching, key_dict, key_search):
    '''Функция ищет в списке словарей, словарь в котором есть запись с ключом key_dict равная по значению key_search'''
    for i in range(len(list_for_searching)):
        if str(list_for_searching[i][key_dict]) == str(key_search):
            return list_for_searching[i]
    return None

def get_vacancies_hh(lang):  #Function is ready
    '''Функция выдает все вакансии по заданному языку программирования'''

    page = pages_number = 0
    all_vacancies = []
    vac_path = 'https://api.hh.ru/vacancies/'

    # Перебираем все страницы
    while page <= pages_number:
        payload = {
            'text':'программист',
            'text':lang,
            'area':'1',
            'period': '30',
            'per_page':'100',
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

def get_vacancies_sj(lang): #Function is ready
    '''Get JSON data with vacancies by language'''

    head = {
        'X-Api-App-Id':'v3.h.3647339.cbe4828cad13eb79d9bc1f91d0c5f17fc48daa61.401d2bd2746a166ccdd2ba598be642dedfc8ce55',
    }
    page = pages_number = 0
    all_vacancies = []
    vac_path = 'https://api.superjob.ru/2.0/vacancies/'

    while page <= pages_number:
        payload = {
            'town':'4',
            'keyword':lang,
            'page':page,
            'count':100,
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
    '''Функция возвращает словарь с рейтингом языков по зарплатам'''

    langs = ['JavaScript', 'Java', 'Python', 'Ruby','PHP','C++','C','Go','Objective-C','Scala','Swift','C#']
    lang_rating = {}
    for lang in langs:
        vacancies = len(get_vacancies_hh(lang))
        if vacancies >= count:
            lang_rating[lang] = vacancies
    return lang_rating

def get_lang_rating_sj(count=0):
    '''Функция возвращает словарь с рейтингом языков по зарплатам'''

    langs = ['JavaScript', 'Java', 'Python', 'Ruby','PHP','C++','C','Go','Objective-C','Scala','Swift','C#']
    lang_rating = {}
    for lang in langs:
        vacancies = len(get_vacancies_sj(lang))
        if vacancies >= count:
            lang_rating[lang] = vacancies
    return lang_rating

def predict_rub_salary_hh(vacancy_id, vacancies):
    '''Предсказывает зарплату по id вакансии'''
    for i in range(len(vacancies)):
        if int(vacancies[i]['id']) == vacancy_id:
            salary = vacancies[i]['salary']
            if salary == None:
                return None

            salary_currency = vacancies[i]['salary']['currency']
            salary_from = vacancies[i]['salary']['from']
            salary_to = vacancies[i]['salary']['to']

            if salary_currency != 'RUR':
                return None
            elif salary_from == None:
                return salary_to * 0.8
            elif salary_to == None:
                return salary_from * 1.2
            else:
                return (salary_from+salary_to)/2

def predict_rub_salary_sj(vacancy_id, vacancies=None):
    '''Функция предсказывает зарплату по вакансиям сайта SuperJob.'''

    #Если в функцию не передали список вакансий, то делаем прямой запрос на SuperJob и ищем вакансию там
    if vacancies == None:
        head = {
            'X-Api-App-Id':'v3.h.3647339.cbe4828cad13eb79d9bc1f91d0c5f17fc48daa61.401d2bd2746a166ccdd2ba598be642dedfc8ce55',
        }
        vac_path = 'https://api.superjob.ru/2.0/vacancies/{}/'.format(vacancy_id)
        response = requests.get(vac_path, headers=head).json()
    #Если на вход функции принят список вакансий, то ищем в нём нужную вакасию
    else:
        response = search_dict_in_list(vacancies,'id',vacancy_id)
    #Используем try: на случай если в словаре не будет необходимых ключей (например, при ошибке запроса)
    try:
        salary_currency = response['currency']
        salary_to = response['payment_to']
        salary_from = response['payment_from']
    except KeyError:
        return

    # Если валюта не равна рублям - возвращаем None
    if salary_currency != 'rub':
        return None
    # Если не указаны зарплаты - возвращаем None
    if salary_from == 0 and salary_to == 0:
        return None
    # Если указан только нижний потолок зарплаты, то предсказываем с коэффициентом 1.2
    if salary_to == 0 and salary_from != 0:
        return salary_from * 1.2
    # Если указан только верхний потолок зарплаты, то предсказываем с коэффициентом 0.8
    if salary_from == 0 and salary_to != 0:
        return salary_to * 0.8
    # Если указан весь диапазон зарплат, то передаём среднюю зарплату
    return (salary_from+salary_to)/2

def get_salary_by_lang_hh(lang):
    '''Function return dictionary like this:
        {
        "vacancies_found": 1000,    # - Количество найденых вакансий
        "vacancies_processed": 10,  # - Количество вакансий в расчёте средней зарплаты
        "average_salary": 100000    # - Средняя зарплата
        }
    '''
    vacancies = get_vacancies_hh(lang)
    vacancies_found = len(vacancies)

    vacancies_processed = 0
    average_salary = 0

    for i in range(vacancies_found):
        salary_id = predict_rub_salary_hh(int(vacancies[i]['id']), vacancies)
        if salary_id != None:
            vacancies_processed += 1
            average_salary += salary_id

    if vacancies_processed == 0:
        average_salary = 0
        
    return {
            'vacancies_found':vacancies_found,
            'vacancies_processed':vacancies_processed,
            'average_salary':int(average_salary/vacancies_processed)
            }

def get_salary_by_lang_sj(lang):
    '''Function return dictionary like this:
        {
        "vacancies_found": 1000,    # - Количество найденых вакансий
        "vacancies_processed": 10,  # - Количество вакансий в расчёте средней зарплаты
        "average_salary": 100000    # - Средняя зарплата
        }
    '''
    vacancies = get_vacancies_sj(lang)
    vacancies_found = len(vacancies)

    vacancies_processed = 0
    average_salary = 0

    for i in range(vacancies_found):
        salary_id = predict_rub_salary_sj(int(vacancies[i]['id']), vacancies)
        if salary_id != None:
            vacancies_processed += 1
            average_salary += salary_id

    if vacancies_processed == 0:
        average_salary = 0

    return {
            'vacancies_found':vacancies_found,
            'vacancies_processed':vacancies_processed,
            'average_salary':average_salary
            }

def average_salary_by_lang_hh():
    '''Function return dictionary of dictionaries with results of works get_salary_by_lang function.'''

    langs = ['JavaScript', 'Java', 'Python', 'Ruby','PHP','C++','Go','Objective-C','Scala','Swift','C#']
    average_salary_by_lang = {}
    for lang in langs:
        average_salary_by_lang[lang] = get_salary_by_lang_hh(lang)
    return average_salary_by_lang

def average_salary_by_lang_sj():
    '''Function return dictionary of dictionaries with results of works get_salary_by_lang function.'''

    langs = ['JavaScript', 'Java', 'Python', 'Ruby','PHP','C++','Go','Objective-C','Scala','Swift','C#']
    average_salary_by_lang = {}
    for lang in langs:
        average_salary_by_lang[lang] = get_salary_by_lang_sj(lang)
    return average_salary_by_lang

if __name__ == '__main__':
    start_time = time.time()

    #print(len(get_vacancies_hh('python')))
    #print(len(get_vacancies_sj('python')))
    #print(get_salary_by_lang_hh('python'))
    print(average_salary_by_lang_sj())

    print("--- %s seconds ---" % (time.time() - start_time))
