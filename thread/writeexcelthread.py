# author : YangWan
# -*- coding: utf-8 -*-
import threading
from queue import Queue
from threading import Thread
from crawler.pcbaidusearch import PcBaiduSearch
import xlwt
class WriteExcelThread(Thread):

    column_num = 10
    '''
        解析Excel线程!!!
    '''
    execl_headers = ['搜索引擎', '关键字', '页码', '排名', '网站标识', '网站标题',
                     '网站简介', '网站链接', '相关搜索', '其他搜索']

    # global_rank_index = {
    # 'PC端百度': 0, 'PC端360': 0, 'PC端搜狗': 0,
    # '移动端百度': 0, '移动端360': 0, '移动端搜狗': 0, '移动端神马': 0
    # }

    result_sheet = None

    work_book = None

    #写当前行
    write_cur_row = 1

    #当前写入生产线程序号
    cur_wirte_index = 0

    def __init__(self, con, product_queue, thread_num, file_name='result.xls', dir_path=''):
        super(WriteExcelThread, self).__init__()
        self.condition = con
        self.product_queue = product_queue
        self.thread_num = thread_num
        self.file_name = file_name
        self.dir_path = dir_path

    def write_for_ready(self):
        self.write_excel_head(self.create_workspace())

    def set_style(self, name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height
        # borders= xlwt.Borders()
        # borders.left= 6
        # borders.right= 6
        # borders.top= 6
        # borders.bottom= 6
        style.font = font
        return style

    #x写excel表头
    def write_excel_head(self, result_sheet):
        print("Info： write the excel headers!!!")
        if result_sheet is not None:
            header_index = 0
            for header_item in self.execl_headers:
                result_sheet.write(0, header_index, header_item)
                header_index += 1
        else:
            print("Error： don't find the sheet, can't write the headers of the excel!!")

    # 创建工作簿
    def create_workspace(self, sheet_name='sheet'):
        self.work_book = xlwt.Workbook()
        # 创建sheet
        self.result_sheet = self.work_book.add_sheet(sheet_name, cell_overwrite_ok=True)
        print("Info： create the work book!!!")
        return self.result_sheet

    # 保存文件
    def save_excel(self):
        self.work_book.save(self.dir_path + self.file_name)
        print("Info： save the excel successfully!!!")


    def write_product_to_excel(self, product_item):
        print("Info： write the crawleritem to excel!!! GODD!!!!!!!")
        if self.work_book is not None:
            relate_search_dit = getattr(product_item, 'relate_dit')
            other_search_dit = getattr(product_item, 'other_dit')
            crawler_list = getattr(product_item, 'crawler_list')
            if crawler_list is not None and len(crawler_list) > 0:
                for crawler_item in crawler_list:
                    self.result_sheet.write(self.write_cur_row, 0, getattr(crawler_item, 'search'))
                    self.result_sheet.write(self.write_cur_row, 1, getattr(crawler_item, 'keyword'))
                    self.result_sheet.write(self.write_cur_row, 2, getattr(crawler_item, 'page'))
                    self.result_sheet.write(self.write_cur_row, 3, getattr(crawler_item, 'index'))
                    self.result_sheet.write(self.write_cur_row, 4, getattr(crawler_item, 'domain'))
                    self.result_sheet.write(self.write_cur_row, 5, getattr(crawler_item, 'title'))
                    content_str = getattr(crawler_item, 'content')
                    if content_str is not None and len(content_str) > 32767:
                        content_str = content_str[0:32766]
                    self.result_sheet.write(self.write_cur_row, 6, content_str)
                    self.result_sheet.write(self.write_cur_row, 7, getattr(crawler_item, 'page_url'))
                    # 相关推荐的写入
                    relate_search_key = getattr(crawler_item, 'relate_search')
                    if relate_search_key in relate_search_dit.keys():
                        relate_str = relate_search_dit[relate_search_key]
                        if relate_str is not None and len(relate_str) > 0:
                            relate_str = relate_str[0:32766]
                        self.result_sheet.write(self.write_cur_row, 8, relate_str)

                    # 其他推荐的写入
                    other_search_key = getattr(crawler_item, 'other_search')
                    if other_search_key in other_search_dit.keys():
                        other_str = other_search_dit[other_search_key]
                        if len(other_str) > 0:
                            other_str = other_str[0:32766]
                        self.result_sheet.write(self.write_cur_row, 9, other_str)

                    self.write_cur_row += 1

    def run(self):
        while True:
            self.condition.acquire()
            # 如果队列不为空，则从里面取出生产对象
            if self.product_queue.empty() is True:
                # 如果队列为空，写excel线程挂起
                self.condition.wait()
                self.condition.notify()
            # 从队头删除并返回一个生产对象
            product_item = self.product_queue.get()
            if product_item is not None:
                self.write_product_to_excel(product_item)
                self.cur_wirte_index += 1
            self.condition.release()
            if self.cur_wirte_index == self.thread_num:
                break

# cond = threading.Condition()
# q = Queue()
# crawler_test = PcBaiduSearch("全民彩票", 1, 1, 5)
# q.put(crawler_test.get_product_item())
# test = WriteExcelThread(cond, q)
# test.write_for_ready()
# test.start()
# test.join()
# test.save_excel()

