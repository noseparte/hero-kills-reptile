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


# 基本牌
class BasicItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 名称
    image = scrapy.Field()  # 头像
    use_time = scrapy.Field()  # 使用时机
    use_target = scrapy.Field()  # 使用目标
    use_effect = scrapy.Field()  # 使用效果
    more_info = scrapy.Field()  # 补充说明
    pass


# 锦囊牌
class SleeveItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 名称
    image = scrapy.Field()  # 头像
    sleeve_describe = scrapy.Field()  # 使用效果
    use_time = scrapy.Field()  # 使用时机
    use_target = scrapy.Field()  # 使用目标
    more_info = scrapy.Field()  # 补充说明
    pass


# 装备牌
class EquipItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 名称
    image = scrapy.Field()  # 头像
    attack_range = scrapy.Field()  # 攻击范围
    equip_skill = scrapy.Field()  # 武器技能
    more_info = scrapy.Field()  # 补充说明
    pass
