# author : YangWan
# -*- coding: utf-8 -*-

class CrawlerItem(object):

    other_search = {}

    def __init__(self, search=None, keyword=None, page=None, index=None, title=None, content=None, page_url=None,
                 domain=None, relate_search=None):
        self.search = search
        self.keyword = keyword
        self.page = page
        self.index = index
        self.title = title
        self.content = content
        self.page_url = page_url
        self.domain = domain
        self.relate_search = relate_search

    def __str__(self):
       object_dec = ("搜索引擎: %s || 关键字: %s || 页码: %s || 搜索排名: %s || 标题: %s || 内容简介: %s || "
                     "链接地址: %s || 网站域名: %s || 推荐搜索: %s || 其他搜索: %s") \
                    % (self.search, self.keyword, self.page, self.index, self.title, self.content, self.page_url,
                       self.domain, self.relate_search, self.other_search)
       return object_dec



    # item = CrawlerItem("百度", "全民彩票", "4", "3", "我爱全名彩票", "我是内容", "页面链接", "网站域名", "推荐搜索", "相关搜索")
# print(item.__str__())