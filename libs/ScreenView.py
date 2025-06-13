# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ScreenView.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QGridLayout,
	QHBoxLayout, QHeaderView, QSizePolicy, QTableView,
	QWidget)

class Ui_ScreenView(object):
	def setupUi(self, ScreenView):
		if not ScreenView.objectName():
			ScreenView.setObjectName(u"ScreenView")
		ScreenView.resize(506, 300)
		self.hL_1 = QHBoxLayout(ScreenView)
		self.hL_1.setSpacing(0)
		self.hL_1.setObjectName(u"hL_1")
		self.hL_1.setContentsMargins(0, 0, 0, 0)
		self.gL_1 = QGridLayout()
		self.gL_1.setSpacing(0)
		self.gL_1.setObjectName(u"gL_1")
		self.gL_2 = QGridLayout()
		self.gL_2.setObjectName(u"gL_2")

		self.gL_1.addLayout(self.gL_2, 0, 1, 1, 1)

		self.hL_2 = QHBoxLayout()
		self.hL_2.setObjectName(u"hL_2")
		self.ddiTable = QTableView(ScreenView)
		self.ddiTable.setObjectName(u"ddiTable")
		self.ddiTable.setMinimumSize(QSize(500, 0))
		self.ddiTable.setStyleSheet(u"alternate-background-color: rgb(94, 92, 100)")
		self.ddiTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.ddiTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
		self.ddiTable.setSelectionMode(QAbstractItemView.SingleSelection)
		self.ddiTable.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.ddiTable.horizontalHeader().setCascadingSectionResizes(True)
		self.ddiTable.horizontalHeader().setStretchLastSection(True)

		self.hL_2.addWidget(self.ddiTable)


		self.gL_1.addLayout(self.hL_2, 0, 0, 1, 1)


		self.hL_1.addLayout(self.gL_1)


		self.retranslateUi(ScreenView)

		QMetaObject.connectSlotsByName(ScreenView)
	# setupUi

	def retranslateUi(self, ScreenView):
		ScreenView.setWindowTitle(QCoreApplication.translate("ScreenView", u"Form", None))
	# retranslateUi

