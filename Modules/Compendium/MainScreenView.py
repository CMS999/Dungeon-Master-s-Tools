from .ScreenView import Ui_ScreenView
from .ddiTypes.Parser import Parser
from .ddiTypes.ddiObjects import ddiObject
from .database.database import pickleJar
from .ddiTypes import Types
from .ddiTypes import Categories
from .ddiTypes.ddiObjects import *
import os
import tempfile
import webbrowser
from .ddiTypes.Images import Base64Images
import re

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget, QItemDelegate, QMenu)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QSortFilterProxyModel, QModelIndex, QItemSelectionModel, Qt, QByteArray)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel, QStandardItem, QCloseEvent)
#from pyside6_utils.models import ExtendedSortFilterProxyModel


class mainScreen(Ui_ScreenView):
    def __init__(self):
        super().__init__()
        self.Jar = pickleJar("database.db")
        self.newWindows : list[QWidget] = []

    
    def setupUi(self, Screen):
        super().setupUi(Screen)
        self.webViewer = QWebEngineView()
        self.webViewer.setObjectName("HTMLRender")
        self.webViewer.setMinimumSize(625, 0)
        self.gL_2.addWidget(self.webViewer)
        self.model : QStandardItemModel = QStandardItemModel()
        self.columnsList = [
            "",
            "Name", 
            "Type",
            "Campaing Setting",
            "Prerequisite(s)",
            "Associated Skills",
            "Role",
            "Power Source",
            "Key Abilities",
            "Level",
            "Main Role",
            "Group Role",
            "XP",
            "Size",
            "Keywords",
            "Alignment",
            "Tier",
            "Category",
            "Mundane",
            "Cost",
            "Rarity",
            "Action",
            "Class",
            "Kind",
            "Usage",
            "Ability Scores",
            "Component Cost",
            "Market Price",
            "Key Skill",
            "Source"
        ]
        self.columnsList = [
            "",
            "Collum1",
            "Collum2",
            "Collum3",
            "Collum4",
            "Collum5",
            "Collum6",
            "Collum7"
        ]
        self.model.setHorizontalHeaderLabels(self.columnsList)
        self.style = '<style type="text/css"> body{ font-size:75%; line-height:1.5em } ol,ul{ list-style:none } blockquote,q{ quotes:none }:focus{ outline:0 } table{ border-collapse:collapse; border-spacing:0 } body,div,p,th,td,li,dd,input,select,textarea{ font-family:Arial, Helvetica, sans-serif; color:#000 } table,thead,tbody,tr,th,td{ font-size:1em } html>body{ font-size:12px } a img{ border-style:none } a:visited{ color:purple } p{ font-size:1em; margin:0 0 1.5em; } p strong,p b{ font-weight:700 } .left{ float:left; margin:0.5em 0.5em 0.5em 0 } .right{ float:right; margin:0.5em 0 0.5em 0.5em } .hidden{ position:absolute; left:-9999em } span.super{ font-size:0.917em; vertical-align:super } span.sub{ font-size:0.917em; vertical-align:sub } h1#WizardsLogo img{ position:absolute; top:5px; left:5px; z-index:3 } h1#WizardsLogo img a{ display:block; width:94px; height:60px } #wrap{ float:left } #container{ position:relative; width:910px; margin:0 auto } #bannerGraphic img{ display:block } .searchControl .textBox{ width:150px } .searchControl .emptyTextBox{ width:150px; font-style:italic } #detail{ background:#fff; float:left; width:560px; color:#000; font-size:8.75pt; padding:15px } #detail p{ padding-left:15px; color:#000; font-size:8.75pt } #detail table{ width:100% } #detail table td{ vertical-align:top; background:#d6d6c2; border-bottom:1px solid #fff; padding:0 10px } #detail p.flavor,#detail span.flavor,#detail ul.flavor{ display:block; background:#d6d6c2; font-size:8.75pt; margin:0; padding:2px 15px } #detail p.powerstat{ background:#FFF; font-size:8.75pt; margin:0; padding:0 0 0 15px } #detail span.ritualstats{ float:right; padding:0 30px 0 0 } #detail p.flavorIndent{ display:block; background:#d6d6c2; margin:0; padding:2px 15px 2px 30px } #detail span.clearIndent{ display:block; background:#FFF; margin:0; padding:2px 15px 2px 30px } #detail p.alt,#detail span.alt,#detail td.alt{ background:#c3c6ad } #detail th{ background:#1d3d5e; color:#fff; text-align:left; padding:0 0 0 5px } #detail ul{ list-style:disc; margin:1em 0 1em 30px } #detail table,#detail ul.flavor{ margin-bottom:1em } #detail ul.flavor li{ list-style-image:url("http://www.wizards.com/dnd/images/symbol/x.gif"); margin-left:15px } #detail blockquote{ background:#d6d6c2; padding:0 0 0 22px } #detail span.block{ display:block; background:#d6d6c2; padding:0 0 0 22px } #detail h1{ font-size:1.09em; line-height:2; padding-left:15px; color:#fff; background:#000; margin:0; float: left; width:545px } #detail h1.player{ background:#1d3d5e; font-size:1.35em } #detail h1.dm{ background:#5c1f34 } #detail h1.trap{ background:#5c1f34; height:38px } #detail h1.atwillpower{ background:#619869 } #detail h1.encounterpower{ background:#961334 } #detail h1.dailypower{ background:#4d4d4f } #detail span.milevel{ font-size:9pt } #detail h1.poison{ background:#000 } #detail h1.poison .level{ padding-right:15px; margin-top:0; text-align:right; float:right; position:relative; top:-24px } #detail h1.utilitypower{ background:#1c3d5f } #detail h1.familiar{ background:#4e5c2e } #detail h1 .level{ padding-right:15px; margin-top:0; text-align:right; float:right } #detail .rightalign{ text-align:right } #detail .traplead{ display:block; background:#fff; margin:0; padding:1px 15px } #detail .trapblocktitle{ display:block; background:#d6d6c2; font-weight:700; margin:0; padding:1px 15px } #detail .trapblockbody{ display:block; background:#fff; margin:0; padding:1px 15px 1px 30px } #detail #RelatedArticles h5{ width:100px; float:left; padding-top:10px; padding-left:20px; color:#3e141e; font-weight:700 } #detail #RelatedArticles ul.RelatedArticles{ float:right; width:430px; list-style:none; margin:0; padding:10px 0 0 } #detail .bodytable{ border:0; width:560px; background:#D1D1BC; margin:0 } #detail .bodytable td{ border-bottom:none; padding-left:15px; padding-right:15px } #detail h2{ font-size:1.25em; padding-left:15px; color:#fff; background:#4e5c2e; height:20px; font-variant:small-caps; padding-top:5px; margin:0 } #detail h1.monster{ background:#4e5c2e; height:38px } #detail h2.monster{ font-size:9pt; padding-left:15px; color:#fff; background:#4e5c2e; height:20px; font-variant:small-caps; padding-top:3px; margin:0 } #detail h3.monster{ font-size:8px; font-weight:700; color:#000; background:#c3c6ad; display:block; margin:0; padding:0 5px 0 10px } #detail p.monster{ background:#CADBB7; font-size:8.75pt; display:block; margin:0; padding:2px 15px } #detail p.monstat{ background:#CADBB7 } #detail p.miflavor{ display:block; background:#EFD09F; font-size:8.75pt; font-style:italic; color:#000; margin:0; padding:2px 15px } #detail table.magicitem{ width:560px; margin-bottom:0 } #detail table.magicitem td{ border:none; font-size:8.75pt; background:#F8E9D5 } #detail td.mic1{ padding-left:20px; padding-right:0; width:50px } #detail td.mic2{ width:40px; padding:0 } #detail td.mic3{ width:100px; text-align:right; padding:0 } #detail td.mic4{ width:100px; padding:0 } #detail h2.magicitem{ background:#EFD09F; color:#000; font-variant:normal; font-size:8.75pt; line-height:18px; padding-top:0; vertical-align:bottom; height:18px } #detail h2.mihead{ display:block; background:#EFD09F; color:#000; font-variant:normal; font-size:8.75pt; line-height:18px; padding-top:0; /* vertical-align:bottom; */ height:18px } #detail p.publishedIn{ font-size:8pt; margin-top:10px } #detail h2.artifactHeading1{ font-size:14pt; padding-left:5px; padding-top:5px; background:#FFF; color:#254950; font-variant:normal; margin:0 } #detail h2.artifactHeading2{ font-size:14pt; padding-left:5px; padding-top:5px; background:#FFF; color:#556C75; font-variant:normal; margin:0 } #detail h2.ah1{ font-size:14pt; padding-left:5px; padding-top:5px; padding-bottom:2px; background:#FFF; color:#254950; font-variant:normal; margin:0 } #detail h2.ah2{ font-size:14pt; padding-left:5px; padding-top:5px; padding-bottom:2px; background:#FFF; color:#556C75; font-variant:normal; margin:0 } #detail h2.ah3{ font-size:12pt; padding-left:5px; padding-top:5px; background:#FFF; color:#556C75; font-variant:normal; margin:0 } #detail p.mistat{ display:block; background:#F8E9D5; font-size:8.75pt; color:#000; margin:0; padding:0 0 0 15px } #detail p.mistatAI{ background:#F8E9D5; font-size:8.75pt; color:#000; height:36px; margin:0; padding:0 0 0 15px } #detail span.miright{ margin-top:0; text-align:right; float:right; position:relative; padding:0 5px 0 0 } #detail p.indent{ text-indent:-15px; padding:0 0 0 30px } #detail p.indent1{ text-indent:-15px; padding:0 0 0 45px } #detail p.indent2{ text-indent:-15px; padding:0 0 0 60px } #detail p.mitext{ background:#FFF; font-size:8.75pt; color:#000; margin:0; padding:0 0 0 5px } #detail ul.mitext{ margin-bottom:1em; display:block; margin-top:0; margin-right:0; background:#FFF; font-size:8.75pt; color:#000; padding:2px 5px } #detail ul.mistat{ background:#F8E9D5; font-size:8.75pt; color:#000; margin:0; padding:2px 5px 2px 30px } #detail h1.miset{ background:#22444B; font-size:12pt; font-weight:700; height:17pt; margin-top:2px; line-height:1.5em } #detail th.miset{ background:#22444B; color:#FFF; text-align:left; padding:0 0 0 5px } #detail h1.thHead{ background:#45133C; height:38px } #detail h1.thHead .thLevel{ margin-top:0; text-align:right; position:relative; top:-60px; padding-right:15px; float:right } #detail h2.thHead{ display:block; background:#65345D; color:#FFF; font-variant:small-caps; font-size:8.75pt; line-height:18px; padding-top:0; /* vertical-align:bottom; */ height:18px } #detail p.thBody{ text-indent:-15px; display:block; background:#E8F2D6; font-size:8.75pt; color:#000; margin:0; padding:0 0 0 30px } #detail p.tbod{ text-indent:-15px; display:block; background:#E8F2D6; font-size:8.75pt; color:#000; margin:0; padding:0 0 0 45px } #detail p.thStat{ display:block; background:#E8F2D6; font-size:8.75pt; color:#000; margin:0; padding:0 0 0 15px } #detail span.thInit{ background:#E8F2D6; font-size:8.75pt; color:#000; position:absolute; left:400px; top:53px } #detail p.th2{ display:block; background:#CADBB7; font-size:8.75pt; color:#000; margin:0; padding:0 0 0 15px } a:link,a:focus,a:hover,a:active{ color:blue } p em,p i,#detail i,#detail em{ font-style:italic } .clear,#MasterMainContent{ clear:both } #detail ul li,#detail a{ color:#3e141e } #detail h1.trap .level,#detail h1.monster .level{ margin-top:0; text-align:right; position:relative; top:-60px } #detail h1.trap .type,#detail h1.trap .xp,#detail h1.monster .type,#detail h1.monster .xp,#detail h1.thHead .thSubHead,#detail h1.thHead .thXP{ display:block; position:relative; z-index:99; top:-0.75em; height:1em; font-weight:400; font-size:0.917em } #detail h1.magicitem,#detail h1.mihead{ background:#DA9722; font-size:12pt; font-weight:700; height:17pt; margin-top:2px; line-height:1.5em } #detail h1.magicitem .milevel,#detail h1.mihead .milevel,#detail h1.miset .milevel{ padding-right:15px; margin-top:0; text-align:right; float:right; position:relative } #detail ul.mitext li,#detail ul.mistat li{ list-style-image:url("http://www.wizards.com/dnd/images/symbol/x.gif"); color:#000 } </style>'
        self.head = '<!DOCTYPE HTML><html><head><title>D&D Compendium</title><meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=EmulateIE7, IE=9\"><style type=\"text/css\">body{font-size:75%;line-height:1.5em}ol,ul{list-style:none}blockquote,q{quotes:none}:focus{outline:0}table{border-collapse:collapse;border-spacing:0}body,div,p,th,td,li,dd,input,select,textarea{font-family:Arial, Helvetica, sans-serif;color:#000}table,thead,tbody,tr,th,td{font-size:1em}html>body{font-size:12px}a img{border-style:none}a:visited{color:purple}p{font-size:1em;margin:0 0 1.5em}p strong,p b{font-weight:700}.left{float:left;margin:0.5em 0.5em 0.5em 0}.right{float:right;margin:0.5em 0 0.5em 0.5em}.hidden{position:absolute;left:-9999em}span.super{font-size:0.917em;vertical-align:super}span.sub{font-size:0.917em;vertical-align:sub}h1#WizardsLogo img{position:absolute;top:5px;left:5px;z-index:3}h1#WizardsLogo img a{display:block;width:94px;height:60px}#wrap{float:left}#container{position:relative;width:910px;margin:0 auto}#bannerGraphic img{display:block}.searchControl .textBox{width:150px}.searchControl .emptyTextBox{width:150px;font-style:italic}#detail{background:#fff;float:left;width:560px;color:#000;font-size:8.75pt;padding:15px}#detail p{padding-left:15px;color:#000;font-size:8.75pt}#detail table{width:100%}#detail table td{vertical-align:top;background:#d6d6c2;border-bottom:1px solid #fff;padding:0 10px}#detail p.flavor,#detail span.flavor,#detail ul.flavor{display:block;background:#d6d6c2;font-size:8.75pt;margin:0;padding:2px 15px}#detail p.powerstat{background:#FFF;font-size:8.75pt;margin:0;padding:0 0 0 15px}#detail span.ritualstats{float:right;padding:0 30px 0 0}#detail p.flavorIndent{display:block;background:#d6d6c2;margin:0;padding:2px 15px 2px 30px}#detail span.clearIndent{display:block;background:#FFF;margin:0;padding:2px 15px 2px 30px}#detail p.alt,#detail span.alt,#detail td.alt{background:#c3c6ad}#detail th{background:#1d3d5e;color:#fff;text-align:left;padding:0 0 0 5px}#detail ul{list-style:disc;margin:1em 0 1em 30px}#detail table,#detail ul.flavor{margin-bottom:1em}#detail ul.flavor li{list-style-image:url(\"http://www.wizards.com/dnd/images/symbol/x.gif\");margin-left:15px}#detail blockquote{background:#d6d6c2;padding:0 0 0 22px}#detail span.block{display:block;background:#d6d6c2;padding:0 0 0 22px}#detail h1{font-size:1.09em;line-height:2;padding-left:15px;color:#fff;background:#000;margin:0}#detail h1.player{background:#1d3d5e;font-size:1.35em}#detail h1.dm{background:#5c1f34}#detail h1.trap{background:#5c1f34;height:38px}#detail h1.atwillpower{background:#619869}#detail h1.encounterpower{background:#961334}#detail h1.dailypower{background:#4d4d4f}#detail span.milevel{font-size:9pt}#detail h1.poison{background:#000}#detail h1.poison .level{padding-right:15px;margin-top:0;text-align:right;float:right;position:relative;top:-24px}#detail h1.utilitypower{background:#1c3d5f}#detail h1.familiar{background:#4e5c2e}#detail h1 .level{padding-right:15px;margin-top:0;text-align:right;float:right}#detail .rightalign{text-align:right}#detail .traplead{display:block;background:#fff;margin:0;padding:1px 15px}#detail .trapblocktitle{display:block;background:#d6d6c2;font-weight:700;margin:0;padding:1px 15px}#detail .trapblockbody{display:block;background:#fff;margin:0;padding:1px 15px 1px 30px}#detail #RelatedArticles h5{width:100px;float:left;padding-top:10px;padding-left:20px;color:#3e141e;font-weight:700}#detail #RelatedArticles ul.RelatedArticles{float:right;width:430px;list-style:none;margin:0;padding:10px 0 0}#detail .bodytable{border:0;width:560px;background:#D1D1BC;margin:0}#detail .bodytable td{border-bottom:none;padding-left:15px;padding-right:15px}#detail h2{font-size:1.25em;padding-left:15px;color:#fff;background:#4e5c2e;height:20px;font-variant:small-caps;padding-top:5px;margin:0}#detail h1.monster{background:#4e5c2e;height:38px}#detail h2.monster{font-size:9pt;padding-left:15px;color:#fff;background:#4e5c2e;height:20px;font-variant:small-caps;padding-top:3px;margin:0}#detail h3.monster{font-size:8px;font-weight:700;color:#000;background:#c3c6ad;display:block;margin:0;padding:0 5px 0 10px}#detail p.monster{background:#CADBB7;font-size:8.75pt;display:block;margin:0;padding:2px 15px}#detail p.monstat{background:#CADBB7}#detail p.miflavor{display:block;background:#EFD09F;font-size:8.75pt;font-style:italic;color:#000;margin:0;padding:2px 15px}#detail table.magicitem{width:560px;margin-bottom:0}#detail table.magicitem td{border:none;font-size:8.75pt;background:#F8E9D5}#detail td.mic1{padding-left:20px;padding-right:0;width:50px}#detail td.mic2{width:40px;padding:0}#detail td.mic3{width:100px;text-align:right;padding:0}#detail td.mic4{width:100px;padding:0}#detail h2.magicitem{background:#EFD09F;color:#000;font-variant:normal;font-size:8.75pt;line-height:18px;padding-top:0;vertical-align:bottom;height:18px}#detail h2.mihead{display:block;background:#EFD09F;color:#000;font-variant:normal;font-size:8.75pt;line-height:18px;padding-top:0;vertical-align:bottom;height:18px}#detail p.publishedIn{font-size:8pt;margin-top:10px}#detail h2.artifactHeading1{font-size:14pt;padding-left:5px;padding-top:5px;background:#FFF;color:#254950;font-variant:normal;margin:0}#detail h2.artifactHeading2{font-size:14pt;padding-left:5px;padding-top:5px;background:#FFF;color:#556C75;font-variant:normal;margin:0}#detail h2.ah1{font-size:14pt;padding-left:5px;padding-top:5px;padding-bottom:2px;background:#FFF;color:#254950;font-variant:normal;margin:0}#detail h2.ah2{font-size:14pt;padding-left:5px;padding-top:5px;padding-bottom:2px;background:#FFF;color:#556C75;font-variant:normal;margin:0}#detail h2.ah3{font-size:12pt;padding-left:5px;padding-top:5px;background:#FFF;color:#556C75;font-variant:normal;margin:0}#detail p.mistat{display:block;background:#F8E9D5;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 15px}#detail p.mistatAI{background:#F8E9D5;font-size:8.75pt;color:#000;height:36px;margin:0;padding:0 0 0 15px}#detail span.miright{margin-top:0;text-align:right;float:right;position:relative;padding:0 5px 0 0}#detail p.indent{text-indent:-15px;padding:0 0 0 30px}#detail p.indent1{text-indent:-15px;padding:0 0 0 45px}#detail p.indent2{text-indent:-15px;padding:0 0 0 60px}#detail p.mitext{background:#FFF;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 5px}#detail ul.mitext{margin-bottom:1em;display:block;margin-top:0;margin-right:0;background:#FFF;font-size:8.75pt;color:#000;padding:2px 5px}#detail ul.mistat{background:#F8E9D5;font-size:8.75pt;color:#000;margin:0;padding:2px 5px 2px 30px}#detail h1.miset{background:#22444B;font-size:12pt;font-weight:700;height:17pt;margin-top:2px;line-height:1.5em}#detail th.miset{background:#22444B;color:#FFF;text-align:left;padding:0 0 0 5px}#detail h1.thHead{background:#45133C;height:38px}#detail h1.thHead .thLevel{margin-top:0;text-align:right;position:relative;top:-60px;padding-right:15px;float:right}#detail h2.thHead{display:block;background:#65345D;color:#FFF;font-variant:small-caps;font-size:8.75pt;line-height:18px;padding-top:0;vertical-align:bottom;height:18px}#detail p.thBody{text-indent:-15px;display:block;background:#E8F2D6;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 30px}#detail p.tbod{text-indent:-15px;display:block;background:#E8F2D6;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 45px}#detail p.thStat{display:block;background:#E8F2D6;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 15px}#detail span.thInit{background:#E8F2D6;font-size:8.75pt;color:#000;position:absolute;left:400px;top:53px}#detail p.th2{display:block;background:#CADBB7;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 15px}a:link,a:focus,a:hover,a:active{color:blue}p em,p i,#detail i,#detail em{font-style:italic}.clear,#MasterMainContent{clear:both}#detail ul li,#detail a{color:#3e141e}#detail h1.trap .level,#detail h1.monster .level{margin-top:0;text-align:right;position:relative;top:-60px}#detail h1.trap .type,#detail h1.trap .xp,#detail h1.monster .type,#detail h1.monster .xp,#detail h1.thHead .thSubHead,#detail h1.thHead .thXP{display:block;position:relative;z-index:99;top:-0.75em;height:1em;font-weight:400;font-size:0.917em}#detail h1.magicitem,#detail h1.mihead{background:#DA9722;font-size:12pt;font-weight:700;height:17pt;margin-top:2px;line-height:1.5em}#detail h1.magicitem .milevel,#detail h1.mihead .milevel,#detail h1.miset .milevel{padding-right:15px;margin-top:0;text-align:right;float:right;position:relative}#detail ul.mitext li,#detail ul.mistat li{list-style-image:url(\\"http://www.wizards.com/dnd/images/symbol/x.gif\\");color:#000}</style></head>'

        self.populateTable()
        
        self.cMenu = QMenu("itemOptions")
        #self.createContextMenu()
        self.ddiTable.setModel(self.model)
        self.searchModel : QStandardItemModel = self.model
        self.ddiTable.horizontalHeader().setSortIndicatorClearable(True)
        self.ddiTable.horizontalHeader().setSortIndicatorShown(True)
        self.ddiTable.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

        self.ddiTable.verticalHeader().setDefaultSectionSize(5)
        self.ddiTable.verticalHeader().resizeSections(QHeaderView.ResizeMode.Fixed)
        self.ddiTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.ddiTable.setAlternatingRowColors(True)
        
        self.ddiTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ddiTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        #self.ddiTable.contex
        #self.model.setSortRole(Qt.ItemDataRole.InitialSortOrderRole)
        #self.model.setSortRole(Qt.ItemDataRole.DisplayRole)
        #self.model.invalidate()
        self.ddiTable.horizontalHeader().setSortIndicatorClearable(True)
        self.ddiTable.setSortingEnabled(True)
        self.ddiTable.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.ddiTable.verticalHeader().hide()
        self.ddiTable.customContextMenuRequested.connect(self.on_context_menu)

    def createContextMenu(self, itemData: dict, index: QModelIndex) -> QMenu:
        cMenu = QMenu()
        action1 = cMenu.addAction("Open in new window")
        action2 = cMenu.addAction("Open in default Browser")
        cMenu.addSeparator()
        action3 = cMenu.addAction("Pin")
        action4 = cMenu.addAction("Unpin")
        cMenu.addSeparator()
        action5 = cMenu.addAction("Bookmark")
        action6 = cMenu.addAction("Remove Bookmark")

        action1.triggered.connect(lambda: self.actionOpenInWindow(itemData))
        action2.triggered.connect(lambda: self.actionOpenInBrowser(itemData))
        action3.triggered.connect(lambda: self.actionPin(index))
        action4.triggered.connect(lambda: self.actionUnpin(index))
        action5.triggered.connect(self.actionBookmark)
        action6.triggered.connect(self.actionRemoveBookmark)
        return cMenu    

    def formatHTML(self, html: str) -> str:
        for image, base64 in Base64Images().getDICT().items():
            html = html.replace(image, base64)
        return self.head + html

    def actionOpenInWindow(self, itemData: dict) -> None:
        newWindow = QWidget()
        newWindow.resize(625,500)
        newWindow.setWindowTitle(itemData[0])
        lay = QHBoxLayout()
        htmlRender = QWebEngineView()
        htmlRender.setMinimumSize(625,0)
        htmlRender.setHtml(self.formatHTML(itemData[32]))
        lay.addWidget(htmlRender)
        newWindow.setLayout(lay)
        self.newWindows.append(newWindow)
        newWindow.show()

    def actionOpenInBrowser(self, itemData: dict) -> None:
        tempFile = tempfile.NamedTemporaryFile(delete=False)
        path = tempFile.name+'.html'
        browerFile = open(path, 'w')
        browerFile.write(self.formatHTML(itemData[32]))
        browerFile.close()
        webbrowser.open('file://' + path)

    def actionPin(self, index: QModelIndex) -> None:
        t = QPixmap()
        t.loadFromData(QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAArxJREFUWIXtlktsjFEUx3/3mD5U7TRCCEnrOSUSjXZKpzOlNBWxssBCY9MFIZEQLGwkCLESCZaVWIiIVDRB+tTqDBmpMl+FpEiwIQTxaqf3WJhOKp0xD+0sxH/33XvO+f1yv3y5H/zPv5r26nn5CiZZXdyC9vJF841xNaLUqdiFiuQLvFe1DxBzhZwvF/2dL7+P7WmpK8kr+Ji7A3QrVsoQCrE2AvIE4XpEXWfXBR6+TirQUeE+oIajBnITWavaQVW21QQHggCdFUtXqeolRIoT9mC/ouagP+CcSSjQ4XEfAw4lGjI2Fv1mrKkHUNEWwUxNpQ847usNHx4n0Fa5ZLOoXEtxyC8Jy2cBg1CYTh9WN/uCTjOAAFzesmUKKqfSGgKIMD1tOICY0xplC8DMV+FqgQVpD8o8JZ2V7uqYgCr+LMKJMn8TmJ1tAazOjQlgTCTrAmKGYwLG6GC2+QZ9FhNQw81sC4iV2zEB/12nD+jOHt72eIOP+2MC0exTGJp8to1Y69o7+hgT8PWG74vqnkkXELOrJvgoNE4AoDrgnFf0yGSxFT3k63UujF2Lex13eJaeBLN/guknfIHwuIsu4Q9Du8d9zkDjhLCVs/5AeHe8vYQCCtLhcTcZ2P5XcLTJ1+s0GNB4+xJvMWpmyZ3RoNCcOdxefTvHvTMRPMr5c1rqSvIKPuTdQFibFlztraJPZlOp4/zx004qAHBz+fJpOVMjt0WMJzW87SkcKlhfFgp9TVaZ8BWMzYb+/i8mP6ceS1+yWoUHw0MFG1OBQ4onMJquNSuK7PCPLkQWx9u32AEzNOL1h56+S3VmSicwGm9331tVVy3wYjxcn1vNrU0HDmmewGhaK93FxnJHDLMA1PLGlSNVVd2P0r7WMxIAaF29xD3FSieAjKjXe89xMp2VcdorS8vaypetzDp4IvMTCqn5D13V18YAAAAASUVORK5CYII="))
        self.ddiTable.model().setData(index, QIcon(t), 1)
        self.ddiTable.model().setData(index, True, 34)
        pass

    def actionUnpin(self, index: QModelIndex) -> None:
        self.ddiTable.model().setData(index, None, 1)
        self.ddiTable.model().setData(index, False, 34)
        pass

    def actionBookmark(self) -> None:
        pass

    def actionRemoveBookmark(self) -> None:
        pass

    def on_context_menu(self, pos: QPoint):
        index = self.ddiTable.indexAt(pos)
        if index.isValid():
            itemData = self.ddiTable.model().itemData(self.ddiTable.model().index(index.row(), 0))
            cMenu = self.createContextMenu(itemData, self.ddiTable.model().index(index.row(), 0))
            cMenu.exec_(self.ddiTable.viewport().mapToGlobal(pos))

    def saveData(self, data: dict) -> None:
        self.Jar.putInJar(data)

    def loadData(self) -> dict:
        return self.Jar.popFromJar().pop()

    def renderHTML(self) -> None:
        html: str = self.ddiTable.model().index(self.ddiTable.currentIndex().row(), 0).data(32)        
        self.webViewer.setHtml(self.formatHTML(html))

    def createRow(self, index: int, ddiObject: ddiObject) -> None:
        newRow = QStandardItem(ddiObject.getType().category.value)
        newRow.setBackground(QColor(ddiObject.getColor()))
        newRow.setData(ddiObject.getHTML(), 32)
        newRow.setData(ddiObject.getType().category.value, 33)
        newRow.setData(False, 34)
        self.model.appendRow(newRow)
        #self.model.setVerticalHeaderItem(index, newRow)
    
    def populateRow(self, index: int, ddiObject: ddiObject) -> None:
        newItem = QStandardItem(ddiObject.getName())
        self.model.setItem(index, self.columnsList.index("Name"), newItem)

        match ddiObject:
            case Associate():
                self.model.setItem(index, self.columnsList.index("Type"), QStandardItem(ddiObject.getTypeA()))
            case Background():
                self.model.setItem(index, self.columnsList.index("Type"), QStandardItem(ddiObject.getTypeB()))
                self.model.setItem(index, self.columnsList.index("Campaing Setting"), QStandardItem(ddiObject.getCampaign()))
                self.model.setItem(index, self.columnsList.index("Prerequisite(s)"), QStandardItem(ddiObject.getPrerequisite()))
                self.model.setItem(index, self.columnsList.index("Associated Skills"), QStandardItem(ddiObject.getSkills()))
            case Classe():
                self.model.setItem(index, self.columnsList.index("Role"), QStandardItem(ddiObject.getRole()))
                self.model.setItem(index, self.columnsList.index("Power Source"), QStandardItem(ddiObject.getPower()))
                self.model.setItem(index, self.columnsList.index("Key Abilities"), QStandardItem(ddiObject.getAbilities()))
            case Companion():
                self.model.setItem(index, self.columnsList.index("Type"), QStandardItem(ddiObject.getTypeC()))
            case Deity():
                self.model.setItem(index, self.columnsList.index("Alignment"), QStandardItem(ddiObject.getAlignment()))
            case Disease():
                self.model.setItem(index, self.columnsList.index("Level"), QStandardItem(str(ddiObject.getLevel())))
            case EpicDestiny():
                self.model.setItem(index, self.columnsList.index("Prerequisite(s)"), QStandardItem(ddiObject.getPrerequisite()))
            case Feat():
                self.model.setItem(index, self.columnsList.index("Prerequisite(s)"), QStandardItem(ddiObject.getPrerequisite()))
                self.model.setItem(index, self.columnsList.index("Tier"), QStandardItem(ddiObject.getTier()))
            case Glossary():
                self.model.setItem(index, self.columnsList.index("Type"), QStandardItem(ddiObject.getTypeG()))
                self.model.setItem(index, self.columnsList.index("Category"), QStandardItem(ddiObject.getCategory()))
            case Item():
                self.model.setItem(index, self.columnsList.index("Level"), QStandardItem(ddiObject.getLevel()))
                self.model.setItem(index, self.columnsList.index("Category"), QStandardItem(ddiObject.getCategory()))
                if ddiObject.getIsMundane():
                    self.model.setItem(index, self.columnsList.index("Mundane"), QStandardItem("Yes"))
                else:
                    self.model.setItem(index, self.columnsList.index("Mundane"), QStandardItem("No"))
                self.model.setItem(index, self.columnsList.index("Cost"), QStandardItem(ddiObject.getCost()))
                self.model.setItem(index, self.columnsList.index("Rarity"), QStandardItem(ddiObject.getRarity()))
            case Monster():
                self.model.setItem(index, self.columnsList.index("Level"), QStandardItem(str(ddiObject.getLevel())))
                self.model.setItem(index, self.columnsList.index("Main Role"), QStandardItem(ddiObject.getModifier()))
                self.model.setItem(index, self.columnsList.index("Group Role"), QStandardItem(ddiObject.getRole()))
                self.model.setItem(index, self.columnsList.index("XP"), QStandardItem(str(ddiObject.getXP())))
                self.model.setItem(index, self.columnsList.index("Size"), QStandardItem(ddiObject.getSize()))
                self.model.setItem(index, self.columnsList.index("Keywords"), QStandardItem(ddiObject.getKeywords()))
            case ParagonPath():
                self.model.setItem(index, self.columnsList.index("Prerequisite(s)"), QStandardItem(ddiObject.getPrerequisite()))
            case Poison():
                self.model.setItem(index, self.columnsList.index("Level"), QStandardItem(str(ddiObject.getLevel())))
                self.model.setItem(index, self.columnsList.index("Cost"), QStandardItem(str(ddiObject.getCost())+" gp"))
            case Power():
                self.model.setItem(index, self.columnsList.index("Level"), QStandardItem(str(ddiObject.getLevel())))
                self.model.setItem(index, self.columnsList.index("Action"), QStandardItem(ddiObject.getAction()))
                self.model.setItem(index, self.columnsList.index("Class"), QStandardItem(ddiObject.getClass()))
                self.model.setItem(index, self.columnsList.index("Kind"), QStandardItem(ddiObject.getKind()))
                self.model.setItem(index, self.columnsList.index("Usage"), QStandardItem(ddiObject.getUsage()))
            case Race():
                self.model.setItem(index, self.columnsList.index("Size"), QStandardItem(ddiObject.getSize()))
                self.model.setItem(index, self.columnsList.index("Ability Scores"), QStandardItem(ddiObject.getDescription()))
            case Ritual():
                self.model.setItem(index, self.columnsList.index("Level"), QStandardItem(str(ddiObject.getLevel())))
                self.model.setItem(index, self.columnsList.index("Component Cost"), QStandardItem(ddiObject.getComponent()))
                self.model.setItem(index, self.columnsList.index("Market Price"), QStandardItem(str(ddiObject.getPrice())))
                self.model.setItem(index, self.columnsList.index("Key Skill"), QStandardItem(ddiObject.getKeySkill()))
            case Skill():
                self.model.setItem(index, self.columnsList.index("Type"), QStandardItem(ddiObject.getTypeS()))
                self.model.setItem(index, self.columnsList.index("Category"), QStandardItem(ddiObject.getCategory()))
            case Terrain():
                self.model.setItem(index, self.columnsList.index("Type"), QStandardItem(ddiObject.getTypeT()))
            case Theme():
                self.model.setItem(index, self.columnsList.index("Prerequisite(s)"), QStandardItem(ddiObject.getPrerequisite()))
                pass
            case Trap():
                self.model.setItem(index, self.columnsList.index("Type"), QStandardItem(ddiObject.getTypeT()))
                self.model.setItem(index, self.columnsList.index("Role"), QStandardItem(ddiObject.getRole()))
                if ddiObject.getLevel().isnumeric():    
                    self.model.setItem(index, self.columnsList.index("Level"), QStandardItem(ddiObject.getLevel()))
                else:
                    self.model.setItem(index, self.columnsList.index("Level"), QStandardItem("*"))
                
                if ddiObject.getXP() != -1:
                    self.model.setItem(index, self.columnsList.index("XP"), QStandardItem(str(ddiObject.getXP())))
                else:
                    self.model.setItem(index, self.columnsList.index("XP"), QStandardItem("*"))
                self.model.setItem(index, self.columnsList.index("Class"), QStandardItem(ddiObject.getClasse()))
            
        
        self.model.setItem(index, self.columnsList.index("Source"), QStandardItem(ddiObject.getSource()))
    
    
    def populateTable(self) -> None: 
        data = {
            "Associate": [], 
            "Background": [], 
            "Class": [], 
            "Companion": [], 
            "Deity": [], 
            "Disease": [], 
            "Epic Destiny": [], 
            "Feat": [], 
            "Glossary": [], 
            "Item": [], 
            "Monster": [], 
            "Paragon Path": [], 
            "Poison": [], 
            "Power": [], 
            "Race": [], 
            "Ritual": [], 
            "Skill": [], 
            "Terrain": [], 
            "Theme": [], 
            "Trap": []
        }
        if not os.path.isfile("pickles/database.db"):
            Parser().buildDDIObjects(data)
            self.saveData(data)
        data = self.loadData()
        index = 0
        for type in data:
            ddiEntry : ddiObject
            for ddiEntry in data[type]:
                self.createRow(index, ddiEntry)
                self.populateRow(index, ddiEntry)
                index += 1

    def textChanged(self, text: str) -> None:
        proxyFilter = PinableBookmarkbleFilterProxy()
        proxyFilter.setSourceModel(self.searchModel)
        proxyFilter.setFilterKeyColumn(1)
        proxyFilter.setFilterRole(0)
        proxyFilter.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        proxyFilter.setFilterRegularExpression(text)
        self.ddiTable.setModel(proxyFilter)
        self.ddiTable.selectionModel().selectionChanged.connect(self.renderHTML)

    def changeTable(self, category: Categories) -> None:
        if category is Categories.ALL:
            self.ddiTable.setModel(self.model)
            self.searchModel = self.model
        else:
            proxyFilter = PinableBookmarkbleFilterProxy()
            proxyFilter.setSourceModel(self.model)
            proxyFilter.setFilterRole(33)
            proxyFilter.setFilterRegularExpression(category.value)
            proxyFilter.filterAcceptsRow
            self.searchModel = proxyFilter
            self.ddiTable.setModel(proxyFilter)
        
        """ for headerItem in range(self.model.columnCount()):
            self.ddiTable.hideColumn(headerItem)
            if self.model.horizontalHeaderItem(headerItem).text() in category.metaData:
                self.ddiTable.showColumn(headerItem) """
        for headerItem in range(self.model.columnCount()):
            self.ddiTable.hideColumn(headerItem)
        for headerItem, columnName in enumerate(category.metaData):
            self.ddiTable.showColumn(headerItem)
            self.model.horizontalHeaderItem(headerItem).setText(columnName)

        self.ddiTable.selectionModel().selectionChanged.connect(self.renderHTML)

class PinableBookmarkbleFilterProxy(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        isRowPinned : bool = False
        index : QModelIndex = self.sourceModel().index(source_row, 0, source_parent)
        try:
            isRowPinned : bool = self.sourceModel().data(index, 34)
        except ValueError:
            isRowPinned = False
        return super().filterAcceptsRow(source_row, source_parent) or isRowPinned