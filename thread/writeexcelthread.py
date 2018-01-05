# author : YangWan
# -*- coding: utf-8 -*-

from threading import Thread


class WriteExcelThread(Thread):
    '''
        解析Excel线程!!!
    '''

    def __init__(self, con, product_queue):
        self.condition = con
        self.product_queue = product_queue

    def run(self):
        pass