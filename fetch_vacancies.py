import requests
import pprint

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
            'page': page,
        }
        response = requests.get(vac_path, params=payload).json()

        page_data = response['items']
        pages_number = response['pages']
        vac_found = response['found']

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
    '''Возвращает словарь типа:
        {
        "vacancies_found": 1000,    # - Количество найденых вакансий
        "vacancies_processed": 10,  # - Количество вакансий в расчёте средней зарплаты
        "average_salary": 100000    # - Средняя зарплата
        }
    '''
    response = get_vacancies(lang).json()
    vacancies_found = response['found']
    vacancies = response['items']

    vacancies_processed = 0
    average_salary = 0

    for i in range(len(vacancies)):
        salary_id = predict_rub_salary(vacancies, int(vacancies[i]['id']))
        if salary_id != None:
            vacancies_processed += 1
            average_salary += salary_id

    return {
            'vacancies_found':vacancies_found,
            'vacancies_processed':vacancies_processed,
            'average_salary':int(average_salary/vacancies_processed)
            }


if __name__ == '__main__':
    print ('Тест функции {}'.format('get_all_vacancies'))

    pprint.pprint(get_all_vacancies('scala'))
# отладка функции get_all_vacancies

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
