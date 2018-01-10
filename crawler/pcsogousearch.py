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


class PcSogouSearch(MySearch):
    # 搜索排名
    page_index = 0

    # 当前解析页面
    cur_parse_page = 0

    website_start_url = 'https://www.sogou.com/web'

    domain_url = 'https://www.sogou.com/web?query='

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
            # 搜索具体内容div
            content_div = beautiful_soup.find('div', attrs={'class': 'results'})
            # 搜索到的推荐搜索div
            other_search_div = beautiful_soup.find('dl', attrs={'class': 'hint2'})
            # 定位到相关搜索
            relate_search_div = beautiful_soup.find('div', attrs={'class': 'hintBox'})
            if other_search_div is not None:
                self.parse_other_search(other_search_div)
            if relate_search_div is not None and \
                            self.relate_search_parseflag is False and self.recommend_search_index < 2:
                self.recommend_search_index += 1
                self.parse_relate_search(relate_search_div)
            self.parse_result_page(content_div)
            self.product_item = ProductItem(self.content_parse_list, self.relate_search_list, self.other_search_dit)

    def parse_relate_search(self, relate_div):
        print("正在解析搜狗相关搜索.....................")
        relate_table = relate_div.find("table", id='hint_container')
        if relate_table is not None:
            relate_search_td = relate_table.find_all("td")
            print("搜索到相关词条数目:", len(relate_search_td))
            relate_str = ''
            item_index = 0
            for relate_search_item in relate_search_td:
                single_dit = dict()
                text = relate_search_item.find("a").string
                relate_url = self.website_start_url + relate_search_item.find("a").get("href")
                url = re.sub('\n', '', relate_url)
                relate_str += '序号: %d ,  词条: %s  ||  ' % \
                              (item_index, text,)
            if self.cur_parse_page > 1:
                self.recommend_search_index = 2
            self.relate_search_list[self.recommend_search_index] = relate_str
            print(self.relate_search_list)
        print("搜狗相关搜索解析完毕.....................")

    '''
    解析相关推荐
    '''

    def parse_other_search(self, result):
        print("正在解析搜狗其他搜索.....................")
        what_title = '相关推荐：'
        what_seach_dd = result.find_all("a")
        dda_list = []
        for dda_item in what_seach_dd:
            dda_dit = {}
            dda_dit['text'] = dda_item.get_text()
            dda_dit['url'] = dda_item.get("href")
            dda_list.append(dda_dit)
        self.other_search_dit[what_title] = dda_list
        print(self.other_search_dit)
        print("正在解析搜狗其他搜索.....................")
        pass

    def parse_result_page(self, result):
        print("正在解析搜狗网站词条内容.....................")
        content_div_list = result.find_all("div", recursive=False)
        for content_div_item in content_div_list:
            # 寻找div树下的h3标签，如果存在，则当网站词条进行解析
            title_h3 = content_div_item.find("h3")
            if title_h3 is not None:
                self.page_index += 1
                craw_item = CrawlerItem()
                setattr(craw_item, 'search', "PC端搜狗")
                setattr(craw_item, 'keyword', self.keyword)
                setattr(craw_item, 'index', self.page_index)
                setattr(craw_item, 'page', str(self.cur_parse_page))
                # PC搜狗只有第一页的相关推荐是不同的
                if self.cur_parse_page == 1:
                    setattr(craw_item, 'relate_search', 1)
                else:
                    setattr(craw_item, 'relate_search', 2)
                title_h3_a = title_h3.find("a")
                if title_h3_a is not None:
                    setattr(craw_item, 'title', title_h3_a.get_text().replace('\n', ''))
                    setattr(craw_item, 'page_url', title_h3_a.get("href").replace('\n', ''))
                    str_info_div = content_div_item.find("div", attrs={'class': 'str_info_div'})
                    if str_info_div is not None:
                        p_text = str_info_div.find("p")
                        if p_text is not None:
                            setattr(craw_item, 'content', p_text.get_text().replace('\n', ''))
                        else:
                            setattr(craw_item, 'content', str_info_div.find("ul").get_text().replace('\n', ''))
                    else:
                        ft_content_div = content_div_item.find("div")
                        setattr(craw_item, 'content', re.sub('[\r\n\t\b ]', '', ft_content_div.get_text()))
                    fb_link_div = content_div_item.find("div", attrs={'class': 'fb'})
                    if fb_link_div is not None:
                        website_domain = fb_link_div.find("cite").get_text().replace('\n', '')
                        setattr(craw_item, 'domain', website_domain)
                # 解析搜狗知识，类似百度知道的模块
                str_pd_box = content_div_item.find("div", attrs={'class': 'str-pd-box'})
                if str_pd_box is not None:
                    start_box_item_start = str_pd_box.find("p", attrs={'class': 'str_time'})
                    if start_box_item_start is not None:
                        craw_box_item = CrawlerItem()
                        setattr(craw_box_item, 'title', start_box_item_start.get_text().replace('\n', ''))
                        setattr(craw_box_item, 'page', start_box_item_start.find("a").get("href").replace('\n', ''))
                        print(craw_box_item)
                    start_box_item_list = str_pd_box.find("ul")
                    if start_box_item_list is not None:
                        li_list = start_box_item_list.find_all("li")
                        for li_list_item in li_list:
                            craw_box_item = CrawlerItem()
                            setattr(craw_box_item, 'title', li_list_item.find("a").get_text().replace('\n', ''))
                            setattr(craw_box_item, 'page', li_list_item.find("a").get("href").replace('\n', ''))
                            print(craw_box_item)
                self.content_parse_list.append(craw_item)
                print(craw_item)
        print("搜索到网站词条数目为:", len(content_div_list))
        print("解析搜狗网站词条内容结束.....................")

# test = PcSogouSearch("全民彩票", 1, 2)
# test.genrate_pageurl()
