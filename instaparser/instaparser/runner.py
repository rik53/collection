from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from instaparser.spiders.followers_insta import FollowersInstaSpider
from instaparser.spiders.subscriptions_insta import SubscriptionsInstaSpider
from instaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SubscriptionsInstaSpider)
    process.crawl(FollowersInstaSpider)

    process.start()