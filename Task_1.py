"""
Урок 3 - задание № 1 - Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать
функцию, которая будет добавлять только новые вакансии в вашу базу. Работный сайт - Head Hunter Russia.
"""


from bs4 import BeautifulSoup
from pymongo import errors
import requests
import re
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 25251)
db = client['hh_vacancy']

js_vacancy = db.js_vacancy


def our_jobs(page, object, update=True):
    uri = 'https://hh.ru/search/vacancy'
    parametrs = {'text': object,
              'page': page,
              'items_on_page': 17
              }
    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}


    replying = requests.get(uri, parametrs=parametrs, heads=heads)
    result = BeautifulSoup(replying.text, 'html.parser')

    list_with_vacancies = result.find_all('div', {'class': 'vacancy-serp-item'})
    if not list_with_vacancies:
        one.append(True)
        return

    for vacancy in list_with_vacancies:
        connection = vacancy.find('a').get('href')
        if connection.find('hh.ru') != -1:
            connection = re.search(r'hh.ru\S([^?#]*)', connection).group()
            _id = re.search(r'(\d*)$', connection).group()
        else:
            _id = connection

        if update and js_vacancy.find_one({'_id': _id}):
            continue

        vacancy_name = vacancy.find('a').getText().replace('\xa0', ' ')

        payroll = {'min': None, 'max': None, 'currency': None}

        payroll_list = vacancy.find_all('span', {'class': 'bloko-header-section-3'})
        if len(payroll_list) > 1:
            payroll_list = payroll_list[1].getText().replace('\u202f', '').replace('\xa0', '').split(' ')
            payroll['currency'] = payroll_list[-1]

            if len(payroll_list) == 4:
                payroll['min'] = int(payroll_list[0])
                payroll['maxn'] = int(payroll_list[2])
            elif len(payroll_list) == 3:

                if payroll_list[0] == 'от':
                    payroll['min'] = int(payroll_list[1])
                elif payroll_list[0] == 'до':
                    payroll['max'] = int(payroll_list[1])

        try:
            js_vacancy.insert_one({'_id': _id,
                                   'vacancy_name': vacancy_name,
                                   'connection': connection,
                                   'payroll': payroll,
                                   'job_site': 'hh.ru'
                                   })
        except errors.DuplicateKeyError:
            continue

object = 'Java Script'


z = 0
one = []
while not one:
    our_jobs(z, object)
    print(z)
    z += 1