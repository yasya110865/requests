import requests
import pprint
import json

url = 'https://api.hh.ru/vacancies'
vacance = 'Data scientist'
params = {
    'text': vacance,
    # есть страницы т.к. данных много
    'page': 0,

}

result = requests.get(url, params=params).json()
#количество страниц
pages_count = result['pages']

#это будет список данных по каждой вакансии
it = []
for i in range(pages_count):
    params = {'text': vacance,
              'page': i

    }
    result = requests.get(url, params=params).json()
    items = result['items']
    it += items

#число найденных вакансий
num_vacances = len(it)

#списки для зарплаты от и до
s_from = []
s_to = []

#если указана зарплата, то добавляем значения в соответствующий список
for i in range(len(it)):
    if it[i]['salary']:
        if it[i]['salary']['from']:
             s_from.append(it[i]['salary']['from'])
        if  it[i]['salary']['to']:
            s_to.append(it[i]['salary']['to'])

#считаем среднюю зарплату нижнюю и верхнюю
mean_salaryfrom = round(sum(s_from)/len(s_from))
mean_salaryto = round(sum(s_to)/len(s_to))


#список требований к кандидатам
requirements = []
for i in range(len(it)):
    req = it[i]['snippet']['requirement']
    requirements.append(req)


#словарь для подсчета количества упоминаний разных скиллов, для начала = 0
req_dict = {
    'Python': 0,
    'ML': 0,
    'SQL':0,
    'DL': 0,
    'Pandas': 0,
    'Numpy': 0,
    'Keras': 0,
    'PyTorch': 0,
    'Sklearn': 0,
    'Matplotlib': 0,
    'Requests': 0,
    'C#, Java': 0,
    'Math skills': 0,
    'English': 0
}

#если есть в строке упоминание, плюсуем к значению в словаре
for req in requirements:


    if 'ython' in req:
        req_dict['Python'] += 1

    if 'ML' in req:
        req_dict['ML'] += 1

    if 'SQL' in req:
        req_dict['SQL'] += 1

    if 'DL'  in req or 'нейрон' in req or 'глубок' in req:
        req_dict['DL'] += 1

    if 'English'  in req or 'английс' in req:
        req_dict['English'] += 1

    if 'ytorch' in req:
        req_dict['PyTorch'] += 1

    if 'andas' in req:
        req_dict['Pandas'] += 1

    if 'umpy' in req:
        req_dict['Numpy'] += 1

    if 'eras' in req:
        req_dict['Keras'] += 1

    if 'klearn' in req:
        req_dict['Sklearn'] += 1

    if 'atplotlib' in req:
        req_dict['Matplotlib'] += 1

    if 'equests' in req:
        req_dict['Requests'] += 1

    if 'C#' in req or 'Java' in req:
        req_dict['C#, Java'] += 1

    if 'матем' in req or 'статист' in req or 'mathem' in req or 'statist' in req:
        req_dict['Math skills'] += 1



#сортируем словарь по значениям
req_dict = dict(sorted(req_dict.items(), key=lambda x: x[1], reverse=True))

#Сптсок для процентов как часто требуются разные скиллы
persents = []
for i in range(len(req_dict)):
    pers = round(list(req_dict.values())[i] * 100/sum(req_dict.values()))
    persents.append(pers)


#cписок скиллов, в него добавляем по каждому требуемому навыку название, количество и процент
skills = []
for i in range(len(req_dict)):
    info = {'name':list(req_dict.keys())[i],
            'count':list(req_dict.values())[i],
            'persent':persents[i]
            }
    skills.append(info)


#создаем финальный файл

final = {
    'name': vacance,
    'count': num_vacances,
    'salary':{'from':mean_salaryfrom,
              'to':mean_salaryto},
    'skills': skills
}


with open('hh.json', 'w') as f:
    json.dump(final, f)

with open('hh.json', 'r') as f:
    text = json.load(f)
    print(json.dumps(text, indent=2, sort_keys=True))