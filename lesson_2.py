import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

params = {
        'tab': 'all',
    }
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

vac = '+'.join(input("Напишите интересующую вас вакансию: ").split(' '))
count = (int(input("Напишите колличество страниц для просмотра: ")))
vacansy = []
link = []
site = []
max_salary = []
min_salary = []
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

            a_f = item.find('a', attrs={'class': "bloko-link"})
            div_f = item.find('div', attrs={'class': "vacancy-serp-item__sidebar"})
            div_split = div_f.text.split()
            vacansy.append(a_f.text)
            link.append(a_f.attrs['href'])
            site.append('hh.ru')
            if len(div_split) == 0:
                max_salary.append(None)
                min_salary.append(None)

            for i in div_split:
                if div_split.count("до") > 0:
                     max_salary.append(' '.join(div_split[1:]))
                     min_salary.append(None)
                break
            for i in div_split:
                if div_split.count("от") > 0:
                     min_salary.append(' '.join(div_split[1:]))
                     max_salary.append(None)
                break
            for i in div_split:
                if '–' in div_split[1]:
                    el1 = ' '.join(div_split[:1])
                    el11 = div_split[-1]
                    min_salary.append(f'{el1} {el11}')
                    max_salary.append(' '.join(div_split[2:]))
                break
            for i in div_split:
                if '–' in div_split[2]:
                    el2 = ' '.join(div_split[:2])
                    el22 = div_split[-1]
                    min_salary.append(f'{el2} {el22}')
                    max_salary.append(' '.join(div_split[3:]))
                break
            info = {
                'vacansy': vacansy,
                'link': link,
                'max_salary': max_salary,
                'min_salary': min_salary,
                'site': site
            }
        df = pd.DataFrame(info)
        return df

    a= serch(r)

pprint(a)
a.to_csv('hh.scv', index=False)
