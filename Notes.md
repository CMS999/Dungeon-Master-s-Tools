- [Architecture](#architecture)
- [UI Files](#ui-files)
- [Codes (Early-Implementations)](#codes-early-implementations)
- [Quick References](#quick-references)
- [Performace Changes](#performace-changes)
	- [Database File Changes](#database-file-changes)
		- [Comparative](#comparative)
		- [Database File Size](#database-file-size)
	- [Modal data](#modal-data)
	- [Estimated Saves](#estimated-saves)

# Architecture
Save plugins as ext files (zip files), load then and execute their plugin interface.
```Mermaid
graph BT
	subgraph DMT[Dungeon Master Tools]
	main
	end

	subgraph P[Plugins]
	Ext1[Extension1.ext]
	ExtN[ExtensionN.ext]

	Ext1 --> main
	ExtN --> main
	end
```

# UI Files
You need to run the following command to generate the ui.py file
``` console
pyside6-uic form.ui -o ui_form.py
```
# Codes (Early-Implementations)

```python
#load and generate ui from .ui file
def buildUI(self):
		ui_file_name = "untitled.ui"
		ui_file = QFile(ui_file_name)
		if not ui_file.open(QIODevice.ReadOnly):
			print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
			sys.exit(-1)
		loader = QUiLoader()
		ui_file.close()
		ui = loader.load(ui_file)
		return 

#Parser sql (power) files and render html in WebEngineView
def renderPower(self):
		p1 = Parser()
		test = {"Power": []}
		p1.sqlToPower(test)
		webV = QWebEngineView()
		webV.setMinimumSize(625, 0)
		self.ui.gridLayout_5.addWidget(webV)
		webV.setHtml(test["Power"][2].getHTML())
```

# Quick References
```cpp
//Roles of DataRoleEnum, used for quick refenrence
	enum ItemDataRole {
		DisplayRole = 0,
		DecorationRole = 1,
		EditRole = 2,
		ToolTipRole = 3,
		StatusTipRole = 4,
		WhatsThisRole = 5,
		// Metadata
		FontRole = 6,
		TextAlignmentRole = 7,
		BackgroundColorRole = 8,
		BackgroundRole = 8,
		TextColorRole = 9,
		ForegroundRole = 9,
		CheckStateRole = 10,
		// Accessibility
		AccessibleTextRole = 11,
		AccessibleDescriptionRole = 12,
		// More general purpose
		SizeHintRole = 13,
		InitialSortOrderRole = 14,
		// Internal UiLib roles. Start worrying when public roles go that high.
		DisplayPropertyRole = 27,
		DecorationPropertyRole = 28,
		ToolTipPropertyRole = 29,
		StatusTipPropertyRole = 30,
		WhatsThisPropertyRole = 31,
		// Reserved
		UserRole = 32
	};

```    
```python
#dicts of Compendium categories, used for quick refenrence
{"Background" : ["Name", "Type", "Campaing Setting", "Prerequisite(s)", "Associated Skills"]}
{"Characters Theme" : ["Name", "Prerequisite(s)"]}
{"Classes" : ["Name", "Role", "Power Source", "Key Abilities"]}
{"Companions & Familiars" : ["Name", "Type"]}
{"Creatures" : ["Name", "Level", "Main Role", "Group Role", "XP", "Size", "Keywords"]}
{"Deities" : ["Name", "Alignment"]}
{"Diseases" : ["Name", "Level"]}
{"Epic Destinies" : ["Name", "Prerequisite(s)"]}
{"Feats" : ["Name", "Tier", "Prerequisite(s)"]}
{"Glossary" : ["Name", "Category", "Type"]}
{"Items" : ["Name", "Category", "Mundane", "Level", "Cost", "Rarity"]}
{"Paragon Paths" : ["Name", "Prerequisite(s)"]}
{"Poisons" : ["Name", "Level", "Cost"]}
{"Powers" : ["Name", "Level", "Action", "Class", "Kind", "Usage"]}
{"Races" : ["Name", "Ability Scores", "Size"]}
{"Rituals" : ["Name", "Level", "Component Cost", "Market Price", "Key Skill"]}
{"Terrain" : ["Name", "Type"]}
{"Trap" : ["Name", "Type", "Role", "Level", "XP", "Class"]}

```

# Performace Changes

## Database File Changes
First iteration serialiazed all HTML data with the style, srcipt and head tags, wasting space (around 10 KB per entry)

Second iterarion removed style portion from HTML and transfered responsability to table render (reduction of around 9 KB per entry)

Third iteration removed head portion from HTML transfered responsability to table render (reduction of around 1 KB per entry)

### Comparative
| Change                     | File Size | Reduction |
|:---------------------------|:---------:|:---------:|
| Orginal file size          |  12,5 KB  |           |
| Removal of Chars           |  12,2 KB  |  0,3 KB   |
| Removal of Style           |  3,1 KB   |  9,1 KB   |
| Removal of Head and script |  2,3 KB   |  0,8 KB   |

Total Reduction ~ 10,2 KB or around 81%

### Database File Size
- First Iterarion: 330 MB
- Second Iterarion:  74 MB
- Third Iterarion:  52 MB

## Modal data 
First iteration stored data in dictionary and them created model data, never releasing dictionary.

Second iteration transered dictionary declaration to model data creation method, releasing on completion.

## Estimated Saves
Around 15 MB