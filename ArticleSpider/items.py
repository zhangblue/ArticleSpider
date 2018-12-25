# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
from ArticleSpider.utils.common import get_md5


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 将日期字符串转化为date类型
def date_convert(value):
    try:
        create_data = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_data = datetime.datetime.now().date()
    return create_data


# 清理date格式的数据
def date_convert_sort_out(value):
    content = value.replace("·", "").strip()
    return content


# 拿取数字
def get_nums(value):
    match_re_css = re.match(r".*?(\d+).*", value)
    if match_re_css:
        nums = int(match_re_css.group(1))
    else:
        nums = 0
    return nums


class ArticleItemLoader(ItemLoader):
    # 自定义item loader, 获取爬取的列表中的第一个值
    default_output_processor = TakeFirst()


def return_value(value):
    return value


# ---------------- jobbole ------------------------
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()  # 文章标题
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert_sort_out, date_convert),  # 调用多函数使用逗号分开
    )  # 文章创建时间
    url = scrapy.Field()  # 文章url
    url_object_id = scrapy.Field(
        input_processor=MapCompose(get_md5)
    )  # 文章url的md5
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
        # input_processor=MapCompose(return_value)
    )  # 文章封面图地址
    front_image_path = scrapy.Field(
        input_processor=MapCompose(return_value)
    )  # 文章封面图本地存放位置
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )  # 点赞数
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )  # 评论数
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )  # 收藏数
    tags = scrapy.Field(
        output_processor=Join(",")
    )  # 文章的标签
    content = scrapy.Field()  # 文章的正文

    def get_insert_sql(self):
        # 执行具体的插入逻辑
        insert_sql = """
            insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tags) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        params = (
            self["title"], self["create_date"], self["url"], self["url_object_id"], self["front_image_url"], self["front_image_path"], self["comment_nums"],
            self["fav_nums"],
            self["praise_nums"], self["tags"])
        return insert_sql, params


# ------------------ dygang --------------------
class DygangMovieMessageItem(scrapy.Item):
    # 电影港电影信息参数
    movie_id = scrapy.Field(
        output_processor=TakeFirst()
    )  # 电影id号
    url = scrapy.Field(
        output_processor=TakeFirst()
    )  # 爬取的url地址
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
        # output_processor=TakeFirst()
    )  # 电影海报url地址
    front_image_path = scrapy.Field(
        input_processor=MapCompose(return_value)
    )  # 电影海报本地下载目录
    movie_title = scrapy.Field(
        output_processor=TakeFirst()
    )  # 电影名称

    def get_insert_sql(self):
        # 执行具体的插入逻辑
        insert_sql = """
            insert into dygang_message(movie_id,movie_title,url,front_image_url,front_image_path) values (%s,%s,%s,%s,%s)
            """
        params = (self["movie_id"], self["movie_title"], self["url"], self["front_image_url"],self["front_image_path"])
        return insert_sql, params


class DygangMovieDownloadAddressItem(scrapy.Item):
    # 电影下载的url
    movie_id = scrapy.Field()  # 电影id号
    download_url = scrapy.Field()  # 下载地址
    download_message = scrapy.Field()  # 下载地址描述
