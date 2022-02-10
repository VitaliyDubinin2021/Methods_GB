"""
Урок 6. Scrapy. Парсинг фото и файлов.
I вариант
2) Создать в имеющемся проекте второго паука по сбору вакансий с сайта superjob.
Паук должен формировать item'ы по аналогичной структуре и складывать данные также в БД.
"""

import scrapy
from items import JobparserItem
from scrapy.http import HtmlResponse


class SuperJobfSpider(scrapy.Spider):
    our_domain = ['superjob.ru']
    denomination = 'sjru'
    our_url = ['https://russia.superjob.ru/vacancy/search/?keywords=Python%20middle']

    def our_parse(self, result: HtmlResponse):
        next_page = result.xpath(
            "//a[contains(@class,'dalshe')]/@href").get()
        if next_page:
            yield result.follow(next_page, callback=self.our_parse)

        references = result.xpath(
            "//div[contains(@class,'vacancy-item')]//a[contains(@target,'_blank')]/@href").getall()
        for reference in references:
            yield result.follow(reference, callback=self.parsing_vacancy)

    def parsing_vacancy(self, result: HtmlResponse):
        denomination = result.xpath("//title/text()").get()
        salary = result.xpath('//div[contains(@class, "vacancy-base-info")]/*/*/*/*/span/span/text()').getall()
        url = result.url
        yield JobparserItem(denomination=denomination, salary=salary, url=url)