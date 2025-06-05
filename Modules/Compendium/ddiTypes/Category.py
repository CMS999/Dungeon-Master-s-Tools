from enum import Enum

class Categories(Enum):
	ALL = ("All", ["", "Name", "Level", "Cost", "Source"])
	BACKGROUND = ("Background", ["", "Name", "Type", "Campaing Setting", "Prerequisite(s)", "Associated Skills"])
	CHARACTERSTHEME = ("Characters Theme", ["", "Name", "Prerequisite(s)"])
	CLASSES = ("Classes", ["", "Name", "Role", "Power Source", "Key Abilities"])
	COMPANIONSFAMILIARS = ("Companions & Familiars", ["", "", "Name", "Type"])
	CREATURES = ("Creatures", ["", "Name", "Level", "Main Role", "Group Role", "XP", "Size", "Keywords"])
	DEITIES = ("Deities", ["", "Name", "Alignment"])
	DISEASES = ("Diseases", ["", "Name", "Level"])
	EPICDESTINIES = ("Epic Destinies", ["", "Name", "Prerequisite(s)"])
	FEATS = ("Feats", ["", "Name", "Tier", "Prerequisite(s)"])
	GLOSSARY = ("Glossary", ["", "Name", "Category", "Type"])
	ITEMS = ("Items", ["", "Name", "Category", "Mundane", "Level", "Cost", "Rarity"])
	PARAGONPATHS = ("Paragon Paths", ["", "Name", "Prerequisite(s)"])
	POISONS = ("Poisons", ["", "Name", "Level", "Cost"])
	POWERS = ("Powers", ["", "Name", "Level", "Action", "Class", "Kind", "Usage"])
	RACES = ("Races", ["", "Name", "Ability Scores", "Size"])
	RITUALS = ("Rituals", ["", "Name", "Level", "Component Cost", "Market Price", "Key Skill"])
	TERRAIN = ("Terrain", ["", "Name", "Type"])
	TRAP = ("Trap", ["", "Name", "Type", "Role", "Level", "XP", "Class"])

	def __new__(cls, category, metaData):
		member = object.__new__(cls)
		member._value_ = category
		member.metaData = metaData
		return member
