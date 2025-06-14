from yapsy.IPlugin import IPlugin
from abc import ABC, abstractmethod

from PySide6.QtWidgets import QToolBar, QWidget

class MainPlugin(IPlugin, ABC):
	def __init__(self, name:str='ScreenPlugin'):
		super().__init__()
		self.name : str = name

	def getPluginName(self) -> str:
		return self.name

	@abstractmethod
	def drawTabOnScreen(self, tab: QWidget) -> bool:
		""" Recives the tab widget so it can add it's on widget, return True if something was made with the tab """
		return False

	@abstractmethod
	def drawToolBarOnScreen(self, toolBar: QToolBar) -> bool:
		""" Recives the toolbar widget so it can add it's on widgets, return True if something was made with the toolBar """
		return False