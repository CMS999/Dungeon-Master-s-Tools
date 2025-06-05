import sys
import os
from MainWindow import *
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow, QApplication, QGridLayout
from PySide6.QtWidgets import QComboBox, QToolBar

from PluginInterface.PluginTypes import MainPlugin
from yapsy.PluginManager import PluginManager

class MainWindow(QMainWindow):
    def closeEvent(self, event):
        QApplication.closeAllWindows()
        event.accept()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.toolList : list[QToolBar] = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.PluginManager = PluginManager()
        self.loadPlugins()
        self.createTabs()
        self.addToolBars()
    
    def loadPlugins(self) -> None:
        self.PluginManager.setPluginPlaces([os.getcwd()+"/Modules"])
        self.PluginManager.setCategoriesFilter({
            "Main": MainPlugin
        })
        self.PluginManager.collectPlugins()

    def createTabs(self) -> None:
        for plugin in self.PluginManager.getPluginsOfCategory("Main"):
            newTab = QWidget()
            newTab.setObjectName(plugin.plugin_object.getPluginName())
            plugin.plugin_object.drawTabOnScreen(newTab)
            self.ui.Tabs.addTab(newTab, plugin.plugin_object.getPluginName())

    def addToolBars(self) -> None:
        self.ui.Tabs.currentChanged.connect(self.currentToolBar)
        for plugin in self.PluginManager.getPluginsOfCategory("Main"):
            newToolBar = QToolBar()
            newToolBar.toggleViewAction().setChecked(True)
            newToolBar.hide()
            plugin.plugin_object.drawToolBarOnScreen(newToolBar)
            newToolBar.setMovable(False)
            self.addToolBar(newToolBar)
            self.toolList.append(newToolBar)
        
        if len(self.toolList) > 0:
            self.toolList[0].show()

    def currentToolBar(self):
        for index, bar in enumerate(self.toolList):
            self.toolList[index].hide()
        self.toolList[self.ui.Tabs.currentIndex()].show()
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
