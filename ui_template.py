# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'templategaVxbB.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_GenerateTemplate(object):
    def setupUi(self, GenerateTemplate):
        if not GenerateTemplate.objectName():
            GenerateTemplate.setObjectName(u"GenerateTemplate")
        GenerateTemplate.resize(531, 97)
        GenerateTemplate.setMinimumSize(QSize(531, 97))
        GenerateTemplate.setMaximumSize(QSize(531, 97))
        self.centralwidget = QWidget(GenerateTemplate)
        self.centralwidget.setObjectName(u"centralwidget")
        self.generate = QPushButton(self.centralwidget)
        self.generate.setObjectName(u"generate")
        self.generate.setGeometry(QRect(400, 50, 121, 41))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(14)
        self.generate.setFont(font)
        self.choose_sce = QPushButton(self.centralwidget)
        self.choose_sce.setObjectName(u"choose_sce")
        self.choose_sce.setGeometry(QRect(400, 10, 121, 31))
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(11)
        self.choose_sce.setFont(font1)
        self.sce_route = QLineEdit(self.centralwidget)
        self.sce_route.setObjectName(u"sce_route")
        self.sce_route.setGeometry(QRect(10, 10, 381, 31))
        font2 = QFont()
        font2.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        self.sce_route.setFont(font2)
        self.generate_text = QPushButton(self.centralwidget)
        self.generate_text.setObjectName(u"generate_text")
        self.generate_text.setGeometry(QRect(270, 50, 121, 41))
        self.generate_text.setFont(font)
        self.back_main = QPushButton(self.centralwidget)
        self.back_main.setObjectName(u"back_main")
        self.back_main.setGeometry(QRect(10, 50, 121, 41))
        self.back_main.setFont(font)
        self.generate_docx = QPushButton(self.centralwidget)
        self.generate_docx.setObjectName(u"generate_docx")
        self.generate_docx.setGeometry(QRect(140, 50, 121, 41))
        self.generate_docx.setFont(font)
        GenerateTemplate.setCentralWidget(self.centralwidget)

        self.retranslateUi(GenerateTemplate)

        QMetaObject.connectSlotsByName(GenerateTemplate)
    # setupUi

    def retranslateUi(self, GenerateTemplate):
        GenerateTemplate.setWindowTitle(QCoreApplication.translate("GenerateTemplate", u"Generate Translation Template", None))
        self.generate.setText(QCoreApplication.translate("GenerateTemplate", u"\u6a21\u677f\u751f\u6210", None))
        self.choose_sce.setText(QCoreApplication.translate("GenerateTemplate", u"\u9009\u62e9\u5267\u60c5\u6587\u4ef6", None))
        self.generate_text.setText(QCoreApplication.translate("GenerateTemplate", u"\u6587\u672c\u63d0\u53d6", None))
        self.back_main.setText(QCoreApplication.translate("GenerateTemplate", u"\u8fd4\u56de\u4e0a\u7ea7", None))
        self.generate_docx.setText(QCoreApplication.translate("GenerateTemplate", u"Docx\u63d0\u53d6", None))
    # retranslateUi

