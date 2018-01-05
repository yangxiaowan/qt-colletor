# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchwin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QProgressDialog
from uipy.searchbar import ProgressBar
import os

class Ui_search(object):

    search_class = {
        'pc_baidu': 0, 'pc_360': 0, 'pc_sogou': 0,
        'm_baidu': 0, 'm_360': 0, 'm_sogou': 0, 'm_shenma': 0
    }

    keyword_list = []

    task_finish = False

    pagenum = 1

    dir_path = 'C:\colletor-result'

    file_name = ''

    def setupUi(self, search):
        search.setObjectName("search")
        search.setEnabled(True)
        search.resize(779, 547)
        search.setAutoFillBackground(False)
        self.pcUrlLabel = QtWidgets.QLabel(search)
        self.pcUrlLabel.setGeometry(QtCore.QRect(70, 70, 121, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pcUrlLabel.setFont(font)
        self.pcUrlLabel.setObjectName("pcUrlLabel")
        self.mUrlLabel = QtWidgets.QLabel(search)
        self.mUrlLabel.setGeometry(QtCore.QRect(60, 289, 121, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.mUrlLabel.setFont(font)
        self.mUrlLabel.setObjectName("mUrlLabel")
        self.keywordLabel = QtWidgets.QLabel(search)
        self.keywordLabel.setGeometry(QtCore.QRect(310, 70, 121, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.keywordLabel.setFont(font)
        self.keywordLabel.setObjectName("keywordLabel")
        self.keywordEdit = QtWidgets.QTextEdit(search)
        self.keywordEdit.setGeometry(QtCore.QRect(410, 80, 261, 41))
        self.keywordEdit.setObjectName("keywordEdit")
        self.keywordEdit.setFont(font)
        self.pagenumLabel = QtWidgets.QLabel(search)
        self.pagenumLabel.setGeometry(QtCore.QRect(310, 140, 121, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pagenumLabel.setFont(font)
        self.pagenumLabel.setObjectName("pagenumLabel")
        self.pagenumDownList = QtWidgets.QComboBox(search)
        self.pagenumDownList.setGeometry(QtCore.QRect(410, 160, 69, 22))
        self.pagenumDownList.setObjectName("pagenumDownList")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumDownList.addItem("")
        self.pagenumEdit = QtWidgets.QTextEdit(search)
        self.pagenumEdit.setGeometry(QtCore.QRect(510, 160, 61, 31))
        self.pagenumEdit.setObjectName("pagenumEdit")
        self.excelButton = QtWidgets.QPushButton(search)
        self.excelButton.setGeometry(QtCore.QRect(310, 420, 381, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pagenumEdit.setFont(font)
        self.excelButton.setFont(font)
        self.excelButton.setObjectName("excelButton")
        self.saveFileLabel = QtWidgets.QLabel(search)
        self.saveFileLabel.setGeometry(QtCore.QRect(310, 280, 121, 61))
        self.saveFileLabel.setFont(font)
        self.saveFileLabel.setObjectName("saveFileLabel")
        self.saveFileEdit = QtWidgets.QTextEdit(search)
        self.saveFileEdit.setGeometry(QtCore.QRect(410, 290, 300, 41))
        self.saveFileEdit.setObjectName("saveFileEdit")
        self.saveFileEdit.setFont(font)

        self.saveFileNameLabel = QtWidgets.QLabel(search)
        self.saveFileNameLabel.setGeometry(QtCore.QRect(310, 340, 121, 61))
        self.saveFileNameLabel.setFont(font)
        self.saveFileNameLabel.setObjectName("saveFileNameLabel")
        self.saveFileNameEdit = QtWidgets.QTextEdit(search)
        self.saveFileNameEdit.setGeometry(QtCore.QRect(420, 350, 200, 41))
        self.saveFileNameEdit.setObjectName("saveFileNameEdit")
        self.saveFileNameEdit.setFont(font)
        # self.isClassLabel = QtWidgets.QLabel(search)
        # self.isClassLabel.setGeometry(QtCore.QRect(310, 340, 121, 61))
        # font = QtGui.QFont()
        # font.setFamily("Calibri")
        # font.setPointSize(12)
        # font.setBold(True)
        # font.setWeight(75)
        # self.isClassLabel.setFont(font)
        # self.isClassLabel.setObjectName("isClassLabel")
        # self.classYesCheckbox = QtWidgets.QCheckBox(search)
        # self.classYesCheckbox.setGeometry(QtCore.QRect(400, 360, 63, 23))
        # font = QtGui.QFont()
        # font.setFamily("Calibri")
        # font.setPointSize(14)
        # font.setBold(True)
        # font.setWeight(75)
        # self.classYesCheckbox.setFont(font)
        # self.classYesCheckbox.setAutoFillBackground(True)
        # self.classYesCheckbox.setObjectName("classYesCheckbox")
        # self.classNoCheckbox = QtWidgets.QCheckBox(search)
        # self.classNoCheckbox.setGeometry(QtCore.QRect(490, 360, 63, 23))
        # font = QtGui.QFont()
        # font.setFamily("Calibri")
        # font.setPointSize(14)
        # font.setBold(True)
        # font.setWeight(75)
        # self.classNoCheckbox.setFont(font)
        # self.classNoCheckbox.setObjectName("classNoCheckbox")
        self.splitter = QtWidgets.QSplitter(search)
        self.splitter.setGeometry(QtCore.QRect(80, 140, 63, 81))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.pcBaiduCheckbox = QtWidgets.QCheckBox(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pcBaiduCheckbox.setFont(font)
        self.pcBaiduCheckbox.setObjectName("pcBaiduCheckbox")
        self.pc360Checkbox = QtWidgets.QCheckBox(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pc360Checkbox.setFont(font)
        self.pc360Checkbox.setObjectName("pc360Checkbox")
        self.pcSogouCheckbox = QtWidgets.QCheckBox(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pcSogouCheckbox.setFont(font)
        self.pcSogouCheckbox.setObjectName("pcSogouCheckbox")
        self.splitter_2 = QtWidgets.QSplitter(search)
        self.splitter_2.setGeometry(QtCore.QRect(70, 360, 63, 108))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.mBaiduCheckbox = QtWidgets.QCheckBox(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.mBaiduCheckbox.setFont(font)
        self.mBaiduCheckbox.setObjectName("mBaiduCheckbox")
        self.m360Checkbox = QtWidgets.QCheckBox(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.m360Checkbox.setFont(font)
        self.m360Checkbox.setObjectName("m360Checkbox")
        self.mSogouCheckbox = QtWidgets.QCheckBox(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.mSogouCheckbox.setFont(font)
        self.mSogouCheckbox.setObjectName("mSogouCheckbox")
        self.mShenmaCheckbox = QtWidgets.QCheckBox(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.mShenmaCheckbox.setFont(font)
        self.mShenmaCheckbox.setObjectName("mShenmaCheckbox")

        self.retranslateUi(search)
        self.excelButton.clicked.connect(self.generateExcel)
        QtCore.QMetaObject.connectSlotsByName(search)

    def generateSearchClass(self):
        if self.pcBaiduCheckbox.isChecked() is True:
            self.search_class['pc_baidu'] = 1
        else:
            self.search_class['pc_baidu'] = 0
        if self.pc360Checkbox.isChecked() is True:
            self.search_class['pc_360'] = 1
        else:
            self.search_class['pc_360'] = 0
        if self.pcSogouCheckbox.isChecked() is True:
            self.search_class['pc_sogou'] = 1
        else:
            self.search_class['pc_sogou'] = 0
        if self.mBaiduCheckbox.isChecked() is True:
            self.search_class['m_baidu'] = 1
        else:
            self.search_class['m_baidu'] = 0
        if self.m360Checkbox.isChecked() is True:
            self.search_class['m_360'] = 1
        else:
            self.search_class['m_360'] = 0
        if self.mSogouCheckbox.isChecked() is True:
            self.search_class['m_sogou'] = 1
        else:
            self.search_class['m_sogou'] = 0
        if self.mShenmaCheckbox.isChecked() is True:
            self.search_class['m_shenma'] = 1
        else:
            self.search_class['m_shenma'] = 0

    def generateExcel(self):
        self.generateSearchClass()
        self.keyword = self.keywordEdit.toPlainText()
        pagenumStr = self.pagenumEdit.toPlainText()
        try:
            if len(pagenumStr.strip()) > 0:
                self.pagenum = int(pagenumStr.strip())
            else:
                self.pagenum = int(self.pagenumDownList.currentText())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.excelButton, "提示", "亲, 输入页码格式不对哦！")
            return
        editDirpath = self.saveFileEdit.toPlainText()
        if len(editDirpath.strip()) > 0:
            if os.path.isdir(editDirpath):
                self.dir_path = editDirpath
            else:
                QtWidgets.QMessageBox.warning(self.excelButton, "提示", "亲, 您输入的不是一个文件目录哦！"
                                                                      "如果你嫌麻烦可以不填写，默认路径为" + self.dir_path)
                return

        if self.search_class['pc_baidu'] == 0 and self.search_class['pc_360'] == 0 \
                and self.search_class['pc_sogou'] == 0 \
                and self.search_class['m_baidu'] == 0 and self.search_class['m_360'] == 0 \
                and self.search_class['m_sogou'] == 0 and self.search_class['m_shenma'] == 0:
            QtWidgets.QMessageBox.information(self.excelButton, "提示", "亲, 未选择搜索引擎分类!")
            return
        if len(self.keyword.strip()) == 0:
            QtWidgets.QMessageBox.information(self.excelButton, "提示", "亲, 请输入关键字，不然无法为您搜索!")
            return
        else:
            self.keyword_list = self.keyword.split(',|，')
        from uipy.crawlerthread import CrawlerHandler
        self.crawler_process = CrawlerHandler()
        # 登陆完成的信号绑定到登陆结束的槽函数
        self.crawler_process.finishSignal.connect(self.finishCrawler)
        # 启动线程
        self.crawler_process.start()

    def finishCrawler(self, words):
        for i in words:
            print(i)
        QtWidgets.QMessageBox.information(self.excelButton, "提示", "爬取任务完成，快去查看你的excel文件吧!")

    def retranslateUi(self, search):
        _translate = QtCore.QCoreApplication.translate
        search.setWindowTitle(_translate("search", "search v-1.0"))
        self.pcUrlLabel.setText(_translate("search", "PC端URL"))
        self.mUrlLabel.setText(_translate("search", "手机端URL"))
        self.keywordLabel.setText(_translate("search", "关键字："))
        self.pagenumLabel.setText(_translate("search", "页码："))
        self.pagenumDownList.setItemText(0, _translate("search", "5"))
        self.pagenumDownList.setItemText(1, _translate("search", "10"))
        self.pagenumDownList.setItemText(2, _translate("search", "20"))
        self.pagenumDownList.setItemText(3, _translate("search", "30"))
        self.pagenumDownList.setItemText(4, _translate("search", "40"))
        self.pagenumDownList.setItemText(5, _translate("search", "50"))
        self.pagenumDownList.setItemText(6, _translate("search", "60"))
        self.pagenumDownList.setItemText(7, _translate("search", "70"))
        self.pagenumDownList.setItemText(8, _translate("search", "80"))
        self.pagenumDownList.setItemText(9, _translate("search", "90"))
        self.pagenumDownList.setItemText(10, _translate("search", "100"))
        self.pagenumDownList.setItemText(11, _translate("search", "200"))
        self.excelButton.setText(_translate("search", "生成excel表格"))
        self.saveFileLabel.setText(_translate("search", "保存路径: "))
        self.saveFileNameLabel.setText(_translate("search", "保存文件名: "))
        # self.isClassLabel.setText(_translate("search", "是否分类"))
        # self.classYesCheckbox.setText(_translate("search", "是"))
        # self.classNoCheckbox.setText(_translate("search", "否"))
        self.pcBaiduCheckbox.setText(_translate("search", "百度"))
        self.pc360Checkbox.setText(_translate("search", "360"))
        self.pcSogouCheckbox.setText(_translate("search", "搜狗"))
        self.mBaiduCheckbox.setText(_translate("search", "百度"))
        self.m360Checkbox.setText(_translate("search", "360"))
        self.mSogouCheckbox.setText(_translate("search", "搜狗"))
        self.mShenmaCheckbox.setText(_translate("search", "神马"))

