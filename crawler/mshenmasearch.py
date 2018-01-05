# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
import re


# http://m.sm.cn/s?q=%E9%85%B8%E5%A5%B6%E4%BB%80%E4%B9%88%E6%97%B6%E5%80%99%E5%96%9D%E6%AF%94%E8%BE%83%E5%A5%BD
class MShenmaSearch(MySearch):
    # 搜索排名
    page_index = 0

    # 档期解析页面
    cur_parse_page = 0

    # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = []

    website_start_url = 'http://m.sm.cn'

    domain_url = 'http://m.sm.cn/s?q='

    # 是否进行了相关搜索的解析
    relate_search_parseflag = False

    # 是否进行推荐搜索的解析
    recommend_search_parseflag = False

    def __init__(self, keyword, pagenum):
        self.keyword = keyword
        self.pagenum = pagenum

    def genrate_pageurl(self):
        super().genrate_pageurl()
        for page_index in range(1, self.pagenum + 1):
            self.cur_parse_page += 1
            # 移动端和pc端连接方式相同
            request_url = self.domain_url + self.keyword + "&page=" + str(page_index)
            print("正在爬取页面url:", request_url)
            page_resource = self.get_content_whitget(request_url, 'utf-8')
            beautiful_soup = BeautifulSoup(page_resource.text, 'lxml')
            parse_div = beautiful_soup.find("body")
            # 定位到相关搜索
            relate_search_div = parse_div.find("div", attrs={'class': 'ali_rel'})
            # 相关搜索的解析
            if self.relate_search_parseflag is False:
                if relate_search_div is not None:
                    self.parse_relate_search(relate_search_div)
                    self.relate_search_parseflag = True
            self.parse_result_page(parse_div)

    def parse_result_page(self, result):
        pass

    def parse_relate_search(self, relate_div):
        pass

    def parse_other_search(self, result):
        pass
