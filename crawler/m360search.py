# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
import re


class M360Search(MySearch):
    website_start_url = 'https://m.baidu.com'

    domain_url = 'https://m.baidu.com/s?word='

    def parse_other_search(self, result):
        super().parse_other_search(result)

    def parse_relate_search(self, relate_div):
        super().parse_relate_search(relate_div)

    def parse_result_page(self, result):
        super().parse_result_page(result)

    def genrate_pageurl(self):
        super().genrate_pageurl()
