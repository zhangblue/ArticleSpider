# Scrapy 爬虫

## 创建Scrapy框架工程

1. 使用命令行，在虚拟化环境中手动创建名为`ArticleSpider`的`Scrapy`框架工程

    ```sybase
     scrapy startproject ArticleSpider
    ```
2. 在工程目录下，使用默认的scrapy模版，创建对`http://blog.jobbole.com`网站爬取模版
    ```sybase
     scrapy genspider jobbole http://blog.jobbole.com
    ```
3. 启动scrapy
    ```sybase
     scrapy crawl jobbole
    ```
4. scrapy 调试器，方便进行调试性验证
    ```sybase
     scrapy shell http://blog.jobbole.com/110287/
  
    # 直接打开了一个scrapy shell窗口。并且response对象已经自动创建好了
    ```
    
# xpath简介

1. xpath使用路径表达式在xml和html中进行导航
2. xpath包含标准函数库
3. xpath是一个w3c的标准


## xpath语法

- `article` 选取所有article元素的所有子节点|
- `/article` 选取跟元素article
- `article/a` 选取所有属于article的子元素为a的元素
- `//div` 选取所有div子元素(无论出现在文档任何地方)
- `article//div` 选取所有属于article元素的后代的div元素，不管他出现在article之下的任何位置
- `//@class` 选取所有名为class的属性

## xpath语法-谓语

- `/article/div[1]` 选取属于article子元素的第一个div元素
- `/article/div[last()]` 选取属于article子元素的随后一个div元素
- `/article/div[last()-1]` 选取属于article子元素的倒数第二个div元素
- `//div[@lang]` 选取所有拥有lang属性的div元素
- `//div[@lang='eng']` 选取所有lang属性为eng的div元素


- `/div/*` 选取属于div元素的所有子节点
- `//*` 选取所有元素
- `//div[@*]` 选取所有带属性的title元素
- `/div/a|//div/p` 选取所有div元素的a和p元素
- `//span|//ul` 选取文档中的span和ul元素
- `article/div/p|//span` 选取所有属于article元素的div元素的p元素，以及文档中所有的span元素
 


# 正则表达式