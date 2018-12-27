# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline  # scrapy中对与图片的下载类
from scrapy.exporters import JsonItemExporter  # scrapy封装的写json文件模块

from twisted.enterprise import adbapi  # 异步数据库交互模块

import MySQLdb
import psycopg2  # 对postgres数据库的连接

import codecs
import json


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 采用同步机制写入数据库
class PostgresPipeline(object):
    # 初始化postgres连接
    def __init__(self):
        self.conn = psycopg2.connect(host='172.16.12.49', user='all-server', dbname='scrapy-db', port='5432')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title,url,url_object_id,create_date,fav_nums) values (%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['url_object_id'], item['create_data'], item['fav_nums']))
        self.conn.commit()


# 使用异步方式写入数据库
class PostgresTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['POSTGRES_HOST'],
            dbname=settings['POSTGRES_DBNAME'],
            user=settings['POSTGRES_USER'],
        )
        dbpool = adbapi.ConnectionPool('psycopg2', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将数据库插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 异常处理回调函数

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入逻辑
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonExporterPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open("articleexport.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


"""
    自定义自己的图片处理pipeline。
    1. 首选需要继承scrapy.pipelines.images.ImagesPipeline.
    2. 其次要重写ImagesPipeline中的函数。
        2.1 重写item_completed函数。设置文件下载后的本地路径
"""


class ArticleImagePipeline(ImagesPipeline):
    # 自定义图片处理pipeline
    def item_completed(self, results, item, info):
        if "front_image_url" in item:  # 只有包含front_image_url字段才会做以下内容
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item
