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


def get_all_vacancies(lang):
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


def get_vacancies_superjob():
    vac_path = 'https://api.superjob.ru/2.0/vacancies/'
    head = {
        'X-Api-App-Id':'v3.h.3647339.cbe4828cad13eb79d9bc1f91d0c5f17fc48daa61.401d2bd2746a166ccdd2ba598be642dedfc8ce55',
    }
    payload = {
        'town':'4',
        'keyword':'python',
    }
    response = requests.get(vac_path, headers=head, params=payload).json()
    return response

def get_predict_rub_salary_sj(vacancies, vacancy_id):

    print(vacancy_id)
    for i in range(len(vacancies)):
        print('++ {} ++'.format(vacancies[i]['id']))
        if int(vacancies[i]['id']) == vacancy_id:
            salary_currency = vacancies[i]['currency']
            salary_from = vacancies[i]['payment_from']
            salary_to = vacancies[i]['payment_to']
            salary = vacancies[i]['payment']

            if salary_currency != 'rub':
                print('salary_currency is {}'.format(salary_currency))
                return None
            elif salary_from == 0:
                print('salary_from is {}'.format(salary_from))
                return salary_to * 0.8
            elif salary_to == 0:
                print('salary_to is {}'.format(salary_to))
                return salary_from * 1.2
            elif salary == 'null':
                print('salary is {}'.format(salary))
                return None
            else:
                return (salary_from+salary_to)/2

    # TODO return number or None

def predict_rub_salary_for_SuperJob():
    return

if __name__ == '__main__':
    start_time = time.time()

    vacancies = get_vacancies_superjob()['objects']

    print(get_predict_rub_salary_sj(vacancies, 31852228))
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
