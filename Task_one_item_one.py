"""
Урок 6. Scrapy. Парсинг фото и файлов.
I вариант
1) Доработать паука в имеющемся проекте, чтобы он формировал item по структуре:
*Наименование вакансии
*Зарплата от
*Зарплата до
*Ссылку на саму вакансию
И складывал все записи в БД(любую).
"""

import scrapy
from items import JobparserItem
from scrapy.http import HtmlResponse


class HeadHunterSpider(scrapy.Spider):
    our_domain = ['hh.ru']
    denomination = 'hhru'
    our_url = ['https://orenburg.hh.ru/search/vacancy?fromSearchLine=true&text=Python+junior&from=suggest_post']

    def our_parse(self, result: HtmlResponse):
        next_page = result.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield result.follow(next_page, callback=self.our_parse)

        references = result.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for reference in references:
            yield result.follow(reference, callback=self.parsing_vacancy)

    def parsing_vacancy(self, result: HtmlResponse):
        denomination = result.xpath("//h1//text()").get()
        salary = result.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = result.url
        yield JobparserItem(denomination=denomination, salary=salary, url=url)