from enum import Enum
from .Types import Types

class Files(Enum):
	DDIASSOCIATE = ("ddiAssociate.sql", Types.ASSOCIATE)
	DDIBACKGROUND = ("ddiBackground.sql", Types.BACKGROUND)
	DDICLASS = ("ddiClass.sql", Types.CLASS)
	DDICOMPANION = ("ddiCompanion.sql", Types.COMPANION)
	DDIDEITY = ("ddiDeity.sql", Types.DEITY)
	DDIDISEASE = ("ddiDisease.sql", Types.DISEASE)
	DDIEPICDESTINY = ("ddiEpicDestiny.sql", Types.EPICDESTINY)
	DDIFEAT = ("ddiFeat.sql", Types.FEAT)
	#DDIGETFILTERSELECT = ("ddiGetFilterSelect.sql", Types.GETFILTERSELECT)
	DDIGLOSSARY = ("ddiGlossary.sql", Types.GLOSSARY)
	DDIITEM = ("ddiItem.sql", Types.ITEM)
	DDIMONSTER = ("ddiMonster.sql", Types.MONSTER)
	DDIPARAGONPATH = ("ddiParagonPath.sql", Types.PARAGONPATH)
	DDIPOISON = ("ddiPoison.sql", Types.POISON)
	DDIPOWER = ("ddiPower.sql", Types.POWER)
	DDIRACE = ("ddiRace.sql", Types.RACE)
	DDIRITUAL = ("ddiRitual.sql", Types.RITUAL)
	DDISKILL = ("ddiSkill.sql", Types.SKILL)
	DDITERRAIN = ("ddiTerrain.sql", Types.TERRAIN)
	DDITHEME = ("ddiTheme.sql", Types.THEME)
	DDITRAP = ("ddiTrap.sql", Types.TRAP)

	def __new__(cls, file, type):
		member = object.__new__(cls)
		member._value_ = file
		member.type = type
		return member
