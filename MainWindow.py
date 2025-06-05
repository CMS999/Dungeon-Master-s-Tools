# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
	QMetaObject, QObject, QPoint, QRect,
	QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
	QCursor, QFont, QFontDatabase, QGradient,
	QIcon, QImage, QKeySequence, QLinearGradient,
	QPainter, QPalette, QPixmap, QRadialGradient,
	QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
	QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
	QWidget)

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		if not MainWindow.objectName():
			MainWindow.setObjectName(u"MainWindow")
		MainWindow.resize(800, 600)
		self.actionchange = QAction(MainWindow)
		self.actionchange.setObjectName(u"actionchange")
		self.actionTetst = QAction(MainWindow)
		self.actionTetst.setObjectName(u"actionTetst")
		self.centralwidget = QWidget(MainWindow)
		self.centralwidget.setObjectName(u"centralwidget")
		sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
		self.centralwidget.setSizePolicy(sizePolicy)
		self.horizontalLayout_8 = QHBoxLayout(self.centralwidget)
		self.horizontalLayout_8.setSpacing(0)
		self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
		self.horizontalLayout_8.setContentsMargins(2, 0, 2, 0)
		self.Tabs = QTabWidget(self.centralwidget)
		self.Tabs.setObjectName(u"Tabs")

		self.horizontalLayout_8.addWidget(self.Tabs)

		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QMenuBar(MainWindow)
		self.menubar.setObjectName(u"menubar")
		self.menubar.setGeometry(QRect(0, 0, 800, 23))
		self.menuOptions = QMenu(self.menubar)
		self.menuOptions.setObjectName(u"menuOptions")
		self.menuTest = QMenu(self.menubar)
		self.menuTest.setObjectName(u"menuTest")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QStatusBar(MainWindow)
		self.statusbar.setObjectName(u"statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.menubar.addAction(self.menuOptions.menuAction())
		self.menubar.addAction(self.menuTest.menuAction())
		self.menuOptions.addAction(self.actionchange)

		self.retranslateUi(MainWindow)

		self.Tabs.setCurrentIndex(-1)


		QMetaObject.connectSlotsByName(MainWindow)
	# setupUi

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Dungeon Master Tools", None))
		self.actionchange.setText(QCoreApplication.translate("MainWindow", u"change", None))
		self.actionTetst.setText(QCoreApplication.translate("MainWindow", u"Tetst", None))
		self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
		self.menuTest.setTitle(QCoreApplication.translate("MainWindow", u"Test", None))
	# retranslateUi

