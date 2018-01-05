# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
import re

'''
搜狗移动端网页爬虫
'''


class MBaiduSearch(MySearch):
    # 搜索排名
    page_index = 0

    # 档期解析页面
    cur_parse_page = 0

    # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = {}

    website_start_url = 'https://wap.sogou.com/web/searchList.jsp'

    domain_url = 'https://wap.sogou.com/web/searchList.jsp?keyword='

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
            request_url = self.domain_url + self.keyword + "&pn=" + str(page_index)
            print("正在爬取页面url:", request_url)
            page_resource = self.get_content_whitget(request_url, 'utf-8')
            beautiful_soup = BeautifulSoup(page_resource.text, 'lxml')
            parse_div = beautiful_soup.find(attrs={'class': 'mainBody'})
            # 搜索具体内容div
            content_div = parse_div.find("div", attrs={'class': 'results'})
            # 搜索到的推荐搜索div --------暂时关闭调用
            other_search_div = parse_div.find(attrs={'class': '***'})
            # 定位到相关搜索
            relate_search_div = parse_div.find("div", id='hint')
            if self.recommend_search_parseflag is False:
                if other_search_div is not None:
                    self.parse_other_search(other_search_div)
            # 相关搜索的解析
            if self.relate_search_parseflag is False:
                if relate_search_div is not None:
                    self.parse_relate_search(relate_search_div)
                    self.relate_search_parseflag = True
            self.parse_result_page(content_div)

    '''
    相关搜索解析，只需解析一次,其他页面的相关搜索是相同的
    传入参数: div @id = rs
    '''

    def parse_relate_search(self, relate_div):
        print("正在为您解析移动搜狗相关搜索.....................")
        relate_rw_list = relate_div.find("ul")
        if relate_rw_list is not None:
            relate_search_a = relate_rw_list.find_all("a")
            print("搜索到相关词条数目:", len(relate_search_a))
            relate_result_list = []
            for relate_search_aitem in relate_search_a:
                single_dit = {}
                single_dit['text'] = relate_search_aitem.get_text()
                single_dit['url'] = self.website_start_url + relate_search_aitem.get("href")
                relate_result_list.append(single_dit)
                print(single_dit['text'], single_dit['url'])
            self.relate_search_list[1] = relate_result_list
            print(self.relate_search_list)
        print("移动端搜狗相关搜索解析完毕.....................")

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
        content_div_list = result.find_all("div", attrs={'class': re.compile("^(vrResult|result)$")})
        print("搜索到网站词条数目: ", len(content_div_list))
        if content_div_list is not None:
            for content_div_item in content_div_list:
                # 创建网站词条搜索对象，保存爬取数据
                data_extquery = content_div_item.get("data-extquery")
                # 如果data-extquery不为空，则为网站词条
                if data_extquery is None:
                    content_title = content_div_item.find("h3", attrs={'class': 'vr-tit'})
                    if content_title is None:
                        content_title = content_div_item.find("h3")
                    if content_title is not None:
                        craw_item = CrawlerItem()
                        self.page_index += 1
                        setattr(craw_item, 'search', "移动端搜狗")
                        setattr(craw_item, 'keyword', self.keyword)
                        setattr(craw_item, 'title', re.sub('[\r\n\t\b ]', '', content_title.get_text()))
                        content_title_a = content_title.find("a")
                        if content_title_a is None:
                            content_title_a = content_div_item.find("a")
                        if content_title_a is not None:
                            setattr(craw_item, 'page_url', content_title_a.get("href"))
                        setattr(craw_item, 'index', self.page_index)
                        setattr(craw_item, 'page', str(self.cur_parse_page))
                        content_desc_div = \
                            content_div_item.find("div", attrs={'class': re.compile("^(info|text-layout)$")})
                        if content_desc_div is None:
                            content_desc_div = content_div_item.find("div")
                        setattr(craw_item, 'content', re.sub('[\r\n\t\b ]', '', content_desc_div.get_text()))
                        website_domain_span = content_div_item.find("div", attrs={'class': re.compile(".*(citeurl).*")})
                        if website_domain_span is not None:
                            setattr(craw_item, 'domain', website_domain_span.get_text())
                        else:
                            setattr(craw_item, 'domain', 'wenwen.sougou.com')
                        print(craw_item)


test = MBaiduSearch("全名彩票", 1)
test.genrate_pageurl()
