import scrapy
from scrapy.selector import Selector

from tutorial.items import BasicItem


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
        host = 'https://yxs.qq.com'
        body = response.body.decode(encoding)
        q = Selector(text=body)

        item = BasicItem()

        items = q.css(".x_card_lst").extract()
        for v in items:
            item['image'] = host + q.css('p img::attr(src)')
