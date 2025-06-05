from .Types import Types

class ddiObject():
	def __init__(self):
		self.color : str = '#ffffff'
		self.ID : int = -1
		self.Name : str = None
		self.Source : str = None
		self.HTML : str = None
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
		self.TypeA : str = None
		self.Teaser : int = None

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
		self.TypeB : str = None
		self.Campaign : str = None
		self.Skills : str = None
		self.Teaser : int = None
		self.prerequisite : str = None

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
		self.Power : str = None
		self.Role : str = None
		self.Abilities : str = None
		self.IsNew : bool = None
		self.IsChanged : bool = None
		self.Teaser : int = None

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
		self.TypeC : str = None
		self.Teaser : int = None

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
		self.Alignment : str = None
		self.Teaser : int = None

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
		self.Level : int = None
		self.Teaser : int = None

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
		self.Prerequisite : str = None
		self.IsNew : bool = None
		self.IsChanged : bool = None
		self.Teaser : int = None

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
		self.IsNew : bool = None
		self.IsChanged : bool = None
		self.Tier : str = None
		self.Sort : int = None
		self.Teaser : int = None
		self.Prerequisite : str = None

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
		self.Category : str = None
		self.TypeG : str = None
		self.Teaser : int = None

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
		self.Cost : str = None
		self.Level : str= None
		self.Category : str = None
		self.Enhancement : str = None
		self.IsMundane : bool = None
		self.FinalCost : str = None
		self.Teaser : int = None
		self.Rarity : str = None
		self.CostSort : int = None
		self.LevelSort : int = None

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
		self.Level : int = None
		self.Modifier : str = None
		self.Role : str = None
		self.IsNew : bool = None
		self.IsChanged : bool = None
		self.Teaser : int = None
		self.XP : int = None
		self.Keywords : str = None
		self.Size : str = None

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

class ParagonPath(ddiObject):
	def __init__(self):
		super().__init__()
		self.Prerequisite : str = None
		self.Teaser : int = None

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
		self.Level : int = None
		self.Cost : str = None
		self.Teaser : int = None

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
		self.Level : int = None
		self.Action : str = None
		self.IsNew : bool = None
		self.IsChanged : bool = None
		self.Class : str = None
		self.Teaser : int = None
		self.Kind : str = None
		self.Usage : str = None

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
		self.Size : str = None
		self.Description : str = None
		self.IsNew : bool = None
		self.IsChanged : bool = None
		self.Teaser : int = None

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
		self.Level : int = None
		self.Component : str = None
		self.Price : int = None
		self.KeySkill : str = None
		self.Teaser : int = None

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
		self.Category : str = None
		self.TypeS : str = None
		self.Teaser : int = None

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
		self.TypeT : str = None
		self.Teaser : int = None

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
		self.Prerequisite : str = None

	def setPrerequisite(self, Prerequisite: str):
		self.Prerequisite = Prerequisite

	def getPrerequisite(self) -> str:
		return self.Prerequisite

class Trap(ddiObject):
	def __init__(self):
		super().__init__()
		self.Role : str = None
		self.TypeT : str = None
		self.Level : str = None
		self.Teaser : int = None
		self.Classe : str = None
		self.XP : int = None

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