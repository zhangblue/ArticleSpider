# -*-coding:utf-8-*-
__author__ = 'zhangdi'

import re

url = "http://www.dygang.net/ys/20181115/41601.htm"

mat=re.match(r".*\/(.*)?.htm$", url)
if mat:
    print(mat.group(1))
else:
    print("no")
