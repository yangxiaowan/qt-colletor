# author : YangWan
# -*- coding: utf-8 -*-
class ProductItem(object):
    '''
    生产对象，初始化参数:
    crawler_list 爬虫爬取的结果数列
    relate_dit 相关搜索的数据字典
    other_dit 其他搜索的数据字典
    '''

    def __init__(self, crawler_list, relate_dit, other_dit):
        self.crawler_list = crawler_list
        self.relate_dit = relate_dit
        self.other_dit = other_dit
