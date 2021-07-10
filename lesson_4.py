import requests
from lxml.html import fromstring
from string import whitespace
from datetime import datetime
CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")
from pymongo import MongoClient
MONGO_HOST = "localhost"
MONG0_PORT = 27017
MONGO_DB = "news"
MONGO_COLLECTION_LENTA = "lenta"
MONGO_COLLECTION_YANDEX = "yandex"
MONGO_COLLECTION_MAIL = "mail"
with MongoClient(MONGO_HOST, MONG0_PORT) as client:
            db = client[MONGO_DB]
            lenta = db[MONGO_COLLECTION_LENTA]
            yandex = db[MONGO_COLLECTION_YANDEX]
            mail = db[MONGO_COLLECTION_MAIL]

params = {
    'tab': 'all',
}
headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

}
def clear_string(s, whitespaces=CUSTOM_WHITESPACE):
    for space in whitespaces:
        s = s.replace(space, " ")
    return s
url_lenta = 'https://lenta.ru/'
url = 'https://yandex.ru/news/'
url_mail = 'https://news.mail.ru/'

def lenta_news(url_lenta, headers):
    respons = requests.get(url_lenta, headers=headers)
    items_xpath = '//div[contains(@class,"js-main__content")]//div[contains(@class, "item") or contains(@class, "first-item")]//a[not(@class)]'

    dom = fromstring(respons.text)
    items = dom.xpath(items_xpath)

    for item in items:
        name = []
        news = []
        link = []
        date = []

        name.append('lenta.ru')
        news.append(list(map(clear_string, item.xpath('./text()'))))
        link.append(item.xpath('./@href'))
        date.append(item.xpath('./ time / @datetime'))

        filter_data = {
                'name': name,
                'news': news,
                'link': link,
                'date': date
            }
        update_data = {
                "$set":
                       {
                        'name': name,
                        'news': news,
                         'link': link,
                         'date': date
                        }}
        lenta.update_many(filter_data, update_data, upsert=True)


        return filter_data


def yandex_news(url):
    t = datetime.today().date()
    t.strftime("%Y-%m-%d")
    respons = requests.get(url)
    items_xpath = '//div[contains(@class, "news-top-flexible-stories")]//div[@class="mg-grid__col mg-grid__col_xs_8" or @class="mg-grid__col mg-grid__col_xs_4" ]'

    dom = fromstring(respons.text)

    items = dom.xpath(items_xpath)

    for item in items:
        name = []
        news = []
        link = []
        date = []

        name.append(item.xpath('.//a[@class="mg-card__source-link"]/text()'))
        news.append(list(map(clear_string, item.xpath('.//h2/text()'))))
        link.append(item.xpath('.//a[contains(@class, "mg-card__source-link")]/@href'))
        time = item.xpath('.//span[contains(@class, "mg-card-source__time")]/text()')
        date.append((f'{t.strftime("%Y-%m-%d")}{time}'))

        filter_data = {
            'name': name,
            'news': news,
            'link': link,
            'date': date
        }
        update_data = {
            "$set":
                {
                    'name': name,
                    'news': news,
                    'link': link,
                    'date': date
                }}
        yandex.update_many(filter_data, update_data, upsert=True)


    return filter_data

def mail_connect(url_mail, headers):
    respons = requests.get(url_mail, headers=headers)
    xpath = '//ul[contains(@class,   list_type_square )] /li/a'
    dom = fromstring(respons.text)
    items = dom.xpath(xpath)

    link = [f'{url_mail}{"/".join(str(item.xpath("./@href")).split("/")[3:5])}' for item in items]

    listr=[]
    for url_new in link:
        respons = requests.get(url_new, headers=headers)
        dom = fromstring(respons.text)
        listr.append(dom)
    return listr


def mail_news(listr):

    for item in listr:

        name = []
        news = []
        link = []
        date = []

        item_name = item.xpath('.//div[contains(@class, "breadcrumbs_article")]//span[contains(@class, "link__text")]/text()')
        if len(item_name) != 0:
            name.append(item_name)

        item_news = list(map(clear_string, item.xpath('//div[contains(@class, "hdr__wrapper")]//h1[contains(@class, "hdr__inner")]/text()')))
        if len(item_news) != 0:
            news.append(item_news)

        item_link = item.xpath('.//div[contains(@class, "breadcrumbs_article")]//a/@href')
        if len(item_link) != 0:
            link.append(item_link)

        item_date = item.xpath('//div[contains(@class, "breadcrumbs_article")]//span[contains(@class, "breadcrumbs__text ")]/@datetime')
        if len(item_date) != 0:
            date.append(item_date)

        filter_data = {
            'name': name,

            'news': news,
            'link': link,
            'date': date
        }
        update_data = {
            "$set":
                {
                    'name': name,

                    'news': news,
                    'link': link,
                    'date': date
                }}

        mail.update_many(filter_data, update_data, upsert=True)
    return filter_data




mc = mail_connect(url_mail, headers)
ln = lenta_news(url_lenta, headers)
yn = yandex_news(url)
print(ln)
print(yn)
print(mail_news(mc))





