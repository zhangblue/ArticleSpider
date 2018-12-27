# -*-coding:utf-8-*-
__author__ = 'zhangdi'
import requests
from fake_useragent import UserAgent
from scrapy.selector import Selector


def crawl_ips():
    # 爬取西刺的免费ip代理

    ua = UserAgent()

    headers = {
        "User-Agent": ua.chrome
    }
    re = requests.get('https://www.xicidaili.com/nn/', headers=headers)
    selector = Selector(text=re.text)

    all_trs = selector.css("#ip_list tr")

    for tr in all_trs:
        tr.css("")

print(crawl_ips())
