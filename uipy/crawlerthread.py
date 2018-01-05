# author : YangWan
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from crawler.pcbaidusearch import PcBaiduSearch

class CrawlerHandler(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(CrawlerHandler, self).__init__(parent)
        pass

    def run(self):
        test = PcBaiduSearch("全民彩票", 1)
        test.genrate_pageurl()
        self.finishSignal.emit(['hello,', 'world', '!'])
