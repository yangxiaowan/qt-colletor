# author : YangWan
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from crawler.pcbaidusearch import PcBaiduSearch
from thread.threadmanager import CrawlerManager
import time

class CrawlerHandler(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)

    def __init__(self, search_class, keyword_list, page_num, dir_path='', file_name='result.xls'):
        super(CrawlerHandler, self).__init__()
        self.search_class = search_class
        self.keyword_list = keyword_list
        self.page_num = page_num
        self.dir_path = dir_path
        self.file_name = file_name
        print("UI后台线程初始化参数: dir_path" + dir_path + "file_name" + file_name)

    def run(self):
        # test = PcBaiduSearch("全民彩票", 1, 2)
        # test.genrate_pageurl()
        start = time.time()
        crawlermanager = CrawlerManager(self.search_class, self.keyword_list, self.page_num, self.dir_path,
                                        self.file_name)
        crawlermanager.create_thread_for_crawler()
        crawlermanager.wait_all_thread_finish()
        end = time.time()
        print("———————————————————————运行用时———————————————————————")
        print(end - start)
        time.sleep(1)
        self.finishSignal.emit(['FINISH'])
