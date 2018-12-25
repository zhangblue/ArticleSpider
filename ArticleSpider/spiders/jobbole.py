# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse


from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']  # 待爬取的url地址

    def parse(self, response):
        """
         1. 获取下一页的url并交给scrapy下载后并进行解析
         2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """

        # 获取下一页的url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive div.floated-thumb div.post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")  # 取图片
            post_url = post_node.css("::attr(href)").extract_first("")  # 取连接
            url = parse.urljoin(response.url, post_url)
            yield Request(url, callback=self.parse_detail, meta={"front_image_url": image_url})  # 将结果重新放在待派去请求中。

        # 提取下一页并交给scrapy进行下载
        # next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        # 通过item_loader加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", 'div.entry-header h1::text')
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", response.url)
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", 'span.vote-post-up h10::text')
        item_loader.add_css("comment_nums", 'a[href="#article-comment"] span::text')
        item_loader.add_css('fav_nums', 'span.bookmark-btn::text')
        item_loader.add_css('tags', "p.entry-meta-hide-on-mobile a[rel='category tag']::text")
        item_loader.add_value("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item
