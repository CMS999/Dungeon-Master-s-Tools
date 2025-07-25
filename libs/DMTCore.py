from .ScreenView import Ui_ScreenView
from .DDIDataStructures import *
from .SourceFilter import Ui_FilterTab
from .ColumnFilter import Ui_ColumnFilter
from .ExtraFilters import Ui_extraFilters
from .DynamicColumnFilter import Ui_DynamicColumnFilter

from threading import Thread
from queue import Queue
from enum import IntEnum
import typing

import os
import tempfile
import webbrowser
import pickle
import typing

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
	QGridLayout, QHBoxLayout, QHeaderView, QSizePolicy,
	QTableWidget, QTableWidgetItem, QWidget, QItemDelegate, QMenu, QComboBox, QToolBar, QLineEdit, QPushButton, QTabWidget, QCheckBox, QStatusBar, QLabel, QSpacerItem, QSpinBox)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
	QMetaObject, QObject, QPoint, QRect,
	QSize, QTime, QUrl, Qt, QSortFilterProxyModel, QModelIndex, QItemSelectionModel, Qt, QByteArray, QRegularExpression, QAbstractItemModel, QSignalMapper)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
	QFont, QFontDatabase, QGradient, QIcon,
	QImage, QKeySequence, QLinearGradient, QPainter,
	QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel, QStandardItem, QCloseEvent, QAction)

__all__ = ["DDIParser", "DDITableItemRole", "PinableFilterProxy", "Base64Icons", "HTMLRenderer", "CompendiumScreen"]

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
		self.sqlPath = "sql"
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
			with open(os.path.join(os.getcwd(), self.sqlPath, file.file), 'r', encoding='utf8') as ddiFile:
				for lineOfFile in ddiFile:
					if lineOfFile.startswith("INSERT"):
						lineOfFile = lineOfFile.strip()
						lineOfFileStart = lineOfFile.find("('")+2
						lineOfFileEnd = len(lineOfFile)-3
						linesInFile.append(lineOfFile[lineOfFileStart:lineOfFileEnd])
		except:
			print("No such file:" + os.path.join(os.getcwd(), self.sqlPath, file.file))

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
		if string == '':
			return 'None'

		for regex in self.stripHTML:
			string = string.replace(regex, "")
		if string.isspace():
			string = 'None'
		return string

	def processException(self, html:str) -> str:
		strings = html.replace(', ', ';;').replace(',', ';;').replace(' or ', ';;').split(';;')
		for index, string in enumerate(strings):
			if 'skill' in string.lower():
				html = html.replace(string, 'Other')
		return html

	def retriveKind(self, html: str) -> str:
		preStart = html.find('<span class="level">')
		preEnd = -1
		if preStart != -1:
			preEnd = html.find("</span>")

		kind : str

		if preStart != -1 and preEnd != -1:
			kind : str = html[preStart+20:preEnd]
			if 'Attack' in kind:
				kind = 'Attack'
			elif 'Utility' in kind:
				kind = 'Utility'
			elif 'Feature' in kind:
				kind = 'Feature'
			elif 'Pact Boon' in kind:
				kind = 'Pact Boon'
			elif 'Racial' in kind:
				kind = 'Racial'
			else:
				kind = ''

		return kind

	def retrivePrerequisite(self, html: str) -> str:
		preStart = html.find("<b>Prerequisite: </b>")
		preEnd1 = -1
		preEnd2 = -1
		if preStart == -1:
			preStart = html.find("<b>Prerequisite</b>: ")
		if preStart != -1:
			preEnd1 = html.find("</p>", preStart)

		if preStart != -1:
			preEnd2 = html.find("<br/>", preStart)

		preEnd = -1

		if preEnd2 != -1 and preEnd2 < preEnd1:
			preEnd = preEnd2
		elif preEnd1 != -1 and preEnd1 < preEnd2:
			preEnd = preEnd1

		if preStart != -1 and preEnd != -1:
			return html[preStart+21:preEnd]
		else:
			return 'None'

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
		b.setSkills(self.processException(self.processString(tokens[4])))
		b.setSource(self.processString(tokens[5]))
		b.setTeaser(tokens[6])
		b.setHTML(self.processHTML(tokens[7]))
		b.setPrerequisite(self.processException(self.retrivePrerequisite(tokens[7])))
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
		if tokens[2] == 'Evil':
			d.setAlignment('True Evil')
		elif tokens[2] == 'Good':
			d.setAlignment('True Good')
		else:
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
		if tokens[2] != '':
			g.setCategory(self.processString(tokens[2]))
		else:
			g.setCategory(self.processString('Skill'))
		if tokens[3] != '':
			g.setTypeG(self.processString(tokens[3]))
		else:
			g.setTypeG(self.processString('Rules'))
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
		m.setModifier(self.processString(tokens[3]).title())
		m.setRole(self.processString(tokens[4]))
		m.setIsNew(tokens[5])
		m.setIsChanged(tokens[6])
		m.setSource(self.processString(tokens[7]))
		m.setTeaser(tokens[8])
		if '<h2>' in tokens[9]:
			m.setIsPostMM3(True)
		else:
			m.setIsPostMM3(False)
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
		kind = self.retriveKind(self.processHTML(tokens[9]))
		if kind == '':
			p.setKind(self.processString(tokens[10]))
		else:
			p.setKind(self.processString(kind))
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
	Source = 35
	IsPostMM3 = 36
	Bookmarked = 37
	test = 38

class BookmarkbleFilterProxy(QSortFilterProxyModel):
	def __init__(self):
		super().__init__()
		self.IsFilterOn : bool = False

	def flipIsFilterOn(self):
		self.IsFilterOn = not self.IsFilterOn

	def filterAcceptsRow(self, source_row, source_parent):
		if not self.IsFilterOn:
			return True

		isRowBookmarked : bool = False
		model : QAbstractItemModel = self.sourceModel()

		isRowBookmarked = model.data(model.index(source_row, 0), DDITableItemRole.Bookmarked)
		return isRowBookmarked

class PinableFilterProxy(QSortFilterProxyModel):
	def filterAcceptsRow(self, source_row, source_parent):
		if super().filterAcceptsRow(source_row, source_parent):
			return True

		isRowPinned : bool = False
		model : QAbstractItemModel = self.sourceModel()

		try:
			isRowPinned = model.data(model.index(source_row, 0), DDITableItemRole.Pinned)
		except ValueError:
			isRowPinned = False

		return isRowPinned

class PinableRangeOptInFilterProxy(QSortFilterProxyModel):
	def __init__(self):
		super().__init__()
		self.FilteringRange : bool = False
		self.min : int = 0
		self.max : int = 0

	def isRangeEnabled(self) -> bool:
		return self.FilteringRange

	@typing.overload
	def enableRange(self, value:bool, minValue:int, maxValue:int) -> None: ...
	@typing.overload
	def enableRange(self, value:bool) -> None: ...

	def enableRange(self, value:bool, /, minValue: int = -1, maxValue: int = -1) -> None:
		self.FilteringRange = value
		if minValue > -1 and maxValue > -1:
			self.min = minValue
			self.max = maxValue

	def setFilteringRange(self, isFiltering) -> None:
		self.FilteringRange = isFiltering

	def filterAcceptsRow(self, source_row, source_parent):
		model : QAbstractItemModel = None
		if self.isRangeEnabled():
			model = self.sourceModel()
			value = -1
			val = model.data(model.index(source_row, self.filterKeyColumn()), DDITableItemRole.test)
			if isinstance(val, int):
				value = val
			if self.min <= value and value <= self.max:
				return True
		elif super().filterAcceptsRow(source_row, source_parent):
			return True

		isRowPinned : bool = False
		model = self.sourceModel()

		try:
			isRowPinned = model.data(model.index(source_row, 0), DDITableItemRole.Pinned)
		except ValueError:
			isRowPinned = False

		return isRowPinned

class PinableSourceFilterProxy(QSortFilterProxyModel):
	def __init__(self):
		super().__init__()
		self.Sources : dict[str:bool] = {
			"Adventurer's Vault": True,
			"Adventurer's Vault 2": True,
			"Arcane Power": True,
			"Beyond the Crystal Cave": True,
			"City of Stormreach": True,
			"Class Compendium": True,
			"Council of Spiders": True,
			"Dangerous Delves": True,
			"Dark Sun Campaign Setting": True,
			"Dark Sun Creature Catalog": True,
			"Demonomicon": True,
			"Divine Power": True,
			"Draconomicon: Chromatic Dragons": True,
			"Draconomicon: Metallic Dragons": True,
			"Dragon Magazine": True,
			"Dragons of Eberron": True,
			"Dungeon Delve": True,
			"Dungeon Magazine": True,
			"Dungeon Master's Guide": True,
			"Dungeon Master's Guide 2": True,
			"Dungeon Master's Kit": True,
			"E1 Death's Reach": True,
			"E2 Kingdom of the Ghouls": True,
			"E3 Prince of Undeath": True,
			"Eberron Campaign Setting": True,
			"Eberron Player's Guide": True,
			"Elder Evils": True,
			"Exemplars of Evil": True,
			"FR1 Scepter Tower of Spellgard": True,
			"Forgotten Realms Campaign Guide": True,
			"Forgotten Realms Player's Guide": True,
			"Fortress of the Yuan-ti": True,
			"H1 Keep on the Shadowfell": True,
			"H2 Thunderspire Labyrinth": True,
			"H3 Pyramid of Shadows": True,
			"HS1 The Slaying Stone": True,
			"HS2 Orcs of Stonefang Pass": True,
			"Halls of Undermountain": True,
			"Hammerfast": True,
			"Heroes of Shadow": True,
			"Heroes of the Elemental Chaos": True,
			"Heroes of the Fallen Lands": True,
			"Heroes of the Feywild": True,
			"Heroes of the Forgotten Kingdoms": True,
			"Into the Unknown: The Dungeon Survival Handbook": True,
			"Legendary Evils": True,
			"Madness at Gardmore Abbey": True,
			"Manual of the Planes": True,
			"Marauders of the Dune Sea": True,
			"Martial Power": True,
			"Martial Power 2": True,
			"Monster Manual": True,
			"Monster Manual 2": True,
			"Monster Manual 3": True,
			"Monster Vault": True,
			"Monster Vault: Threats to the Nentir Vale": True,
			"Mordenkainen's Magnificent Emporium": True,
			"Neverwinter Campaign Setting": True,
			"Open Grave": True,
			"P1 King of the Trollhaunt Warrens": True,
			"P2 Demon Queen Enclave": True,
			"P3 Assault on Nightwyrm Fortress": True,
			"PH Heroes: Series 1": True,
			"PH Heroes: Series 2": True,
			"Player's Handbook": True,
			"Player's Handbook 2": True,
			"Player's Handbook 3": True,
			"Player's Handbook Races: Dragonborn": True,
			"Player's Handbook Races: Tiefling": True,
			"Primal Power": True,
			"Psionic Power": True,
			"Red Box Starter Set": True,
			"Revenge of the Giants": True,
			"Rules Compendium": True,
			"Savage Encounters": True,
			"Seekers of the Ashen Crown": True,
			"The Book of Vile Darkness": True,
			"The Plane Above": True,
			"The Plane Below": True,
			"The Shadowfell": True,
			"Tomb of Horrors": True,
			"Underdark": True,
			"Vor Rukoth": True,
			"Web of the Spider Queen": True
		}

	def filterAcceptsRow(self, source_row, source_parent):
		model : QAbstractItemModel = self.sourceModel()
		index : QModelIndex = model.index(source_row, 0)
		source : str = model.data(index, DDITableItemRole.Source)

		for source in source.split(', '):
			if 'agazine' in source:
				if 'ragon' in source:
					source = 'Dragon Magazine'
				if 'ungeon' in source:
					source = 'Dungeon Magazine'
			if self.Sources[source]:
				return True

		isRowPinned : bool = False
		try:
			isRowPinned = model.data(index, DDITableItemRole.Pinned)
		except ValueError:
			isRowPinned = False

		return isRowPinned

	def flipSource(self, source:str) -> None:
		self.Sources[source] = not self.Sources[source]

	def selectNone(self):
		for source in self.Sources:
			self.Sources[source] = False

	def selectALL(self):
		for source in self.Sources:
			self.Sources[source] = True

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

class DataQCheckBox(QCheckBox):
	def __init__(self, text:str):
		super().__init__(text)
		self.data = None

class DDISourceFilter(Ui_FilterTab):
	def setupUi(self, FilterTab):
		super().setupUi(FilterTab)
		self.checkBoxes : list[DataQCheckBox] = []
		self.createSourceList()
		self.selectAll.clicked.connect(self.actionSelectAll)
		self.selectNone.clicked.connect(self.actionSelectNone)

	def createSourceList(self):
		row : int = 0
		column : int = 0
		Sources : list[str] = [
			"Adventurer's Vault",
			"Adventurer's Vault 2",
			"Arcane Power",
			"Beyond the Crystal Cave",
			"City of Stormreach",
			"Class Compendium",
			"Council of Spiders",
			"Dangerous Delves",
			"Dark Sun Campaign Setting",
			"Dark Sun Creature Catalog",
			"Demonomicon",
			"Divine Power",
			"Draconomicon: Chromatic Dragons",
			"Draconomicon: Metallic Dragons",
			"Dragon Magazine",
			"Dragons of Eberron",
			"Dungeon Delve",
			"Dungeon Magazine",
			"Dungeon Master's Guide",
			"Dungeon Master's Guide 2",
			"Dungeon Master's Kit",
			"E1 Death's Reach",
			"E2 Kingdom of the Ghouls",
			"E3 Prince of Undeath",
			"Eberron Campaign Setting",
			"Eberron Player's Guide",
			"Elder Evils",
			"Exemplars of Evil",
			"FR1 Scepter Tower of Spellgard",
			"Forgotten Realms Campaign Guide",
			"Forgotten Realms Player's Guide",
			"Fortress of the Yuan-ti",
			"H1 Keep on the Shadowfell",
			"H2 Thunderspire Labyrinth",
			"H3 Pyramid of Shadows",
			"HS1 The Slaying Stone",
			"HS2 Orcs of Stonefang Pass",
			"Halls of Undermountain",
			"Hammerfast",
			"Heroes of Shadow",
			"Heroes of the Elemental Chaos",
			"Heroes of the Fallen Lands",
			"Heroes of the Feywild",
			"Heroes of the Forgotten Kingdoms",
			"Into the Unknown: The Dungeon Survival Handbook",
			"Legendary Evils",
			"Madness at Gardmore Abbey",
			"Manual of the Planes",
			"Marauders of the Dune Sea",
			"Martial Power",
			"Martial Power 2",
			"Monster Manual",
			"Monster Manual 2",
			"Monster Manual 3",
			"Monster Vault",
			"Monster Vault: Threats to the Nentir Vale",
			"Mordenkainen's Magnificent Emporium",
			"Neverwinter Campaign Setting",
			"Open Grave",
			"P1 King of the Trollhaunt Warrens",
			"P2 Demon Queen Enclave",
			"P3 Assault on Nightwyrm Fortress",
			"PH Heroes: Series 1",
			"PH Heroes: Series 2",
			"Player's Handbook",
			"Player's Handbook 2",
			"Player's Handbook 3",
			"Player's Handbook Races: Dragonborn",
			"Player's Handbook Races: Tiefling",
			"Primal Power",
			"Psionic Power",
			"Red Box Starter Set",
			"Revenge of the Giants",
			"Rules Compendium",
			"Savage Encounters",
			"Seekers of the Ashen Crown",
			"The Book of Vile Darkness",
			"The Plane Above",
			"The Plane Below",
			"The Shadowfell",
			"Tomb of Horrors",
			"Underdark",
			"Vor Rukoth",
			"Web of the Spider Queen"
		]
		for source in Sources:
			newCheckBox = DataQCheckBox(source)
			self.checkBoxes.append(newCheckBox)
			newCheckBox.setText(newCheckBox.fontMetrics().elidedText(source, Qt.TextElideMode.ElideRight, 260))
			newCheckBox.data = source
			newCheckBox.setChecked(True)
			self.gL_3.addWidget(newCheckBox, row, column, 1, 1)
			if column == 1:
				column = 0
				row += 1
			else:
				column += 1

	def actionSelectAll(self):
		for source in self.checkBoxes:
			source.blockSignals(True)
			source.setChecked(True)
			source.blockSignals(False)

	def actionSelectNone(self):
		for source in self.checkBoxes:
			source.blockSignals(True)
			source.setChecked(False)
			source.blockSignals(False)


class DynamicPrimaryFilter(Ui_DynamicColumnFilter):
	def __init__(self):
		super().__init__()
		self.CheckBoxes : list[QCheckBox] = []
		self.FilterItems : list[QComboBox | tuple[QSpinBox, QSpinBox]] = []
		self.vSpacer1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.Templates : dict[str, typing.Callable] = {}
		self.Templates.update({'' : self.removeCurrentTemplate})
		self.ModelFilters : list[PinableRangeOptInFilterProxy] = []
		self.model : QAbstractItemModel = None

	def setModel(self, model:QAbstractItemModel):
		self.model = model

	def getModel(self) -> QAbstractItemModel:
		if len(self.ModelFilters)-1 >= 0:
			return self.ModelFilters[len(self.ModelFilters)-1]
		else:
			return self.model

	def setupUi(self, DynamicColumnFilter):
		super().setupUi(DynamicColumnFilter)
		self.btnReset.clicked.connect(self.actionResetFilters)

	def registerNewTemplate(self, templateName:str, boxesLabels:list[str], boxOptions:list[set | range]):
		if len(self.ModelFilters) < len(boxesLabels):
			for x in range(len(self.ModelFilters), len(self.ModelFilters) + len(boxesLabels) - len(self.ModelFilters)):
				n = PinableRangeOptInFilterProxy()
				n.setObjectName(str(x))
				if x == 0:
					n.setSourceModel(self.model)
				else:
					n.setSourceModel(self.ModelFilters[x-1])
				self.ModelFilters.append(n)
		self.Templates.update({templateName: lambda Labels=boxesLabels, Options=boxOptions: self.createFiltersBoxesFromTemplate(Labels, Options)})

	def changeTemplate(self, templateToCall:str):
		for n in self.ModelFilters:
			n.enableRange(False)
			n.setFilterRegularExpression('')
		self.Templates[templateToCall]()

	def actionResetFilters(self) -> None:
		rangeIndex : int = 0
		for item in self.FilterItems:
			if isinstance(item, QComboBox):
				item.setCurrentIndex(0)
			elif isinstance(item, tuple):
				min, max = item
				min.blockSignals(True)
				max.blockSignals(True)

				min.setValue(min.minimum())
				max.setValue(max.maximum())

				min.blockSignals(False)
				max.blockSignals(False)

				self.CheckBoxes[rangeIndex].setChecked(False)
				rangeIndex += 1

	def removeCurrentTemplate(self) -> None:
		for item in self.scrollAreaContents.children():
			if isinstance(item, (QComboBox, QLabel, QSpinBox, QCheckBox)):
				self.gL2.removeWidget(item)
				item.deleteLater()
			elif isinstance(item, QHBoxLayout):
				self.gL2.removeItem(item)
				item.deleteLater()
		self.gL2.removeItem(self.vSpacer1)
		self.CheckBoxes = []
		self.FilterItems = []

	def createFiltersBoxesFromTemplate(self, boxes:list[str], boxOptions:list[set | range]) -> list[QComboBox | tuple[QSpinBox]]:
		lastindex : int = 0
		self.removeCurrentTemplate()

		for indexN, box in enumerate(boxes):
			self.ModelFilters[indexN].setFilterKeyColumn(indexN+2)
			if isinstance(boxOptions[indexN], set):
				newLabel : QLabel = QLabel(self.scrollAreaContents)
				newLabel.setText(box)
				self.gL2.addWidget(newLabel, indexN, 0, 1, 1)

				newComboBox : QComboBox = QComboBox(self.scrollAreaContents)
				boxOptions[indexN].add('')
				newComboBox.addItems(list(sorted(boxOptions[indexN])))
				self.gL2.addWidget(newComboBox, indexN, 1, 1, 1)
				newComboBox.setObjectName(box+"_ComboBox")
				newComboBox.currentIndexChanged.connect(lambda data, idx=indexN, cBox=newComboBox: self.filterModel(idx, cBox))

				self.FilterItems.append(newComboBox)

			else:
				newRangeBox : QCheckBox = QCheckBox(box, self.scrollAreaContents)
				self.gL2.addWidget(newRangeBox, indexN, 0, 1, 1)
				self.CheckBoxes.append(newRangeBox)

				newRangeLayout : QHBoxLayout = QHBoxLayout()

				newRangeMin : QSpinBox = QSpinBox(self.scrollAreaContents)
				newRangeMin.setMinimum(boxOptions[indexN].start)
				newRangeMin.setMaximum(boxOptions[indexN].stop)
				newRangeMin.setValue(boxOptions[indexN].start)

				newRangeMax : QSpinBox = QSpinBox(self.scrollAreaContents)
				newRangeMax.setMinimum(boxOptions[indexN].start)
				newRangeMax.setMaximum(boxOptions[indexN].stop)
				newRangeMax.setValue(boxOptions[indexN].stop)

				newRangeLayout.addWidget(newRangeMin)
				newRangeLayout.addWidget(newRangeMax)
				self.gL2.addItem(newRangeLayout, indexN, 1, 1, 1)

				newRangeBox.setChecked(False)
				newRangeMin.setDisabled(True)
				newRangeMax.setDisabled(True)
				newRangeBox.checkStateChanged.connect(lambda data, idx=indexN, min=newRangeMin, max=newRangeMax: self.disableRange(data, idx, min, max))

				newRangeMin.valueChanged.connect(lambda data, idx=indexN, min=newRangeMin, max=newRangeMax: self.filterRangeModel(idx, min, max))
				newRangeMax.valueChanged.connect(lambda data, idx=indexN, min=newRangeMin, max=newRangeMax: self.filterRangeModel(idx, min, max))

				newRangeMin.setVisible(True)
				newRangeMax.setVisible(True)
				self.FilterItems.append((newRangeMin, newRangeMax))
			lastindex = indexN

		self.gL2.addItem(self.vSpacer1, lastindex+1, 0, 1, 2)
		return

	def filterRangeModel(self, index:int, min:QSpinBox, max:QSpinBox) -> None:
		self.ModelFilters[index].enableRange(True, min.value(), max.value())
		self.ModelFilters[index].setFilterRegularExpression('')

	def disableRange(self, state:Qt.CheckState, index:int, min:QSpinBox, max:QSpinBox) -> None:
		max.setEnabled(not min.isEnabled())
		min.setEnabled(not min.isEnabled())
		if state is Qt.CheckState.Unchecked:
			self.ModelFilters[index].enableRange(False)
			self.ModelFilters[index].setFilterRegularExpression('')


	def filterModel(self, index:int, cBox:QComboBox):
		self.ModelFilters[index].setFilterRegularExpression(cBox.currentText())


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

		self.webViewer = self.createWebViewer()
		self.Filters = self.createFilterTab()
		self.gL_2.addWidget(self.webViewer)
		self.swap1 = self.webViewer
		self.swap2 = self.Filters

		newTab = self.addFilterTab('Primary Filters')
		self.pfTab = DynamicPrimaryFilter()
		self.pfTab.setupUi(newTab)

		newTab = self.addFilterTab('Sourcebook Filters')
		self.sfTab = self.createSourcebookFilterTab(newTab)

		newTab = self.addFilterTab('Extra Filters')
		n = Ui_extraFilters()
		n.setupUi(newTab)
		self.efTab = n
		self.efTab.MM3Box.setChecked(True)
		self.efTab.MM3Box.checkStateChanged.connect(lambda state, x=self.efTab.MM3Box: self.filterPreMM3Monsters(x))

		self.model : QStandardItemModel = QStandardItemModel()

		columnsList = [
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

		self.model.setHorizontalHeaderLabels(columnsList)
		self.set1 = set()
		self.set2 = set()

		self.templateSets : dict[str:list] = {
			"Backgrounds": [set(), set(), set(), set()],
			"Characters Themes": [set()],
			"Classes": [set(), set(), set(["Strength", "Dexterity", "Constitutiton", "Wisdom", "Intelligence", "Charisma"])],
			"Companions & Familiars": [set()],
			"Creatures": [range(0,36), set(), set(), range(0,275000), set(), set()],
			"Deities": [set()],
			"Diseases": [range(0,32)],
			"Epic Destinies": [set()],
			"Feats": [set(), set()],
			"Glossary": [set(), set()],
			"Items": [set(), set(), range(0,32), range(1, 3125000), set()],
			"Paragon Paths": [set()],
			"Poisons": [range(5,25), range(50, 156250)],
			"Powers": [range(0,32), set(), set(), set(), set(['Special'])],
			"Races": [set(), set()],
			"Rituals": [range(0,32), range(0,0), range(0,600000), set()],
			"Terrains": [set()],
			"Traps": [set(), set(), range(0,32), range(0,95000), set()]
		}

		self.populateModel()

		self.setupDDITable()

		self.SourceFilter = self.createSourceFilterProxy(self.model)
		self.preMM3Filter = self.createMM3FilterProxy(self.SourceFilter)
		self.CategoryFilter = self.createCategoryFilterProxy(self.preMM3Filter)
		self.SearchFilter = self.createSearchFilter(self.CategoryFilter)
		self.pfTab.setModel(self.SearchFilter)

		self.pfTab.registerNewTemplate("Backgrounds", ["Type", "Campaing Setting", "Prerequisite(s)", "Associated Skills"], self.templateSets["Backgrounds"])
		self.pfTab.registerNewTemplate("Characters Themes", ["Prerequisite(s)"], self.templateSets["Characters Themes"])
		self.pfTab.registerNewTemplate("Classes", ["Role", "Power Source", "Key Abilities"], self.templateSets["Classes"])
		self.pfTab.registerNewTemplate("Companions & Familiars", ["Type"], self.templateSets["Companions & Familiars"])
		self.pfTab.registerNewTemplate("Creatures", ["Level", "Main Role", "Group Role", "XP", "Size", "Keywords"], self.templateSets["Creatures"])
		self.pfTab.registerNewTemplate("Deities", ["Alignment"], self.templateSets["Deities"])
		self.pfTab.registerNewTemplate("Diseases", ["Level"], self.templateSets["Diseases"])
		self.pfTab.registerNewTemplate("Epic Destinies", ["Prerequisite(s)"], self.templateSets["Epic Destinies"])
		self.pfTab.registerNewTemplate("Feats", ["Tier", "Prerequisite(s)"], self.templateSets["Feats"])
		self.pfTab.registerNewTemplate("Glossary", ["Category", "Type"], self.templateSets["Glossary"])
		self.pfTab.registerNewTemplate("Items", ["Category", "Mundane", "Level", "Cost", "Rarity"], self.templateSets["Items"])
		self.pfTab.registerNewTemplate("Paragon Paths", ["Prerequisite(s)"], self.templateSets["Paragon Paths"])
		self.pfTab.registerNewTemplate("Poisons", ["Level", "Cost"], self.templateSets["Poisons"])
		self.pfTab.registerNewTemplate("Powers", ["Level", "Action", "Class", "Kind", "Usage"], self.templateSets["Powers"])
		self.pfTab.registerNewTemplate("Races", ["Ability Scores", "Size"], self.templateSets["Races"])
		self.pfTab.registerNewTemplate("Rituals", ["Level", "Component Cost", "Market Price", "Key Skill"], self.templateSets["Rituals"])
		self.pfTab.registerNewTemplate("Terrains", ["Type"], self.templateSets["Terrains"])
		self.pfTab.registerNewTemplate("Traps", ["Type", "Role", "Level", "XP", "Class"], self.templateSets["Traps"])

		self.BookmarkFilter = self.createBookmarkFilter(self.pfTab.getModel())
		self.SearchAll : bool = False
		self.Bookmarks : bool = False

		self.ddiTable.setModel(self.BookmarkFilter)
		self.ddiTable.selectionModel().selectionChanged.connect(self.itemSelected)
		self.statusTest : QStatusBar = None

	def registerRowCounter(self, sBar:QStatusBar) -> None:
		self.statusTest = sBar

	def updateRowCount(self) -> str:
		self.statusTest.showMessage(str(self.ddiTable.model().rowCount()))

	def filterPreMM3Monsters(self, cBox:QCheckBox):
		if cBox.isChecked():
			self.preMM3Filter.setFilterRegularExpression('')
		else:
			self.preMM3Filter.setFilterRegularExpression('Y')
		self.updateRowCount()

	def createBookmarkFilter(self, model:QAbstractItemModel) -> BookmarkbleFilterProxy:
		sFilter = BookmarkbleFilterProxy()
		sFilter.setFilterKeyColumn(0)
		sFilter.setFilterRole(DDITableItemRole.Bookmarked)
		sFilter.setSortRole(DDITableItemRole.test)
		sFilter.setDynamicSortFilter(True)
		sFilter.setSourceModel(model)
		return sFilter

	def createMM3FilterProxy(self, model:QAbstractItemModel) -> PinableFilterProxy:
		sFilter = PinableFilterProxy()
		sFilter.setFilterKeyColumn(0)
		sFilter.setFilterRole(DDITableItemRole.IsPostMM3)
		sFilter.setSourceModel(model)
		return sFilter

	def createSearchFilter(self, model:QAbstractItemModel) -> PinableFilterProxy:
		sFilter = PinableFilterProxy()
		sFilter.setSourceModel(model)
		sFilter.setFilterKeyColumn(1)
		sFilter.setFilterRole(0)
		sFilter.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		return sFilter

	def createSourcebookFilterTab(self, tab:QWidget):
		sfTab = DDISourceFilter()
		sfTab.setupUi(tab)
		sfTab.selectAll.clicked.connect(self.selectAll)
		sfTab.selectNone.clicked.connect(self.selectNone)
		for checkBox in sfTab.checkBoxes:
			checkBox.checkStateChanged.connect(lambda state, x=checkBox: self.sourceFilterChanged(x))
		return sfTab

	def createCategoryFilterProxy(self, model:QAbstractItemModel) -> PinableFilterProxy:
		sFilter = PinableFilterProxy()
		sFilter.setFilterKeyColumn(0)
		sFilter.setFilterRole(DDITableItemRole.Category)
		sFilter.setSourceModel(model)
		return sFilter

	def createSourceFilterProxy(self, model:QAbstractItemModel) -> PinableSourceFilterProxy:
		psFilter = PinableSourceFilterProxy()
		psFilter.setSourceModel(model)
		psFilter.setDynamicSortFilter(True)
		psFilter.setFilterRole(DDITableItemRole.Source)
		psFilter.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
		return psFilter

	def createFilterTab(self) -> QTabWidget:
		filterTab = QTabWidget()
		filterTab.setMinimumSize(625,0)
		filterTab.setMaximumWidth(625)
		return filterTab

	def addFilterTab(self, name:str) -> QWidget:
		newTab = QWidget()
		newTab.setObjectName(name)
		self.Filters.addTab(newTab, name)
		return newTab

	def createWebViewer(self) -> HTMLRenderer:
		wViewer = HTMLRenderer()
		return wViewer

	def selectAll(self):
		self.SourceFilter.selectALL()
		self.SourceFilter.setFilterRegularExpression('')

	def selectNone(self):
		self.SourceFilter.selectNone()
		self.SourceFilter.setFilterRegularExpression('')

	def setupDDITable(self) -> None:
		#self.ddiTable.setModel(self.model)
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
		for category in Categories:
			newComboBox.addItem(category.title, category)
		newComboBox.currentIndexChanged.connect(lambda data, cBox=newComboBox: self.changeTable(cBox))
		self.changeTable(newComboBox)
		return newComboBox

	def createFilterLine(self) -> QLineEdit:
		newLineEdit = QLineEdit()
		newLineEdit.setMinimumSize(150,15)
		newLineEdit.setMaximumSize(150,35)
		newLineEdit.textEdited.connect(lambda data: self.textChanged(data))
		return newLineEdit

	def createFilters(self) -> QPushButton:
		newButton = QPushButton('Filters')
		newButton.clicked.connect(self.changeView)
		return newButton

	def createSearchAllCheck(self) -> QCheckBox:
		newAllBox = QCheckBox('All')
		newAllBox.checkStateChanged.connect(self.changeSearchAll)
		return newAllBox

	def changeSearchAll(self):
		self.SearchAll = not self.SearchAll
		if self.SearchAll:
			self.SearchFilter.setFilterKeyColumn(-1)
		else:
			self.SearchFilter.setFilterKeyColumn(1)

	def createBookmarkButton(self) -> QPushButton:
		newButton = QPushButton('Bookmarks')
		newButton.clicked.connect(self.searchBookmarks)
		return newButton

	def searchBookmarks(self):
		self.BookmarkFilter.flipIsFilterOn()
		self.BookmarkFilter.setFilterRegularExpression('')
		self.updateRowCount()

	def changeView(self):
		self.gL_2.replaceWidget(self.swap1, self.swap2)
		self.webViewer.setVisible(not self.webViewer.isVisible())
		self.Filters.setVisible(not self.Filters.isVisible())
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
		action5.triggered.connect(lambda: self.actionBookmark(index))

		action6 = cMenu.addAction("Remove Bookmark")
		action6.triggered.connect(lambda: self.actionRemoveBookmark(index))

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

	def actionBookmark(self, index: QModelIndex) -> None:
		self.ddiTable.model().setData(index, True, DDITableItemRole.Bookmarked)

	def actionRemoveBookmark(self, index: QModelIndex) -> None:
		self.ddiTable.model().setData(index, False, DDITableItemRole.Bookmarked)

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
		newRow.setData(False, DDITableItemRole.Bookmarked)
		newRow.setData(ddiObject.getSource(), DDITableItemRole.Source)
		newRow.setData('Y', DDITableItemRole.IsPostMM3)
		if isinstance(ddiObject, Monster) and not ddiObject.getIsPostMM3():
			newRow.setData('N', DDITableItemRole.IsPostMM3)

		self.model.appendRow(newRow)

	def populateRow(self, row: int, ddiObject: ddiObject) -> None:
		newItem = QStandardItem(ddiObject.getName())
		newItem.setData(ddiObject.getName(), DDITableItemRole.test)
		self.model.setItem(row, 1, newItem)

		match ddiObject.getType():
			case Types.ASSOCIATE:
				newItem2 = QStandardItem(ddiObject.getTypeA())
				newItem2.setData(ddiObject.getTypeA(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				self.templateSets["Companions & Familiars"][0].add(ddiObject.getTypeA())
			case Types.BACKGROUND:
				newItem2 = QStandardItem(ddiObject.getTypeB())
				newItem2.setData(ddiObject.getTypeB(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getCampaign())
				newItem2.setData(ddiObject.getCampaign(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				newItem2 = QStandardItem(ddiObject.getPrerequisite())
				newItem2.setData(ddiObject.getPrerequisite(), DDITableItemRole.test)
				self.model.setItem(row, 4, newItem2)

				newItem2 = QStandardItem(ddiObject.getSkills())
				newItem2.setData(ddiObject.getSkills(), DDITableItemRole.test)
				self.model.setItem(row, 5, newItem2)


				self.templateSets["Backgrounds"][0].add(ddiObject.getTypeB())
				self.templateSets["Backgrounds"][1].add(ddiObject.getCampaign())

				for string in ddiObject.getPrerequisite().replace(', or ', ';;').replace(' or ', ';;').replace(', ', ';;').replace(',', ';;').split(';;'):
					self.templateSets["Backgrounds"][2].add(string)

				for string in ddiObject.getSkills().replace(', ', ';;').replace(',', ';;').split(';;'):
					self.templateSets["Backgrounds"][3].add(string)
			case Types.CLASS:
				newItem2 = QStandardItem(ddiObject.getRole())
				newItem2.setData(ddiObject.getRole(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getPower())
				newItem2.setData(ddiObject.getPower(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				newItem2 = QStandardItem(ddiObject.getAbilities())
				newItem2.setData(ddiObject.getAbilities(), DDITableItemRole.test)
				self.model.setItem(row, 4, newItem2)

				for string in ddiObject.getRole().split(' and '):
					self.templateSets["Classes"][0].add(string)
				self.templateSets["Classes"][1].add(ddiObject.getPower())
			case Types.COMPANION:
				newItem2 = QStandardItem(ddiObject.getTypeC())
				newItem2.setData(ddiObject.getTypeC(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				self.templateSets["Companions & Familiars"][0].add(ddiObject.getTypeC())
			case Types.DEITY:
				newItem2 = QStandardItem(ddiObject.getAlignment())
				newItem2.setData(ddiObject.getAlignment(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				self.templateSets["Deities"][0].add(ddiObject.getAlignment())
			case Types.DISEASE:
				newItem2 = QStandardItem()
				newItem2.setData(ddiObject.getLevel(), Qt.ItemDataRole.DisplayRole)
				newItem2.setData(ddiObject.getLevel(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)
			case Types.EPICDESTINY:
				newItem2 = QStandardItem(ddiObject.getPrerequisite())
				newItem2.setData(ddiObject.getPrerequisite(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				self.templateSets["Epic Destinies"][0].add(ddiObject.getPrerequisite())
			case Types.FEAT:
				newItem2 = QStandardItem(ddiObject.getTier())
				newItem2.setData(ddiObject.getTier(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getPrerequisite())
				newItem2.setData(ddiObject.getPrerequisite(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				self.templateSets["Feats"][0].add(ddiObject.getTier())

				for string in ddiObject.getPrerequisite().split(', '):
					self.templateSets["Feats"][1].add(string)
			case Types.GLOSSARY:
				newItem2 = QStandardItem(ddiObject.getTypeG())
				newItem2.setData(ddiObject.getTypeG(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getCategory())
				newItem2.setData(ddiObject.getCategory(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				self.templateSets["Glossary"][0].add(ddiObject.getTypeG())
				self.templateSets["Glossary"][1].add(ddiObject.getCategory())
			case Types.ITEM:
				newItem2 = QStandardItem(ddiObject.getCategory())
				newItem2.setData(ddiObject.getCategory(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				if ddiObject.getIsMundane():
					newItem2 = QStandardItem("Yes")
					newItem2.setData("Yes", DDITableItemRole.test)
					self.model.setItem(row, 3, newItem2)
					self.templateSets["Items"][1].add("Yes")
				else:
					newItem2 = QStandardItem("No")
					newItem2.setData("No", DDITableItemRole.test)
					self.model.setItem(row, 3, newItem2)
					self.templateSets["Items"][1].add("No")

				newItem2 = QStandardItem(ddiObject.getLevel())
				level : int = 0
				if ddiObject.getLevel() == 'Heroic':
					level = 10
				elif ddiObject.getLevel() == 'Paragon':
					level = 11
				elif ddiObject.getLevel() == 'Epic':
					level = 21
				elif ddiObject.getLevel() == 'None':
					level = 0
				else:
					level = int(ddiObject.getLevel().replace('+', ''))
				newItem2.setData(level, DDITableItemRole.test)
				self.model.setItem(row, 4, newItem2)

				newItem2 = QStandardItem(ddiObject.getCost())
				cost : int = 0
				if ddiObject.getCost() == 'None':
					cost = -1
				else:
					cost = int(ddiObject.getCost().replace(',', '').replace('.', '').replace('+', '').replace(' gp', ''))
				newItem2.setData(cost, DDITableItemRole.test)
				self.model.setItem(row, 5, newItem2)

				newItem2 = QStandardItem(ddiObject.getRarity())
				newItem2.setData(ddiObject.getRarity(), DDITableItemRole.test)
				self.model.setItem(row, 6, newItem2)


				self.templateSets["Items"][0].add(ddiObject.getCategory())

				self.templateSets["Items"][4].add(ddiObject.getRarity())
			case Types.MONSTER:
				newItem2 = QStandardItem(str(ddiObject.getLevel()))
				newItem2.setData(ddiObject.getLevel(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getRole())
				newItem2.setData(ddiObject.getRole(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				newItem2 = QStandardItem(ddiObject.getModifier())
				newItem2.setData(ddiObject.getModifier(), DDITableItemRole.test)
				self.model.setItem(row, 4, newItem2)

				newItem2 = QStandardItem(str(ddiObject.getXP()))
				newItem2.setData(ddiObject.getXP(), DDITableItemRole.test)
				self.model.setItem(row, 5, newItem2)

				newItem2 = QStandardItem(ddiObject.getSize())
				newItem2.setData(ddiObject.getSize(), DDITableItemRole.test)
				self.model.setItem(row, 6, newItem2)

				newItem2 = QStandardItem(ddiObject.getKeywords())
				newItem2.setData(ddiObject.getKeywords(), DDITableItemRole.test)
				self.model.setItem(row, 7, newItem2)

				for string in ddiObject.getRole().split(', '):
					self.templateSets["Creatures"][1].add(string)
				self.templateSets["Creatures"][2].add(ddiObject.getModifier())
				self.templateSets["Creatures"][4].add(ddiObject.getSize())
			case Types.PARAGONPATH:
				newItem2 = QStandardItem(ddiObject.getPrerequisite())
				newItem2.setData(ddiObject.getPrerequisite(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				self.templateSets["Paragon Paths"][0].add(ddiObject.getPrerequisite())
			case Types.POISON:
				newItem2 = QStandardItem(str(ddiObject.getLevel()))
				newItem2.setData(ddiObject.getLevel(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getCost()+" gp")
				newItem2.setData(int(ddiObject.getCost()), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)
			case Types.POWER:
				newItem2 = QStandardItem(str(ddiObject.getLevel()))
				newItem2.setData(ddiObject.getLevel(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)


				newItem2 = QStandardItem(ddiObject.getAction())
				newItem2.setData(ddiObject.getAction(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				newItem2 = QStandardItem(ddiObject.getClass())
				newItem2.setData(ddiObject.getClass(), DDITableItemRole.test)
				self.model.setItem(row, 4, newItem2)

				newItem2 = QStandardItem(ddiObject.getKind())
				newItem2.setData(ddiObject.getKind(), DDITableItemRole.test)
				self.model.setItem(row, 5, newItem2)

				newItem2 = QStandardItem(ddiObject.getUsage())
				newItem2.setData(ddiObject.getUsage(), DDITableItemRole.test)
				self.model.setItem(row, 6, newItem2)

				self.templateSets["Powers"][1].add(ddiObject.getAction())
				self.templateSets["Powers"][2].add(ddiObject.getClass())
				self.templateSets["Powers"][3].add(ddiObject.getKind())
				for string in ddiObject.getUsage().replace(' (Special)', '').split(','):
					self.templateSets["Powers"][4].add(string)

			case Types.RACE:
				newItem2 = QStandardItem(ddiObject.getDescription())
				newItem2.setData(ddiObject.getDescription(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getSize())
				newItem2.setData(ddiObject.getSize(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				for string in ddiObject.getDescription().replace('+2 ', '').split(', '):
					self.templateSets["Races"][0].add(string)
				self.templateSets["Races"][1].add(ddiObject.getSize())
			case Types.RITUAL:
				newItem2 = QStandardItem(str(ddiObject.getLevel()))
				newItem2.setData(ddiObject.getLevel(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getComponent())
				newItem2.setData(ddiObject.getComponent(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				newItem2 = QStandardItem(str(ddiObject.getPrice())+' gp')
				newItem2.setData(ddiObject.getPrice(), DDITableItemRole.test)
				self.model.setItem(row, 4, newItem2)

				newItem2 = QStandardItem(ddiObject.getKeySkill())
				newItem2.setData(ddiObject.getKeySkill(), DDITableItemRole.test)
				self.model.setItem(row, 5, newItem2)

				for string in ddiObject.getKeySkill().split(' or '):
					self.templateSets["Rituals"][3].add(string)
			case Types.TERRAIN:
				newItem2 = QStandardItem(ddiObject.getTypeT())
				newItem2.setData(ddiObject.getTypeT(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				self.templateSets["Terrains"][0].add(ddiObject.getTypeT())
			case Types.THEME:
				newItem2 = QStandardItem(ddiObject.getPrerequisite())
				newItem2.setData(ddiObject.getPrerequisite(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				self.templateSets["Characters Themes"][0].add(ddiObject.getPrerequisite())
			case Types.TRAP:
				newItem2 = QStandardItem(ddiObject.getTypeT())
				newItem2.setData(ddiObject.getTypeT(), DDITableItemRole.test)
				self.model.setItem(row, 2, newItem2)

				newItem2 = QStandardItem(ddiObject.getRole())
				newItem2.setData(ddiObject.getRole(), DDITableItemRole.test)
				self.model.setItem(row, 3, newItem2)

				if ddiObject.getLevel().isnumeric():
					newItem2 = QStandardItem(ddiObject.getLevel())
					newItem2.setData(int(ddiObject.getLevel()), DDITableItemRole.test)
					self.model.setItem(row, 4, newItem2)
				else:
					newItem2 = QStandardItem('*')
					newItem2.setData(0, DDITableItemRole.test)
					self.model.setItem(row, 4, newItem2)

				if ddiObject.getXP() != -1:
					newItem2 = QStandardItem(str(ddiObject.getXP()))
					newItem2.setData(ddiObject.getXP(), DDITableItemRole.test)
					self.model.setItem(row, 5, newItem2)
				else:
					newItem2 = QStandardItem('*')
					newItem2.setData(0, DDITableItemRole.test)
					self.model.setItem(row, 5, newItem2)

				newItem2 = QStandardItem(ddiObject.getClasse())
				newItem2.setData(ddiObject.getClasse(), DDITableItemRole.test)
				self.model.setItem(row, 6, newItem2)

				self.templateSets["Traps"][0].add(ddiObject.getTypeT())
				self.templateSets["Traps"][1].add(ddiObject.getRole())
				self.templateSets["Traps"][4].add(ddiObject.getClasse())

		self.model.setItem(row, 8, QStandardItem(ddiObject.getSource()))

	def populateModel(self) -> None:
		ddiEntry : ddiObject
		for type in Types:
			for ddiEntry in self.DDIData[type.title]:
				self.createRow(ddiEntry)
				self.populateRow(self.model.rowCount()-1, ddiEntry)

	def itemSelected(self):
		try:
			self.webViewer.renderHTML(self.ddiTable.model().index(self.ddiTable.currentIndex().row(), 0).data(32).getHTML())
			if self.swap1 != self.webViewer:
				self.changeView()
		except:
			pass

	def textChanged(self, text: str) -> None:
		self.SearchFilter.setFilterRegularExpression(text)
		self.updateRowCount()

	def changeTable(self, cBox:QComboBox) -> None:
		category = cBox.itemData(cBox.currentIndex(), Qt.ItemDataRole.UserRole)
		if category is Categories.ALL:
			self.CategoryFilter.setFilterRegularExpression('')
			self.pfTab.changeTemplate("")
		else:
			self.CategoryFilter.setFilterRegularExpression(category.title)
			self.pfTab.changeTemplate(category.title)

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

		self.ddiTable.horizontalHeader().resizeSections(QHeaderView.ResizeMode.Stretch)

		#set horizontal header zero to it's ideal size
		self.ddiTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		idealSize = self.ddiTable.horizontalHeader().sectionSize(0)
		self.ddiTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
		self.ddiTable.horizontalHeader().resizeSection(0, idealSize)
		self.updateRowCount()

	def sourceFilterChanged(self, cb:DataQCheckBox):
		self.SourceFilter.flipSource(cb.data)
		self.SourceFilter.setFilterRegularExpression('')
		self.updateRowCount()