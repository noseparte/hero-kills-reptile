# encoding:UTF-8
import redis
import scrapy
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings

from tutorial.items import BasicItem

settings = get_project_settings()


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["yxs.qq.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial.pipelines.BasicPipeline': 10
        }
    }
    start_urls = [
        'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1697/m1628/201203/56649.shtml?1'
    ]

    def parse(self, response):
        encoding = response.encoding
        host = 'http:'
        body = response.body.decode(encoding)
        q = Selector(text=body)

        item = BasicItem()

        items = q.css(".x_card_lst p")
        for v in items:
            redis_host = settings.get('REDIS_HOST')
            redis_port = settings.get('REDIS_PORT')
            key = settings.get('REDIS_BASIC_KEY')
            # 初始化redis
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
            r = redis.Redis(connection_pool=pool)
            # self.logger.info("v ===========   %s" % v)
            # self.logger.info("v's type ===========   %s" % type(v))
            img = v.css('img::attr(src)').extract_first()
            if img is None:
                img = ""
            item['image'] = host + img
            # self.logger.info("item ===========   %s" % item)
            table = v.css('p + table')
            # self.logger.info("table ===========   %s" % table)
            props = table.css('tbody tr')
            # self.logger.info("props ===========   %s" % props)
            # use_time = props[0].css('th::text').extract_first()
            if len(props) >= 4:
                item['use_time'] = props[0].css('td p::text').extract()
                item['use_target'] = props[1].css('td p::text').extract()
                item['use_effect'] = props[2].css('td p::text').extract()
                item['more_info'] = props[3].css('td p::text').extract()
                result = str(item)
                r.sadd(key, result)
                yield item
