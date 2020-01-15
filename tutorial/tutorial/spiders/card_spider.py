# encoding:UTF-8
import scrapy
from scrapy.selector import Selector
import sys
import redis
from tutorial.items import CardItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class CardSpider(scrapy.Spider):
    name = "card"

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

        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        # 初始化redis
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        key = settings.get('REDIS_CARD_KEY')

        body = response.body.decode(encoding)
        q = Selector(text=body)

        item = CardItem()

        items = q.css(".cont-box ul li a span::text").extract()
        for v in items:
            r.sadd(key, v)
            item['type'] = v
            self.log('result %s \n' % item)
            yield item

