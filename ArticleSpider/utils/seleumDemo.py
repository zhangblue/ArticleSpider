#-*-coding:utf-8-*- 
__author__ = 'zhangdi'

from urllib import parse
from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path="/Users/zhangdi/work/workspace/PycharmProjects/ArticleSpider/drivers/chromedriver")
browser.get("http://jandan.net/ooxx")

t_selector = Selector(text=browser.page_source)
image_urls = t_selector.css("img::attr(src)").extract()
next_page_tmp = t_selector.css(".previous-comment-page::attr(href)").extract()[0]

#next_page = parse.urljoin(browser.current_url,next_page_tmp)



print("cccc")




