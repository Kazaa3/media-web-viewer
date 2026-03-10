<!-- Category: bug -->
<!-- Title_DE: Bekannte Probleme (Stand v1.3.3) -->
<!-- Title_EN: Known Issues (Status v1.3.3) -->
<!-- Summary_DE: Zentrale Liste offener Bugs und technischer Probleme -->
<!-- Summary_EN: Central list of open bugs and technical issues -->
<!-- Status: ACTIVE -->
<!-- Date: 2026-03-09 -->

# Bekannte Probleme (Stand v1.3.3)


## Offene Punkte
- Laufende Bugs und technische Schulden werden hier gesammelt.
- Detailanalysen können in separaten Logbuch-Einträgen dokumentiert werden.

## Arbeitsregel
- Neue Bugs zuerst hier erfassen.
- Nach Fix in „Behoben“ verschieben oder auf den zugehörigen Eintrag verlinken.

## Aktuelle offene Bugs (Stand 2026-03-09)

### GUI-Bugs
- Weitere GUI-Probleme vorhanden (Detailanalyse ausstehend)

### Kleinere Bugs
- Diverse kleinere Probleme, die zunächst zurückgestellt werden
- Priorisierung steht noch aus

## Technische Schulden
- Parser-Pipeline benötigt Refactoring (siehe [Eintrag 15](15_Parser_Pipeline_Rework.md))
- Scraper-Integration ausstehend (siehe [Eintrag 80](80_Scraper_Integration_und_Qualitaet.md))

## Behobene Probleme (heute)
- **Logbuch Markdown-Rendering**: marked.js integriert für korrekte HTML-Darstellung ✅ ([Eintrag 82](82_Logbuch_Markdown_Rendering.md))
- Branch Protection für main eingerichtet ✅ ([Eintrag 60](60_Branch_Protection_main.md))

<!-- lang-split -->

# Known Issues (Status v1.3.3)

## Open items
- Ongoing bugs and technical debt are tracked here.
- Detailed analyses can be documented in dedicated logbook entries.

## Working rule
- Add new bugs here first.
- After fixing, move to "Resolved" or link to the related entry.
- Datei: audio statt .m1a (Datei-Endung). Durch Datenbankänderung
- get Imprint nicht verwendet, sondern i8n
- 

## Current Open Bugs (as of 2026-03-09)

### GUI Bugs
- Additional GUI problems exist (detailed analysis pending)

### Minor Bugs
- Various minor issues deferred for now
- Prioritization pending

## Technical Debt
- Parser pipeline needs refactoring (see [Entry 15](15_Parser_Pipeline_Rework.md))
- Scraper integration pending (see [Entry 80](80_Scraper_Integration_und_Qualitaet.md))

## Resolved Issues (today)
- **Logbook Markdown Rendering**: marked.js integrated for correct HTML display ✅ ([Entry 82](82_Logbuch_Markdown_Rendering.md))
- Branch protection for main set up ✅ ([Entry 60](60_Branch_Protection_main.md))
