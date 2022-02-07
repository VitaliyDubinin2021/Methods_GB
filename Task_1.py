"""
Урок 5. Scrapy.
Вариант I.
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный).
Логин тестового ящика: study.ai_172@mail.ru.
Пароль тестового ящика: NextPassword172#.
"""

import time
from pymongo import MongoClient
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

options_from_google_chrome.add_argument("start-maximized")
options_from_google_chrome.add_argument("--headless")
options_from_google_chrome = Options()

with webdriver.Chrome(options=options_from_google_chrome) as aim:
    aim.implicitly_wait(15)
    aim.get('https://e.mail.ru')
    operations = ActionChains(aim)
    our = aim.find_element(By.XPATH, '//input[@name = "username"]')
    our.send_keys('study.ai_172@mail.ru')
    our.send_keys(Keys.ENTER)

    our = aim.find_element(By.XPATH, '//input[@name = "password"]')
    our.send_keys('NextPassword172#')
    our.send_keys(Keys.ENTER)
    now_same_again = 0
    last_users_messages = []
    set_messages = set()
    searcher = '//a[contains(@class, "llc llc_normal")]'

    while True:
        try:
            ours = aim.find_elements(By.XPATH, searcher)
            if ours == last_users_messages:
                now_same_again += 1
                if now_same_again > 10:
                    break
            else:
                now_same_again = 0
                last_users_messages = ours[::]
                for our in ours:
                    link = our.get_attribute('href')
                    set_messages.add(link)

            step_our = len(ours) - 1
            for i in range(step_our):
                operations.send_keys(Keys.ARROW_DOWN)
                operations.perform()
                time.sleep(1.25)
        except Exception:
            print("Процесс скраппинга прерван !!!")
            break

    information_about_messages = []
    for our_message in set_messages:
        dictionary_with_messages = {}
        aim.get(our_message)
        our_titles = aim.find_element(By.CLASS_NAME, "thread-subject").text
        remitter_element = aim.find_element(By.XPATH, "//span[@class = 'letter-contact']")
        remitter = remitter_element.get_attribute('our_titles')
        our_date = aim.find_element(By.CLASS_NAME, "letter__date").text
        goals = aim.find_elements(By.CLASS_NAME, "letter-body")

        our_text = ''
        for goal in goals:
            our_text += goal.text
        dictionary_with_messages['link'] = our_message
        dictionary_with_messages['title'] = our_titles
        dictionary_with_messages['from'] = remitter
        dictionary_with_messages['datestring'] = our_date
        dictionary_with_messages['text'] = our_text
        dictionary_with_messages['current_date'] = datetime.today().strftime('%d-%m-%Y')
        information_about_messages.append(dictionary_with_messages)

    our_client = MongoClient('127.0.0.1', 25251)
    result = our_client['Mail_ru']
    if result.inbox == None:
        result.inbox.insert_many(information_about_messages)
    else:
        for indicator in information_about_messages:
            if not result.inbox.find_one({'link': indicator['link']}):
                result.inbox.insert_one(indicator)