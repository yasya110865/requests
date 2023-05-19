import requests
import time
import pprint
from collections import Counter
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

# это будет список навыков (в виде словарей name: навык)

collect_skills = []
#тут индекс чтобы не замучать HH
for i in range(len(it[:10])):

    vac_url = it[i]['url']
    vac = requests.get(vac_url).json()
    time.sleep(1)
    # print(vac)
    nonempty_skills = 0
# если не пустое значение у очередной вакансии
    if vac['key_skills']:
        skills_dict = vac['key_skills']
        # print(skills_dict)
        nonempty_skills += 1
        # то добавляем в список
        collect_skills.extend(skills_dict)

# print(collect_skills)
# print(len(collect_skills))

# делаем список из значений
skills_list = []
for i in range(len(collect_skills)):
    skill = list(collect_skills[i].values())
    skills_list.extend(skill)
# print(skills_list)
# считакм количесьво по каждому навыку
skills_result = Counter(skills_list)
# и сортируем
final_skills = dict(sorted(skills_result.items(), key=lambda x: x[1], reverse=True))
# print(final_skills)
# print(len(final_skills))
# print(sum(list(final_skills.values())))
# теперь проценты по количеству каждого навыка
persents = []
for i in range(len(final_skills)):
    pers = round(list(final_skills.values())[i] * 100/sum(final_skills.values()))
    persents.append(pers)
# print(persents)
# print(sum(persents))


#cписок скиллов, в него добавляем по каждому требуемому навыку название, количество и процент
skills = []
for i in range(len(final_skills)):
    info = {'name':list(final_skills.keys())[i],
            'count':list(final_skills.values())[i],
            'persent':persents[i]
            }
    skills.append(info)
pprint.pprint(skills)

final = {
    'name': vacance,
    'count': num_vacances,
    'salary':{'from':mean_salaryfrom,
              'to':mean_salaryto},
    'skills': skills
}


with open('hh.json', 'w', encoding='utf-8') as f:
    json.dump(final, f)

with open('hh.json', 'r', encoding='utf-8') as f:
    text = json.load(f)
    print(json.dumps(text, indent=2, ensure_ascii=False, sort_keys=True))