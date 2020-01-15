# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    image = scrapy.Field()
    use_time = scrapy.Field()
    pass


class CardItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    pass


class HeroItem(scrapy.Item):
    # define the fields for your item here like:
    roll_img = scrapy.Field()  # 头像
    blood = scrapy.Field()  # 血量
    Identity = scrapy.Field()  # 阵营
    name = scrapy.Field()  # 名称
    skills = scrapy.Field()  # 技能
    rules = scrapy.Field()  # 规则
    biography = scrapy.Field()  # 人物生平
    pass
