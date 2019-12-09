import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1696/1700/m1622/201312/241458.shtml',
            'http://quotes.toscrape.com/page/2/http://quotes.toscrape.com/page/2/',
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1698/m1628/201203/56650.shtml?2',
            'https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1699/m1628/201203/56651.shtml?3',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)