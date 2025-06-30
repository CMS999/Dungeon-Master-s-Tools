# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ColumnFiltersTab_base.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_ColumnFilter(object):
    def setupUi(self, ColumnFilter):
        if not ColumnFilter.objectName():
            ColumnFilter.setObjectName(u"ColumnFilter")
        ColumnFilter.resize(625, 431)
        ColumnFilter.setMinimumSize(QSize(625, 0))
        ColumnFilter.setMaximumSize(QSize(625, 16777215))
        self.gL_1 = QGridLayout(ColumnFilter)
        self.gL_1.setObjectName(u"gL_1")
        self.scrollArea = QScrollArea(ColumnFilter)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QWidget()
        self.scrollAreaContents.setObjectName(u"scrollAreaContents")
        self.scrollAreaContents.setGeometry(QRect(0, 0, 605, 377))
        self.gL_2 = QGridLayout(self.scrollAreaContents)
        self.gL_2.setObjectName(u"gL_2")
        self.sizeLabel = QLabel(self.scrollAreaContents)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.gL_2.addWidget(self.sizeLabel, 7, 2, 1, 1)

        self.roleLabel = QLabel(self.scrollAreaContents)
        self.roleLabel.setObjectName(u"roleLabel")

        self.gL_2.addWidget(self.roleLabel, 4, 4, 1, 1)

        self.tierLabel = QLabel(self.scrollAreaContents)
        self.tierLabel.setObjectName(u"tierLabel")

        self.gL_2.addWidget(self.tierLabel, 7, 4, 1, 1)

        self.actionBox = QComboBox(self.scrollAreaContents)
        self.actionBox.setObjectName(u"actionBox")
        self.actionBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)

        self.gL_2.addWidget(self.actionBox, 0, 3, 1, 1)

        self.pSourceLabel = QLabel(self.scrollAreaContents)
        self.pSourceLabel.setObjectName(u"pSourceLabel")

        self.gL_2.addWidget(self.pSourceLabel, 3, 4, 1, 1)

        self.pSourceBox = QComboBox(self.scrollAreaContents)
        self.pSourceBox.setObjectName(u"pSourceBox")

        self.gL_2.addWidget(self.pSourceBox, 3, 5, 1, 1)

        self.alignmentBox = QComboBox(self.scrollAreaContents)
        self.alignmentBox.setObjectName(u"alignmentBox")

        self.gL_2.addWidget(self.alignmentBox, 0, 5, 1, 1)

        self.caregotyBox = QComboBox(self.scrollAreaContents)
        self.caregotyBox.setObjectName(u"caregotyBox")

        self.gL_2.addWidget(self.caregotyBox, 1, 5, 1, 1)

        self.rarityBox = QComboBox(self.scrollAreaContents)
        self.rarityBox.setObjectName(u"rarityBox")

        self.gL_2.addWidget(self.rarityBox, 4, 3, 1, 1)

        self.mundaneBox = QComboBox(self.scrollAreaContents)
        self.mundaneBox.setObjectName(u"mundaneBox")

        self.gL_2.addWidget(self.mundaneBox, 9, 3, 1, 1)

        self.roleBox = QComboBox(self.scrollAreaContents)
        self.roleBox.setObjectName(u"roleBox")

        self.gL_2.addWidget(self.roleBox, 4, 5, 1, 1)

        self.mundaneLabel = QLabel(self.scrollAreaContents)
        self.mundaneLabel.setObjectName(u"mundaneLabel")

        self.gL_2.addWidget(self.mundaneLabel, 9, 2, 1, 1)

        self.tierBox = QComboBox(self.scrollAreaContents)
        self.tierBox.setObjectName(u"tierBox")

        self.gL_2.addWidget(self.tierBox, 7, 5, 1, 1)

        self.classBox = QComboBox(self.scrollAreaContents)
        self.classBox.setObjectName(u"classBox")

        self.gL_2.addWidget(self.classBox, 2, 3, 1, 1)

        self.usageBox = QComboBox(self.scrollAreaContents)
        self.usageBox.setObjectName(u"usageBox")

        self.gL_2.addWidget(self.usageBox, 8, 5, 1, 1)

        self.actionLabel = QLabel(self.scrollAreaContents)
        self.actionLabel.setObjectName(u"actionLabel")

        self.gL_2.addWidget(self.actionLabel, 0, 2, 1, 1)

        self.campaignBox = QComboBox(self.scrollAreaContents)
        self.campaignBox.setObjectName(u"campaignBox")

        self.gL_2.addWidget(self.campaignBox, 1, 3, 1, 1)

        self.costCheck = QCheckBox(self.scrollAreaContents)
        self.costCheck.setObjectName(u"costCheck")

        self.gL_2.addWidget(self.costCheck, 9, 4, 1, 1)

        self.hL_2 = QHBoxLayout()
        self.hL_2.setObjectName(u"hL_2")
        self.levelMin = QSpinBox(self.scrollAreaContents)
        self.levelMin.setObjectName(u"levelMin")
        self.levelMin.setMinimum(0)
        self.levelMin.setMaximum(35)
        self.levelMin.setValue(0)

        self.hL_2.addWidget(self.levelMin)

        self.levelMax = QSpinBox(self.scrollAreaContents)
        self.levelMax.setObjectName(u"levelMax")
        self.levelMax.setMinimum(0)
        self.levelMax.setMaximum(35)
        self.levelMax.setValue(35)

        self.hL_2.addWidget(self.levelMax)


        self.gL_2.addLayout(self.hL_2, 10, 3, 1, 1)

        self.typeBox = QComboBox(self.scrollAreaContents)
        self.typeBox.setObjectName(u"typeBox")

        self.gL_2.addWidget(self.typeBox, 8, 3, 1, 1)

        self.kindBox = QComboBox(self.scrollAreaContents)
        self.kindBox.setObjectName(u"kindBox")

        self.gL_2.addWidget(self.kindBox, 3, 3, 1, 1)

        self.hL_3 = QHBoxLayout()
        self.hL_3.setObjectName(u"hL_3")
        self.costMin = QSpinBox(self.scrollAreaContents)
        self.costMin.setObjectName(u"costMin")
        self.costMin.setAccelerated(True)
        self.costMin.setMinimum(0)
        self.costMin.setMaximum(3125000)
        self.costMin.setValue(0)

        self.hL_3.addWidget(self.costMin)

        self.costMax = QSpinBox(self.scrollAreaContents)
        self.costMax.setObjectName(u"costMax")
        self.costMax.setAccelerated(True)
        self.costMax.setProperty(u"showGroupSeparator", True)
        self.costMax.setMinimum(0)
        self.costMax.setMaximum(3125000)
        self.costMax.setValue(3125000)
        self.costMax.setDisplayIntegerBase(10)

        self.hL_3.addWidget(self.costMax)


        self.gL_2.addLayout(self.hL_3, 9, 5, 1, 1)

        self.gRoleLabel = QLabel(self.scrollAreaContents)
        self.gRoleLabel.setObjectName(u"gRoleLabel")

        self.gL_2.addWidget(self.gRoleLabel, 2, 4, 1, 1)

        self.sizeBox = QComboBox(self.scrollAreaContents)
        self.sizeBox.setObjectName(u"sizeBox")

        self.gL_2.addWidget(self.sizeBox, 7, 3, 1, 1)

        self.classLabel = QLabel(self.scrollAreaContents)
        self.classLabel.setObjectName(u"classLabel")

        self.gL_2.addWidget(self.classLabel, 2, 2, 1, 1)

        self.campaignLabel = QLabel(self.scrollAreaContents)
        self.campaignLabel.setObjectName(u"campaignLabel")

        self.gL_2.addWidget(self.campaignLabel, 1, 2, 1, 1)

        self.categoryLabel = QLabel(self.scrollAreaContents)
        self.categoryLabel.setObjectName(u"categoryLabel")

        self.gL_2.addWidget(self.categoryLabel, 1, 4, 1, 1)

        self.typeLabel = QLabel(self.scrollAreaContents)
        self.typeLabel.setObjectName(u"typeLabel")

        self.gL_2.addWidget(self.typeLabel, 8, 2, 1, 1)

        self.levelCheck = QCheckBox(self.scrollAreaContents)
        self.levelCheck.setObjectName(u"levelCheck")

        self.gL_2.addWidget(self.levelCheck, 10, 2, 1, 1)

        self.usageLabel = QLabel(self.scrollAreaContents)
        self.usageLabel.setObjectName(u"usageLabel")

        self.gL_2.addWidget(self.usageLabel, 8, 4, 1, 1)

        self.alignmentLabel = QLabel(self.scrollAreaContents)
        self.alignmentLabel.setObjectName(u"alignmentLabel")

        self.gL_2.addWidget(self.alignmentLabel, 0, 4, 1, 1)

        self.rarityLabel = QLabel(self.scrollAreaContents)
        self.rarityLabel.setObjectName(u"rarityLabel")

        self.gL_2.addWidget(self.rarityLabel, 4, 2, 1, 1)

        self.kindLabel = QLabel(self.scrollAreaContents)
        self.kindLabel.setObjectName(u"kindLabel")

        self.gL_2.addWidget(self.kindLabel, 3, 2, 1, 1)

        self.gRoleBox = QComboBox(self.scrollAreaContents)
        self.gRoleBox.setObjectName(u"gRoleBox")

        self.gL_2.addWidget(self.gRoleBox, 2, 5, 1, 1)

        self.vSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gL_2.addItem(self.vSpacer, 11, 2, 1, 4)

        self.scrollArea.setWidget(self.scrollAreaContents)

        self.gL_1.addWidget(self.scrollArea, 2, 0, 1, 1)

        self.hL_1 = QHBoxLayout()
        self.hL_1.setObjectName(u"hL_1")
        self.hSpacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hL_1.addItem(self.hSpacer1)

        self.btnReset = QPushButton(ColumnFilter)
        self.btnReset.setObjectName(u"btnReset")

        self.hL_1.addWidget(self.btnReset)

        self.hSpacer2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hL_1.addItem(self.hSpacer2)


        self.gL_1.addLayout(self.hL_1, 0, 0, 1, 1)


        self.retranslateUi(ColumnFilter)

        QMetaObject.connectSlotsByName(ColumnFilter)
    # setupUi

    def retranslateUi(self, ColumnFilter):
        ColumnFilter.setWindowTitle(QCoreApplication.translate("ColumnFilter", u"Form", None))
        self.sizeLabel.setText(QCoreApplication.translate("ColumnFilter", u"Size", None))
        self.roleLabel.setText(QCoreApplication.translate("ColumnFilter", u"Role", None))
        self.tierLabel.setText(QCoreApplication.translate("ColumnFilter", u"Tier", None))
        self.pSourceLabel.setText(QCoreApplication.translate("ColumnFilter", u"Power Source", None))
        self.mundaneLabel.setText(QCoreApplication.translate("ColumnFilter", u"Mundane", None))
        self.actionLabel.setText(QCoreApplication.translate("ColumnFilter", u"Action", None))
        self.costCheck.setText(QCoreApplication.translate("ColumnFilter", u"Cost", None))
        self.costMax.setSuffix("")
        self.gRoleLabel.setText(QCoreApplication.translate("ColumnFilter", u"Group Role", None))
        self.classLabel.setText(QCoreApplication.translate("ColumnFilter", u"Class", None))
        self.campaignLabel.setText(QCoreApplication.translate("ColumnFilter", u"Campaign", None))
        self.categoryLabel.setText(QCoreApplication.translate("ColumnFilter", u"Category", None))
        self.typeLabel.setText(QCoreApplication.translate("ColumnFilter", u"Type", None))
        self.levelCheck.setText(QCoreApplication.translate("ColumnFilter", u"Level", None))
        self.usageLabel.setText(QCoreApplication.translate("ColumnFilter", u"Usage", None))
        self.alignmentLabel.setText(QCoreApplication.translate("ColumnFilter", u"Alignment", None))
        self.rarityLabel.setText(QCoreApplication.translate("ColumnFilter", u"Rarity", None))
        self.kindLabel.setText(QCoreApplication.translate("ColumnFilter", u"Kind", None))
        self.btnReset.setText(QCoreApplication.translate("ColumnFilter", u"Reset Filters", None))
    # retranslateUi

