from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from collection.leroyparser.spiders.leroy import LeroySpider
from collection.leroyparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    # input = ('')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroySpider, search='обои')

    process.start()