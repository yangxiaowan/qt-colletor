# author : YangWan
# -*- coding: utf-8 -*-

import threading
import time
from crawler.pcbaidusearch import PcBaiduSearch
from crawler.pc360search import Pc360Search
from crawler.pcsogousearch import PcSogouSearch

'''
负责爬虫调度和多任务并发
'''


class CrawlerManager():
    # 爬虫线程数列
    thread_list = []

    def __init__(self, search_class, keyword_list, page_num=5, dir_path='C:\colletor-result', file_name=None):
        self.search_class = search_class
        self.keyword_list = keyword_list
        self.page_num = page_num
        self.dir_path = dir_path
        self.file_name = file_name

    '''
       为每个搜索引擎爬虫创建单独的线程，以免某个搜索的http请求延迟太久影响效率 
    '''

    def create_thread_for_crawler(self):
        for key_item in self.search_class.keys():
            # 字典中元素为1的才会分配线程
            if self.search_class[key_item] == 1:
                # 对每个关键字新建一个单独的爬取线程
                for keyword_item in self.keyword_list:
                    crawler_thread = threading.Thread(target=self.start_crawler, args=(key_item, keyword_item))
                    crawler_thread.start()
                    self.thread_list.append(crawler_thread)

    '''
    根据搜索引擎名称和关键字来启动爬虫
    '''

    def start_crawler(self, search_name, keyword):
        if search_name == 'pc_baidu':
            PcBaiduSearch(keyword, self.page_num).genrate_pageurl()
        elif search_name == 'pc_360':
            Pc360Search(keyword, self.page_num).genrate_pageurl()
        elif search_name == 'pc_sogou':
            PcSogouSearch(keyword, self.page_num).genrate_pageurl()

    def wait_all_finish(self):
        for thread_item in self.thread_list:
            thread_item.join()


search_class = {
    'pc_baidu': 1, 'pc_360': 1, 'pc_sogou': 0,
    'm_baidu': 0, 'm_360': 0, 'm_sogou': 0, 'm_shenma': 0
}
keyword_list = ['全民彩票']
start = time.time()
crawlermanager = CrawlerManager(search_class, keyword_list, 50)
crawlermanager.create_thread_for_crawler()
crawlermanager.wait_all_finish()
end = time.time()

print("———————————————————————运行用时———————————————————————")
print(end - start)
