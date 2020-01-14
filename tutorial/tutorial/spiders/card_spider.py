# encoding:UTF-8
from bs4 import BeautifulSoup
import scrapy
from scrapy.selector import Selector
import sys


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

        # soup = BeautifulSoup(response.body, fromEncoding=default_encoding)
        # print("soup %s " % soup)
        # html = response.content.decode(encoding, "ignore")
        body = response.body.decode(encoding)
        q = Selector(text=body)

        # 武将属性区域
        roll_img = q.css(".hero-intro #roll_img p img::attr(src)").extract_first()
        print("武将牌的头像图片地址为： " + "http:" + roll_img)
        blood = len(q.css(".hero-intro .blood .grain").extract())
        print("武将牌的初始血量为：%s " % blood)
        Identity = q.css(".hero-intro .intro h4 .don::text").get()
        print("武将牌的身份为：%s " % Identity)
        name = q.css(".hero-intro .intro h4 .fwb::text").extract_first()
        print("武将牌的名称为：%s " % name)
        skill = q.css(".hero-intro .intro .cb::text").extract_first()
        print("武将牌的技能说明：%s " % skill)

        # 技能介绍
        skills = q.css(".skill").extract()
        for skill_intro in skills:
            intro = Selector(text=skill_intro)
            skill_name = intro.css(".fwb::text").extract_first()
            skill_type = intro.css(".ml10::text").extract_first()
            skill_desc = intro.css("p::text").extract_first()
            self.log('skill_name %s \n ' % skill_name)
            self.log('skill_type %s \n ' % skill_type)
            self.log('skill_desc %s \n ' % skill_desc)

        # 技能规则
        rules = q.css(".intro .c896 p::text").extract()
        for rule in rules:
            self.log('rule %s \n ' % rule)

        # 人物生平
        biography = q.css(".hero-intro .more-intro h5::text").extract_first()
        self.log('biography %s \n ' % biography)
        biography_intros = q.css(".hero-intro .more-intro p::text").extract()
        for biography_intro in biography_intros:
            self.log('biography_intro %s \n ' % biography_intro)

        items = q.css(".cont-box ul li a span::text").extract()
        filename = 'hero-kills-card.html'
        with open(filename, 'w') as f:
            for item in items:
                # print(chardet.detect(item))
                name = item.encode('utf-8')
                self.log('result %s \n' % name)
                f.write(name + '\n')
