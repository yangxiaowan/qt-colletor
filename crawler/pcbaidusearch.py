# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch

class PcBaiduSearch(MySearch):

    domain_url = 'https://www.baidu.com/s?wd='

    def __init__(self, keyword, pagenum):
        self.keyword = keyword
        self.pagenum = pagenum

    def genrate_pageurl(self):
        super().genrate_pageurl()
        for page_index in range(1, self.pagenum + 1):
            request_url = self.domain_url + self.keyword + "&pn=" + str(page_index)
            print("正在爬取页面url:", request_url)
            page_resource = self.get_content_whitget(request_url, 'utf-8')
            beautiful_soup = BeautifulSoup(page_resource.text, 'lxml')
            parse_div = beautiful_soup.find(attrs={'class': 'container_s'})
            content_div = parse_div.find(id='content_left')



    def parse_recommend_search(self):
        super().parse_recommend_search()

    def parse_other_search(self):
        super().parse_other_search()

    def parse_result_page(self, result):
        super().parse_result_page()


test = PcBaiduSearch("全民彩票", 1)
test.genrate_pageurl()
