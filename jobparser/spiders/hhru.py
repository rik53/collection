import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhRuSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post']

    def parse(self, response:HtmlResponse):# указываем, что respons является классом html response
        vacancies = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()#выбираем 1-ы элемент списка
        for link in vacancies:
            yield response.follow(link, callback=self.vacansy_parse) #- передаем результат в def vacansy_parse

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//h1/text()").extract_first()
        vacancy_salary_min = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        vacancy_salary_max = 0
        vacancy_link = response.url
        site = 'hh.ru'
        curency = None

        item = JobparserItem(name=vacancy_name, vacancy_salary_min=vacancy_salary_min,  vacancy_salary_max= vacancy_salary_max, link=vacancy_link, site=site, curency=curency)#отправляем результаты в item
        yield item
