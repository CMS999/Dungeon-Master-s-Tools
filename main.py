from MainWindow import *
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QApplication, QToolBar
from PySide6.QtCore import Qt

import os
import sys

from yapsy.PluginManager import PluginManager

from libs.PluginTypes import MainPlugin
from libs.DMTCore import CompendiumScreen

class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.toolList : list[QToolBar] = []
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.Compendium = CompendiumScreen()
		self.Compendium.setupUi(self.createTab('Compendium'))
		self.ui.Tabs.currentChanged.connect(self.currentToolBar)
		self.createToolBar('Compendium')
		if len(self.toolList) > 0:
			self.toolList[0].addWidget(self.Compendium.createFilterBox())
			self.toolList[0].addWidget(self.Compendium.createFilterLine())

		if not os.path.isdir('Modules'):
			os.makedirs("Modules")
		self.PluginManager = PluginManager()
		self.loadPlugins()
		self.addPluginsTabs()
		self.addPluginsToolBars()

		if len(self.toolList) > 0:
			self.toolList[0].show()

	def closeEvent(self, event):
		QApplication.closeAllWindows()
		event.accept()

	def createTab(self, tabName:str='NewTab') -> QWidget:
		newTab = QWidget()
		newTab.setObjectName(tabName)
		self.ui.Tabs.addTab(newTab, tabName)
		return newTab

	def createToolBar(self, toolBarName:str='NewToolBar') -> QToolBar:
		newToolBar = QToolBar()
		newToolBar.setObjectName(toolBarName)
		newToolBar.toggleViewAction().setChecked(True)
		newToolBar.hide()
		newToolBar.setMovable(False)
		newToolBar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
		self.addToolBar(newToolBar)
		self.toolList.append(newToolBar)
		return newToolBar

	def currentToolBar(self):
		for index, bar in enumerate(self.toolList):
			self.toolList[index].hide()
		self.toolList[self.ui.Tabs.currentIndex()].show()

	def loadPlugins(self) -> None:
		self.PluginManager.setPluginPlaces([os.getcwd()+"/Modules"])
		self.PluginManager.setCategoriesFilter({
			"Main": MainPlugin
		})
		self.PluginManager.collectPlugins()

	def addPluginsTabs(self) -> None:
		for plugin in self.PluginManager.getPluginsOfCategory("Main"):
			newTab = self.createTab(plugin.plugin_object.getPluginName())
			plugin.plugin_object.drawTabOnScreen(newTab)

	def addPluginsToolBars(self) -> None:
		for plugin in self.PluginManager.getPluginsOfCategory("Main"):
			newToolBar = self.createToolBar(plugin.plugin_object.getPluginName())
			plugin.plugin_object.drawToolBarOnScreen(newToolBar)

if __name__ == "__main__":
	QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)
	app = QApplication([])
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
