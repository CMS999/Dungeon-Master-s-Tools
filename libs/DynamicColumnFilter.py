# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DynamicColumnFilterTab_base.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QWidget)

class Ui_DynamicColumnFilter(object):
    def setupUi(self, DynamicColumnFilter):
        if not DynamicColumnFilter.objectName():
            DynamicColumnFilter.setObjectName(u"DynamicColumnFilter")
        DynamicColumnFilter.resize(400, 300)
        self.gL1 = QGridLayout(DynamicColumnFilter)
        self.gL1.setObjectName(u"gL1")
        self.hL_1 = QHBoxLayout()
        self.hL_1.setObjectName(u"hL_1")
        self.hSpacer1 = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hL_1.addItem(self.hSpacer1)

        self.btnReset = QPushButton(DynamicColumnFilter)
        self.btnReset.setObjectName(u"btnReset")

        self.hL_1.addWidget(self.btnReset)

        self.hSpacer2 = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hL_1.addItem(self.hSpacer2)


        self.gL1.addLayout(self.hL_1, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(DynamicColumnFilter)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QWidget()
        self.scrollAreaContents.setObjectName(u"scrollAreaContents")
        self.scrollAreaContents.setGeometry(QRect(0, 0, 380, 232))
        self.gL2 = QGridLayout(self.scrollAreaContents)
        self.gL2.setObjectName(u"gL2")
        self.scrollArea.setWidget(self.scrollAreaContents)

        self.gL1.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.retranslateUi(DynamicColumnFilter)

        QMetaObject.connectSlotsByName(DynamicColumnFilter)
    # setupUi

    def retranslateUi(self, DynamicColumnFilter):
        DynamicColumnFilter.setWindowTitle(QCoreApplication.translate("DynamicColumnFilter", u"Form", None))
        self.btnReset.setText(QCoreApplication.translate("DynamicColumnFilter", u"Reset Filters", None))
    # retranslateUi

