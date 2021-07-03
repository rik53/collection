"""1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
пользователя, сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев."""
import requests
import json
import os
from dotenv import load_dotenv
# pip install python-dotenv
load_dotenv()

TOKEN = os.environ.get("TOKEN", None)
URL = os.environ.get("URL", None)
token = TOKEN
url = URL

def auth(token, url):
    headers = {
        'Authorization': token
    }
    response = requests.get(url, headers=headers)
    r = response.json()
    return r
a = auth(token, url)

def ref(a):
    reference = []
    for i in a:
        reference.append(i['name'])
    return reference
print(ref(a))

def ref_dump(a):
    path = "repos.json"

    for j in a:
        with open(path, "a") as f:
            json.dump(j, f, indent=2)
    return j

auth(token, url)
ref(a)
ref_dump(a)

"""2. Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный 
момент для города, название которого получается через input. https://openweathermap.org/current"""
import requests
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("TOKEN_openweather", None)

def weather(q):
    params = {
    ('q', q),
    ('appid', token),
    }
    url = 'http://api.openweathermap.org/data/2.5/weather'

    response = requests.get(url, params=params)
    pprint(response.json()['main'])
q= input('Введите город: ')
weather(q)