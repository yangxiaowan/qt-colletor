# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
from file.productitem import ProductItem
import re

'''
百度移动端网页爬虫
'''


class MBaiduSearch(MySearch):
    # 搜索排名
    page_index = 0

    # 档期解析页面
    cur_parse_page = 0

    website_start_url = 'https://m.baidu.com'

    domain_url = 'https://m.baidu.com/s?word='

    # 是否进行了相关搜索的解析
    relate_search_parseflag = False

    # 是否进行推荐搜索的解析
    recommend_search_parseflag = False

    def genrate_pageurl(self):
        # 网站词条解析数组
        self.content_parse_list = []

        # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
        self.other_search_dit = {}
        self.relate_search_list = {}

        self.cur_parse_page = self.start_parse_index - 1
        for page_index in range(self.start_parse_index, self.end_parse_index + 1):
            self.cur_parse_page += 1
            # 移动端和pc端连接方式相同
            if page_index > 1:
                request_url = self.domain_url + self.keyword + "&pn=" + str((page_index - 1) * 10)
            else:
                request_url = self.domain_url + self.keyword
            print("正在爬取页面url:", request_url)
            page_resource = self.get_content_whitget(request_url, 'utf-8')
            beautiful_soup = BeautifulSoup(page_resource.text, 'lxml')
            parse_div = beautiful_soup.find(attrs={'class': 'search-page'})
            # 搜索具体内容div
            content_div = parse_div.find(attrs={'id': 'results', 'class': 'results'})
            # 搜索到的推荐搜索div --------暂时关闭调用
            other_search_div = beautiful_soup.find(attrs={'class': '***'})
            # 定位到相关搜索
            relate_search_div = parse_div.find(id='reword')
            if self.recommend_search_parseflag is False:
                if other_search_div is not None:
                    self.parse_other_search(other_search_div)
            # 相关搜索的解析
            if self.relate_search_parseflag is False:
                if relate_search_div is not None:
                    self.parse_relate_search(relate_search_div)
                    self.relate_search_parseflag = True
            self.parse_result_page(content_div)
            self.product_item = ProductItem(self.content_parse_list, self.relate_search_list, self.other_search_dit)

    '''
    相关搜索解析，只需解析一次,其他页面的相关搜索是相同的
    传入参数: div @id = rs
    '''

    def parse_relate_search(self, relate_div):
        print("正在为您解析移动百度相关搜索.....................")
        relate_rw_list = relate_div.find(attrs={'class': 'rw-list'})
        if relate_rw_list is not None:
            relate_search_a = relate_rw_list.find_all("a")
            print("搜索到相关词条数目:", len(relate_search_a))
            relate_str = ''
            item_index = 0
            for relate_search_aitem in relate_search_a:
                item_index += 1
                text = relate_search_aitem.get_text()
                url = relate_search_aitem.get("href")
                relate_str += '%s , ' % (text,)
            self.relate_search_list[0] = relate_str
            print(self.relate_search_list)
        print("移动端百度相关搜索解析完毕.....................")

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
        content_div_list = result.find_all("div", attrs={'class': 'c-container'})
        print("搜索到网站词条数目: ", len(content_div_list))
        if content_div_list is not None:
            for content_div_item in content_div_list:
                # 创建网站词条搜索对象，保存爬取数据
                craw_item = CrawlerItem()
                content_a = content_div_item.find("a", attrs={'class': 'c-blocka'})
                if content_a is not None:
                    self.page_index += 1
                    setattr(craw_item, 'search', "移动端百度")
                    setattr(craw_item, 'keyword', self.keyword)
                    setattr(craw_item, 'title', content_a.get_text())
                    setattr(craw_item, 'page_url', content_a.get("href"))
                    setattr(craw_item, 'index', self.page_index)
                    setattr(craw_item, 'page', str(self.cur_parse_page))
                    setattr(craw_item, 'relate_search', 0)
                    content_desc_p = content_div_item.find("p", attrs={'class': re.compile(".*(c-line).*")})
                    if content_desc_p is not None:
                        setattr(craw_item, 'content', content_desc_p.get_text())
                    else:
                        setattr(craw_item, 'content', content_div_item.get_text())
                    website_domain_span = content_div_item.find("span", attrs={'class': 'c-showurl'})
                    if website_domain_span is not None:
                        setattr(craw_item, 'domain', website_domain_span.get_text())
                    else:
                        showurl_div = content_div_item.find("div", attrs={'class': re.compile(".*(c-line-clamp1).*")})
                        if showurl_div is not None:
                            setattr(craw_item, 'domain', showurl_div.get_text())
                    offset_div = content_div_item.find("div", attrs={'class': "c-offset"})
                    # 解析类似于百度知道的下拉连接
                    # if offset_div is not None:
                    #     craw_other_item = CrawlerItem()
                    #     down_list_tr = offset_div.find_all("tr")
                    #     print("解析百度知道，找到下拉连接个数： ", len(down_list_tr))
                    #     for down_item in down_list_tr:
                    #         setattr(craw_other_item, 'title', down_item.find("a").get_text())
                    #         setattr(craw_other_item, 'page', down_item.find("a").get("href"))
                    #         print(craw_other_item)
                self.content_parse_list.append(craw_item)
                print(craw_item)

# test = MBaiduSearch("捡到彩票中奖犯法吗", 11, 10)
# test.genrate_pageurl()
