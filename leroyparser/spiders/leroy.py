import scrapy
from scrapy.http import HtmlResponse
from collection.leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroySpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//a[contains(@class,'iypgduq_plp')]")
        next_page = response.xpath("//a[contains(@data-qa-pagination-item,'right')]/@href").extract_first()

        for link in ads_links:
            yield response.follow(link, callback=self.parse_good)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_good(self, response: HtmlResponse):

        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photos', '//img[@slot="thumbs"]/@src')
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('list__term', "//dt/text()")
        loader.add_xpath('list__definition', "//dd/text()")
        yield loader.load_item()

