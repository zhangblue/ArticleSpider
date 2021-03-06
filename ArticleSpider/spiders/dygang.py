# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ArticleSpider.items import DygangMovieMessageItem, DygangMovieDownloadAddressItem
from ArticleSpider.utils.common import get_num_to_last
import time
import os


class DygangSpider(scrapy.Spider):
    name = 'dygang'
    allowed_domains = ['www.dygang.net']
    start_urls = ['http://www.dygang.net/ys/']

    # project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__))),  # 设置目录为当前文件所在的目录的父目录
    # print("-----"+os.path.join(project_dir, "images"))

    # 对这个spider单独设置settings
    custom_settings = {
        "COOKIES_ENABLED": True,  # 关闭cookie
        "DOWNLOAD_DELAY": 2,  # 设置下载延迟
        # 设置图片下载参数
        "IMAGES_URLS_FIELD": "front_image_url",  # 设置自动下载图片时使用的url字段
        "IMAGES_STORE": os.path.join('/tmp', "images/dygang")  # 设置下载图片的本地目录
    }

    def parse(self, response):
        class_border1s = response.css(".border1")
        # 提取当前页所有电影
        for class_border1 in class_border1s:
            url = class_border1.css("a::attr(href)").extract_first("")
            detail_url = parse.urljoin(response.url, url)
            image = class_border1.css("img::attr(src)").extract_first("")
            title = class_border1.css("img::attr(alt)").extract_first("")
            yield Request(detail_url, meta={"image_url": image, "movie_title": title}, callback=self.parse_detail)  # 将结果重新放在待爬取请求中。

        # 得到下一页的url
        next_urls = response.css("td[align='middle'] a")
        for next_url in next_urls:
            text = next_url.css("::text").extract_first("")
            if text == "下一页":
                next_url_path = next_url.css("::attr(href)").extract_first("")
                url_next = parse.urljoin(response.url, next_url_path)
                yield Request(url=url_next, callback=self.parse)

    def parse_detail(self, response):
        # 对单个的电影内容进行爬取
        dygang_movie_message_item = DygangMovieMessageItem()
        movie_id = get_num_to_last(response.url)
        movie_message_item_loader = ItemLoader(item=DygangMovieMessageItem(), response=response)
        movie_message_item_loader.add_value("movie_id", int(movie_id))  # 电影id编号
        movie_message_item_loader.add_value('url', response.url)  # 电影url地址
        movie_message_item_loader.add_value("front_image_url", [response.meta.get("image_url")])  # 从response的meta字段中获取image url
        movie_message_item_loader.add_value('movie_title', response.meta.get("movie_title"))  # 从response的meta字段中获取电影名称
        dygang_movie_message_item = movie_message_item_loader.load_item()

        yield dygang_movie_message_item

        # download_selectors = response.css("td[bgcolor='#ffffbb']")
        # for download_selector in download_selectors:
        #     dygangMovieDownloadAddressItem = DygangMovieDownloadAddressItem()
        #     download_address_item_loader = ItemLoader(item=DygangMovieDownloadAddressItem(), selector=download_selector)
        #     download_address_item_loader.add_value("movie_id", movie_id)
        #     download_address_item_loader.add_css("download_message", "::text")
        #     download_address_item_loader.add_css("download_url", "a::attr(href)")
        #     dygangMovieDownloadAddressItem = download_address_item_loader.load_item()
        #     yield dygangMovieDownloadAddressItem
