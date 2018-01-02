# author : YangWan
from PyQt5.QtWidgets import QMainWindow
import sys
from PyQt5.QtWidgets import QMessageBox

class MyQMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '警告！！！', '您确认要关闭吗?请你查看后台任务是否执行结束，否则不能获得爬取结果！',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
