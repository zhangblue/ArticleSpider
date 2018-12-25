# -*-coding:utf-8-*-
__author__ = 'zhangdi'
import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


# 从后取数字
def get_num_to_last(message):
    ma = re.match(r".*\/(.*)?.htm$", message)
    if ma:
        num = ma.group(1)
    else:
        num = -1
    return num

if __name__ == "__main__":
    print(get_md5('http://jobbole.com'.encode("utf8")))
