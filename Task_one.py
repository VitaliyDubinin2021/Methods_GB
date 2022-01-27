# В качестве работного сайти используем HeadHunter Russia.

import requests

import pandas as panda
from bs4 import BeautifulSoup as BS

print('Здравствуйте! В качестве работного сайти используем HeadHunter Russia')
print('Результат поиска по вашему запросу будет представлен в .csv-формате!')
goal_searching = input('Спасибо, что выбрали нашу программу по поиску '
                       'вакансий! Пожалуйста, введите параметры для поиска: ')

if not goal_searching:
    goal_searching = 'Python-developement'

points = {
    'page': '0',
    'salary': '',
    'text': goal_searching
}

names = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}

address = 'https://hh.ru/search/vacancy'

result_bs = BS(requests.get(address, headers=names, params=points).text, 'html.parser')

our_list = result_bs.find_all('div', {'class': ['vacancy-serp-item', 'vacancy-serp-item_redesigned']})
jobs_searching = []

number_of_page = 2

while our_list:
    for python_job in our_list:
        title = python_job.find('a', {'data-qa':'vacancy-serp__vacancy-title'})
        dictionary_python_job = {'title' : title.text.replace(',', ';')}
        dictionary_python_job['link'] = title.get('href').split('?')[0]
        salary = python_job.find('span', {'data-qa':'vacancy-serp__vacancy-compensation'})

        if salary:
            salary = salary.getText().replace('\u202f', '').replace('\xa0', '')
            salary_list = salary.split()
            if salary_list[0].isalpha():
                dictionary_python_job['salary_minimal'] = None
                dictionary_python_job['normal_salary'] = salary_list[-1]
                dictionary_python_job['salary_maximal'] = int(salary_list[1])


            else:
                dictionary_python_job['salary_minimal'] = int(salary_list[0])
                dictionary_python_job['normal_salary'] = salary_list[-1]
                dictionary_python_job['salary_maximal'] = int(salary_list[2])

        else:
            dictionary_python_job['salary_minimal'] = None
            dictionary_python_job['salary_maximal'] = None
            dictionary_python_job['normal_salary'] = None

        dictionary_python_job['source'] = 'hh.ru'
        jobs_searching.append(dictionary_python_job)

    number_of_page += 1

    points['page'] = str(number_of_page)
    result_bs = BS(requests.get(address, headers=names, params=points).text, 'html.parser')

    our_list = result_bs.find_all('div', {'class': ['vacancy-serp-item', 'vacancy-serp-item_redesigned']})

print('Результат поиска по Вашему запросу представлен ниже: ')

result = panda.DataFrame(jobs_searching)
print(result.to_string())

result.to_csv('Task_one_result_to_scv.csv', sep='\t', encoding='utf-8')






