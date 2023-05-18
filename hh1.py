import requests
import pprint
from collections import Counter
import time
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
collect_skills = []
for i in range(len(items[:10])):

    vac_url = items[i]['url']
    vac = requests.get(vac_url).json()
    nonempty_skills = 0
    print(vac)

    if vac['key_skills']:
        time.sleep()
        skills_dict = vac['key_skills']
        print(skills_dict)
        nonempty_skills += 1
        collect_skills.extend(skills_dict)

print(collect_skills)
print(len(collect_skills))


skills_list = []
for i in range(len(collect_skills)):
    skill = list(collect_skills[i].values())
    skills_list.extend(skill)
print(skills_list)
skills_result = Counter(skills_list)
print(dict(skills_result))
final_skills = dict(sorted(skills_result.items(), key=lambda x: x[1], reverse=True))
print(final_skills)
print(len(final_skills))
print(sum(list(final_skills.values())))

persents = []
for i in range(len(final_skills)):
    pers = round(list(final_skills.values())[i] * 100/sum(final_skills.values()))
    persents.append(pers)
print(persents)
print(sum(persents))


#cписок скиллов, в него добавляем по каждому требуемому навыку название, количество и процент
skills = []
for i in range(len(final_skills)):
    info = {'name':list(final_skills.keys())[i],
            'count':list(final_skills.values())[i],
            'persent':persents[i]
            }
    skills.append(info)
pprint.pprint(skills)
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

