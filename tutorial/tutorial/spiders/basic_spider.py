import scrapy
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "basic"

    def start_requests(self):
        urls = [
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1697/m1628/201203/56649.shtml?1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        body = response.body
        q = Selector(text=body)
        items = q.css(".x_card_lst p img::attr(src)").extract()
        filename = 'hero-kills-basic.html'
        with open(filename, 'ws') as f:
            for item in items:
                # print(chardet.detect(item))
                name = item.encode('utf-8')
                self.log('result %s \n' % name)
                f.write('https' + name + '\n')
