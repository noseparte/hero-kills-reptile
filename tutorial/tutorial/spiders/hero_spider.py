import scrapy
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "hero"

    def start_requests(self):
        urls = [
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1696/1700/m1622/201204/63819.shtml'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        body = response.body
        q = Selector(text=body)
        items = q.css(".cont-box a::attr(href)").extract()
        filename = 'hero-kills-hero.html'
        with open(filename, 'w') as f:
            for item in items:
                self.log('results %s \n' % item)
                f.write('https://yxs.qq.com' + item + '\n')
