import requests

def get_vacancies():
    vac_path = 'https://api.hh.ru/vacancies/'

    payload = {
        'text':'программист',
        'text':'python',
    }
    response = requests.get(vac_path, params=payload)
    return response

if __name__ == '__main__':
    response = get_vacancies().json()['items']
    for vacancy in range(len(response)):
        print(response[vacancy]['name'])
