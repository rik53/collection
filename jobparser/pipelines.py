# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from itemadapter import ItemAdapter
from pymongo import MongoClient



class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies090721

    def process_item(self, item, spider):

        if spider.name == 'hhru':
            item = self.process_hh(item)
        else:
            item = self.process_sj(item)
        collection = self.mongobase[spider.name]
        collection.insert_one(item)



        return item

    def process_hh(self, item ):

        salary = ' '.join(item['vacancy_salary_min']).split(' ')
        if salary[0] == 'от' and salary[2] == 'до':

            item['vacancy_salary_min'] = salary[1].replace("\xa0", ' ')
            item['vacancy_salary_max'] = salary[3].replace("\xa0", ' ')
            item['curency'] = salary[4]
        elif salary[0] == 'до':
            item['vacancy_salary_min'] = None
            item['vacancy_salary_max'] = salary[3].replace("\xa0", ' ')
            item['curency'] = salary[2]


        elif salary[0] == 'от':
            item['vacancy_salary_min'] = salary[1].replace("\xa0", ' ')
            item['vacancy_salary_max'] = None
            item['curency'] = salary[2]
        else:
            item['vacancy_salary_min'] = 'з/п не указана'
            item['vacancy_salary_max'] = 'з/п не указана'
            item['curency'] = None

        return item

    def process_sj(self, item):


        if item['vacancy_salary_min'][0] == 'от':
            item['vacancy_salary_min'] = item['vacancy_salary_min'][2].replace("\xa0", ' ')
            item['vacancy_salary_max'] = None
            item['curency'] = "".join((' '.join(item['vacancy_salary_min'])).split(' ')[-4:])
        elif item['vacancy_salary_min'][0] == 'до':
            item['vacancy_salary_max'] = item['vacancy_salary_min'][2].replace("\xa0", ' ')
            item['curency'] = ((item['vacancy_salary_min'][2]).split())[2]
            item['vacancy_salary_min'] =None


        elif item['vacancy_salary_min'][0] == 'По договорённости':
            item['vacancy_salary_min'] = 'По договорённости'
            item['vacancy_salary_max'] = 'По договорённости'
            item['curency'] = None

        else:
            item['vacancy_salary_max'] = item['vacancy_salary_min'][4].replace("\xa0", ' ')
            item['curency'] = item['vacancy_salary_min'][6]
            item['vacancy_salary_min'] = item['vacancy_salary_min'][0].replace("\xa0", ' ')


        return item