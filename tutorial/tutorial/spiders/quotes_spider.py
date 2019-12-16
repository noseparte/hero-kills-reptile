import json

import scrapy
from scrapy import Selector


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1696/1700/m1622/201204/63819.shtml'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'hero-kills-reptile-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
            # f.write(response.css(".content a::attr(href)").extract())
        self.log('Saved file %s' % filename)