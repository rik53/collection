"""1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172!"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from string import whitespace
import os
from dotenv import load_dotenv
from pymongo import MongoClient
MONGO_HOST = "localhost"
MONG0_PORT = 27017
MONGO_DB = "post"
MONGO_COLLECTION = "mail_inbox"
with MongoClient(MONGO_HOST, MONG0_PORT) as client:
    db = client[MONGO_DB]
    mail_inbox = db[MONGO_COLLECTION]

load_dotenv()

USERNAME = os.environ.get("USERNAM", None)
PASSWORD = os.environ.get("PASSWORD", None)
chrome_options = Options()
chrome_options.add_argument('start-maximized')

CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")

driver = webdriver.Chrome(executable_path='/home/rik/PycharmProjects/pythonProject/collection/chromedriver', options=chrome_options)
url = "https://mail.ru/"

def clear_string(s, whitespaces=CUSTOM_WHITESPACE):
    for space in whitespaces:
        s = s.replace(space, " ")
    return s


def auth(url):
    driver.get(url=url)
    elem_login = driver.find_element_by_class_name('email-input')
    elem_login.send_keys(USERNAME)

    button_login = driver.find_element_by_class_name('button')
    button_login.click()


    elem_pas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'password-input')))
    elem_pas.send_keys(PASSWORD)

    button_pas = driver.find_element_by_class_name('second-button')
    button_pas.click()
    return



def scroll():
    hrf = 0
    at = 0
    links = set()

    while hrf != 'A':
        time.sleep(5)
        hrf = driver.find_elements_by_class_name('js-letter-list-item')
        for el in hrf:
            link = el.get_attribute('href')
            links.add(link)
        a = len(hrf) - 1

        hrf_new = hrf[a]
        hrf_new.send_keys(Keys.PAGE_DOWN)
        if at != hrf_new:
            at = hrf_new
        else:
            hrf = 'A'
            return links

def pars(r):

    for i in r:
        email = []
        date = []
        theme = []
        texts = []
        driver.get(i)
        time.sleep(5)
        letter = driver.find_element_by_xpath('//span[contains(@class, "letter-contact")]')
        mail = letter.get_attribute('title')
        email.append(mail)

        times = driver.find_element_by_xpath('//div[contains(@class, "letter__date")]')
        b = times.text
        date.append(b)

        th = driver.find_element_by_xpath('//h2[contains(@class, "thread__subject")]')
        c = th.text
        theme.append(c)

        text = driver.find_element_by_xpath('//div[contains(@class, "letter__body")]')
        d = ' '.join(list(map(clear_string, text.text)))
        texts.append(d)
        info = {
            'email': email,
            'date': date,
            'theme': theme,
            'texts': texts

            }
        mail_inbox.insert_one(info)
        print(info)
        time.sleep(5)


auth(url)
r = scroll()
pars(r)
driver.close()










