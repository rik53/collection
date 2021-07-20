# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import strip_html5_whitespace


def change_photo_link(value):
    value = value.replace(',w_82,h_82,c_pad,b_white,d_photoiscoming.png', '')
    return value


class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_photo_link))
    link = scrapy.Field()
    list__term = scrapy.Field()
    list__definition = scrapy.Field(input_processor=MapCompose(strip_html5_whitespace))
    feature = scrapy.Field()
    _id = scrapy.Field()
