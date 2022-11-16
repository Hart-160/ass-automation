# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'run_assGSQxfC.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ASS_automation(object):
    def setupUi(self, ASS_automation):
        if not ASS_automation.objectName():
            ASS_automation.setObjectName(u"ASS_automation")
        ASS_automation.resize(650, 600)
        ASS_automation.setMinimumSize(QSize(650, 600))
        ASS_automation.setMaximumSize(QSize(10000, 10000))
        self.centralwidget = QWidget(ASS_automation)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.video_route = QLineEdit(self.centralwidget)
        self.video_route.setObjectName(u"video_route")
        self.video_route.setMinimumSize(QSize(0, 30))
        self.video_route.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        self.video_route.setFont(font)

        self.horizontalLayout_2.addWidget(self.video_route)

        self.choose_video = QPushButton(self.centralwidget)
        self.choose_video.setObjectName(u"choose_video")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_video.sizePolicy().hasHeightForWidth())
        self.choose_video.setSizePolicy(sizePolicy)
        self.choose_video.setMinimumSize(QSize(120, 30))
        self.choose_video.setMaximumSize(QSize(120, 30))
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(11)
        self.choose_video.setFont(font1)

        self.horizontalLayout_2.addWidget(self.choose_video)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.sce_route = QLineEdit(self.centralwidget)
        self.sce_route.setObjectName(u"sce_route")
        self.sce_route.setMinimumSize(QSize(0, 30))
        self.sce_route.setMaximumSize(QSize(16777215, 30))
        self.sce_route.setFont(font)

        self.horizontalLayout_3.addWidget(self.sce_route)

        self.choose_sce = QPushButton(self.centralwidget)
        self.choose_sce.setObjectName(u"choose_sce")
        sizePolicy.setHeightForWidth(self.choose_sce.sizePolicy().hasHeightForWidth())
        self.choose_sce.setSizePolicy(sizePolicy)
        self.choose_sce.setMinimumSize(QSize(120, 30))
        self.choose_sce.setMaximumSize(QSize(120, 30))
        self.choose_sce.setFont(font1)

        self.horizontalLayout_3.addWidget(self.choose_sce)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.template_route = QLineEdit(self.centralwidget)
        self.template_route.setObjectName(u"template_route")
        self.template_route.setMinimumSize(QSize(0, 30))
        self.template_route.setMaximumSize(QSize(16777215, 30))
        self.template_route.setFont(font)

        self.horizontalLayout_4.addWidget(self.template_route)

        self.choose_template = QPushButton(self.centralwidget)
        self.choose_template.setObjectName(u"choose_template")
        sizePolicy.setHeightForWidth(self.choose_template.sizePolicy().hasHeightForWidth())
        self.choose_template.setSizePolicy(sizePolicy)
        self.choose_template.setMinimumSize(QSize(120, 30))
        self.choose_template.setMaximumSize(QSize(120, 30))
        self.choose_template.setFont(font1)

        self.horizontalLayout_4.addWidget(self.choose_template)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.back_main = QPushButton(self.centralwidget)
        self.back_main.setObjectName(u"back_main")
        sizePolicy.setHeightForWidth(self.back_main.sizePolicy().hasHeightForWidth())
        self.back_main.setSizePolicy(sizePolicy)
        self.back_main.setMinimumSize(QSize(120, 40))
        self.back_main.setMaximumSize(QSize(120, 40))
        font2 = QFont()
        font2.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font2.setPointSize(14)
        self.back_main.setFont(font2)

        self.horizontalLayout.addWidget(self.back_main)

        self.generate = QPushButton(self.centralwidget)
        self.generate.setObjectName(u"generate")
        sizePolicy.setHeightForWidth(self.generate.sizePolicy().hasHeightForWidth())
        self.generate.setSizePolicy(sizePolicy)
        self.generate.setMinimumSize(QSize(120, 40))
        self.generate.setMaximumSize(QSize(120, 40))
        self.generate.setFont(font2)

        self.horizontalLayout.addWidget(self.generate)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(8)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(70, 30))
        self.label.setMaximumSize(QSize(70, 30))
        font3 = QFont()
        font3.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font3.setPointSize(10)
        self.label.setFont(font3)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 30))
        self.progressBar.setMaximumSize(QSize(16777215, 30))
        self.progressBar.setFont(font3)
        self.progressBar.setValue(0)

        self.horizontalLayout_5.addWidget(self.progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.output_window = QTextBrowser(self.centralwidget)
        self.output_window.setObjectName(u"output_window")
        font4 = QFont()
        font4.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font4.setPointSize(9)
        self.output_window.setFont(font4)

        self.verticalLayout.addWidget(self.output_window)

        ASS_automation.setCentralWidget(self.centralwidget)

        self.retranslateUi(ASS_automation)

        QMetaObject.connectSlotsByName(ASS_automation)
    # setupUi

    def retranslateUi(self, ASS_automation):
        ASS_automation.setWindowTitle(QCoreApplication.translate("ASS_automation", u"D4DJ ASS Automation", None))
        self.choose_video.setText(QCoreApplication.translate("ASS_automation", u"\u9009\u62e9\u89c6\u9891\u6587\u4ef6", None))
        self.choose_sce.setText(QCoreApplication.translate("ASS_automation", u"\u9009\u62e9\u5267\u60c5\u6587\u4ef6", None))
        self.choose_template.setText(QCoreApplication.translate("ASS_automation", u"\u9009\u62e9\u7ffb\u8bd1\u6a21\u677f", None))
        self.back_main.setText(QCoreApplication.translate("ASS_automation", u"\u8fd4\u56de\u4e0a\u7ea7", None))
        self.generate.setText(QCoreApplication.translate("ASS_automation", u"\u5b57\u5e55\u751f\u6210", None))
        self.label.setText(QCoreApplication.translate("ASS_automation", u"\u8f74\u673a\u8fdb\u5ea6", None))
    # retranslateUi

