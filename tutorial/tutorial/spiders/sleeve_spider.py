import scrapy
import redis
from scrapy.selector import Selector

from scrapy.utils.project import get_project_settings

from tutorial.items import SleeveItem

settings = get_project_settings()


# 锦囊牌
class SleeveSpider(scrapy.Spider):
    name = "sleeve"
    allowed_domains = ["yxs.qq.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial.pipelines.SleevePipeline': 50
        }
    }
    start_urls = [
        'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1698/m1628/201203/56650.shtml?2'
    ]

    def parse(self, response):
        encoding = response.encoding
        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        key = settings.get('REDIS_SLEEVE_KEY')
        # 初始化redis
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        r = redis.Redis(connection_pool=pool)

        host = 'http:'
        body = response.body.decode(encoding)
        q = Selector(text=body)

        # 锦囊牌介绍
        card = q.css(".x_card_lst .x_card_tit strong::text").extract_first()
        content = q.css(".x_card_lst .x_card_txt p::text").extract()
        smalls = []
        images = q.css(".x_card_lst .x_card_txt p img::attr(src)").extract()
        for image in images:
            smalls.append(host + image)
        meta = {
            "card": card,
            "content": content,
            "images": smalls
        }
        result = str(meta)
        r.sadd(card, result)

        # 锦囊牌列表
        item = SleeveItem()

        items = q.css(".x_card_lst p")

        for v in items:
            img = v.css('img::attr(src)').extract_first()
            if img is None:
                img = ""
                name = ""
            else:
                name = img.split("/")[-1].split('.')[0]
                item['name'] = name
            item['image'] = host + img
            table = v.css('p + table')
            props = table.css('tbody tr')
            # use_time = props[0].css('th::text').extract_first()
            if len(props) >= 4:
                item['sleeve_describe'] = props[0].css('td p::text').extract()
                item['use_time'] = props[1].css('td p::text').extract()
                item['use_target'] = props[2].css('td p::text').extract()
                item['more_info'] = props[3].css('td p::text').extract()
                result = str(item)
                r.sadd(key + name, result)
                yield item
