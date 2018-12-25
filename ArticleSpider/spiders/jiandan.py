# -*- coding: utf-8 -*-
import scrapy


class JiandanSpider(scrapy.Spider):
    name = 'jiandan'
    allowed_domains = ['jandan.net/ooxx']
    start_urls = ['http://jandan.net/ooxx/']

    def parse(self, response):
        #image_urls = response.css("img::attr(src)").extract()

        response.text

        pass
