# -*-coding:utf-8-*-
__author__ = 'zhangdi'

from scrapy.cmdline import execute

import sys
import os

# os.path.abspath(__file__) 得到当前文件的所在目录
# os.path.dirname() 获得文件的父目录
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 设置工程主目录
execute(["scrapy", "crawl", "jobbole"])  # 运行系统命令 scrapy crawl jobbole
