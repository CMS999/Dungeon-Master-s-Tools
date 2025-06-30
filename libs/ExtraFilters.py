# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExtraFiltersTab_base.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_extraFilters(object):
    def setupUi(self, extraFilters):
        if not extraFilters.objectName():
            extraFilters.setObjectName(u"extraFilters")
        extraFilters.resize(625, 282)
        extraFilters.setMinimumSize(QSize(625, 0))
        extraFilters.setMaximumSize(QSize(625, 16777215))
        self.gL_1 = QGridLayout(extraFilters)
        self.gL_1.setObjectName(u"gL_1")
        self.MM3Box = QCheckBox(extraFilters)
        self.MM3Box.setObjectName(u"MM3Box")

        self.gL_1.addWidget(self.MM3Box, 0, 0, 1, 1)

        self.vSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gL_1.addItem(self.vSpacer, 1, 0, 1, 1)


        self.retranslateUi(extraFilters)

        QMetaObject.connectSlotsByName(extraFilters)
    # setupUi

    def retranslateUi(self, extraFilters):
        extraFilters.setWindowTitle(QCoreApplication.translate("extraFilters", u"Form", None))
        self.MM3Box.setText(QCoreApplication.translate("extraFilters", u"Include old Monsters (Pre-MM3, old stat blocks)", None))
    # retranslateUi

