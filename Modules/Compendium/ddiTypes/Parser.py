from . import Files, Types
from .ddiObjects import *

from threading import Thread
from queue import Queue



class Parser:
	def __init__(self):
		self.sqlPath = "sql/"
		self.files = Files
		self.stripHTML = ["\\r", "\\n", "\\"]

	def fileParse(self, file, list: dict, sQueue: Queue):
		linesInFile = []
		try:
			with open(self.sqlPath + file.value, 'r') as ddiFile:
				for lineOfFile in ddiFile:
					if lineOfFile.startswith("INSERT"):
						lineOfFile = lineOfFile.strip()
						lineOfFileStart = lineOfFile.find("('")+2
						lineOfFileEnd = len(lineOfFile)-3
						linesInFile.append(lineOfFile[lineOfFileStart:lineOfFileEnd])
		except:
			print("No such file:" + self.sqlPath + file.value)

		for lineOfFile in linesInFile:
			lineTokens = lineOfFile.split("','")
			match file.type:
				case Types.ASSOCIATE:
					list[file.type.value].append(self.associateParse(lineTokens, Types.ASSOCIATE))
				case Types.BACKGROUND:
					list[file.type.value].append(self.backgroundParse(lineTokens, Types.BACKGROUND))
				case Types.CLASS:
					list[file.type.value].append(self.classParse(lineTokens, Types.CLASS))
				case Types.COMPANION:
					list[file.type.value].append(self.companionParse(lineTokens, Types.COMPANION))
				case Types.DEITY:
					list[file.type.value].append(self.deityParse(lineTokens, Types.DEITY))
				case Types.DISEASE:
					list[file.type.value].append(self.diseaseParse(lineTokens, Types.DISEASE))
				case Types.EPICDESTINY:
					list[file.type.value].append(self.epicdestinyParse(lineTokens, Types.EPICDESTINY))
				case Types.FEAT:
					list[file.type.value].append(self.featParse(lineTokens, Types.FEAT))
				case Types.GLOSSARY:
					list[file.type.value].append(self.glossaryParse(lineTokens, Types.GLOSSARY))
				case Types.ITEM:
					list[file.type.value].append(self.itemParse(lineTokens, Types.ITEM))
				case Types.MONSTER:
					list[file.type.value].append(self.monsterParse(lineTokens, Types.MONSTER))
				case Types.PARAGONPATH:
					list[file.type.value].append(self.paragonpathParse(lineTokens, Types.PARAGONPATH))
				case Types.POISON:
					list[file.type.value].append(self.poisonParse(lineTokens, Types.POISON))
				case Types.POWER:
					list[file.type.value].append(self.powerParse(lineTokens, Types.POWER))
				case Types.RACE:
					list[file.type.value].append(self.raceParse(lineTokens, Types.RACE))
				case Types.RITUAL:
					list[file.type.value].append(self.ritualParse(lineTokens, Types.RITUAL))
				case Types.SKILL:
					list[file.type.value].append(self.skillParse(lineTokens, Types.SKILL))
				case Types.TERRAIN:
					list[file.type.value].append(self.terrainParse(lineTokens, Types.TERRAIN))
				case Types.THEME:
					list[file.type.value].append(self.themeParse(lineTokens, Types.THEME))
				case Types.TRAP:
					list[file.type.value].append(self.trapParse(lineTokens, Types.TRAP))
		sQueue.put(list)


	def buildDDIObjects(self, ddiDict: dict[str:list]):
		sharedQueue = Queue()
		threads = []

		file : Files
		for file in self.files:
			newDict = {file.type.value: []}
			thread = Thread(target=self.fileParse, args=(file, newDict, sharedQueue))
			threads.append(thread)

		t : Thread
		for t in threads:
			t.start()

		t : Thread
		for t in threads:
			t.join()

		while not sharedQueue.empty():
			subDDIDict : dict = sharedQueue.get()
			for ddiType in subDDIDict:
				ddiDict[ddiType] = subDDIDict[ddiType]

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
		preStart = html.find("<b>Prerequisite</b>: ")
		if(preStart == -1):
			preStart = html.find("<b>Prerequisite: </b>")

		if(preStart != -1):
			preEnd = html.find("<br/>", preStart)
			if(preEnd != -1):
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

	def associateParse(self, tokens: list, type: Types):
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

	def backgroundParse(self, tokens: list, type: Types):
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

	def classParse(self, tokens:list[str], type:Types):
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

	def companionParse(self, tokens:list[str], type:Types):
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

	def deityParse(self, tokens:list[str], type:Types):
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

	def diseaseParse(self, tokens:list[str], type:Types):
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

	def epicdestinyParse(self, tokens:list[str], type:Types):
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

	def featParse(self, tokens:list[str], type:Types):
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

	def glossaryParse(self, tokens:list[str], type:Types):
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

	def itemParse(self, tokens:list[str], type:Types):
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

	def monsterParse(self, tokens:list[str], type:Types):
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

	def paragonpathParse(self, tokens:list[str], type:Types):
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

	def poisonParse(self, tokens:list[str], type:Types):
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

	def powerParse(self, tokens:list[str], type: Types):
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

	def raceParse(self, tokens:list[str], type: Types):
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

	def ritualParse(self, tokens:list[str], type: Types):
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

	def skillParse(self, tokens:list[str], type: Types):
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

	def terrainParse(self, tokens:list[str], type: Types):
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

	def themeParse(self, tokens:list[str], type: Types):
		t = Theme()
		t.setColor('#1d3d5e')
		t.setID(tokens[0])
		t.setName(self.processString(tokens[1]))
		t.setSource(self.processString(tokens[2]))
		t.setHTML(self.processHTML(tokens[3]))
		t.setPrerequisite(self.retrivePrerequisite(tokens[3]))
		t.setType(type)
		return t

	def trapParse(self, tokens:list[str], type: Types):
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