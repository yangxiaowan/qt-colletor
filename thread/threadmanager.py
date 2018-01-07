# author : YangWan
# -*- coding: utf-8 -*-

import threading
import time
from queue import Queue
from thread.crawlerparsethread import CrawlerParseThread
from thread.writeexcelthread import WriteExcelThread

'''
负责爬虫调度和多任务并发
'''


class CrawlerManager():
    # 爬虫线程数列
    thread_list = []

    # 分配线程的步长
    step_len = 5

    cond = threading.Condition()

    product_queue = Queue()

    excel_thread = None

    def __init__(self, search_class, keyword_list, page_num=5, dir_path='', file_name='result.xlsx'):
        self.search_class = search_class
        self.keyword_list = keyword_list
        self.page_num = page_num
        self.dir_path = dir_path
        self.file_name = file_name

    #启动写excel进程
    def start_write_excel_thread(self, thread_num):
        self.excel_thread = WriteExcelThread(self.cond, self.product_queue, thread_num, self.dir_path, self.file_name)
        self.excel_thread.write_for_ready()
        self.excel_thread.start()

    '''
       为每个搜索引擎爬虫创建单独的线程，以免某个搜索的http请求延迟太久影响效率
    '''
    def create_thread_for_crawler(self):

        for key_item in self.search_class.keys():
            # 字典中元素为1的才会分配线程
            if self.search_class[key_item] == 1:
                # 对每个关键字新建一个单独的爬取线程
                for keyword_item in self.keyword_list:
                    for page_index in range(0, self.page_num + self.step_len, self.step_len):
                        crawler_thread = None
                        if page_index + self.step_len < self.page_num:
                            crawler_thread = CrawlerParseThread(self.cond, self.product_queue, key_item,
                                                                keyword_item, page_index + 1,
                                                                page_index + self.step_len)
                        else:
                            # 如果起始页码大于终止页码，则不分配线程
                            if page_index <= self.page_num:
                                crawler_thread = CrawlerParseThread(self.cond, self.product_queue, key_item,
                                                                    keyword_item, page_index + 1, self.page_num)
                        if crawler_thread is not None:
                            # 启动分页爬虫
                            crawler_thread.start()
                            self.thread_list.append(crawler_thread)
        self.start_write_excel_thread(len(self.thread_list))

    def wait_all_thread_finish(self):
        time.sleep(2)
        #主线程睡眠1秒，保证所有的爬虫线程都已经启动了
        for thread_item in self.thread_list:
            thread_item.join()
        if self.excel_thread is not None:
            self.excel_thread.join()
            self.excel_thread.save_excel()


search_class = {
    'pc_baidu': 1, 'pc_360': 1, 'pc_sogou': 1,
    'm_baidu': 0, 'm_360': 0, 'm_sogou': 0, 'm_shenma': 0
}
keyword_list = ['全民彩票']
start = time.time()
crawlermanager = CrawlerManager(search_class, keyword_list, 11)
crawlermanager.create_thread_for_crawler()
crawlermanager.wait_all_thread_finish()
end = time.time()
print("———————————————————————运行用时———————————————————————")
print(end - start)
