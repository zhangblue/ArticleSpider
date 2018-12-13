# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field  # 文章标题
    create_data = scrapy.Field  # 文章创建时间
    url = scrapy.Field  # 文章url
    url_object_id = scrapy.Field  # 文章url的md5
    front_image_url = scrapy.Field  # 文章封面图地址
    front_image_path = scrapy.Field  # 文章封面图本地存放位置
    praise_nums = scrapy.Field  # 点赞数
    comment_nums = scrapy.Field  # 评论数
    fav_nums = scrapy.Field  # 收藏数
    tags = scrapy.Field  # 文章的标签
    content = scrapy.Field  # 文章的正文
