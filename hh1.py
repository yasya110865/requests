import requests
import pprint
import json

url = 'https://api.hh.ru/vacancies'
vacance = 'python'
params = {
    'text': vacance,'area': 1,
    # есть страницы т.к. данных много
    'page': 0

}

result = requests.get(url, params=params).json()
#количество страниц
pages_count = result['pages']
items = result['items']
vac_url = items[0]['url']
vac = requests.get(vac_url).json()
pprint.pprint(vac)

#это будет список данных по каждой вакансии
# it = []
# for i in range(pages_count):
#     params = {'text': vacance,
#               'page': i
#
#     }
#     result = requests.get(url, params=params).json()
#     items = result['items']
#     it += items

#число найденных вакансий
# num_vacances = len(it)

