import requests
import pprint
import time

def get_vacancies(lang):
    vac_path = 'https://api.hh.ru/vacancies/'
    payload = {
        'text':'программист',
        'text':lang,
        'area':'1',
        'period': '30',
    }
    response = requests.get(vac_path, params=payload)
    return response

def search_dict_in_list(list_for_searching, key_dict, key_search):
    '''Функция ищет в списке словарей, словарь в котором есть запись с ключом key_dict равная по значению key_search'''
    for i in range(len(list_for_searching)):
        if str(list_for_searching[i][key_dict]) == str(key_search):
            return list_for_searching[i]
    return None

def get_all_vacancies(lang):  #Function is ready
    '''Функция выдает все вакансии по заданному языку программирования'''

    page = pages_number = 0
    all_vacancies = []
    vac_path = 'https://api.hh.ru/vacancies/'

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

        #Отладка функции get_all_vacancies
        #pprint.pprint(page_data)

        #print('Длина списка all_vacancies = {}'.format(len(all_vacancies))) # Отладочный print
        #print('Количество вакансий на странице = {}'.format(len(page_data))) # Отладочный print
        #print('Номер страницы = {}'.format(page)) # Отладочный print
        #print('Всего страниц = {}'.format(pages_number)) # Отладочный print
        #print('Найдено вакансий = {}'.format(vac_found)) # Отладочный print
        #print("______________________________")

        #a = input('Дальше?')
        #if a == 'z':
        #    break
        #End of debugging get_all_vacancies

        page += 1

        all_vacancies = all_vacancies + page_data

    return all_vacancies


def get_lang_rating(count):
    langs = ['JavaScript', 'Java', 'Python', 'Ruby','PHP','C++','C','Go','Objective-C','Scala','Swift','C#']
    lang_rating = {}
    for lang in langs:
        vacancies = get_vacancies(lang).json()['found']
        if vacancies >= count:
            lang_rating[lang] = vacancies

    return lang_rating

def get_salary_by_lang(vacancies):
    '''Возвращает зарплаты при заданном языке программирования. На вход принимает результат работы функции get_vacancies'''
    salary = []
    for i in range(len(vacancies)):
        salary.append(vacancies[i]['salary'])
    return salary

def predict_rub_salary(vacancies, vacancy_id):
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

def get_salary_by_lang(lang):
    '''Function return dictionary like this:
        {
        "vacancies_found": 1000,    # - Количество найденых вакансий
        "vacancies_processed": 10,  # - Количество вакансий в расчёте средней зарплаты
        "average_salary": 100000    # - Средняя зарплата
        }
    '''
    vacancies = get_all_vacancies(lang)
    vacancies_found = len(vacancies)
    #print("Amount of vacancies: {}".format(vacancies_found)) # Test print

    vacancies_processed = 0
    average_salary = 0

    for i in range(vacancies_found):
        salary_id = predict_rub_salary(vacancies, int(vacancies[i]['id']))
        #print("Salary ID of {} -- is: {}".format(i, salary_id)) # Test print
        if salary_id != None:
            vacancies_processed += 1
            average_salary += salary_id

    return {
            'vacancies_found':vacancies_found,
            'vacancies_processed':vacancies_processed,
            'average_salary':int(average_salary/vacancies_processed)
            }

def average_salary_by_lang():
    '''Function return dictionary of dictionaries with results of works get_salary_by_lang function.'''

    langs = ['JavaScript', 'Java', 'Python', 'Ruby','PHP','C++','Go','Objective-C','Scala','Swift','C#']
    average_salary_by_lang = {}
    for lang in langs:
        average_salary_by_lang[lang] = get_salary_by_lang(lang)
    return average_salary_by_lang


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

def predict_rub_salary_sj(vacancy_id, vacancies=None):
    '''Функция предсказывает зарплату по вакансиям сайта SuperJob.'''

    if vacancies == None:
        head = {
            'X-Api-App-Id':'v3.h.3647339.cbe4828cad13eb79d9bc1f91d0c5f17fc48daa61.401d2bd2746a166ccdd2ba598be642dedfc8ce55',
        }
        vac_path = 'https://api.superjob.ru/2.0/vacancies/{}/'.format(vacancy_id)
        response = requests.get(vac_path, headers=head).json()
        try:
            salary_currency = response['currency']
            salary_to = response['payment_to']
            salary_from = response['payment_from']
        except KeyError:
            return
    else:
        for i in range(len(vacancies)):
            if int(vacancies[i]['id']) == vacancy_id:
                salary_currency = vacancies[i]['currency']
                salary_from = vacancies[i]['payment_from']
                salary_to = vacancies[i]['payment_to']
            break
        return -1

    if salary_currency != 'rub':
        return None

    if salary_from == 0 and salary_to == 0:
        return None

    if salary_to == 0 and salary_from != 0:
        return salary_from * 1.2

    if salary_from == 0 and salary_to != 0:
        return salary_to * 0.8

    return (salary_from+salary_to)/2

if __name__ == '__main__':
    start_time = time.time()

    vacancies = get_vacancies_sj('python')

    print(search_dict_in_list(vacancies, 'profession', 'Разработчик Python'))
    #print(type(vacancies))
    #print(predict_rub_salary_sj(32018045,vacancies))

    #print(len(vacancies))




    #print('Вызов со всей ЗП по нулям.  {}'.format(predict_rub_salary_sj(vacancies,31625649)))

    #print('Вызов с только с from.  {}'.format(predict_rub_salary_sj(vacancies,31686638)))
    #print('Вызов с только с to.  {}'.format(predict_rub_salary_sj(vacancies,31756672)))
    #print('Вызов когда есть to и from, payment=0.  {}'.format(predict_rub_salary_sj(vacancies,31947344)))

    #for vacancy in vacancies:
    #    print('{}, {}'.format(vacancy['profession'],vacancy['town']['title']))

    #v3.h.3647339.cbe4828cad13eb79d9bc1f91d0c5f17fc48daa61.401d2bd2746a166ccdd2ba598be642dedfc8ce55
    #code=f65ca76e3ef77f7c16fdf74aeac893b6393358de6a9f5360d6c0e09811a2f8e3.9abdd22caeda398b73f47c49bc7ba1e895b1caa7

    print("--- %s seconds ---" % (time.time() - start_time))

#    pprint.pprint(average_salary_by_lang())
#    print ('Тест функции {}'.format('get_all_vacancies'))
#    get_all_vacancies('python')

            #Отладка функции get_all_vacancies
            #pprint.pprint(page_data)

            #print('Длина списка all_vacancies = {}'.format(len(all_vacancies))) # Отладочный print
            #print('Количество вакансий на странице = {}'.format(len(page_data))) # Отладочный print
            #print('Номер страницы = {}'.format(page)) # Отладочный print
            #print('Всего страниц = {}'.format(pages_number)) # Отладочный print
            #print('Найдено вакансий = {}'.format(vac_found)) # Отладочный print
            #print("______________________________")

            #a = input('Дальше?')
            #if a == 'z':
            #    break



    #print ('Тест функции {}'.format('get_salary_by_lang'))
    #langs = ['JavaScript', 'Java', 'Python', 'Ruby','PHP','C++','C','Go','Objective-C','Scala','Swift','C#']
    #salary_by_lang = {}
    #for lang in langs:
    #    salary_by_lang[lang] = get_salary_by_lang(lang)
    #print(salary_by_lang)


#    print ('Тест функции {}'.format('predict_rub_salary'))
#    vacancies = get_vacancies('Python').json()['items']
#    for i in range(len(vacancies)):
#        print(predict_rub_salary(vacancies, int(vacancies[i]['id'])))

    #print('Вызов с salary = null.  {}'.format()
    #print('Вызов с USD = {}'.format(predict_rub_salary('Python',30524028)))
    #print('Вызов с from = null.  {}'.format(predict_rub_salary('Python',30223179)))
    #print('Вызов с to = null.  {}'.format(predict_rub_salary('Python',28755864)))
    #print('Полный вызов.  {}'.format(predict_rub_salary('Python',30673508)))
