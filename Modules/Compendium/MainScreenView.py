from .ScreenView import Ui_ScreenView
from .ddiTypes.Parser import Parser
from .database.database import pickleJar
from .ddiTypes.DDIDataStructures import *
from abc import ABC, abstractmethod

from enum import IntEnum

import os
import tempfile
import webbrowser

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
	QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel, QStandardItem, QCloseEvent, QAction)
	
class DDITableItemRole(IntEnum):
	Data = 32
	Category = 33
	Pinned = 34

class PinableBookmarkbleFilterProxy(QSortFilterProxyModel):
	def filterAcceptsRow(self, source_row, source_parent):
		isRowPinned : bool = False
		index : QModelIndex = self.sourceModel().index(source_row, 0, source_parent)
		try:
			isRowPinned = self.sourceModel().data(index, DDITableItemRole.Pinned)
		except ValueError:
			isRowPinned = False
		return super().filterAcceptsRow(source_row, source_parent) or isRowPinned

class Base64Icons():
	def PinIcon(self) -> str:
		return "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAArxJREFUWIXtlktsjFEUx3/3mD5U7TRCCEnrOSUSjXZKpzOlNBWxssBCY9MFIZEQLGwkCLESCZaVWIiIVDRB+tTqDBmpMl+FpEiwIQTxaqf3WJhOKp0xD+0sxH/33XvO+f1yv3y5H/zPv5r26nn5CiZZXdyC9vJF841xNaLUqdiFiuQLvFe1DxBzhZwvF/2dL7+P7WmpK8kr+Ji7A3QrVsoQCrE2AvIE4XpEXWfXBR6+TirQUeE+oIajBnITWavaQVW21QQHggCdFUtXqeolRIoT9mC/ouagP+CcSSjQ4XEfAw4lGjI2Fv1mrKkHUNEWwUxNpQ847usNHx4n0Fa5ZLOoXEtxyC8Jy2cBg1CYTh9WN/uCTjOAAFzesmUKKqfSGgKIMD1tOICY0xplC8DMV+FqgQVpD8o8JZ2V7uqYgCr+LMKJMn8TmJ1tAazOjQlgTCTrAmKGYwLG6GC2+QZ9FhNQw81sC4iV2zEB/12nD+jOHt72eIOP+2MC0exTGJp8to1Y69o7+hgT8PWG74vqnkkXELOrJvgoNE4AoDrgnFf0yGSxFT3k63UujF2Lex13eJaeBLN/guknfIHwuIsu4Q9Du8d9zkDjhLCVs/5AeHe8vYQCCtLhcTcZ2P5XcLTJ1+s0GNB4+xJvMWpmyZ3RoNCcOdxefTvHvTMRPMr5c1rqSvIKPuTdQFibFlztraJPZlOp4/zx004qAHBz+fJpOVMjt0WMJzW87SkcKlhfFgp9TVaZ8BWMzYb+/i8mP6ceS1+yWoUHw0MFG1OBQ4onMJquNSuK7PCPLkQWx9u32AEzNOL1h56+S3VmSicwGm9331tVVy3wYjxcn1vNrU0HDmmewGhaK93FxnJHDLMA1PLGlSNVVd2P0r7WMxIAaF29xD3FSieAjKjXe89xMp2VcdorS8vaypetzDp4IvMTCqn5D13V18YAAAAASUVORK5CYII="

class HTMLRenderer(QWebEngineView):
	def __init__(self):
		super().__init__()
		self.setObjectName("HTMLRender")
		self.setMinimumSize(625, 0)
		self.head = self.__buildHTMLHead()
		
	def __buildHTMLHead(self) -> str:
		headText : str = ''
		headText += '<!DOCTYPE HTML>'
		headText += '<html>'
		headText += '<head>'
		headText += '<title>D&D Compendium</title>'
		headText += '<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">'
		headText += '<meta http-equiv=\"X-UA-Compatible\" content=\"IE=EmulateIE7, IE=9\">'
		headText += '<style type=\"text/css\">'
		headText += 'body{font-size:75%;line-height:1.5em}'
		headText += 'ol,ul{list-style:none}'
		headText += 'blockquote,q{quotes:none}:focus{outline:0}table{border-collapse:collapse;border-spacing:0}'
		headText += 'body,div,p,th,td,li,dd,input,select,textarea{font-family:Arial, Helvetica, sans-serif;color:#000}'
		headText += 'table,thead,tbody,tr,th,td{font-size:1em}html>body{font-size:12px}'
		headText += 'a img{border-style:none}a:visited{color:purple}'
		headText += 'p{font-size:1em;margin:0 0 1.5em}'
		headText += 'p strong,p b{font-weight:700}'
		headText += '.left{float:left;margin:0.5em 0.5em 0.5em 0}'
		headText += '.right{float:right;margin:0.5em 0 0.5em 0.5em}'
		headText += '.hidden{position:absolute;left:-9999em}'
		headText += 'span.super{font-size:0.917em;vertical-align:super}'
		headText += 'span.sub{font-size:0.917em;vertical-align:sub}'
		headText += 'h1#WizardsLogo img{position:absolute;top:5px;left:5px;z-index:3}'
		headText += 'h1#WizardsLogo img a{display:block;width:94px;height:60px}'
		headText += '#wrap{float:left}'
		headText += '#container{position:relative;width:910px;margin:0 auto}'
		headText += '#bannerGraphic img{display:block}'
		headText += '.searchControl .textBox{width:150px}'
		headText += '.searchControl .emptyTextBox{width:150px;font-style:italic}'
		headText += '#detail{background:#fff;float:left;width:560px;color:#000;font-size:8.75pt;padding:15px}'
		headText += '#detail p{padding-left:15px;color:#000;font-size:8.75pt}'
		headText += '#detail table{width:100%}'
		headText += '#detail table td{vertical-align:top;background:#d6d6c2;border-bottom:1px solid #fff;padding:0 10px}'
		headText += '#detail p.flavor,#detail span.flavor,#detail ul.flavor{display:block;background:#d6d6c2;font-size:8.75pt;margin:0;padding:2px 15px}'
		headText += '#detail p.powerstat{background:#FFF;font-size:8.75pt;margin:0;padding:0 0 0 15px}'
		headText += '#detail span.ritualstats{float:right;padding:0 30px 0 0}'
		headText += '#detail p.flavorIndent{display:block;background:#d6d6c2;margin:0;padding:2px 15px 2px 30px}'
		headText += '#detail span.clearIndent{display:block;background:#FFF;margin:0;padding:2px 15px 2px 30px}'
		headText += '#detail p.alt,#detail span.alt,#detail td.alt{background:#c3c6ad}'
		headText += '#detail th{background:#1d3d5e;color:#fff;text-align:left;padding:0 0 0 5px}'
		headText += '#detail ul{list-style:disc;margin:1em 0 1em 30px}'
		headText += '#detail table,#detail ul.flavor{margin-bottom:1em}'
		headText += '#detail ul.flavor li{list-style-image:url(\"http://www.wizards.com/dnd/images/symbol/x.gif\");margin-left:15px}'
		headText += '#detail blockquote{background:#d6d6c2;padding:0 0 0 22px}'
		headText += '#detail span.block{display:block;background:#d6d6c2;padding:0 0 0 22px}'
		headText += '#detail h1{font-size:1.09em;line-height:2;padding-left:15px;color:#fff;background:#000;margin:0}'
		headText += '#detail h1.player{background:#1d3d5e;font-size:1.35em}'
		headText += '#detail h1.dm{background:#5c1f34}'
		headText += '#detail h1.trap{background:#5c1f34;height:38px}'
		headText += '#detail h1.atwillpower{background:#619869}'
		headText += '#detail h1.encounterpower{background:#961334}'
		headText += '#detail h1.dailypower{background:#4d4d4f}'
		headText += '#detail span.milevel{font-size:9pt}'
		headText += '#detail h1.poison{background:#000}'
		headText += '#detail h1.poison .level{padding-right:15px;margin-top:0;text-align:right;float:right;position:relative;top:-24px}'
		headText += '#detail h1.utilitypower{background:#1c3d5f}'
		headText += '#detail h1.familiar{background:#4e5c2e}'
		headText += '#detail h1 .level{padding-right:15px;margin-top:0;text-align:right;float:right}'
		headText += '#detail .rightalign{text-align:right}'
		headText += '#detail .traplead{display:block;background:#fff;margin:0;padding:1px 15px}'
		headText += '#detail .trapblocktitle{display:block;background:#d6d6c2;font-weight:700;margin:0;padding:1px 15px}'
		headText += '#detail .trapblockbody{display:block;background:#fff;margin:0;padding:1px 15px 1px 30px}'
		headText += '#detail #RelatedArticles h5{width:100px;float:left;padding-top:10px;padding-left:20px;color:#3e141e;font-weight:700}'
		headText += '#detail #RelatedArticles ul.RelatedArticles{float:right;width:430px;list-style:none;margin:0;padding:10px 0 0}'
		headText += '#detail .bodytable{border:0;width:560px;background:#D1D1BC;margin:0}'
		headText += '#detail .bodytable td{border-bottom:none;padding-left:15px;padding-right:15px}'
		headText += '#detail h2{font-size:1.25em;padding-left:15px;color:#fff;background:#4e5c2e;height:20px;font-variant:small-caps;padding-top:5px;margin:0}'
		headText += '#detail h1.monster{background:#4e5c2e;height:38px;display:flex}'
		headText += '#detail h2.monster{font-size:9pt;padding-left:15px;color:#fff;background:#4e5c2e;height:20px;font-variant:small-caps;padding-top:3px;margin:0}'
		headText += '#detail h3.monster{font-size:8px;font-weight:700;color:#000;background:#c3c6ad;display:block;margin:0;padding:0 5px 0 10px}'
		headText += '#detail p.monster{background:#CADBB7;font-size:8.75pt;display:block;margin:0;padding:2px 15px}'
		headText += '#detail p.monstat{background:#CADBB7}'
		headText += '#detail p.miflavor{display:block;background:#EFD09F;font-size:8.75pt;font-style:italic;color:#000;margin:0;padding:2px 15px}'
		headText += '#detail table.magicitem{width:560px;margin-bottom:0}'
		headText += '#detail table.magicitem td{border:none;font-size:8.75pt;background:#F8E9D5}'
		headText += '#detail td.mic1{padding-left:20px;padding-right:0;width:50px}'
		headText += '#detail td.mic2{width:40px;padding:0}'
		headText += '#detail td.mic3{width:100px;text-align:right;padding:0}'
		headText += '#detail td.mic4{width:100px;padding:0}'
		headText += '#detail h2.magicitem{background:#EFD09F;color:#000;font-variant:normal;font-size:8.75pt;line-height:18px;padding-top:0;vertical-align:bottom;height:18px}'
		headText += '#detail h2.mihead{display:block;background:#EFD09F;color:#000;font-variant:normal;font-size:8.75pt;line-height:18px;padding-top:0;vertical-align:bottom;height:18px}'
		headText += '#detail p.publishedIn{font-size:8pt;margin-top:10px}'
		headText += '#detail h2.artifactHeading1{font-size:14pt;padding-left:5px;padding-top:5px;background:#FFF;color:#254950;font-variant:normal;margin:0}'
		headText += '#detail h2.artifactHeading2{font-size:14pt;padding-left:5px;padding-top:5px;background:#FFF;color:#556C75;font-variant:normal;margin:0}'
		headText += '#detail h2.ah1{font-size:14pt;padding-left:5px;padding-top:5px;padding-bottom:2px;background:#FFF;color:#254950;font-variant:normal;margin:0}'
		headText += '#detail h2.ah2{font-size:14pt;padding-left:5px;padding-top:5px;padding-bottom:2px;background:#FFF;color:#556C75;font-variant:normal;margin:0}'
		headText += '#detail h2.ah3{font-size:12pt;padding-left:5px;padding-top:5px;background:#FFF;color:#556C75;font-variant:normal;margin:0}'
		headText += '#detail p.mistat{display:block;background:#F8E9D5;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 15px}'
		headText += '#detail p.mistatAI{background:#F8E9D5;font-size:8.75pt;color:#000;height:36px;margin:0;padding:0 0 0 15px}'
		headText += '#detail span.miright{margin-top:0;text-align:right;float:right;position:relative;padding:0 5px 0 0}'
		headText += '#detail p.indent{text-indent:-15px;padding:0 0 0 30px}'
		headText += '#detail p.indent1{text-indent:-15px;padding:0 0 0 45px}'
		headText += '#detail p.indent2{text-indent:-15px;padding:0 0 0 60px}'
		headText += '#detail p.mitext{background:#FFF;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 5px}'
		headText += '#detail ul.mitext{margin-bottom:1em;display:block;margin-top:0;margin-right:0;background:#FFF;font-size:8.75pt;color:#000;padding:2px 5px}'
		headText += '#detail ul.mistat{background:#F8E9D5;font-size:8.75pt;color:#000;margin:0;padding:2px 5px 2px 30px}'
		headText += '#detail h1.miset{background:#22444B;font-size:12pt;font-weight:700;height:17pt;margin-top:2px;line-height:1.5em}'
		headText += '#detail th.miset{background:#22444B;color:#FFF;text-align:left;padding:0 0 0 5px}'
		headText += '#detail h1.thHead{background:#45133C;height:38px}'
		headText += '#detail h1.thHead .thLevel{margin-top:0;text-align:right;position:relative;top:-60px;padding-right:15px;float:right}'
		headText += '#detail h2.thHead{display:block;background:#65345D;color:#FFF;font-variant:small-caps;font-size:8.75pt;line-height:18px;padding-top:0;vertical-align:bottom;height:18px}'
		headText += '#detail p.thBody{text-indent:-15px;display:block;background:#E8F2D6;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 30px}'
		headText += '#detail p.tbod{text-indent:-15px;display:block;background:#E8F2D6;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 45px}'
		headText += '#detail p.thStat{display:block;background:#E8F2D6;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 15px}'
		headText += '#detail span.thInit{background:#E8F2D6;font-size:8.75pt;color:#000;position:absolute;left:400px;top:53px}'
		headText += '#detail p.th2{display:block;background:#CADBB7;font-size:8.75pt;color:#000;margin:0;padding:0 0 0 15px}'
		headText += 'a:link,a:focus,a:hover,a:active{color:blue}'
		headText += 'p em,p i,#detail i,#detail em{font-style:italic}'
		headText += '.clear,#MasterMainContent{clear:both}'
		headText += '#detail ul li,#detail a{color:#3e141e}'
		headText += '#detail h1.trap .level,#detail h1.monster .level{margin-top:0;text-align:right;top:-60px; margin-left:auto}'
		headText += '#detail h1.trap .type,#detail h1.trap .xp,#detail h1.monster .type,#detail h1.monster .xp,#detail h1.thHead .thSubHead,#detail h1.thHead .thXP{display:block;position:relative;z-index:99;top:-0.75em;height:1em;font-weight:400;font-size:0.917em}'
		headText += '#detail h1.magicitem,#detail h1.mihead{background:#DA9722;font-size:12pt;font-weight:700;height:17pt;margin-top:2px;line-height:1.5em}'
		headText += '#detail h1.magicitem .milevel,#detail h1.mihead .milevel,#detail h1.miset .milevel{padding-right:15px;margin-top:0;text-align:right;float:right;position:relative}'
		headText += '#detail ul.mitext li,#detail ul.mistat li{list-style-image:url(\\"http://www.wizards.com/dnd/images/symbol/x.gif\\");color:#000} '
		headText += '#detail h1.monster .type{display:block;position:absolute;z-index:99;top:39px;height:1em;font-weight:400;font-size:0.917em}'
		headText += '</style>'
		headText += '</head>'
		return headText

	def formatHTML(self, html: str) -> str:
		imagesInBase64 : list[tuple[str, str]] = [
			("../images/bullet.gif", "data:image/gif;base64,R0lGODlhCwALAMQSAEVCVlsyRmEyRWAyRWYyRURCVlcyRmQyRVI7T09FWGIyRVUyRlUyR1EzSHQyQ05EV0RCVyIyTH8yQgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAABIALAAAAAALAAsAAAUsoCSKwWiKCnSaUbSsUtFG5ShAc4s4UpL/DAkBl2ucHrMBDBAxwESAp+hwCgEAOw=="),
			("images/bullet.gif", "data:image/gif;base64,R0lGODlhCwALAMQSAEVCVlsyRmEyRWAyRWYyRURCVlcyRmQyRVI7T09FWGIyRVUyRlUyR1EzSHQyQ05EV0RCVyIyTH8yQgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAABIALAAAAAALAAsAAAUsoCSKwWiKCnSaUbSsUtFG5ShAc4s4UpL/DAkBl2ucHrMBDBAxwESAp+hwCgEAOw=="),
			("images/symbol/1.gif", "data:image/gif;base64,R0lGODlhDgAOAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAOAA4AAAg+AK/9G0iw4ECB1xIqXJjwIMOHDh8ujCix4b+HrBhSZDUwo0KKAv8FmnhxYSBWHi1WJLnyY8mWICVeNEjzYkAAOw=="),
			("images/symbol/1a.gif", "data:image/gif;base64,R0lGODlhDAAMAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAMAAwAAAg2AK8BGEiwoMBrCBMqHKiwoUAADhdCTMiqIcOEAwNhnHiN1cCKCC8iZEVyY0STJx+mPFiwJcSAADs="),
			("images/symbol/2.gif", "data:image/gif;base64,R0lGODlhDgAOAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAOAA4AAAhFAK/9G0iw4ECB1xIqXJjwIMOErBQ6fDgwkMB/D6+xGhhxIkNWIC9mZOhxpMOIJjFetEgR48Z/KEmqBBlzYcmMGA3qxBgQADs="),
			("images/symbol/2a.gif", "data:image/gif;base64,R0lGODlhDAAMAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAMAAwAAAg6AK8BGEiwoMBrCBMiZCUQgMKFA1kNfIhwYKCJFAOxkuiQYkKMHhsu9BgxIsWJFk861MjwocOCMB0GBAA7"),
			("images/symbol/3.gif", "data:image/gif;base64,R0lGODlhDgAOAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAOAA4AAAhMAK/9G0iw4ECB1xIqXJjwIMOErBQ6fDgwkMB/D6+xGhhxIkSNrEJeZMhxoceN/yxKxKgRosqVDVNmPIgyIkWWIW2SZJlR4kWDBq8FBAA7"),
			("images/symbol/3a.gif", "data:image/gif;base64,R0lGODlhDAAMAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAMAAwAAAg9AK8BGEiwoMBrCBMiZCUQgMKFA1kNfIhwYKCJCRmy2ijRYcKIHz1e6xgo5MiRHE2CfBjRIsWJKVk2LGgwIAA7"),
			("images/symbol/4.gif", "data:image/gif;base64,R0lGODlhDgAOAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAOAA4AAAhQAK/9G0iw4ECB1xIqXJjw4DVWDCE2/DcxkMKBFg+yGihx4z+IDlmJVCgSJEWGKB2iXBgy4sWTGBN6zEjRo0SBH3HKHJkw0EiVKxviNGjwWkAAOw=="),
			("images/symbol/4a.gif", "data:image/gif;base64,R0lGODlhDAAMAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAMAAwAAAhEAK8BGEiwoMBr11ghXKhwICuHCB8CkCgQQKCFAwMNvBaIlUKEHSkuHIlwI8mRJj8yrCjxY8uNGTFa3BhyYUgAFQsaDAgAOw=="),
			("images/symbol/5.gif", "data:image/gif;base64,R0lGODlhDgAOAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAOAA4AAAhQAK/9G0iw4ECB1xIqXJjw4DVWDCE2/DcxkMKBFg+yGihx4z+IDlmJhDgSJEWFHiVOZIhxYciHIx+uFPjxYk2NLR+2DCkSZU+HDFnSNGjwWkAAOw=="),
			("images/symbol/5a.gif", "data:image/gif;base64,R0lGODlhDAAMAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAMAAwAAAhGAK8BGEiwoMBr11ghXKhwICuHCB8CkCgQQKCFAwMNvBaIlUKPIDdinDiSYcaSH0EmrFhRYUKHMC2O1AggoUeGHmsW3FkzIAA7"),
			("images/symbol/6.gif", "data:image/gif;base64,R0lGODlhDgAOAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAOAA4AAAhVAK/9G0iw4ECB1xIqXJjw4DVWDCE2/DcxkMKBFg+yGihx4z+IDgMFknhNJEiKAj8m9HjyIcaL/zKiFLlwZMuUFl2q1MgRpsyVrEiOnMiwKEKDSCkGBAA7"),
			("images/symbol/6a.gif", "data:image/gif;base64,R0lGODlhDAAMAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAMAAwAAAhHAK8BGEiwoMBr11ghXKhwICuHCB8CkCgQQKCFAwMNvBYokMKEHiWKxDhxY8aIGTd2/MiRlUiICR2anEhSIwCQLF0+rFjQYEAAOw=="),
			("images/symbol/aura.png", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oGDxIfFo5+vM4AAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAA7ElEQVQoz43SsSuFURgG8F8Ud3WVLO6NKJvBKIvsd1KSdDMalNHoD+APUKxmGe1SshhuymCyXCIZxbW8n47Td+/nqVPnPO/7nvO+z3Pojzns+AdGs/M5XlFPuFqxGU7IJVxiDE1s4QMNTOIQ85HzB1Po4Q6LCT+O04jtlrU6hE68WIYTtHIRDvCAzQEa1NGNC1aK2brRSqNCwBt8Y78gmjHbTEXhFdZy8hjbA4omcI+RlFzAF54w28fjixhnLw2c4R2feEY71K1hGddR1Cv5FL+4TZLSNZ17V6acsGgVb3jBY9Wf3cB65vNRnvQDAd4w0asMzsIAAAAASUVORK5CYII="),
			("images/symbol/S1.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///////wAAACH5BAEAAAIALAAAAAAOAA4AAAIjlAWpd9v5GIhIsgrNvK62mCnhlH3a5l1IiYLWW6Zs3D0iUwAAOw=="),
			("images/symbol/S2.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAOAA4AAAIqnAepd9v5mIhIAnbhEff1/RkayCDfxVXixynTGo6mumK1kd5mNzmYIisAADs="),
			("images/symbol/S3.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAOAA4AAAIqnAepd9v5GIPIuCEqtaCifQhdJAEi2XCqcaZfJ2YpNMrlKn3PyPH7NSgAADs="),
			("images/symbol/S4.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAOAA4AAAIrnAepd9v5GIOo2UqHAEgYZ3GR4mkLJKSl+onhlG1dW32XmEkZiOSt4hoUAAA7"),
			("images/symbol/x.gif", "data:image/gif;base64,R0lGODlhBwAKAPcAAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAMyZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBmMzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZpkAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/MZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmWaZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwzzP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/zMA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM/8zM///M/wD//zP//2b//5n//8z//////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANcALAAAAAAHAAoAAAgjAK8JHEiwoEAABQMBCDRQIYCF1x5KfHjNIUSBCq0URGhwYEAAOw=="),
			("images/symbol/Z1.gif", "data:image/gif;base64,R0lGODlhFAAUAJEAAAAAAP///////wAAACH5BAEAAAIALAAAAAAUABQAAAIflI+py+0Po0xgnmoFtltDgIHiA1JSx2WXaqDsC8dxAQA7"),
			("images/symbol/Z1a.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///////wAAACH5BAEAAAIALAAAAAAOAA4AAAIYlI+pu8DonomSCjsj2Dt1yGCPGEqgiUoFADs="),
			("images/symbol/Z2.gif", "data:image/gif;base64,R0lGODlhFAAUAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAUABQAAAIhnI+py+0Po0xiHgGswXpw/UkZl0UYgFYT2rFgCXbyTD8FADs="),
			("images/symbol/Z2a.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAOAA4AAAIanI+pu8IowDtxmmoxk1U2AALOA1pDmXmZyRQAOw=="),
			("images/symbol/Z3.gif", "data:image/gif;base64,R0lGODlhFAAUAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAUABQAAAIinI+py+0Po5wL2CPmBXQI3gEfBV7QeIDOl6VR28XyTNdRAQA7"),
			("images/symbol/Z3a.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAOAA4AAAIbnI+pyz0Aj2gRuCHsBdnpqHSHhmTTuJzXyrIFADs="),
			("images/symbol/Z4.gif", "data:image/gif;base64,R0lGODlhFAAUAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAUABQAAAIknI+py+0Po5wMHCuFBYLuCITdoIWOgI7p9E3awLEXRdf2jVMFADs="),
			("images/symbol/Z4a.gif", "data:image/gif;base64,R0lGODlhDgAOAJEAAAAAAP///4yLi////yH5BAEAAAMALAAAAAAOAA4AAAIdnI+py21wIBMQCFcX2HfQjQhiNzZZQw2WGTnuCxcAOw==")
		]
		for image, base64 in imagesInBase64:
			html = html.replace(image, base64)
		return self.head + html

	def renderHTML(self, html: str) -> None:
		self.setHtml(self.formatHTML(html))

class mainScreen(Ui_ScreenView):
	def __init__(self):
		super().__init__()
		self.Jar = pickleJar("database.db")
		self.newWindows : list[QWidget] = []

	def setupUi(self, Screen) -> None:
		super().setupUi(Screen)
		self.webViewer = HTMLRenderer()
		self.gL_2.addWidget(self.webViewer)
		self.model : QStandardItemModel = QStandardItemModel()
		self.columnsList = [
			"",
			"Column1",
			"Column2",
			"Column3",
			"Column4",
			"Column5",
			"Column6",
			"Column7",
			"Column8"
		]
		self.model.setHorizontalHeaderLabels(self.columnsList)
		self.populateModel()

		self.setupDDITable()
		self.searchModel : QStandardItemModel = self.model

	def setupDDITable(self) -> None:
		self.ddiTable.setModel(self.model)
		self.ddiTable.horizontalHeader().setSortIndicatorClearable(True)
		self.ddiTable.horizontalHeader().setSortIndicatorShown(True)
		self.ddiTable.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

		self.ddiTable.verticalHeader().setDefaultSectionSize(5)
		self.ddiTable.verticalHeader().resizeSections(QHeaderView.ResizeMode.Fixed)
		self.ddiTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
		self.ddiTable.setAlternatingRowColors(True)

		self.ddiTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
		self.ddiTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
		self.ddiTable.horizontalHeader().setSortIndicatorClearable(True)
		self.ddiTable.setSortingEnabled(True)
		self.ddiTable.sortByColumn(1, Qt.SortOrder.AscendingOrder)
		self.ddiTable.verticalHeader().hide()
		self.ddiTable.customContextMenuRequested.connect(self.on_context_menu)

	def getRowData(self, row:int) -> ddiObject:
		if row >= 0 and row <= self.ddiTable.model().rowCount():
			return self.ddiTable.model().index(row, 0).data(32)
		else:
			raise IndexError

	def createContextMenu(self, itemData: dict, index: QModelIndex) -> QMenu:
		cMenu = QMenu()
		action1 = cMenu.addAction("Open in new window")
		action1.triggered.connect(lambda: self.actionOpenInNewWindow(itemData))

		action2 = cMenu.addAction("Open in default Browser")
		action2.triggered.connect(lambda: self.actionOpenInBrowser(itemData))

		cMenu.addSeparator()

		action3 = cMenu.addAction("Pin")
		action3.triggered.connect(lambda: self.actionPin(index))

		action4 = cMenu.addAction("Unpin")
		action4.triggered.connect(lambda: self.actionUnpin(index))

		cMenu.addSeparator()

		action5 = cMenu.addAction("Bookmark")
		action5.triggered.connect(self.actionBookmark)

		action6 = cMenu.addAction("Remove Bookmark")
		action6.triggered.connect(self.actionRemoveBookmark)

		return cMenu

	def actionOpenInNewWindow(self, itemData: dict) -> None:
		newWindow = QWidget()
		newWindow.resize(625,500)
		newWindow.setWindowTitle(itemData[0])
		HorizontalBoxLayout = QHBoxLayout()
		htmlRender = HTMLRenderer()
		htmlRender.renderHTML(itemData[32].getHTML())
		HorizontalBoxLayout.addWidget(htmlRender)
		newWindow.setLayout(HorizontalBoxLayout)
		self.newWindows.append(newWindow)
		newWindow.show()

	def actionOpenInBrowser(self, itemData: dict) -> None:
		with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tempFile:
			tempFile.write(bytes(self.webViewer.formatHTML(itemData[32].getHTML()), encoding='utf-8'))
			webbrowser.open('file://' + tempFile.name)

	def actionPin(self, index: QModelIndex) -> None:
		pinIcon = QPixmap()
		pinIcon.loadFromData(QByteArray.fromBase64(bytes(Base64Icons().PinIcon(), 'utf-8')))
		self.ddiTable.model().setData(index, QIcon(pinIcon), 1)
		self.ddiTable.model().setData(index, True, DDITableItemRole.Pinned)

	def actionUnpin(self, index: QModelIndex) -> None:
		self.ddiTable.model().setData(index, None, 1)
		self.ddiTable.model().setData(index, False, DDITableItemRole.Pinned)

	def actionBookmark(self) -> None:
		pass

	def actionRemoveBookmark(self) -> None:
		pass

	def on_context_menu(self, position: QPoint):
		index = self.ddiTable.indexAt(position)
		if index.isValid():
			for column in range(self.ddiTable.model().columnCount()):
				print(self.ddiTable.model().itemData(self.ddiTable.model().index(index.row(), column)))
			itemData = self.ddiTable.model().itemData(self.ddiTable.model().index(index.row(), 0))
			cMenu = self.createContextMenu(itemData, self.ddiTable.model().index(index.row(), 0))
			cMenu.exec_(self.ddiTable.viewport().mapToGlobal(position))

	def saveData(self, data: dict) -> None:
		self.Jar.putInJar(data)

	def loadData(self) -> dict:
		return self.Jar.popFromJar().pop()

	def createRow(self, ddiObject: ddiObject) -> None:
		newRow = QStandardItem(ddiObject.getType().category.title)
		newRow.setBackground(QColor(ddiObject.getColor()))
		newRow.setData(ddiObject, DDITableItemRole.Data)
		newRow.setData(ddiObject.getType().category.title, DDITableItemRole.Category)
		newRow.setData(False, DDITableItemRole.Pinned)
		self.model.appendRow(newRow)

	def populateRow(self, row: int, ddiObject: ddiObject) -> None:
		newItem = QStandardItem(ddiObject.getName())
		self.model.setItem(row, 1, newItem)

		match ddiObject.getType():
			case Types.ASSOCIATE:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeA()))
			case Types.BACKGROUND:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeB()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getCampaign()))
				self.model.setItem(row, 4, QStandardItem(ddiObject.getPrerequisite()))
				self.model.setItem(row, 5, QStandardItem(ddiObject.getSkills()))
			case Types.CLASS:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getRole()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getPower()))
				self.model.setItem(row, 4, QStandardItem(ddiObject.getAbilities()))
			case Types.COMPANION:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeC()))
			case Types.DEITY:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getAlignment()))
			case Types.DISEASE:
				self.model.setItem(row, 2, QStandardItem(str(ddiObject.getLevel())))
			case Types.EPICDESTINY:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getPrerequisite()))
			case Types.FEAT:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getPrerequisite()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getTier()))
			case Types.GLOSSARY:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeG()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getCategory()))
			case Types.ITEM:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getLevel()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getCategory()))
				if ddiObject.getIsMundane():
					self.model.setItem(row, 4, QStandardItem("Yes"))
				else:
					self.model.setItem(row, 4, QStandardItem("No"))
				self.model.setItem(row, 5, QStandardItem(ddiObject.getCost()))
				self.model.setItem(row, 6, QStandardItem(ddiObject.getRarity()))
			case Types.MONSTER:
				self.model.setItem(row, 2, QStandardItem(str(ddiObject.getLevel())))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getModifier()))
				self.model.setItem(row, 4, QStandardItem(ddiObject.getRole()))
				self.model.setItem(row, 5, QStandardItem(str(ddiObject.getXP())))
				self.model.setItem(row, 6, QStandardItem(ddiObject.getSize()))
				self.model.setItem(row, 7, QStandardItem(ddiObject.getKeywords()))
			case Types.PARAGONPATH:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getPrerequisite()))
			case Types.POISON:
				self.model.setItem(row, 2, QStandardItem(str(ddiObject.getLevel())))
				self.model.setItem(row, 3, QStandardItem(str(ddiObject.getCost())+" gp"))
			case Types.POWER:
				self.model.setItem(row, 2, QStandardItem(str(ddiObject.getLevel())))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getAction()))
				self.model.setItem(row, 4, QStandardItem(ddiObject.getClass()))
				self.model.setItem(row, 5, QStandardItem(ddiObject.getKind()))
				self.model.setItem(row, 6, QStandardItem(ddiObject.getUsage()))
			case Types.RACE:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getSize()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getDescription()))
			case Types.RITUAL:
				self.model.setItem(row, 2, QStandardItem(str(ddiObject.getLevel())))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getComponent()))
				self.model.setItem(row, 4, QStandardItem(str(ddiObject.getPrice())))
				self.model.setItem(row, 5, QStandardItem(ddiObject.getKeySkill()))
			case Types.GLOSSARY:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeS()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getCategory()))
			case Types.TERRAIN:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeT()))
			case Types.THEME:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getPrerequisite()))
			case Types.TRAP:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeT()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getRole()))
				if ddiObject.getLevel().isnumeric():
					self.model.setItem(row, 4, QStandardItem(ddiObject.getLevel()))
				else:
					self.model.setItem(row, 4, QStandardItem("*"))

				if ddiObject.getXP() != -1:
					self.model.setItem(row, 5, QStandardItem(str(ddiObject.getXP())))
				else:
					self.model.setItem(row, 5, QStandardItem("*"))
				self.model.setItem(row, 6, QStandardItem(ddiObject.getClasse()))

		self.model.setItem(row, self.columnsList.index("Column8"), QStandardItem(ddiObject.getSource()))

	def populateModel(self) -> None:
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
				self.createRow(ddiEntry)
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
		self.ddiTable.selectionModel().selectionChanged.connect(lambda: self.webViewer.renderHTML(self.ddiTable.model().index(self.ddiTable.currentIndex().row(), 0).data(32).getHTML()))

	def changeTable(self, category: Categories) -> None:
		if category is Categories.ALL:
			self.ddiTable.setModel(self.model)
			self.searchModel = self.model
		else:
			proxyFilter = PinableBookmarkbleFilterProxy()
			proxyFilter.setSourceModel(self.model)
			proxyFilter.setFilterRole(33)
			proxyFilter.setFilterRegularExpression(category.title)
			proxyFilter.filterAcceptsRow
			self.searchModel = proxyFilter
			self.ddiTable.setModel(proxyFilter)

		for headerItem in range(self.model.columnCount()):
			self.ddiTable.hideColumn(headerItem)

		#ugly
		if category is Categories.ALL:
			self.ddiTable.showColumn(0)
			self.ddiTable.showColumn(1)
			self.ddiTable.showColumn(8)
			self.model.horizontalHeaderItem(1).setText("Name")
			self.model.horizontalHeaderItem(8).setText("Source")
		else:
			for headerItem, columnName in enumerate(category.fields):
				self.ddiTable.showColumn(headerItem)
				self.model.horizontalHeaderItem(headerItem).setText(columnName)

		self.ddiTable.selectionModel().selectionChanged.connect(lambda: self.webViewer.renderHTML(self.ddiTable.model().index(self.ddiTable.currentIndex().row(), 0).data(32).getHTML()))