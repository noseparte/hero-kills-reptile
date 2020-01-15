# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

# 卡牌类型
models = ("武将牌", "基本牌", "锦囊牌", "装备牌")


class TutorialPipeline(object):
    def process_item(self, item, spider):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['card']

        return item


class CardPipeline(object):
    collection_name = 'card'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class HeroPipeline(object):

    def process_item(self, item, spider):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['hero-kill']
        collection = db['hero']
        collection.insert_one(dict(item))
        client.close()
        return item
