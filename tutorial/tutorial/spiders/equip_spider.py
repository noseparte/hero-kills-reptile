import re

import redis
import scrapy
from scrapy.selector import Selector
from scrapy import Request
from scrapy.utils.project import get_project_settings

from tutorial.items import EquipItem

settings = get_project_settings()


# 装备牌
class EquipSpider(scrapy.Spider):
    name = "equip"

    allowed_domains = ["yxs.qq.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial.pipelines.EquipPipeline': 50
        }
    }
    start_urls = [
        'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1699/m1628/201203/56651.shtml?3'
    ]

    def parse(self, response):
        encoding = response.encoding
        # html = response.content.decode(encoding, "ignore")
        # host = 'https://yxs.qq.com'
        body = response.body.decode(encoding)
        q = Selector(text=body)
        # items = q.css(".x_card_lst p.cl.mb15.fl.mt25")

        # 选择所有的 p 元素
        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        redis_db = settings.get('REDIS_DB')
        key = settings.get('REDIS_EQUIP_KEY')
        # 初始化redis
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        r = redis.Redis(connection_pool=pool)

        p_elements = q.css(".x_card_lst p.cl.mb15.fl.mt25")
        for p in p_elements:
            item = EquipItem()
            name = ""
            # 武将属性区域
            image = p.css('img::attr(src)').extract_first()
            # self.log("image's type ======================== %s " % type(image))
            if image is None:
                image = ""
            roll_img = "http:" + image

            table = p.css('p + table')
            props = table.css('tbody tr')
            # use_time = props[0].css('th::text').extract_first()
            if len(props) >= 3:
                item['image'] = roll_img
                item['attack_range'] = props[0].css('td p::text').extract()
                item['equip_skill'] = props[1].css('td p::text').extract()
                more_info = props[2].css('td p::text').extract()
                item['more_info'] = more_info
                # pattern = r'【(.*?)】'
                print("more_info--------------", more_info)
                # match = re.search(pattern, more_info)
                # if match:
                #     name = match.group(1)
                item['name'] = name
                result = str(item)
                r.sadd(key + name, result)
                yield item
