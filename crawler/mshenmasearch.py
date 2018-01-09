# author : YangWan
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawler.mysearch import MySearch
from file.crawleritem import CrawlerItem
from file.productitem import ProductItem
# http://m.sm.cn/s?q=%E9%85%B8%E5%A5%B6%E4%BB%80%E4%B9%88%E6%97%B6%E5%80%99%E5%96%9D%E6%AF%94%E8%BE%83%E5%A5%BD
class MShenmaSearch(MySearch):
    # 搜索排名
    page_index = 0

    # 档期解析页面
    cur_parse_page = 0

    # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = {}

    website_start_url = 'http://m.sm.cn'

    domain_url = 'http://m.sm.cn/s?q='

    # 是否进行了相关搜索的解析
    relate_search_parseflag = False

    # 是否进行推荐搜索的解析
    recommend_search_parseflag = False

    # 网站词条解析数组
    content_parse_list = []

    def genrate_pageurl(self):
        super().genrate_pageurl()
        self.cur_parse_page = self.start_parse_index - 1
        for page_index in range(self.start_parse_index, self.end_parse_index + 1):
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
            if relate_search_div is not None:
                self.parse_relate_search(relate_search_div)
            self.parse_result_page(parse_div)
            self.product_item = ProductItem(self.content_parse_list, self.relate_search_list, self.other_search_dit)

    def parse_result_page(self, result):
        content_div_list = result.find_all("div", attrs={'class': 'article ali_row'})
        if content_div_list is not None and len(content_div_list) > 0:
            for content_div_item in content_div_list:
                title_h2 = content_div_item.find("h2")
                if title_h2 is not None:
                    self.page_index += 1
                    craw_item = CrawlerItem()
                    setattr(craw_item, 'search', "移动端神马")
                    setattr(craw_item, 'relate_search', self.cur_parse_page)
                    setattr(craw_item, 'keyword', self.keyword)
                    setattr(craw_item, 'index', self.page_index)
                    setattr(craw_item, 'page', str(self.cur_parse_page))
                    setattr(craw_item, 'title', title_h2.get_text().replace("\n", ""))
                    setattr(craw_item, 'page_url', title_h2.find("a").get("href"))
                    content_desc_p = content_div_item.find("p")
                    if content_desc_p is not None:
                        setattr(craw_item, 'content', content_desc_p.get_text())
                    else:
                        setattr(craw_item, 'content', content_div_item.get_text())
                    down_link_div = result.find("div", attrs={'class': 'other'})
                    if down_link_div is not None:
                        setattr(craw_item, 'domain', down_link_div.get_text())
                self.content_parse_list.append(craw_item)
                print(craw_item)

    def parse_relate_search(self, relate_div):
        print("正在解析移动端神马相关搜索.....................")
        relate_ul = relate_div.find("ul")
        if relate_ul is not None:
            relate_search_a = relate_ul.find_all("a")
            print("搜索到相关词条数目:", len(relate_search_a))
            relate_str = ''
            item_index = 0
            for relate_search_item in relate_search_a:
                item_index += 1
                text = relate_search_item.get_text()
                url = self.website_start_url + relate_search_item.get("href")
                relate_str += '序号: %d ,  词条: %s  ||  ' % (item_index, text,)
            self.relate_search_list[self.cur_parse_page] = relate_str
            print(self.relate_search_list)
        print("移动端神马相关搜索解析完毕.....................")

    def parse_other_search(self, result):
        pass


test = MShenmaSearch("全名彩票", 1, 2)
test.genrate_pageurl()
