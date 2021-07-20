from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings # Подключаем настройки
from jobparser.spiders.hhru import HhRuSpider # Импортируем класс нашего паука из HhRuSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)#устанавливаем наши настройки

    process = CrawlerProcess(settings=crawler_settings)#пустой процесс с настройками
    process.crawl(HhRuSpider)#процесс
    process.crawl(SjruSpider)
    process.start()


