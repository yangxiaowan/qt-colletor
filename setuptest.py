# author : YangWan# author : YangWan
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

import sys
from uipy.test import Ui_Form


app = QApplication(sys.argv)
mainwindow = QMainWindow()
mwind = Ui_Form()
mwind.setupUi(mainwindow)
mainwindow.show()
sys.exit(app.exec_())



