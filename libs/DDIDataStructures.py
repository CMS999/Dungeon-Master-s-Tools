from enum import Enum
from dataclasses import dataclass

__all__ = ["Categories", "Types", "Files", "ddiObject", "Associate", "Background", "Classe", "Companion", "Deity", "Disease", "EpicDestiny", "Feat", "Glossary", "Item", "Monster", "ParagonPath", "Poison", "Power", "Race", "Ritual", "Skill", "Terrain", "Theme", "Trap"]

@dataclass
class CategoryData:
	title : str
	fields : list[str]

class Categories(CategoryData, Enum):
	ALL = "All", ["", "Name", "Source"]
	BACKGROUND = "Backgrounds", ["", "Name", "Type", "Campaing Setting", "Prerequisite(s)", "Associated Skills"]
	CHARACTERSTHEME = "Characters Themes", ["", "Name", "Prerequisite(s)"]
	CLASSES = "Classes", ["", "Name", "Role", "Power Source", "Key Abilities"]
	COMPANIONSFAMILIARS = "Companions & Familiars", ["", "Name", "Type"]
	CREATURES = "Creatures", ["", "Name", "Level", "Main Role", "Group Role", "XP", "Size", "Keywords"]
	DEITIES = "Deities", ["", "Name", "Alignment"]
	DISEASES = "Diseases", ["", "Name", "Level"]
	EPICDESTINIES = "Epic Destinies", ["", "Name", "Prerequisite(s)"]
	FEATS = "Feats", ["", "Name", "Tier", "Prerequisite(s)"]
	GLOSSARY = "Glossary", ["", "Name", "Category", "Type"]
	ITEMS = "Items", ["", "Name", "Category", "Mundane", "Level", "Cost", "Rarity"]
	PARAGONPATHS = "Paragon Paths", ["", "Name", "Prerequisite(s)"]
	POISONS = "Poisons", ["", "Name", "Level", "Cost"]
	POWERS = "Powers", ["", "Name", "Level", "Action", "Class", "Kind", "Usage"]
	RACES = "Races", ["", "Name", "Ability Scores", "Size"]
	RITUALS = "Rituals", ["", "Name", "Level", "Component Cost", "Market Price", "Key Skill"]
	TERRAIN = "Terrains", ["", "Name", "Type"]
	TRAP = "Traps", ["", "Name", "Type", "Role", "Level", "XP", "Class"]

@dataclass
class TypesData:
	title : str
	fields : list[str]
	category : Categories

class Types(TypesData, Enum):
	ASSOCIATE = "Associate", ["ID", "Name", "Type", "Source", "Teaser", "HTML"], Categories.COMPANIONSFAMILIARS
	BACKGROUND = "Background", ["ID", "Name", "Type", "Campaign", "Skills", "Source", "Teaser", "HTML"], Categories.BACKGROUND
	CLASS = "Class", ["ID", "Name", "Power", "Role", "Abilities", "IsNew", "IsChanged", "Source", "Teaser", "HTML"], Categories.CLASSES
	COMPANION = "Companion", ["ID", "Name", "Type", "Source", "Teaser", "HTML"], Categories.COMPANIONSFAMILIARS
	DEITY = "Deity", ["ID", "Name", "Alignment", "Source", "Teaser", "HTML"], Categories.DEITIES
	DISEASE = "Disease", ["ID", "Name", "Level", "Source", "Teaser", "HTML"], Categories.DISEASES
	EPICDESTINY = "Epic Destiny", ["ID", "Name", "Prerequisite", "IsNew", "IsChanged", "Source", "Teaser", "HTML"], Categories.EPICDESTINIES
	FEAT = "Feat", ["ID", "Name", "IsNew", "IsChanged", "Source", "Tier", "Sort", "Teaser", "HTML"], Categories.FEATS
	GLOSSARY = "Glossary", ["ID", "Name", "Category", "Type", "Source", "Teaser", "HTML"], Categories.GLOSSARY
	ITEM = "Item", ["ID", "Name", "Cost", "Level", "Category", "Enhancement", "IsMundade", "FinalCost", "Source", "Teaser", "HTML", "Rarity", "CostSort", "LevelSort"], Categories.ITEMS
	MONSTER = "Monster", ["ID", "Name", "Level", "Modifier", "Role", "IsNew", "IsChanged", "Source", "Teaser", "HTML", "XP", "Keywords"], Categories.CREATURES
	PARAGONPATH = "Paragon Path", ["ID", "Name", "Prerequisite", "Sourcer", "Teaser", "HTML"], Categories.PARAGONPATHS
	POISON = "Poison", ["ID", "Name", "Level", "Cost", "Source", "Teaser", "HTML"], Categories.POISONS
	POWER = "Power", ["ID", "Name", "Level", "Action", "IsNew", "IsChanged", "Source", "Class", "Teaser", "HTML", "Kind", "Usage"], Categories.POWERS
	RACE = "Race", ["ID", "Name", "Size", "Description", "IsNew", "IsChanged", "Source", "Teaser", "HTML"], Categories.RACES
	RITUAL = "Ritual", ["ID", "Name", "Level", "Component", "Price", "KeySkill", "Source", "Teaser", "HTML"], Categories.RITUALS
	SKILL = "Skill", ["ID", "Name", "Category", "Type", "Source", "Teaser", "HTML"], Categories.GLOSSARY
	TERRAIN = "Terrain", ["ID", "Name", "Type", "Source", "Teaser", "HTML"], Categories.TERRAIN
	THEME = "Theme", ["ID", "Name", "Source", "HTML"], Categories.CHARACTERSTHEME
	TRAP = "Trap", ["ID", "Name", "Role", "Type", "Level", "Source", "Teaser", "HTML", "Class"], Categories.TRAP

@dataclass
class FilesData:
	file : str
	type : Types

class Files(FilesData, Enum):
	DDIASSOCIATE = "ddiAssociate.sql", Types.ASSOCIATE
	DDIBACKGROUND = "ddiBackground.sql", Types.BACKGROUND
	DDICLASS = "ddiClass.sql", Types.CLASS
	DDICOMPANION = "ddiCompanion.sql", Types.COMPANION
	DDIDEITY = "ddiDeity.sql", Types.DEITY
	DDIDISEASE = "ddiDisease.sql", Types.DISEASE
	DDIEPICDESTINY = "ddiEpicDestiny.sql", Types.EPICDESTINY
	DDIFEAT = "ddiFeat.sql", Types.FEAT
	DDIGLOSSARY = "ddiGlossary.sql", Types.GLOSSARY
	DDIITEM = "ddiItem.sql", Types.ITEM
	DDIMONSTER = "ddiMonster.sql", Types.MONSTER
	DDIPARAGONPATH = "ddiParagonPath.sql", Types.PARAGONPATH
	DDIPOISON = "ddiPoison.sql", Types.POISON
	DDIPOWER = "ddiPower.sql", Types.POWER
	DDIRACE = "ddiRace.sql", Types.RACE
	DDIRITUAL = "ddiRitual.sql", Types.RITUAL
	DDISKILL = "ddiSkill.sql", Types.SKILL
	DDITERRAIN = "ddiTerrain.sql", Types.TERRAIN
	DDITHEME = "ddiTheme.sql", Types.THEME
	DDITRAP = "ddiTrap.sql", Types.TRAP

class ddiObject():
	def __init__(self):
		self.color : str = ''
		self.ID : int = -1
		self.Name : str = ''
		self.Source : str = ''
		self.HTML : str = ''
		self.type : Types = None

	def setColor(self, color: str):
		self.color = color

	def setID(self, ID: str):
		self.ID = int(ID)

	def setName(self, Name: str):
		self.Name = Name

	def setSource(self, Source: str):
		self.Source = Source

	def setHTML(self, HTML: str):
		self.HTML = HTML

	def setType(self, Type: Types):
		self.type = Type

	def getColor(self) -> str:
		return self.color

	def getID(self) -> int:
		return self.ID

	def getName(self) -> str:
		return self.Name

	def getSource(self) -> str:
		return self.Source

	def getHTML(self) -> str:
		return self.HTML

	def getType(self) -> Types:
		return self.type

class Associate(ddiObject):
	def __init__(self):
		super().__init__()
		self.TypeA : str = ''
		self.Teaser : int = 0

	def setTypeA(self, Type: str):
		self.TypeA = Type

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getTypeA(self) -> str:
		return self.TypeA

	def getTeaser(self) -> int:
		return self.Teaser

class Background(ddiObject):
	def __init__(self):
		super().__init__()
		self.TypeB : str = ''
		self.Campaign : str = ''
		self.Skills : str = ''
		self.Teaser : int = 0
		self.prerequisite : str = ''

	def setTypeB(self, TypeB: str):
		self.TypeB = TypeB

	def setCampaign(self, Campaign: str):
		self.Campaign = Campaign

	def setSkills(self, Skills: str):
		self.Skills = Skills

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def setPrerequisite(self, prerequisite: str):
		self.prerequisite = prerequisite

	def getTypeB(self) -> str:
		return self.TypeB

	def getCampaign(self) -> str:
		return self.Campaign

	def getSkills(self) -> str:
		return self.Skills

	def getTeaser(self) -> int:
		return self.Teaser

	def getPrerequisite(self) -> str:
		return self.prerequisite

class Classe(ddiObject):
	def __init__(self):
		super().__init__()
		self.Power : str = ''
		self.Role : str = ''
		self.Abilities : str = ''
		self.IsNew : bool = False
		self.IsChanged : bool = False
		self.Teaser : int = 0

	def setPower(self, Power: str):
		self.Power = Power

	def setRole(self, Role: str):
		self.Role = Role

	def setAbilities(self, Abilities: str):
		self.Abilities = Abilities

	def setIsNew(self, IsNew: str):
		self.IsNew = bool(int(IsNew))

	def setIsChanged(self, IsChanged: str):
		self.IsChanged = bool(int(IsChanged))

	def setTeaser(self, Teaser: str):
		self.Teaser = Teaser

	def getPower(self) -> str:
		return self.Power

	def getRole(self) -> str:
		return self.Role

	def getAbilities(self) -> str:
		return self.Abilities

	def getIsNew(self) -> bool:
		return self.IsNew

	def getIsChanged(self) -> bool:
		return self.IsChanged

	def getTeaser(self) -> int:
		return self.Teaser

class Companion(ddiObject):
	def __init__(self):
		super().__init__()
		self.TypeC : str = ''
		self.Teaser : int = 0

	def setTypeC(self, TypeC: str):
		self.TypeC = TypeC

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getTypeC(self) -> str:
		return self.TypeC

	def getTeaser(self) -> int:
		return self.Teaser

class Deity(ddiObject):
	def __init__(self):
		super().__init__()
		self.Alignment : str = ''
		self.Teaser : int = 0

	def setAlignment(self, Alignment: str):
		self.Alignment = Alignment

	def setTeaser(self, Teaser: str):
		self.Teaser = Teaser

	def getAlignment(self) -> str:
		return self.Alignment

	def getTeaser(self) -> int:
		return self.Teaser

class Disease(ddiObject):
	def __init__(self):
		super().__init__()
		self.Level : int = 0
		self.Teaser : int = 0

	def setLevel(self, Level: str):
		self.Level = int(Level)

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getLevel(self) -> int:
		return self.Level

	def getTeaser(self) -> int:
		return self.Teaser

class EpicDestiny(ddiObject):
	def __init__(self):
		super().__init__()
		self.Prerequisite : str = ''
		self.IsNew : bool = False
		self.IsChanged : bool = False
		self.Teaser : int = 0

	def setPrerequisite(self, Prerequisite: str):
		self.Prerequisite = Prerequisite

	def setIsNew(self, IsNew: str):
		self.IsNew = bool(int(IsNew))

	def setIsChanged(self, IsChanged: str):
		self.IsChanged = bool(int(IsChanged))

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getPrerequisite(self) -> str:
		return self.Prerequisite

	def getIsNew(self) -> bool:
		return self.IsNew

	def getIsChanged(self) -> bool:
		return self.IsChanged

	def getTeaser(self) -> int:
		return self.Teaser

class Feat(ddiObject):
	def __init__(self):
		super().__init__()
		self.IsNew : bool = False
		self.IsChanged : bool = False
		self.Tier : str = ''
		self.Sort : int = 0
		self.Teaser : int = 0
		self.Prerequisite : str = ''

	def setIsNew(self, IsNew: str):
		self.IsNew = bool(int(IsNew))

	def setIsChanged(self, IsChanged: str):
		self.IsChanged = bool(int(IsChanged))

	def setTier(self, Tier: str):
		self.Tier = Tier

	def setSort(self, Sort: str):
		self.Sort = int(Sort)

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def setPrerequisite(self, Prerequisite: str):
		self.Prerequisite = Prerequisite

	def getIsNew(self) -> bool:
		return self.IsNew

	def getIsChanged(self) -> bool:
		return self.IsChanged

	def getTier(self) -> str:
		return self.Tier

	def getSort(self) -> int:
		return self.Sort

	def getTeaser(self) -> int:
		return self.Teaser

	def getPrerequisite(self) -> str:
		return self.Prerequisite

class Glossary(ddiObject):
	def __init__(self):
		super().__init__()
		self.Category : str = ''
		self.TypeG : str = ''
		self.Teaser : int = 0

	def setCategory(self, Category: str):
		self.Category = Category

	def setTypeG(self, TypeG: str):
		self.TypeG = TypeG

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getCategory(self) -> str:
		return self.Category

	def getTypeG(self) -> str:
		return self.TypeG

	def getTeaser(self) -> int:
		return self.Teaser

class Item(ddiObject):
	def __init__(self):
		super().__init__()
		self.Cost : str = ''
		self.Level : str = ''
		self.Category : str = ''
		self.Enhancement : str = ''
		self.IsMundane : bool = False
		self.FinalCost : str = ''
		self.Teaser : int = 0
		self.Rarity : str = ''
		self.CostSort : int = 0
		self.LevelSort : int = 0

	def setCost(self, Cost: str):
		self.Cost = Cost

	def setLevel(self, Level: str):
		self.Level = Level

	def setCategory(self, Category: str):
		self.Category = Category

	def setEnhancement(self, Enhancement: str):
		self.Enhancement = Enhancement

	def setIsMundane(self, IsMundane: str):
		self.IsMundane = bool(int(IsMundane))

	def setFinalCost(self, FinalCost: str):
		self.FinalCost = FinalCost

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def setRarity(self, Rarity: str):
		self.Rarity = Rarity

	def setCostSort(self, CostSort: str):
		self.CostSort = int(CostSort)

	def setLevelSort(self, LevelSort: str):
		self.LevelSort = int(LevelSort)

	def getCost(self) -> str:
		return self.Cost

	def getLevel(self) -> str:
		return self.Level

	def getCategory(self) -> str:
		return self.Category

	def getEnhancement(self) -> str:
		return self.Enhancement

	def getIsMundane(self) -> bool:
		return self.IsMundane

	def getFinalCost(self) -> str:
		return self.FinalCost

	def getTeaser(self) -> int:
		return self.Teaser

	def getRarity(self) -> str:
		return self.Rarity

	def getCostSort(self) -> int:
		return self.CostSort

	def getLevelSort(self) -> int:
		return self.LevelSort

class Monster(ddiObject):
	def __init__(self):
		super().__init__()
		self.Level : int = 0
		self.Modifier : str = ''
		self.Role : str = ''
		self.IsNew : bool = False
		self.IsChanged : bool = False
		self.Teaser : int = 0
		self.XP : int = 0
		self.Keywords : str = ''
		self.Size : str = ''
		self.IsPostMM3 : bool = False

	def setLevel(self, Level: str):
		self.Level = int(Level)

	def setModifier(self, Modifier: str):
		self.Modifier = Modifier

	def setRole(self, Role: str):
		self.Role = Role

	def setIsNew(self, IsNew: str):
		self.IsNew = bool(int(IsNew))

	def setIsChanged(self, IsChanged: str):
		self.IsChanged = bool(int(IsChanged))

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def setXP(self, XP: str):
		self.XP = int(XP)

	def setKeywords(self, Keywords: str):
		self.Keywords = Keywords

	def setSize(self, Size: str):
		self.Size = Size

	def setIsPostMM3(self, IsPostMM3: bool):
		self.IsPostMM3 = IsPostMM3

	def getLevel(self) -> int:
		return self.Level

	def getModifier(self) -> str:
		return self.Modifier

	def getRole(self) -> str:
		return self.Role

	def getIsNew(self) -> bool:
		return self.IsNew

	def getIsChanged(self) -> bool:
		return self.IsChanged

	def getTeaser(self) -> int:
		return self.Teaser

	def getXP(self) -> int:
		return self.XP

	def getKeywords(self) -> str:
		return self.Keywords

	def getSize(self) -> str:
		return self.Size

	def getIsPostMM3(self) -> bool:
		return self.IsPostMM3

class ParagonPath(ddiObject):
	def __init__(self):
		super().__init__()
		self.Prerequisite : str = ''
		self.Teaser : int = 0

	def setPrerequisite(self, Prerequisite: str):
		self.Prerequisite = Prerequisite

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getPrerequisite(self):
		return self.Prerequisite

	def getTeaser(self):
		return self.Teaser

class Poison(ddiObject):
	def __init__(self):
		super().__init__()
		self.Level : int = 0
		self.Cost : str = ''
		self.Teaser : int = 0

	def setLevel(self, Level: str):
		self.Level = int(Level)

	def setCost(self, Cost: str):
		self.Cost = Cost

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getLevel(self) -> int:
		return self.Level

	def getCost(self) -> str:
		return self.Cost

	def getTeaser(self) -> int:
		return self.Teaser

class Power(ddiObject):
	def __init__(self):
		super().__init__()
		self.Level : int = 0
		self.Action : str = ''
		self.IsNew : bool = False
		self.IsChanged : bool = False
		self.Class : str = ''
		self.Teaser : int = 0
		self.Kind : str = ''
		self.Usage : str = ''

	def getLevel(self) -> int:
		return self.Level

	def getAction(self) -> str:
		return self.Action

	def getIsNew(self) -> bool:
		return self.IsNew

	def getIsChanged(self) -> bool:
		return self.IsChanged

	def getClass(self) -> str:
		return self.Class

	def getTeaser(self) -> int:
		return self.Teaser

	def getKind(self) -> str:
		return self.Kind

	def getUsage(self) -> str:
		return self.Usage

	def setLevel(self, Level: str):
		self.Level = int(Level)

	def setAction(self, Action: str):
		self.Action = Action

	def setIsNew(self, IsNew: str):
		self.IsNew = bool(int(IsNew))

	def setIsChanged(self, IsChanged: str):
		self.IsChanged = bool(int(IsChanged))

	def setClass(self, Class: str):
		self.Class = Class

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def setKind(self, Kind: str):
		self.Kind = Kind

	def setUsage(self, Usage: str):
		self.Usage = Usage

class Race(ddiObject):
	def __init__(self):
		super().__init__()
		self.Size : str = ''
		self.Description : str = ''
		self.IsNew : bool = False
		self.IsChanged : bool = False
		self.Teaser : int = 0

	def setSize(self, Size: str):
		self.Size = Size

	def setDescription(self, Description: str):
		self.Description = Description

	def setIsNew(self, IsNew: str):
		self.IsNew = bool(int(IsNew))

	def setIsChanged(self, IsChanged: str):
		self.IsChanged = bool(int(IsChanged))

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getSize(self) -> str:
		return self.Size

	def getDescription(self) -> str:
		return self.Description

	def getIsNew(self) -> bool:
		return self.IsNew

	def getIsChanged(self) -> bool:
		return self.IsChanged

	def getTeaser(self) -> int:
		return self.Teaser

class Ritual(ddiObject):
	def __init__(self):
		super().__init__()
		self.Level : int = 0
		self.Component : str = ''
		self.Price : int = 0
		self.KeySkill : str = ''
		self.Teaser : int = 0

	def setLevel(self, Level: str):
		self.Level = int(Level)

	def setComponent(self, Component: str):
		self.Component = Component

	def setPrice(self, Price: str):
		self.Price = int(Price)

	def setKeySkill(self, KeySkill: str):
		self.KeySkill = KeySkill

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getLevel(self) -> int:
		return self.Level

	def getComponent(self) -> str:
		return self.Component

	def getPrice(self) -> int:
		return self.Price

	def getKeySkill(self) -> str:
		return self.KeySkill

	def getTeaser(self) -> int:
		return self.Teaser

class Skill(ddiObject):
	def __init__(self):
		super().__init__()
		self.Category : str = ''
		self.TypeS : str = ''
		self.Teaser : int = 0

	def setCategory(self, Category: str):
		self.Category = Category

	def setTypeS(self, TypeS: str):
		self.TypeS = TypeS

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getCategory(self) -> str:
		return self.Category

	def getTypeS(self) -> str:
		return self.TypeS

	def getTeaser(self) -> int:
		return self.Teaser

class Terrain(ddiObject):
	def __init__(self):
		super().__init__()
		self.TypeT : str = ''
		self.Teaser : int = 0

	def setTypeT(self, TypeT: str):
		self.TypeT = TypeT

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def getTypeT(self) -> str:
		return self.TypeT

	def getTeaser(self) -> int:
		return self.Teaser

class Theme(ddiObject):
	def __init__(self):
		super().__init__()
		self.Prerequisite : str = ''

	def setPrerequisite(self, Prerequisite: str):
		self.Prerequisite = Prerequisite

	def getPrerequisite(self) -> str:
		return self.Prerequisite

class Trap(ddiObject):
	def __init__(self):
		super().__init__()
		self.Role : str = ''
		self.TypeT : str = ''
		self.Level : str = ''
		self.Teaser : int = 0
		self.Classe : str = ''
		self.XP : int = 0

	def setRole(self, Role: str):
		self.Role = Role

	def setTypeT(self, TypeT: str):
		self.TypeT = TypeT

	def setLevel(self, Level: str):
		self.Level = Level

	def setTeaser(self, Teaser: str):
		self.Teaser = int(Teaser)

	def setClasse(self, Classe: str):
		self.Classe = Classe

	def setXP(self, XP: str):
		self.XP = int(XP)

	def getRole(self) -> str:
		return self.Role

	def getTypeT(self) -> str:
		return self.TypeT

	def getLevel(self) -> str:
		return self.Level

	def getTeaser(self) -> int:
		return self.Teaser

	def getClasse(self) -> str:
		return self.Classe

	def getXP(self) -> int:
		return self.XP