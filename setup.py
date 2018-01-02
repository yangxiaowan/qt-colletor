# author : YangWan
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from uipy.mwindow import MyQMainWindow

import sys
from uipy.searchwin import Ui_search


app = QApplication(sys.argv)
mainwindow = MyQMainWindow()
mwind = Ui_search()
mwind.setupUi(mainwindow)
mainwindow.show()
sys.exit(app.exec_())
