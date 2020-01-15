# encoding:UTF-8
import sys

import redis
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings

from tutorial.items import HeroItem

settings = get_project_settings()


class HeroSpider(scrapy.Spider):
    name = "hero"

    def start_requests(self):
        urls = [
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1696/1700/m1622/201204/63819.shtml'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        encoding = response.encoding
        print("response encoding %s " % encoding)
        default_encoding = sys.getdefaultencoding()
        print("default_encoding %s " % default_encoding)
        print("===============================================================================")
        print("===============================================================================")

        host = 'https://yxs.qq.com'

        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        # 初始化redis
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        key = settings.get('REDIS_HERO_KEY')

        body = response.body.decode(encoding)
        q = Selector(text=body)

        item = HeroItem()

        items = q.css(".cont-box a::attr(href)").extract()
        for v in items:
            url = host + v
            # 武将属性区域
            roll_img = "http:" + q.css(".hero-intro #roll_img p img::attr(src)").extract_first()
            blood = len(q.css(".hero-intro .blood .grain").extract())
            Identity = q.css(".hero-intro .intro h4 .don::text").get()
            name = q.css(".hero-intro .intro h4 .fwb::text").extract_first()
            # 技能介绍
            skills = []
            skill_list = q.css(".skill").extract()
            for skill_intro in skill_list:
                intro = Selector(text=skill_intro)
                skill_name = intro.css(".fwb::text").extract_first()
                skill_type = intro.css(".ml10::text").extract_first()
                skill_desc = intro.css("p::text").extract_first()
                skill = {
                    "skill_name": skill_name,
                    "skill_type": skill_type,
                    "skill_desc": skill_desc
                }
                skills.append(skill)

            # 技能规则
            rules = q.css(".intro .c896 p::text").extract()
            # 人物生平
            biography = []
            biographyLst = q.css(".hero-intro .more-intro p::text").extract()
            for l in biographyLst:
                print("l==============================" + l)
                l = str(l).strip()
                biography.append(l)
            item['roll_img'] = roll_img
            item['blood'] = blood
            item['Identity'] = Identity
            item['name'] = name
            item['skills'] = skills
            item['rules'] = rules
            item['biography'] = biography
            # meta = {
            #     'roll_img': roll_img,
            #     'blood': blood,
            #     'Identity': Identity,
            #     'name': name,
            #     'skills': skills,
            #     'rules': rules,
            #     'biography': biography
            # }
            result = str(item)
            r.sadd(key + name, result)
            yield item
            yield Request(url, callback=self.parse)
            # pass

    # def parse_item(self, response):
    #     item = HeroItem()
    #     self.log("item前 ================================ %s " % item)
    #     item = dict(item, **response.meta)
    #     self.log("item后 ================================ %s " % item)
    #     yield item
