from Modules.Compendium.MainScreenView import mainScreen
from Modules.Compendium.MainScreenView import mainScreen
from Modules.Compendium.MainScreenView import mainScreen
from Modules.Compendium.ddiTypes.DDIDataStructures import Types, Categories

import PluginInterface.PluginTypes as Ptypes

from PySide6.QtWidgets import QMenuBar, QMenu, QToolBar, QComboBox, QLineEdit, QWidget
from PySide6.QtCore import Qt


class Compendium(Ptypes.MainPlugin):
	def __init__(self):
		super().__init__("Compendium")
		self.screen : mainScreen = None

	def drawTabOnScreen(self, tab: QWidget) -> bool:
		self.screen = mainScreen()
		self.screen.setupUi(tab)
		return True

	def drawToolBarOnScreen(self, toolBar: QToolBar) -> bool:
		ddiFilter = QComboBox()
		ddiFilter.currentIndexChanged.connect(lambda: self.itemChange(ddiFilter.itemData(ddiFilter.currentIndex(), Qt.ItemDataRole.UserRole)))
		for category in Categories:
			ddiFilter.addItem(category.title, category)
		toolBar.addWidget(ddiFilter)

		searchBox = QLineEdit()
		searchBox.setMinimumSize(150,15)
		searchBox.setMaximumSize(150,35)
		searchBox.textEdited.connect(lambda: self.textSearch(searchBox.text()))
		toolBar.addWidget(searchBox)
		return True

	def itemChange(self, ddiType: Categories) -> None:
		self.screen.changeTable(ddiType)

	def textSearch(self, text: str) -> None:
		self.screen.textChanged(text)