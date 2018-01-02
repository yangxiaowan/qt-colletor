# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
import re

'''
百度网页爬虫
'''
class PcBaiduSearch(MySearch):

    #其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = []

    website_start_url = 'https://www.baidu.com'

    domain_url = 'https://www.baidu.com/s?wd='

    #是否进行了相关搜索的解析
    relate_search_parseflag = False

    #是否进行推荐搜索的解析
    recommend_search_parseflag = False

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
            #搜索具体内容div
            content_div = parse_div.find(id='content_left')
            #搜索到的推荐搜索div
            other_search_div = beautiful_soup.find(attrs={'class': 'hint_toprq_tips f13 se_common_hint'})
            #定位到相关搜索
            relate_search_div = parse_div.find(id='rs')
            if self.recommend_search_parseflag is False:
                if other_search_div is not None:
                    self.parse_other_search(other_search_div)
            if self.relate_search_parseflag is False:
                self.parse_relate_search(relate_search_div)
            self.parse_result_page(content_div)

    '''
    相关搜索解析，只需解析一次,其他页面的相关搜索是相同的
    传入参数: div @id = rs
    '''
    def parse_relate_search(self, relate_div):
        print("正在解析百度相关搜索.....................")
        relate_table = relate_div.find("table")
        if relate_table is not None:
            relate_search_th = relate_table.find_all("th")
            print("搜索到相关词条数目:", len(relate_search_th))
            for relate_search_item in relate_search_th:
                single_dit = {}
                single_dit['text'] = relate_search_item.find("a").string
                single_dit['url'] = self.website_start_url + relate_search_item.find("a").get("href")
                self.relate_search_list.append(single_dit)
                print(single_dit['text'], single_dit['url'])
            print(self.relate_search_list)
        print("百度相关搜索解析完毕.....................")

    '''
        推荐搜索解析，只需解析一次,其他页面的推荐搜索是相同的
        传入参数: div @class = hint_toprq_tips f13 se_common_hint
    '''
    def parse_other_search(self, result):
        print("正在解析百度为您推荐.....................")
        recommend_span = result.find("span", attrs={'class': 'hint_toprq_tips_items'})
        recommend_diva = recommend_span.find_all("a")
        recommend_search_list = []
        for recommend_diva_item in recommend_diva:
            single_dit = {}
            single_dit['text'] = recommend_diva_item.string
            single_dit['url'] = self.website_start_url + recommend_diva_item.get("href")
            recommend_search_list.append(single_dit)
        self.other_search_dit['为您推荐'] = recommend_search_list
        print("为您推荐: ", self.other_search_dit)
        print("解析百度为您推荐结束.....................")

    '''
    解析页面内容
    '''
    def parse_result_page(self, result):
        content_div_list = result.find_all("div", attrs={'class': re.compile(".*(c-container).*")})
        print("搜索到网站词条数目: ", len(content_div_list))
        if content_div_list is not None:
            for content_div_item in content_div_list:
                #创建网站词条搜索对象，保存爬取数据
                craw_item = CrawlerItem()
                content_h3 = content_div_item.find("h3", attrs={'class': re.compile("t.*")})
                if content_h3 is not None:
                    content_titlea = content_h3.find("a")
                    print(content_titlea.txt)
                    # craw_item.__setattr__('title', content_titlea.string)
                    # craw_item.__setattr__('pageurl', content_titlea.get("href"))
                    # print(craw_item)


test = PcBaiduSearch("全民彩票", 1)
test.genrate_pageurl()
