from .Screen import Ui_Screen
from .ddiTypes.Parser import Parser
from .ddiTypes.ddiObjects import ddiObject

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
	QGridLayout, QHBoxLayout, QHeaderView, QSizePolicy,
	QTableWidget, QTableWidgetItem, QWidget)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
	QMetaObject, QObject, QPoint, QRect,
	QSize, QTime, QUrl, Qt, QSortFilterProxyModel)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
	QFont, QFontDatabase, QGradient, QIcon,
	QImage, QKeySequence, QLinearGradient, QPainter,
	QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel)

class ddiWidgetItem(QTableWidgetItem):
	def __init__(self):
		super().__init__()
		self.ddiObject : ddiObject = None

	def setddiObject(self, object: ddiObject):
		self.ddiObject = object

	def getddiObject(self):
		return self.ddiObject


class mainScreen(Ui_Screen):
	def __init__(self):
		super().__init__()
		self.data = {"Power": [], "Monster": [], "Class": []}
		#self.Filter = QSortFilterProxyModel()
		#self.model = MyItemModel(self)

	def setupUi(self, Screen):
		super().setupUi(Screen)
		self.webViewer = QWebEngineView()
		self.webViewer.setObjectName("HTMLRender")
		self.webViewer.setMinimumSize(625, 0)
		self.gL_2.addWidget(self.webViewer)
		#self.ddiTable.itemSelectionChanged.connect(lambda: self.renderHTML())
		#self.populateTable()

	def renderHTML(self):
		self.webViewer.setHtml(self.ddiTable.verticalHeaderItem(self.ddiTable.currentRow()).getddiObject().getHTML())

	def populateTable(self):
		Parser().sqlToPower(self.data)
		count = 0
		for type in self.data:
			for ddiEntry in self.data[type]:
				self.ddiTable.setRowCount(self.ddiTable.rowCount()+1)
				newTableRow = ddiWidgetItem()
				self.ddiTable.setVerticalHeaderItem(count, newTableRow)
				newTableRow.setText(QCoreApplication.translate("Screen", type, None))

				ddiItem = QTableWidgetItem()
				ddiItem.setFlags(ddiItem.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsDropEnabled & ~Qt.ItemFlag.ItemIsDragEnabled & ~Qt.ItemFlag.ItemIsUserCheckable)
				self.ddiTable.setItem(count, 0, ddiItem)
				ddiItem.setText(QCoreApplication.translate("Screen", ddiEntry.getName()))
				newTableRow.setddiObject(ddiEntry)
				newTableRow.setBackground(QColor(ddiEntry.getColor()))
				count+=1

	def changeTable(self, text):
		print(text)
		#self.ddiTable.setModel()
		#print(self.ddiTable.model())
		tera = QSortFilterProxyModel()
		tera.setSourceModel(self.ddiTable.model())
		self.ddiTable.setModel(tera)
		self.ddiTable.setSortingEnabled()


