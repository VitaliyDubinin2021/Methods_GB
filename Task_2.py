"""
Урок 3 - задание №2 - Написать функцию, которая производит поиск и выводит на экран вакансии с заработной
платой больше введённой суммы (необходимо анализировать оба поля зарплаты). То есть цифра
вводится одна, а запрос проверяет оба поля.
"""

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 25251)
z = client['hh_vacancy']
v = 21350

for result in z.js_vacancy.find({'payroll.current': 'руб.',
                               '$or': [{'payroll.min': {'$gt': v}},
                                       {'payroll.max': {'$gt': v}}]}):
    pprint(result)