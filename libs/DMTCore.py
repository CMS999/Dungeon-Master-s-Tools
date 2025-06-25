from .ScreenView import Ui_ScreenView
from .DDIDataStructures import *
from .FilterTest import Ui_FilterTab

from abc import ABC, abstractmethod
from threading import Thread
from queue import Queue
from enum import IntEnum

import os
import tempfile
import webbrowser
import pickle
import typing

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
	QGridLayout, QHBoxLayout, QHeaderView, QSizePolicy,
	QTableWidget, QTableWidgetItem, QWidget, QItemDelegate, QMenu, QComboBox, QToolBar, QLineEdit, QPushButton, QTabWidget, QCheckBox)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
	QMetaObject, QObject, QPoint, QRect,
	QSize, QTime, QUrl, Qt, QSortFilterProxyModel, QModelIndex, QItemSelectionModel, Qt, QByteArray)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
	QFont, QFontDatabase, QGradient, QIcon,
	QImage, QKeySequence, QLinearGradient, QPainter,
	QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel, QStandardItem, QCloseEvent, QAction)

__all__ = ["DDIParser", "DDITableItemRole", "PinableBookmarkbleFilterProxy", "Base64Icons", "HTMLRenderer", "CompendiumScreen"]

class Serializer:
	def __init__(self, path:str='data/', SerializerName:str='Serializer'):
		self.filename = path+SerializerName
		if not os.path.isdir(path):
			os.makedirs(path)

	def write(self, object: typing.Any) -> None:
		with open(self.filename, 'wb') as serializer:
			pickle.dump(object, serializer, protocol=pickle.HIGHEST_PROTOCOL)
			serializer.close()

	def load(self) -> typing.Any:
		data : typing.Any = None
		with open(self.filename, 'rb') as serializer:
			try:
				data = pickle.load(serializer)
			except:
				raise ("No serialized file found")
			serializer.close()
		return data

class DDIParser:
	def __init__(self):
		self.sqlPath = "sql/"
		self.stripHTML = ["\\r", "\\n", "\\"]
		self.sqlDDITypes : dict[str:list] = {
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

	def parseFile(self, file: Files, sDict: dict, sQueue: Queue):
		linesInFile : list[str] = []
		try:
			with open(self.sqlPath + file.file, 'r') as ddiFile:
				for lineOfFile in ddiFile:
					if lineOfFile.startswith("INSERT"):
						lineOfFile = lineOfFile.strip()
						lineOfFileStart = lineOfFile.find("('")+2
						lineOfFileEnd = len(lineOfFile)-3
						linesInFile.append(lineOfFile[lineOfFileStart:lineOfFileEnd])
		except:
			print("No such file:" + self.sqlPath + file.file)

		for lineOfFile in linesInFile:
			lineTokens = lineOfFile.split("','")
			match file.type:
				case Types.ASSOCIATE:
					sDict[file.type.title].append(self.parseAssociate(lineTokens, Types.ASSOCIATE))
				case Types.BACKGROUND:
					sDict[file.type.title].append(self.parseBackground(lineTokens, Types.BACKGROUND))
				case Types.CLASS:
					sDict[file.type.title].append(self.parseClass(lineTokens, Types.CLASS))
				case Types.COMPANION:
					sDict[file.type.title].append(self.parseCompanion(lineTokens, Types.COMPANION))
				case Types.DEITY:
					sDict[file.type.title].append(self.parseDeity(lineTokens, Types.DEITY))
				case Types.DISEASE:
					sDict[file.type.title].append(self.parseDisease(lineTokens, Types.DISEASE))
				case Types.EPICDESTINY:
					sDict[file.type.title].append(self.parseEpicdestiny(lineTokens, Types.EPICDESTINY))
				case Types.FEAT:
					sDict[file.type.title].append(self.parseFeat(lineTokens, Types.FEAT))
				case Types.GLOSSARY:
					sDict[file.type.title].append(self.parseGlossary(lineTokens, Types.GLOSSARY))
				case Types.ITEM:
					sDict[file.type.title].append(self.parseItem(lineTokens, Types.ITEM))
				case Types.MONSTER:
					sDict[file.type.title].append(self.parseMonster(lineTokens, Types.MONSTER))
				case Types.PARAGONPATH:
					sDict[file.type.title].append(self.parseParagonpath(lineTokens, Types.PARAGONPATH))
				case Types.POISON:
					sDict[file.type.title].append(self.parsePoison(lineTokens, Types.POISON))
				case Types.POWER:
					sDict[file.type.title].append(self.parsePower(lineTokens, Types.POWER))
				case Types.RACE:
					sDict[file.type.title].append(self.parseRace(lineTokens, Types.RACE))
				case Types.RITUAL:
					sDict[file.type.title].append(self.parseRitual(lineTokens, Types.RITUAL))
				case Types.SKILL:
					sDict[file.type.title].append(self.parseSkill(lineTokens, Types.SKILL))
				case Types.TERRAIN:
					sDict[file.type.title].append(self.parseTerrain(lineTokens, Types.TERRAIN))
				case Types.THEME:
					sDict[file.type.title].append(self.parseTheme(lineTokens, Types.THEME))
				case Types.TRAP:
					sDict[file.type.title].append(self.parseTrap(lineTokens, Types.TRAP))
		sQueue.put(sDict)

	def buildDDIObjects(self) -> dict[str:list]:
		sQueue = Queue()
		threads : list[Thread] = []

		for file in Files:
			newDict = {file.type.title: []}
			thread = Thread(target=self.parseFile, args=(file, newDict, sQueue))
			threads.append(thread)

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

		while not sQueue.empty():
			sDict : dict = sQueue.get()
			for ddiType in sDict:
				self.sqlDDITypes[ddiType] = sDict[ddiType]

		return self.sqlDDITypes

	def processHTML(self, html: str) -> str:
		for regex in self.stripHTML:
			html = html.replace(regex, "")
		bodyStart = html.find("<body")
		if bodyStart != -1:
			bodyEnd = html.find("/body>")+6
			html = html[bodyStart:bodyEnd]
		return html

	def processString(self, string: str) -> str:
		for regex in self.stripHTML:
			string = string.replace(regex, "")
		return string

	def retrivePrerequisite(self, html: str) -> str:
		preStart = html.find("<b>Prerequisite: </b>")
		preEnd1 = -1
		preEnd2 = -1
		if preStart != -1:
			preEnd1 = html.find("</p>", preStart)

		if preStart != -1:
			preEnd2 = html.find("<br/>", preStart)

		preEnd = -1

		if preEnd2 != -1 and preEnd2 < preEnd1:
			preEnd = preEnd2
		elif preEnd1 != -1 and preEnd1 < preEnd2:
			preEnd = preEnd1

		if preEnd != -1:
			return html[preStart+21:preEnd]

	def retriveSize(self, html: str) -> str:
		preStart = html.find('<span class=\\"type\\">')
		if(preStart != -1):
			preEnd = html.find(" ", preStart+21)
			if(preEnd != -1):
				return html[preStart+21:preEnd]

	def retriveXP(self, html: str) -> str:
		preStart = html.find(">XP ")

		if(preStart != -1):
			preEnd = html.find("<", preStart+4)
			if(preEnd != -1):
				return html[preStart+4:preEnd]
		return html

	def parseAssociate(self, tokens: list[str], type: Types):
		a = Associate()
		a.setColor("#4e5c2e")
		a.setID(tokens[0])
		a.setName(self.processString(tokens[1]))
		a.setTypeA(self.processString(tokens[2]))
		a.setSource(self.processString(tokens[3]))
		a.setTeaser(tokens[4])
		a.setHTML(self.processHTML(tokens[5]))
		a.setType(type)
		return a

	def parseBackground(self, tokens: list[str], type: Types):
		b = Background()
		b.setColor('#1d3d5e')
		b.setID(tokens[0])
		b.setName(self.processString(tokens[1]))
		b.setTypeB(self.processString(tokens[2]))
		b.setCampaign(self.processString(tokens[3]))
		b.setSkills(self.processString(tokens[4]))
		b.setSource(self.processString(tokens[5]))
		b.setTeaser(tokens[6])
		b.setHTML(self.processHTML(tokens[7]))
		b.setPrerequisite(self.retrivePrerequisite(tokens[7]))
		b.setType(type)
		return b

	def parseClass(self, tokens:list[str], type:Types):
		c = Classe()
		c.setColor("#1d3d5e")
		c.setID(tokens[0])
		c.setName(self.processString(tokens[1]))
		c.setPower(self.processString(tokens[2]))
		c.setRole(self.processString(tokens[3]))
		c.setAbilities(self.processString(tokens[4]))
		c.setIsNew(tokens[5])
		c.setIsChanged(tokens[6])
		c.setSource(self.processString(tokens[7]))
		c.setTeaser(tokens[8])
		c.setHTML(self.processHTML(tokens[9]))
		c.setType(type)
		return c

	def parseCompanion(self, tokens:list[str], type:Types):
		c = Companion()
		c.setColor("#1d3d5e")
		c.setID(tokens[0])
		c.setName(self.processString(tokens[1]))
		c.setTypeC(self.processString(tokens[2]))
		c.setSource(self.processString(tokens[3]))
		c.setTeaser(tokens[4])
		c.setHTML(self.processHTML(tokens[5]))
		c.setType(type)
		return c

	def parseDeity(self, tokens:list[str], type:Types):
		d = Deity()
		d.setColor("#1d3d5e")
		d.setID(tokens[0])
		d.setName(self.processString(tokens[1]))
		d.setAlignment(self.processString(tokens[2]))
		d.setSource(self.processString(tokens[3]))
		d.setTeaser(tokens[4])
		d.setHTML(self.processHTML(tokens[5]))
		d.setType(type)
		return d

	def parseDisease(self, tokens:list[str], type:Types):
		d = Disease()
		d.setColor("#619869")
		d.setID(tokens[0])
		d.setName(self.processString(tokens[1]))
		d.setLevel(tokens[2])
		d.setSource(self.processString(tokens[3]))
		d.setTeaser(tokens[4])
		d.setHTML(self.processHTML(tokens[5]))
		d.setType(type)
		return d

	def parseEpicdestiny(self, tokens:list[str], type:Types):
		ed = EpicDestiny()
		ed.setColor("#1d3d5e")
		ed.setID(tokens[0])
		ed.setName(self.processString(tokens[1]))
		ed.setPrerequisite(self.processString(tokens[2]))
		ed.setIsNew(tokens[3])
		ed.setIsChanged(tokens[4])
		ed.setSource(self.processString(tokens[5]))
		ed.setTeaser(tokens[6])
		ed.setHTML(self.processHTML(tokens[7]))
		ed.setType(type)
		return ed

	def parseFeat(self, tokens:list[str], type:Types):
		f = Feat()
		f.setColor("#1d3d5e")
		f.setID(tokens[0])
		f.setName(self.processString(tokens[1]))
		f.setIsNew(tokens[2])
		f.setIsChanged(tokens[3])
		f.setSource(self.processString(tokens[4]))
		f.setTier(self.processString(tokens[5]))
		f.setSort(tokens[6])
		f.setTeaser(tokens[7])
		f.setHTML(self.processHTML(tokens[8]))
		f.setPrerequisite(self.retrivePrerequisite(tokens[8]))
		f.setType(type)
		return f

	def parseGlossary(self, tokens:list[str], type:Types):
		g = Glossary()
		g.setColor("#1d3d5e")
		g.setID(tokens[0])
		g.setName(self.processString(tokens[1]))
		g.setCategory(self.processString(tokens[2]))
		g.setTypeG(self.processString(tokens[3]))
		g.setSource(self.processString(tokens[4]))
		g.setTeaser(tokens[5])
		g.setHTML(self.processHTML(tokens[6]))
		g.setType(type)
		return g

	def parseItem(self, tokens:list[str], type:Types):
		i = Item()
		i.setID(tokens[0])
		i.setName(self.processString(tokens[1]))
		i.setCost(self.processString(tokens[2]))
		i.setLevel(self.processString(tokens[3]))
		i.setCategory(self.processString(tokens[4]))
		i.setEnhancement(self.processString(tokens[5]))
		i.setIsMundane(tokens[6])
		i.setFinalCost(self.processString(tokens[7]))
		i.setSource(self.processString(tokens[8]))
		i.setTeaser(tokens[9])
		i.setHTML(self.processHTML(tokens[10]))
		i.setRarity(self.processString(tokens[11]))
		i.setCostSort(tokens[12])
		i.setLevelSort(tokens[13])
		i.setType(type)
		if i.getLevelSort() == 0:
			match i.getCategory():
				case "Armor" | "Equipment" | "Weapon":
					i.setIsMundane("1")
					i.setColor("#1d3d5e")
		else:
			i.setColor("#EFD09F")
		return i

	def parseMonster(self, tokens:list[str], type:Types):
		m = Monster()
		m.setColor("#4e5c2e")
		m.setID(tokens[0])
		m.setName(self.processString(tokens[1]))
		m.setLevel(tokens[2])
		m.setModifier(self.processString(tokens[3]))
		m.setRole(self.processString(tokens[4]))
		m.setIsNew(tokens[5])
		m.setIsChanged(tokens[6])
		m.setSource(self.processString(tokens[7]))
		m.setTeaser(tokens[8])
		m.setHTML(self.processHTML(tokens[9]))
		m.setSize(self.retriveSize(tokens[9]))
		m.setXP(tokens[10])
		m.setKeywords(self.processString(tokens[11]))
		m.setType(type)
		return m

	def parseParagonpath(self, tokens:list[str], type:Types):
		p = ParagonPath()
		p.setColor("#1d3d5e")
		p.setID(tokens[0])
		p.setName(self.processString(tokens[1]))
		p.setPrerequisite(self.processString(tokens[2]))
		p.setSource(self.processString(tokens[3]))
		p.setTeaser(tokens[4])
		p.setHTML(self.processHTML(tokens[5]))
		p.setType(type)
		return p

	def parsePoison(self, tokens:list[str], type:Types):
		p = Poison()
		p.setColor("#000")
		p.setID(tokens[0])
		p.setName(self.processString(tokens[1]))
		p.setLevel(tokens[2])
		p.setCost(tokens[3])
		p.setSource(self.processString(tokens[4]))
		p.setTeaser(tokens[5])
		p.setHTML(self.processHTML(tokens[6]))
		p.setType(type)
		return p

	def parsePower(self, tokens:list[str], type: Types):
		p = Power()
		if('Daily' in tokens[11]):
			p.setColor('#4d4d4f')
		elif('Encounter' in tokens[11]):
			p.setColor('#961334')
		elif('At-Will' in tokens[11]):
			p.setColor('#619869')
		p.setID(tokens[0])
		p.setName(self.processString(tokens[1]))
		p.setLevel(tokens[2])
		p.setAction(self.processString(tokens[3]))
		p.setIsNew(tokens[4])
		p.setIsChanged(tokens[5])
		p.setSource(self.processString(tokens[6]))
		p.setClass(self.processString(tokens[7]))
		p.setTeaser(tokens[8])
		p.setHTML(self.processHTML(tokens[9]))
		p.setKind(self.processString(tokens[10]))
		p.setUsage(self.processString(tokens[11]))
		p.setType(type)
		return p

	def parseRace(self, tokens:list[str], type: Types):
		r = Race()
		r.setColor('#1d3d5e')
		r.setID(tokens[0])
		r.setName(self.processString(tokens[1]))
		r.setSize(self.processString(tokens[2]))
		r.setDescription(self.processString(tokens[3]))
		r.setIsNew(tokens[4])
		r.setIsChanged(tokens[5])
		r.setSource(self.processString(tokens[6]))
		r.setTeaser(tokens[7])
		r.setHTML(self.processHTML(tokens[8]))
		r.setType(type)
		return r

	def parseRitual(self, tokens:list[str], type: Types):
		r = Ritual()
		r.setColor('#1d3d5e')
		r.setID(tokens[0])
		r.setName(self.processString(tokens[1]))
		r.setLevel(tokens[2])
		r.setComponent(self.processString(tokens[3]))
		r.setPrice(tokens[4])
		r.setKeySkill(self.processString(tokens[5]))
		r.setSource(self.processString(tokens[6]))
		r.setTeaser(tokens[7])
		r.setHTML(self.processHTML(tokens[8]))
		r.setType(type)
		return r

	def parseSkill(self, tokens:list[str], type: Types):
		s = Skill()
		s.setColor('#1d3d5e')
		s.setID(tokens[0])
		s.setName(self.processString(tokens[1]))
		s.setCategory(self.processString(tokens[2]))
		s.setTypeS(self.processString(tokens[3]))
		s.setSource(self.processString(tokens[4]))
		s.setTeaser(tokens[5])
		s.setHTML(self.processHTML(tokens[6]))
		s.setType(type)
		return s

	def parseTerrain(self, tokens:list[str], type: Types):
		t = Terrain()
		t.setColor('#5c1f34')
		t.setID(tokens[0])
		t.setName(self.processString(tokens[1]))
		t.setTypeT(self.processString(tokens[2]))
		t.setSource(self.processString(tokens[3]))
		t.setTeaser(tokens[4])
		t.setHTML(self.processHTML(tokens[5]))
		t.setType(type)
		return t

	def parseTheme(self, tokens:list[str], type: Types):
		t = Theme()
		t.setColor('#1d3d5e')
		t.setID(tokens[0])
		t.setName(self.processString(tokens[1]))
		t.setSource(self.processString(tokens[2]))
		t.setHTML(self.processHTML(tokens[3]))
		t.setPrerequisite(self.retrivePrerequisite(tokens[3]))
		t.setType(type)
		return t

	def parseTrap(self, tokens:list[str], type: Types):
		t = Trap()
		t.setColor('#5c1f34')
		t.setID(tokens[0])
		t.setName(self.processString(tokens[1]))
		t.setRole(self.processString(tokens[2]))
		t.setTypeT(self.processString(tokens[3]))
		t.setLevel(self.processString(tokens[4]))
		t.setSource(self.processString(tokens[5]))
		t.setTeaser(tokens[6])
		t.setHTML(self.processHTML(tokens[7]))
		try:
			t.setXP(int(self.retriveXP(tokens[7])))
		except Exception:
			t.setXP(-1)
		t.setClasse(self.processString(tokens[8]).title())
		t.setType(type)
		return t

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

class CompendiumScreen(Ui_ScreenView):
	def __init__(self):
		super().__init__()
		self.database = Serializer(SerializerName="database.db")
		self.DDIData : dict
		try:
			self.DDIData = self.loadData()
		except:
			self.DDIData = DDIParser().buildDDIObjects()
			self.saveData(self.DDIData)
		self.newWindows : list[QWidget] = []

	def saveData(self, data: dict) -> None:
		self.database.write(data)

	def loadData(self) -> dict:
		return self.database.load()

	def setupUi(self, Screen) -> None:
		super().setupUi(Screen)
		self.webViewer = HTMLRenderer()
		self.filterOptions = QTabWidget()
		newTab = QWidget()
		newTab.setObjectName('Sourcebook Filters')
		self.filterOptions.addTab(newTab, 'Sourcebook Filters')
		self.gL_2.addWidget(self.webViewer)
		self.swap1 = self.webViewer
		self.swap2 = self.filterOptions
		self.filterOptions.setMinimumSize(625,0)
		self.filterOptions.setMaximumWidth(625)
		newTab = QWidget()
		newTab.setObjectName('test')
		self.filterOptions.addTab(newTab, 'test')
		TestUI = Ui_FilterTab()
		TestUI.setupUi(newTab)
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
		self.ddiTable.horizontalHeader().resizeSections(QHeaderView.ResizeMode.Stretch)
		#self.ddiTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		#self.ddiTable.horizontalHeader().setCascadingSectionResizes(True)
		#self.ddiTable.horizontalHeader().setStretchLastSection(True)

		self.ddiTable.verticalHeader().setDefaultSectionSize(5)
		self.ddiTable.verticalHeader().resizeSections(QHeaderView.ResizeMode.Fixed)
		self.ddiTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
		self.ddiTable.setAlternatingRowColors(True)

		self.ddiTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
		self.ddiTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
		self.ddiTable.horizontalHeader().setSortIndicatorClearable(True)
		self.ddiTable.horizontalHeader().setSortIndicatorShown(True)
		self.ddiTable.setSortingEnabled(True)
		self.ddiTable.sortByColumn(-1, Qt.SortOrder.AscendingOrder)
		self.ddiTable.verticalHeader().hide()
		self.ddiTable.customContextMenuRequested.connect(self.on_context_menu)

	def createFilterBox(self) -> QComboBox:
		newComboBox = QComboBox()
		newComboBox.currentIndexChanged.connect(lambda: self.changeTable(newComboBox.itemData(newComboBox.currentIndex(), Qt.ItemDataRole.UserRole)))
		for category in Categories:
			newComboBox.addItem(category.title, category)
		return newComboBox

	def createFilterLine(self) -> QLineEdit:
		newLineEdit = QLineEdit()
		newLineEdit.setMinimumSize(150,15)
		newLineEdit.setMaximumSize(150,35)
		newLineEdit.textEdited.connect(lambda: self.textChanged(newLineEdit.text()))
		return newLineEdit

	def createFilterOptions(self) -> QPushButton:
		newButton = QPushButton('Filters')
		newButton.clicked.connect(self.changeView)
		return newButton
	
	def changeView(self):
		self.gL_2.replaceWidget(self.swap1, self.swap2)
		self.webViewer.setVisible(not self.webViewer.isVisible())
		self.filterOptions.setVisible(not self.filterOptions.isVisible())
		temp = self.swap2
		self.swap2 = self.swap1
		self.swap1 = temp

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
			itemData = self.ddiTable.model().itemData(self.ddiTable.model().index(index.row(), 0))
			cMenu = self.createContextMenu(itemData, self.ddiTable.model().index(index.row(), 0))
			cMenu.exec_(self.ddiTable.viewport().mapToGlobal(position))

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
				newItem2 = QStandardItem()
				newItem2.setData(ddiObject.getLevel(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 2, newItem2)
			case Types.EPICDESTINY:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getPrerequisite()))
			case Types.FEAT:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTier()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getPrerequisite()))
			case Types.GLOSSARY:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getTypeG()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getCategory()))
			case Types.ITEM:
				newItem2 = QStandardItem()
				self.model.setItem(row, 2, QStandardItem(ddiObject.getCategory()))
				if ddiObject.getIsMundane():
					self.model.setItem(row, 3, QStandardItem("Yes"))
				else:
					self.model.setItem(row, 3, QStandardItem("No"))
				if ddiObject.getLevel().isnumeric():
					newItem2.setData(int(ddiObject.getLevel()), Qt.ItemDataRole.DisplayRole)
				else:
					newItem2.setData(ddiObject.getLevel(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 4, newItem2)
				self.model.setItem(row, 5, QStandardItem(ddiObject.getCost()))
				self.model.setItem(row, 6, QStandardItem(ddiObject.getRarity()))
			case Types.MONSTER:
				newItem2 = QStandardItem()
				newItem2.setData(ddiObject.getLevel(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 2, newItem2)
				self.model.setItem(row, 3, QStandardItem(ddiObject.getModifier()))
				self.model.setItem(row, 4, QStandardItem(ddiObject.getRole()))
				newItem3 = QStandardItem()
				newItem3.setData(ddiObject.getXP(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 5, newItem3)
				self.model.setItem(row, 6, QStandardItem(ddiObject.getSize()))
				self.model.setItem(row, 7, QStandardItem(ddiObject.getKeywords()))
			case Types.PARAGONPATH:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getPrerequisite()))
			case Types.POISON:
				newItem2 = QStandardItem()
				newItem2.setData(ddiObject.getLevel(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 2, newItem2)
				self.model.setItem(row, 3, QStandardItem(str(ddiObject.getCost())+" gp"))
			case Types.POWER:
				newItem2 = QStandardItem()
				newItem2.setData(ddiObject.getLevel(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 2, newItem2)
				self.model.setItem(row, 3, QStandardItem(ddiObject.getAction()))
				self.model.setItem(row, 4, QStandardItem(ddiObject.getClass()))
				self.model.setItem(row, 5, QStandardItem(ddiObject.getKind()))
				self.model.setItem(row, 6, QStandardItem(ddiObject.getUsage()))
			case Types.RACE:
				self.model.setItem(row, 2, QStandardItem(ddiObject.getDescription()))
				self.model.setItem(row, 3, QStandardItem(ddiObject.getSize()))
			case Types.RITUAL:
				newItem2 = QStandardItem()
				newItem2.setData(ddiObject.getLevel(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 2, newItem2)
				self.model.setItem(row, 3, QStandardItem(ddiObject.getComponent()))
				newItem3 = QStandardItem()
				newItem3.setData(ddiObject.getPrice(), Qt.ItemDataRole.DisplayRole)
				self.model.setItem(row, 4, newItem3)
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
					newItem2 = QStandardItem()
					newItem2.setData(int(ddiObject.getLevel()), Qt.ItemDataRole.DisplayRole)
					self.model.setItem(row, 4, newItem2)
				else:
					self.model.setItem(row, 4, QStandardItem("*"))

				if ddiObject.getXP() != -1:
					newItem3 = QStandardItem()
					newItem3.setData(ddiObject.getXP(), Qt.ItemDataRole.DisplayRole)
					self.model.setItem(row, 5, newItem3)
				else:
					self.model.setItem(row, 5, QStandardItem("*"))
				self.model.setItem(row, 6, QStandardItem(ddiObject.getClasse()))

		self.model.setItem(row, 8, QStandardItem(ddiObject.getSource()))

	def populateModel(self) -> None:
		ddiEntry : ddiObject
		for type in Types:
			for ddiEntry in self.DDIData[type.title]:
				self.createRow(ddiEntry)
				self.populateRow(self.model.rowCount()-1, ddiEntry)

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
			proxyFilter.setFilterRole(DDITableItemRole.Category)
			proxyFilter.setFilterRegularExpression(category.title)
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
		self.ddiTable.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)