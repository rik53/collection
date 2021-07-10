"""3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта."""
import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
MONGO_HOST = "localhost"
MONG0_PORT = 27017
MONGO_DB = "hh"
MONGO_COLLECTION = "vacancy"
with MongoClient(MONGO_HOST, MONG0_PORT) as client:
    db = client[MONGO_DB]
    vacancy = db[MONGO_COLLECTION]

params = {
    'tab': 'all',
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

vac = '+'.join(input("Напишите интересующую вас вакансию: ").split(' '))
count = (int(input("Напишите колличество страниц для просмотра: ")))

for i in range(count):
    url = f"https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text={vac}&page={count}"


    def get(url, headers, params):
        r = requests.get(
            url,
            headers=headers,
            params=params,
        )
        return r


    r = get(url, headers, params)


    def serch(r):
        soup = bs(r.text, 'html.parser')
        vacancy_items = soup.find_all('div', attrs={"class": "vacancy-serp-item"})

        for item in vacancy_items:
            vacansy = []
            link = []
            site = []
            max_salary = []
            min_salary = []

            a_f = item.find('a', attrs={'class': "bloko-link"})
            div_f = item.find('div', attrs={'class': "vacancy-serp-item__sidebar"})
            div_split = div_f.text.split()
            vacansy.append(a_f.text)
            link.append(a_f.attrs['href'])
            site.append('hh.ru')
            if len(div_split) == 0:
                max_salary.append(None)
                min_salary.append(None)


            elif div_split.count("до") > 0:
                del div_split[-1]
                max_salary.append(int(''.join(div_split[1:])))
                min_salary.append(None)


            elif div_split.count("от") > 0:
                del div_split[-1]
                min_salary.append(int(''.join(div_split[1:])))
                max_salary.append(None)


            elif '–' in div_split[1]:
                del div_split[-1]
                el1 = int(' '.join(div_split[:1]))
                min_salary.append(f'{el1}')
                max_salary.append(int(''.join(div_split[2:])))


            elif '–' in div_split[2]:
                del div_split[-1]
                el2 = int(''.join(div_split[:2]))
                min_salary.append(f'{el2}')
                max_salary.append(int(''.join(div_split[3:])))

            filter_data = {
            'vacansy': vacansy,
            'link': link,
            'max_salary': max_salary,
            'min_salary': min_salary,
            'site': site
            }

            update_data = {
                "$set":
                {
            'vacansy': vacansy,
            'link': link,
            'max_salary': max_salary,
            'min_salary': min_salary,
            'site': site
            }}
            vacancy.update_many(filter_data, update_data, upsert=True)

        return
    serch(r)
