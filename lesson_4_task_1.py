from lxml import html
import requests

from pymongo import MongoClient
from pprint import pprint


def goal(url='https://yandex.ru/news'):
    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    }

    aim = requests.get(url, heads=heads).text

    with open("aim.html", 'w', encoding='utf-8') as f:
        f.write(aim)

def parsing(goal_to_news):
    information = {}
    name = goal_to_news.xpath(".//h2[@class='mg-card__title']/a/text()")[0].replace('\xa0',' ')
    info_time = goal_to_news.xpath(".//span[@class='mg-card-source__time']/text()")[0]
    resource = goal_to_news.xpath(".//span[@class='mg-card-source__source']//a/text()")[0]
    connection = goal_to_news.xpath(".//h2[@class='mg-card__title']/a/@href")[0]
    print(name, info_time, resource, connection)
    information['information'], information['info_time'], information['resource'], information['connection'] = name, info_time, resource, connection
    return information

def parsing_from_yandex():
    list_with_news = {}
    with open("aim.html", 'r', encoding='utf-8') as f:
        aim = str(f.read())
    purpose = html.fromstring(aim)
    main_things = purpose.xpath("//section[@aria-labelledby]")
    for main_thing in main_things:
        names = main_thing.xpath(".//h1//text()")
        for main_thing_title in names:
            information = []
            if main_thing_title == 'Главное':
                main_info = main_thing.xpath(".//div[contains(@class, 'mg-grid__col_xs_8')]")
                information.append(parsing(main_info[0]))
                news_info = main_thing.xpath(".//div[contains(@class, 'mg-grid__col_xs_4')]")
                for goal_to_news in news_info:
                    information.append(parsing(goal_to_news))
                list_with_news[main_thing_title] = information
            else:
                main_info = main_thing.xpath(".//div[contains(@class, 'mg-grid__col_xs_4')]")
                information.append(parsing(main_info[0]))
                news_info = main_thing.xpath(".//div[contains(@class, 'mg-grid__col_xs_6')]")
                for goal_to_news in news_info:
                    information.append(parsing(goal_to_news))
                list_with_news[main_thing_title] = information
    return(list_with_news)


if __name__ == '__main__':
    goal()
    client = MongoClient('127.0.0.1', 25251)
    one = client['Yandex-News']
    city_name = 'Оренбург'
    resulting_search = parsing_from_yandex()[city_name]
    pprint(resulting_search)
    one.result_parse.insert_many(resulting_search)

