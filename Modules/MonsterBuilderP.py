from Modules.MonsterBuilder import mp
from yapsy.IPlugin import IPlugin
from PySide6.QtWidgets import QMenuBar, QMenu, QToolBar, QComboBox, QLineEdit
from PySide6.QtCore import Qt

class MonsterBuilder(IPlugin):
	def __init__(self):
		#super().__init__("MonsterB")
		#self.name = mp().name()
		pass

	def getName(self):
		return "MB"

	def drawScreen(self, drawableScreen: any) -> None:
		pass

	def drawMenu(self, drawableMenu: any) -> None:
		if isinstance(drawableMenu, QToolBar):
			ddiMenus = QComboBox()
			drawableMenu.addWidget(ddiMenus)