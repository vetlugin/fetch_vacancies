import requests

def get_vacancies(lang):
    vac_path = 'https://api.hh.ru/vacancies/'

    payload = {
        'text':'программист',
        'text':lang,
        'area':'3',
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

def get_salary_by_lang(lang):

    vacancies = get_vacancies(lang).json()['items']

    salary = []
    for i in range(len(vacancies)):
        salary.append(vacancies[i]['salary'])
    return salary

if __name__ == '__main__':
    #print(get_lang_rating(150))
    print(get_salary_by_lang('python'))
