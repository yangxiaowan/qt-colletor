# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
from file.productitem import ProductItem
import re

'''
百度网页爬虫
'''
class PcBaiduSearch(MySearch):
    # 搜索排名
    page_index = 0

    # 档期解析页面
    cur_parse_page = 0

    #其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = {}

    website_start_url = 'https://www.baidu.com'

    domain_url = 'https://www.baidu.com/s?wd='

    #是否进行了相关搜索的解析
    relate_search_parseflag = False

    #是否进行推荐搜索的解析
    recommend_search_parseflag = False

    def genrate_pageurl(self):
        self.cur_parse_page = self.start_parse_index - 1
        for page_index in range(self.start_parse_index, self.end_parse_index + 1):
            self.cur_parse_page += 1
            if page_index > 1:
                request_url = self.domain_url + self.keyword + "&pn=" + str((page_index - 1) * 10)
            else:
                request_url = self.domain_url + self.keyword
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
            # 获得生成对象，在接下来的get_product_item方法时会返回生产对象
            self.product_item = ProductItem(self.content_parse_list, self.relate_search_list, self.other_search_dit)

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
            relate_result_list = []
            for relate_search_item in relate_search_th:
                single_dit = {}
                single_dit['text'] = relate_search_item.find("a").string
                single_dit['url'] = self.website_start_url + relate_search_item.find("a").get("href")
                relate_result_list.append(single_dit)
                print(single_dit['text'], single_dit['url'])
            self.relate_search_list[1] = relate_result_list
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
                    self.page_index += 1
                    content_titlea = content_h3.find("a")
                    setattr(craw_item, 'search', "PC端百度")
                    setattr(craw_item, 'keyword', self.keyword)
                    setattr(craw_item, 'title', content_titlea.get_text())
                    setattr(craw_item, 'page_url', content_titlea.get("href"))
                    setattr(craw_item, 'index', self.page_index)
                    setattr(craw_item, 'page', str(self.cur_parse_page))
                content_desc_div = content_div_item.find("div", attrs={'class': re.compile(".*(c-abstract).*")})
                if content_desc_div is not None:
                    setattr(craw_item, 'content', content_desc_div.get_text())
                else:
                    content_desc_div = content_div_item.find(attrs={'class': re.compile(".*(c-row).*")})
                    if content_desc_div is not None:
                        setattr(craw_item, 'content', re.sub('[\r\n\t\b ]', '', content_desc_div.get_text()))
                    else:
                        setattr(craw_item, 'content', re.sub('[\r\n\t\b ]', '', content_div_item.get_text()))
                website_domain_div = content_div_item.find("div", attrs={'class': re.compile(".*f13.*")})
                if website_domain_div is not None:
                    showurl_a = website_domain_div.find(attrs={'class': "c-showurl"})
                    if showurl_a is None:
                        showurl_a = website_domain_div.find("a")
                    if showurl_a is not None:
                        setattr(craw_item, 'domain', showurl_a.get_text())
                else:
                    showurl_a = content_div_item.find_all("span", attrs={'class': "c-showurl"})[0]
                    setattr(craw_item, 'domain', showurl_a.get_text())
                offset_div = content_div_item.find("div", attrs={'class': "c-offset"})
                # 将解析词条加入数列
                self.content_parse_list.append(craw_item)
                # 解析类似于百度知道的下拉连接
                if offset_div is not None:
                    craw_other_item = CrawlerItem()
                    down_list_tr = offset_div.find_all("tr")
                    print("解析百度知道，找到下拉连接个数： ", len(down_list_tr))
                    for down_item in down_list_tr:
                        setattr(craw_other_item, 'title', down_item.find("a").get_text())
                        setattr(craw_other_item, 'page', down_item.find("a").get("href"))
                        print(craw_other_item)
                        self.content_parse_list.append(craw_other_item)
                print(craw_item)

# test = PcBaiduSearch("全民彩票", 10, 10, 5)
# test.genrate_pageurl()
