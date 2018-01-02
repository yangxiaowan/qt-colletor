# author : YangWan
from PyQt5 import QtCore, QtGui
import time


class CrawlerHandler(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(CrawlerHandler, self).__init__(parent)
        pass

    def run(self):
        time.sleep(6)
        self.finishSignal.emit(['hello,', 'world', '!'])
