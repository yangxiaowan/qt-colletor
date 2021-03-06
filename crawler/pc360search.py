# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
from file.productitem import ProductItem
import re

'''
搜狗搜索引擎爬虫
'''

class Pc360Search(MySearch):
    # 搜索排名
    page_index = 0

    # 当前解析页面
    cur_parse_page = 0

    website_start_url = 'https://www.so.com'

    domain_url = 'https://www.so.com/s?q='

    # 是否进行了相关搜索的解析
    relate_search_parseflag = False

    # 是否进行推荐搜索的解析
    recommend_search_parseflag = False

    recommend_search_index = 0

    def genrate_pageurl(self):
        # 网站词条解析数组
        self.content_parse_list = []

        # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
        self.other_search_dit = {}
        self.relate_search_list = {}

        self.cur_parse_page = self.start_parse_index - 1
        for page_index in range(self.start_parse_index, self.end_parse_index + 1):
            self.cur_parse_page += 1
            request_url = self.domain_url + self.keyword + "&page=" + str(page_index)
            print("正在爬取页面url:", request_url)
            page_resource = self.get_content_whitget(request_url, 'utf-8')
            beautiful_soup = BeautifulSoup(page_resource.text, 'lxml')
            parse_div = beautiful_soup.find("div", attrs={'id': 'main'})
            # 搜索具体内容div
            content_div = parse_div.find("ul", attrs={'class': 'result'})
            # 搜索到的推荐搜索div
            other_search_div = beautiful_soup.find("dl", attrs={'class': 'so-pdr'})
            # 定位到相关搜索
            relate_search_div = beautiful_soup.find("div", attrs={'class': 'mod-relation'})
            if self.recommend_search_parseflag is False:
                if other_search_div is not None:
                    self.parse_other_search(other_search_div)
                    self.recommend_search_parseflag = True
            if self.relate_search_parseflag is False:
                self.parse_relate_search(relate_search_div)
                self.relate_search_parseflag = True
            self.parse_result_page(content_div)
            self.product_item = ProductItem(self.content_parse_list, self.relate_search_list, self.other_search_dit)

    def parse_other_search(self, result):
        print("正在解析360为您推荐.....................")
        every_search_a = result.find_all("a")
        every_search_list = []
        for every_search_aitem in every_search_a:
            single_search_dit = {}
            single_search_dit['text'] = every_search_aitem.get_text()
            single_search_dit['url'] = self.website_start_url + every_search_aitem.get("href")
            every_search_list.append(single_search_dit)
        self.other_search_dit['为您推荐'] = every_search_list
        print(self.other_search_dit)
        print("解析360为您推荐结束.....................")

    def parse_relate_search(self, relate_div):
        print("正在解析360相关搜索.....................")
        data_table = relate_div.find("table")
        if data_table is not None:
            every_search_a = data_table.find_all("a")
            relate_str = ''
            item_index = 0
            for every_search_aitem in every_search_a:
                item_index += 1
                text = every_search_aitem.get_text()
                url = self.website_start_url + every_search_aitem.get("href")
                relate_str += '%s , ' % (text,)
            self.relate_search_list[0] = relate_str
        print(self.relate_search_list)
        print("解析360相关搜索结束......................")

    def parse_result_page(self, result):
        print("正在解析360页面......................")
        res_list = result.find_all("li", attrs={'class': 'res-list'})
        print("找到解析网站词条数目: ", len(res_list))
        for res_list_item in res_list:
            res_list_h3 = res_list_item.find("h3")
            if res_list_h3 is not None:
                self.page_index += 1
                craw_item = CrawlerItem()
                setattr(craw_item, 'search', "PC端360")
                setattr(craw_item, 'keyword', self.keyword)
                setattr(craw_item, 'index', self.page_index)
                setattr(craw_item, 'page', str(self.cur_parse_page))
                setattr(craw_item, 'relate_search', 0)
                res_list_h3_a = res_list_h3.find("a")
                if res_list_h3_a is not None:
                    setattr(craw_item, 'title', res_list_h3_a.get_text().replace("\n", ""))
                    setattr(craw_item, 'page_url', res_list_h3_a.get("href"))
                desc_content_p = res_list_item.find(attrs={'class': re.compile(".*(res-desc).*")})
                if desc_content_p is not None:
                    page_content = desc_content_p.get_text()
                else:
                    page_content_div = res_list_item.find("div")
                    page_content = page_content_div.get_text()
                setattr(craw_item, 'content', page_content.replace("\n", ""))
                res_linkinfo_p = res_list_item.find(attrs={"class": "res-linkinfo"})
                linkinfo = ''
                if res_linkinfo_p is not None:
                    linkinfo = res_linkinfo_p.find("cite").get_text()
                else:
                    temp_url = res_list_item.find(attrs={"class": "mh-showurl"})
                    if temp_url is not None:
                        linkinfo = temp_url.find("cite").get_text()
                setattr(craw_item, 'domain', linkinfo)
                setattr(craw_item, 'index', self.page_index)
                self.content_parse_list.append(craw_item)
                more_answer = res_list_item.find("ul", attrs={"class", "more-ans"})
                print(craw_item)
                if more_answer is not None:
                    more_answer_alist = more_answer.find_all("a")
                    if len(more_answer_alist) > 0:
                        for more_answer_item in more_answer_alist:
                            craw_son_item = CrawlerItem()
                            setattr(craw_son_item, 'title', more_answer_item.get_text())
                            setattr(craw_son_item, 'page_url', more_answer_item.get("href"))
                            self.content_parse_list.append(craw_son_item)
                            print(craw_son_item)
        print("解析360页面结束......................")

# test = Pc360Search("全民彩票合法吗", 1, 2, 10)
# test.genrate_pageurl()
