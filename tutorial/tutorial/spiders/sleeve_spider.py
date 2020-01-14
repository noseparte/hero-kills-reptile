import scrapy
from scrapy.selector import Selector


class CardSpider(scrapy.Spider):

    def start_requests(self):
        urls = [
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1696/1700/m1622/201204/63819.shtml'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

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
