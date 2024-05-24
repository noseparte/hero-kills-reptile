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
    allowed_domains = ["yxs.qq.com"]
    start_urls = [
        'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1696/1700/m1622/201204/63819.shtml',
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial.pipelines.HeroPipeline': 100
        }
    }

    def parse(self, response):
        encoding = response.encoding
        # print("response encoding %s " % encoding)
        default_encoding = sys.getdefaultencoding()
        # print("default_encoding %s " % default_encoding)
        print("===============================================================================")
        print("===============================================================================")

        host = 'https://yxs.qq.com'

        body = response.body.decode(encoding)
        q = Selector(text=body)
        items = q.css(".cont-box .hero-list a::attr(href)").extract()
        for v in items:
            url = host + v
            yield Request(url, callback=self.parse_item)
        pass

    def parse_item(self, response):
        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        redis_db = settings.get('REDIS_DB')
        key = settings.get('REDIS_HERO_KEY')
        # 初始化redis
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        item = HeroItem()
        q = response.css
        # 武将属性区域
        image = q(".hero-intro #roll_img p img::attr(src)").extract_first()
        # self.log("image's type ======================== %s " % type(image))
        if image is None:
            image = ""
        roll_img = "http:" + image
        blood = len(q(".hero-intro .blood .grain").extract())
        Identity = q(".hero-intro .intro h4 .fl::text").extract_first()
        name = q(".hero-intro .intro h4 .fwb::text").extract_first()
        if name == '唐室砥柱':
            name = str(q(".hero-intro .intro h4::text").extract_first()).strip() + name
        # 技能介绍
        skills = []
        skill_list = q(".skill").extract()
        for skill_intro in skill_list:
            intro = Selector(text=skill_intro)
            skill_name = intro.css(".fwb::text").extract_first()
            if skill_name is None:
                skill_name = str(intro.css(".skill::text").extract_first()).split("[")[0]
                # self.logger.info("狄仁杰: skill_name %s " % skill_name)
            skill_type = intro.css(".ml10::text").extract_first()
            if skill_type is None:
                skill_type = "[" + str(intro.css(".skill::text").extract_first()).split("[")[1]
                # self.logger.info("狄仁杰: skill_type %s " % skill_type)
            skill_desc = intro.css("p::text").extract_first()
            skill = {
                "skill_name": skill_name,
                "skill_type": skill_type,
                "skill_desc": skill_desc
            }
            skills.append(skill)

        # 技能规则
        rules = q(".intro .c896 p::text").extract()
        # 人物生平
        biography = []
        biographyLst = q(".hero-intro .more-intro p::text").extract()
        for l in biographyLst:
            l = str(l).strip()
            if l != "":
                biography.append(l)

        item['roll_img'] = roll_img
        item['blood'] = blood
        item['Identity'] = Identity
        item['name'] = name
        item['skills'] = skills
        item['rules'] = rules
        item['biography'] = biography
        if blood < 3:
            self.logger.info("hero pipeline item ====================== %s " % item)
        else:
            result = str(item)
            r.sadd(key + name, result)
            yield item
