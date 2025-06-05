# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Screen.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_Screen(object):
    def setupUi(self, Screen):
        if not Screen.objectName():
            Screen.setObjectName(u"Screen")
        Screen.resize(682, 532)
        self.hL_1 = QHBoxLayout(Screen)
        self.hL_1.setSpacing(0)
        self.hL_1.setObjectName(u"hL_1")
        self.hL_1.setContentsMargins(0, 0, 0, 0)
        self.gL_1 = QGridLayout()
        self.gL_1.setSpacing(2)
        self.gL_1.setObjectName(u"gL_1")
        self.gL_1.setContentsMargins(0, -1, -1, -1)
        self.gL_2 = QGridLayout()
        self.gL_2.setObjectName(u"gL_2")
        self.gL_2.setVerticalSpacing(0)
        self.gL_2.setContentsMargins(-1, -1, 0, -1)

        self.gL_1.addLayout(self.gL_2, 0, 6, 1, 1)

        self.hL_2 = QHBoxLayout()
        self.hL_2.setObjectName(u"hL_2")
        self.hL_2.setContentsMargins(0, -1, -1, -1)
        self.ddiTable = QTableWidget(Screen)
        if (self.ddiTable.columnCount() < 1):
            self.ddiTable.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.ddiTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.ddiTable.rowCount() < 1):
            self.ddiTable.setRowCount(1)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ddiTable.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.ddiTable.setItem(0, 0, __qtablewidgetitem2)
        self.ddiTable.setObjectName(u"ddiTable")
        self.ddiTable.setEnabled(True)
        self.ddiTable.setMinimumSize(QSize(500, 0))
        self.ddiTable.setAutoFillBackground(False)
        self.ddiTable.setStyleSheet(u"background: rgb(61, 56, 70)")
        self.ddiTable.setFrameShape(QFrame.StyledPanel)
        self.ddiTable.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ddiTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ddiTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ddiTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ddiTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ddiTable.setSortingEnabled(False)
        self.ddiTable.setColumnCount(1)

        self.hL_2.addWidget(self.ddiTable)


        self.gL_1.addLayout(self.hL_2, 0, 2, 1, 1)


        self.hL_1.addLayout(self.gL_1)


        self.retranslateUi(Screen)

        QMetaObject.connectSlotsByName(Screen)
    # setupUi

    def retranslateUi(self, Screen):
        Screen.setWindowTitle(QCoreApplication.translate("Screen", u"Form", None))
        ___qtablewidgetitem = self.ddiTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Screen", u"Name", None));
        ___qtablewidgetitem1 = self.ddiTable.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Screen", u"Name", None));

        __sortingEnabled = self.ddiTable.isSortingEnabled()
        self.ddiTable.setSortingEnabled(False)
        ___qtablewidgetitem2 = self.ddiTable.item(0, 0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Screen", u"asdasd", None));
        self.ddiTable.setSortingEnabled(__sortingEnabled)

    # retranslateUi

