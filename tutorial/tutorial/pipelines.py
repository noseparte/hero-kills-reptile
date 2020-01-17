# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

# 卡牌类型
models = ("武将牌", "基本牌", "锦囊牌", "装备牌")


# class TutorialPipeline(object):
#     def process_item(self, item, spider):
#         client = pymongo.MongoClient(host="127.0.0.1", port=27017)
#         db = client['card']
#
#         return item


class CardPipeline(object):
    def process_item(self, item, spider):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['hero-kill']
        collection = db['hk_card']
        collection.insert_one(dict(item))
        client.close()
        return item


class HeroPipeline(object):

    def process_item(self, item, spider):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['hero-kill']
        collection = db['hk_hero_card']
        collection.insert_one(dict(item))
        client.close()
        return item


class BasicPipeline(object):

    def process_item(self, item, spider):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['hero-kill']
        collection = db['hk_basic_card']
        collection.insert_one(dict(item))
        client.close()
        return item


class SleevePipeline(object):

    def process_item(self, item, spider):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['hero-kill']
        collection = db['hk_sleeve_card']
        collection.insert_one(dict(item))
        client.close()
        return item
