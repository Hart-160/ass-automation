# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'entryBEAhGZ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(271, 161)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(271, 161))
        MainWindow.setMaximumSize(QSize(271, 161))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 251, 141))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.generate_template = QPushButton(self.layoutWidget)
        self.generate_template.setObjectName(u"generate_template")
        sizePolicy.setHeightForWidth(self.generate_template.sizePolicy().hasHeightForWidth())
        self.generate_template.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.generate_template.setFont(font)

        self.verticalLayout.addWidget(self.generate_template)

        self.run_ass = QPushButton(self.layoutWidget)
        self.run_ass.setObjectName(u"run_ass")
        sizePolicy.setHeightForWidth(self.run_ass.sizePolicy().hasHeightForWidth())
        self.run_ass.setSizePolicy(sizePolicy)
        self.run_ass.setFont(font)

        self.verticalLayout.addWidget(self.run_ass)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"D4", None))
        self.generate_template.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u7ffb\u8bd1\u6a21\u677f", None))
        self.run_ass.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u8f74\u673a\u7a0b\u5e8f", None))
    # retranslateUi

