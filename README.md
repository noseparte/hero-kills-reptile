# hero-kills-reptile(英雄杀-爬虫)

## 简介

本人是一名**英雄杀**迷，一切都是兴趣使然，绝不会用作商业用途。做这个项目的初衷：
1. 想通过这个项目熟悉一下scrapy框架的使用。
2. 为英雄杀项目提供素材资源

## 爬虫内容
- **牌型：** 武将牌、基本牌、锦囊牌、装备牌
- **武将牌：** 阵营、头像、人物生平、主动被动技能、血量
- **基本牌：** 图标、使用目标、使用效果、补充说明
- **锦囊牌：** 图标、锦囊描述、使用时机、使用目标、补充说明
- **装备牌：** 图标、攻击范围、武器技能、补充说明

[英雄杀素材地址](https://yxs.qq.com/webplat/info/news_version3/416/1620/1695/1696/1700/m1622/201312/241458.shtml)
## 爬取流程

```
hero-kills-reptile
└─tutorial
    ├─spiders
    │  
    |- quotes_spider.py 全部
    |- card_spider.py 卡牌类型
    |- hero_spider.py 武将牌
    |- basic_spider.py 基本牌
    |- sleeve_spider.py 锦囊牌
    |- equip_spider.py 装备牌
    └─
```

## 项目部署

## 总结

```markdown
# 乱码问题 setting.py添加 但是没有生效
FEED_EXPORT_ENCODING = 'utf-8'

# pipelines.py对爬取结果进行解析，解耦
# xpath、css俩种方式对response进行解析需要深入学习用法

```

