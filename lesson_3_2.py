"""2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
больше введённой суммы."""
from pprint import pprint
from pymongo import MongoClient
MONGO_HOST = "localhost"
MONG0_PORT = 27017
MONGO_DB = "hh"
MONGO_COLLECTION = "vacancy"
a = int(input("Введите зарплату: "))

def salary(a):
    with MongoClient(MONGO_HOST, MONG0_PORT) as client:
        db = client[MONGO_DB]
        users = db[MONGO_COLLECTION]
        cursor = users.find({"min_salary": {"$gt": a}})

        return cursor
c = salary(a)

def print_salary(c):
    for doc in c:
        pprint(doc)
print_salary(c)