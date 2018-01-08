# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
from file.productitem import ProductItem
import re

'''
移动端360搜索引擎爬虫
'''

class M360Search(MySearch):
    # 搜索排名
    page_index = 0

    # 当前解析页面
    cur_parse_page = 0

    # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = {}

    website_start_url = 'https://m.so.com'

    domain_url = 'https://m.so.com/nextpage?ajax=1&q='

    # 是否进行了相关搜索的解析
    relate_search_parseflag = False

    # 是否进行推荐搜索的解析
    recommend_search_parseflag = False

    recommend_search_index = 0

    # 网站词条解析数组
    content_parse_list = []

    def genrate_pageurl(self):
        super().genrate_pageurl()
        self.cur_parse_page = self.start_parse_index - 1
        for page_index in range(self.start_parse_index, self.end_parse_index + 1):
            self.cur_parse_page += 1
            print("starting！！！！！")
            request_url = self.domain_url + self.keyword + "&pn=" + str(page_index)
            print("正在爬取页面url:", request_url)
            page_resource = self.get_content_whitget(request_url, 'utf-8')
            beautiful_soup = BeautifulSoup(page_resource.text, 'lxml')
            other_search_div = beautiful_soup.find_all("div", attrs={'class': re.compile(".*(cli-recommend).*")})
            relate_search_div = beautiful_soup.find("div", attrs={'class': re.compile(".*(related-search).*")})
            if other_search_div is not None:
                self.parse_other_search(other_search_div)
            if relate_search_div is not None and self.relate_search_parseflag is False:
                self.parse_relate_search(relate_search_div)
                self.relate_search_parseflag = True
            self.parse_result_page(beautiful_soup)
            self.product_item = ProductItem(self.content_parse_list, self.relate_search_list, self.other_search_dit)

    def parse_other_search(self, result):
        print("正在解析360为您推荐.....................")
        result_str = ''
        item_index = 0
        for result_item in result:
            result_item_alist = result_item.find_all("a")
            if len(result_item_alist) > 0:
                for every_a in result_item_alist:
                    item_index += 1
                    text = every_a.get_text()
                    url = self.website_start_url + str(every_a.get("href"))
                    result_str += '序号: %d ,  词条: %s  ||  ' % (item_index, text,)
        self.other_search_dit[self.cur_parse_page] = result_str
        print(self.other_search_dit)
        print("解析360为您推荐结束.....................")

    def parse_relate_search(self, relate_div):
        print("正在解析移动端360相关搜索.....................")
        every_search_li = relate_div.find_all("li")
        relate_str = ''
        item_index = 0
        for every_search_item in every_search_li:
            item_index += 1
            text = every_search_item.get_text()
            url = self.website_start_url + str(every_search_item.get("href"))
            relate_str += '序号: %d ,  词条: %s  ||  ' % (item_index, text,)
        self.relate_search_list[0] = relate_str
        print(self.relate_search_list)
        print("解析移动端360相关搜索结束......................")

    def parse_result_page(self, result):
        print("正在解析移动端360页面......................")
        res_list = result.find_all("div", attrs={'class': re.compile(".*(g-card).*")})
        print("找到解析网站词条数目: ", len(res_list))
        for res_list_item in res_list:
            res_list_h3 = res_list_item.find("h3", attrs={'class': 'res-title'})
            if res_list_h3 is not None:
                self.page_index += 1
                craw_item = CrawlerItem()
                setattr(craw_item, 'search', "移动端360")
                setattr(craw_item, 'keyword', self.keyword)
                setattr(craw_item, 'index', self.page_index)
                setattr(craw_item, 'page', str(self.cur_parse_page))
                setattr(craw_item, 'relate_search', 0)
                setattr(craw_item, 'other_search', self.cur_parse_page)
                setattr(craw_item, 'title', res_list_h3.get_text().replace("\n", ""))
                res_list_alink = res_list_item.find("a", attrs={'class': 'alink'})
                if res_list_alink is not None:
                    setattr(craw_item, 'page_url', res_list_alink.get("href"))
                desc_content_p = res_list_item.find(attrs={'class': re.compile(".*(summary).*")})
                if desc_content_p is not None:
                    page_content = desc_content_p.get_text()
                else:
                    page_content_div = res_list_item.find("div")
                    page_content = page_content_div.get_text()
                setattr(craw_item, 'content', page_content.replace("\n", ""))
                res_linkinfo_p = res_list_item.find(attrs={"class": "res-site-url"})
                linkinfo = ''
                if res_linkinfo_p is not None:
                    linkinfo = res_linkinfo_p.get_text()
                else:
                    temp_url = res_list_item.find(attrs={"class": "res-site-name"})
                    if temp_url is not None:
                        linkinfo = temp_url.get_text()
                setattr(craw_item, 'domain', linkinfo)
                setattr(craw_item, 'index', self.page_index)
                self.content_parse_list.append(craw_item)
                print(craw_item)
        print("解析移动端360页面结束......................")

# test = M360Search("全民彩票", 1, 4, 3)
# test.genrate_pageurl()
