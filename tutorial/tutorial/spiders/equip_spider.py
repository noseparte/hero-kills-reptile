import scrapy
from scrapy.selector import Selector


# 装备牌
class EquipSpider(scrapy.Spider):
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
        body = response.body
        q = Selector(text=body)
        items = q.css(".cont-box ul li a span::text").extract()
        filename = 'hero-kills-sleeve.html'
        with open(filename, 'ws') as f:
            for item in items:
                # print(chardet.detect(item))
                name = item.encode('utf-8')
                self.log('result %s \n' % name)
                f.write(name + '\n')
