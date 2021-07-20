import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):  # указываем, что respons является классом html response
        vacancies = response.xpath("//div[contains(@class, '_1h3Zg _2rfUm _2hCDz _21a7u')]//a/@href").extract()
        next_page = response.xpath("//div[contains(@class, '_3zucV L1p51 _1Fty7 _2tD21 _3SGgo')]//a[contains(@class, 'f-test-link-Dalshe')]/@href").extract_first()

        for link in vacancies:
            yield response.follow(link, callback=self.vacansy_parse) #- передаем результат в def vacansy_parse

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//div[contains(@class, '_3MVeX')]//h1/text()").extract()
        vacancy_salary_min = response.xpath("//span[contains(@class, 'ZON4b')]//text()").extract()
        vacancy_salary_max = 0
        vacancy_link = response.url
        site = 'superjob.ru'
        curency = None

        item = JobparserItem(name=vacancy_name, vacancy_salary_min=vacancy_salary_min,
                                     vacancy_salary_max=vacancy_salary_max, link=vacancy_link, site=site,
                                     curency=curency)  # отправляем результаты в item
        yield item
