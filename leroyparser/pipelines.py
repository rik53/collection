# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.goods

    def process_item(self, item, spider):
        item = self.process_feature(item)
        collection = self.mongobase['leroy']
        collection.insert_one(item)
        return item

    def process_feature(self, item):
        feature_list = []
        for i in range(len(item['list__term']) - 1):
            feature_list.append([item['list__term'][i], item['list__definition'][i]])
        item['feature'] = dict(feature_list)
        del item['list__term']
        del item['list__definition']
        return item


class LeroyparserPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'full/{item["name"]}/{item["name"]}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
