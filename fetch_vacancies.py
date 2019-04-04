import requests

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

if __name__ == '__main__':

    vacancies = get_vacancies('Python').json()['items']
    for i in range(len(vacancies)):
        print(predict_rub_salary(vacancies, int(vacancies[i]['id'])))


    #print('Вызов с salary = null.  {}'.format()
    #print('Вызов с USD = {}'.format(predict_rub_salary('Python',30524028)))
    #print('Вызов с from = null.  {}'.format(predict_rub_salary('Python',30223179)))
    #print('Вызов с to = null.  {}'.format(predict_rub_salary('Python',28755864)))
    #print('Полный вызов.  {}'.format(predict_rub_salary('Python',30673508)))
