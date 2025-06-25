# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FilterUITest.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLayout,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_FilterTab(object):
    def setupUi(self, FilterTab):
        if not FilterTab.objectName():
            FilterTab.setObjectName(u"FilterTab")
        FilterTab.resize(625, 303)
        FilterTab.setMinimumSize(QSize(625, 0))
        FilterTab.setMaximumSize(QSize(625, 16777215))
        self.gridLayout_3 = QGridLayout(FilterTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout_3.setContentsMargins(0, 9, 0, 0)
        self.gL_1 = QGridLayout()
        self.gL_1.setObjectName(u"gL_1")
        self.gL_1.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.hL_1 = QHBoxLayout()
        self.hL_1.setObjectName(u"hL_1")
        self.hL_1.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.hSpacer_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hL_1.addItem(self.hSpacer_1)

        self.selectAll = QPushButton(FilterTab)
        self.selectAll.setObjectName(u"selectAll")

        self.hL_1.addWidget(self.selectAll)

        self.selectNone = QPushButton(FilterTab)
        self.selectNone.setObjectName(u"selectNone")

        self.hL_1.addWidget(self.selectNone)

        self.hSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hL_1.addItem(self.hSpacer_2)


        self.gL_1.addLayout(self.hL_1, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(FilterTab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.sAContents = QWidget()
        self.sAContents.setObjectName(u"sAContents")
        self.sAContents.setGeometry(QRect(0, 0, 607, 256))
        self.gridLayout_4 = QGridLayout(self.sAContents)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.scrollArea.setWidget(self.sAContents)

        self.gL_1.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gL_1, 0, 0, 1, 1)


        self.retranslateUi(FilterTab)

        QMetaObject.connectSlotsByName(FilterTab)
    # setupUi

    def retranslateUi(self, FilterTab):
        FilterTab.setWindowTitle(QCoreApplication.translate("FilterTab", u"Form", None))
        self.selectAll.setText(QCoreApplication.translate("FilterTab", u"Select All", None))
        self.selectNone.setText(QCoreApplication.translate("FilterTab", u"Select None", None))
    # retranslateUi

