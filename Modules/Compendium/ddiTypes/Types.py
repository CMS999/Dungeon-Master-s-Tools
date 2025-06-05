from enum import Enum
from .Category import Categories

class Types(Enum):
    ASSOCIATE = ("Associate", ["ID", "Name", "Type", "Source", "Teaser", "HTML"], Categories.COMPANIONSFAMILIARS)
    BACKGROUND = ("Background", ["ID", "Name", "Type", "Campaign", "Skills", "Source", "Teaser", "HTML"], Categories.BACKGROUND)
    CLASS = ("Class", ["ID", "Name", "Power", "Role", "Abilities", "IsNew", "IsChanged", "Source", "Teaser", "HTML"], Categories.CLASSES)
    COMPANION = ("Companion", ["ID", "Name", "Type", "Source", "Teaser", "HTML"], Categories.COMPANIONSFAMILIARS)
    DEITY = ("Deity", ["ID", "Name", "Alignment", "Source", "Teaser", "HTML"], Categories.DEITIES)
    DISEASE = ("Disease", ["ID", "Name", "Level", "Source", "Teaser", "HTML"], Categories.DISEASES)
    EPICDESTINY = ("Epic Destiny", ["ID", "Name", "Prerequisite", "IsNew", "IsChanged", "Source", "Teaser", "HTML"], Categories.EPICDESTINIES)
    FEAT = ("Feat", ["ID", "Name", "IsNew", "IsChanged", "Source", "Tier", "Sort", "Teaser", "HTML"], Categories.FEATS)
    #GETFILTERSELECT = ("Getfilterselect", [])
    GLOSSARY = ("Glossary", ["ID", "Name", "Category", "Type", "Source", "Teaser", "HTML"], Categories.GLOSSARY)
    ITEM = ("Item", ["ID", "Name", "Cost", "Level", "Category", "Enhancement", "IsMundade", "FinalCost", "Source", "Teaser", "HTML", "Rarity", "CostSort", "LevelSort"], Categories.ITEMS)
    MONSTER = ("Monster", ["ID", "Name", "Level", "Modifier", "Role", "IsNew", "IsChanged", "Source", "Teaser", "HTML", "XP", "Keywords"], Categories.CREATURES)
    PARAGONPATH = ("Paragon Path", ["ID", "Name", "Prerequisite", "Sourcer", "Teaser", "HTML"], Categories.PARAGONPATHS)
    POISON = ("Poison", ["ID", "Name", "Level", "Cost", "Source", "Teaser", "HTML"], Categories.POISONS)
    POWER = ("Power", ["ID", "Name", "Level", "Action", "IsNew", "IsChanged", "Source", "Class", "Teaser", "HTML", "Kind", "Usage"], Categories.POWERS)
    RACE = ("Race", ["ID", "Name", "Size", "Description", "IsNew", "IsChanged", "Source", "Teaser", "HTML"], Categories.RACES)
    RITUAL = ("Ritual", ["ID", "Name", "Level", "Component", "Price", "KeySkill", "Source", "Teaser", "HTML"], Categories.RITUALS)
    SKILL = ("Skill", ["ID", "Name", "Category", "Type", "Source", "Teaser", "HTML"], Categories.GLOSSARY)
    TERRAIN = ("Terrain", ["ID", "Name", "Type", "Source", "Teaser", "HTML"], Categories.TERRAIN)
    THEME = ("Theme", ["ID", "Name", "Source", "HTML"], Categories.CHARACTERSTHEME)
    TRAP = ("Trap", ["ID", "Name", "Role", "Type", "Level", "Source", "Teaser", "HTML", "Class"], Categories.TRAP)


    def __new__(cls, type, fields, category):
        member = object.__new__(cls)
        member._value_ = type
        member.fields = fields
        member.category = category
        return member