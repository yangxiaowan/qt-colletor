# author : YangWan
# -*- coding: utf-8 -*-
import threading
import time
from crawler.pcbaidusearch import PcBaiduSearch
from crawler.pc360search import Pc360Search
from crawler.pcsogousearch import PcSogouSearch
from crawler.mbaidusearch import MBaiduSearch
from crawler.m360search import M360Search
from crawler.msougousearch import MSogouSearch
from crawler.mshenmasearch import MShenmaSearch
from queue import Queue
from file.productitem import ProductItem


class CrawlerParseThread(threading.Thread):
    product_item = None
    '''
    初始化爬虫线程
    cond 锁对象
    product_queue 生产队列
    search_name 搜索引擎种类
    keyword 关键字
    start_index 开始搜索页面索引
    end_index 结束搜索页面索引
    '''

    def __init__(self, cond, product_queue, search_name, keyword, start_index, end_index):
        super(CrawlerParseThread, self).__init__()
        self.condition = cond
        self.product_queue = product_queue
        self.search_name = search_name
        self.keyword = keyword
        self.start_index = start_index
        self.end_index = end_index
        print("进程初始化完成!!! search_name: " + self.search_name + " start_index: " + str(
            self.start_index) + " end_index: " + str(self.end_index))

    def run(self):
        super().run()
        if self.search_name == 'pc_baidu':
            self.product_item = PcBaiduSearch(self.keyword, self.start_index, self.end_index).get_product_item()
        elif self.search_name == 'pc_360':
            self.product_item = Pc360Search(self.keyword, self.start_index, self.end_index).get_product_item()
        elif self.search_name == 'pc_sogou':
            self.product_item = PcSogouSearch(self.keyword, self.start_index, self.end_index).get_product_item()
        elif self.search_name == 'm_baidu':
            self.product_item = MBaiduSearch(self.keyword, self.start_index, self.end_index).get_product_item()
        elif self.search_name == 'm_360':
            self.product_item = M360Search(self.keyword, self.start_index, self.end_index).get_product_item()
        elif self.search_name == 'm_sogou':
            self.product_item = MSogouSearch(self.keyword, self.start_index, self.end_index).get_product_item()
        elif self.search_name == 'm_shenma':
            self.product_item = MShenmaSearch(self.keyword, self.start_index, self.end_index).get_product_item()
        self.condition.acquire()
        if self.product_queue.qsize() > 10:
            self.condition.wait()
        self.product_queue.put(self.product_item)
        self.condition.notify()
        self.condition.release()
        print("当前生产队列未写入爬取数据个数: " + str(self.product_queue.qsize()))

    def get_product_queue(self):
        return self.product_queue

# cond = threading.Condition()
# q = Queue()
# test = CrawlerParseThread(cond, q, "pc_baidu", "杨万", 1, 2)
# test.start()
