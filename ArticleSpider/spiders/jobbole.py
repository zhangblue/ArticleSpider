# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

from ArticleSpider.items import JobBoleArticleItem


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
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):

        article_item = JobBoleArticleItem()

        print("----------url [%s] begin -------" % response.url)
        # 提取文章的具体字段，
        # 使用xpath进行解析
        # title_xpath = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]  # 获取标题
        # create_data_xpath = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip().replace("·", "").replace(" ", "")  # 获取文章创建时间
        # article_type_xpath = response.xpath('//*[@id="post-110287"]/div[2]/p/a[@rel="category tag"]/text()').extract()[0]  # 得到文章的类型
        #
        # praise_nums_xpath = response.xpath('//*[@id="110287votetotal"]/text()').extract()[0]  # 得到赞的数量
        #
        # fav_nums_xpath = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/span[2]/text()').extract()[0]  # 得到收藏的数量
        # match_re_xpath = re.match(r".*?(\d+).*", fav_nums_xpath)
        # if match_re_xpath:
        #     fav_nums_xpath = int(match_re_xpath.group(1))
        # else:
        #     fav_nums_xpath = 0
        #
        # comment_nums_xpath = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/a/span/text()').extract()[0]  # 得到评论的数量
        # match_re_xpath = re.match(r".*?(\d+).*", comment_nums_xpath)
        # if match_re_xpath:
        #     comment_nums_xpath = int(match_re_xpath.group(1))
        # else:
        #     comment_nums_xpath = 0
        #
        # content_xpath = response.xpath('//*[@id="post-110287"]/div[3]').extract()[0]  # 得到文章正文内容

        # 使用css选择器进行解析
        front_image_url = response.meta.get("front_image_url", "")  # 获取封面图
        print("front_image_url = %s" % front_image_url)
        title_css = response.css('div.entry-header h1::text').extract_first()  # 得到title
        print("title = %s" % title_css)
        create_data_css = response.css('p.entry-meta-hide-on-mobile::text').extract_first("").replace("·", "").strip()  # 得到创建时间
        print("create_data = %s" % create_data_css)
        tag_css = response.css("p.entry-meta-hide-on-mobile a[rel='category tag']::text").extract_first("")  # 得到文章类型
        print("article_type = %s" % tag_css)

        praise_nums_css = response.css('span.vote-post-up h10::text').extract_first("")  # 得到赞的数量
        print("praise_nums = %s" % praise_nums_css)

        fav_nums_css = response.css('span.bookmark-btn::text').extract_first("")  # 得到收藏数量
        match_re_css = re.match(r".*?(\d+).*", fav_nums_css)
        if match_re_css:
            fav_nums_css = int(match_re_css.group(1))
        else:
            fav_nums_css = 0

        print("fav_nums = %s" % fav_nums_css)

        comment_nums_css = response.css('a[href="#article-comment"] span::text').extract_first("")  # 得到评论的数量
        match_re_css = re.match(r".*?(\d+).*", comment_nums_css)
        if match_re_css:
            comment_nums_css = int(match_re_css.group(1))
        else:
            comment_nums_css = 0
        print("comment_nums = %s" % comment_nums_css)

        content_css = response.css("div.entry").extract_first("")  # 得到文章正文

        article_item["title"] = title_css

        article_item["create_data"] = scrapy.Field  # 文章创建时间
        url = scrapy.Field  # 文章url
        url_object_id = scrapy.Field  # 文章url的md5
        front_image_url = scrapy.Field  # 文章封面图地址
        front_image_path = scrapy.Field  # 文章封面图本地存放位置
        praise_nums = scrapy.Field  # 点赞数
        comment_nums = scrapy.Field  # 评论数
        fav_nums = scrapy.Field  # 收藏数
        tags = scrapy.Field  # 文章的标签
        content = scrapy.Field  # 文章的正文


        pass
