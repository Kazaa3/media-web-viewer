# Bugs & Features Overview

<!-- Category: Bug -->
<!-- Title_DE: Bekannte Probleme (Stand v1.3.3) -->
<!-- Title_EN: Known Issues (Status v1.3.3) -->
<!-- Summary_DE: Zentrale Liste offener Bugs und technischer Probleme. -->
<!-- Summary_EN: Central list of open bugs and technical issues. -->
<!-- Status: ACTIVE -->
<!-- Anchor: 00_Known_Issues -->
<!-- Redundancy: Section covers known issues, bug tracking, technical debt, GUI bugs, parser pipeline, markdown rendering, branch protection. -->

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


# Features
<!-- Category: Feature -->
<!-- Title_DE: Features -->
<!-- Title_EN: Features -->
<!-- Summary_DE: Zentrale Übersicht geplanter und umgesetzter Features. -->
<!-- Summary_EN: Central overview of planned and delivered features. -->
<!-- Status: ACTIVE -->
<!-- Anchor: 01_Features -->
<!-- Redundancy: Section covers feature tracking, planned features, completed features, milestone links, central collection. -->

<!-- ANKER: Features -->
# Features

## Purpose
- This entry is the central collection point for feature requests and feature status.

## Working rule
- Capture new feature ideas here first.
- For larger scope, move to dedicated logbook entry and link here.

## References
- For milestone-specific planning see the respective M1/M2/M3/M4 entries.

## Open Features (as of 2026-03-09)

### Planned
- **[15] Parser Pipeline Rework** - Planned parser pipeline redesign for robustness, prioritization, and better fault tolerance
  - [Entry 15_Parser_Pipeline_Rework.md](15_Parser_Pipeline_Rework.md)
  
- **[76] Milestone 3 - New GUI** - Planned UI/UX modernization with incremental migration
  - [Entry 76_Redundant_Milestone_3.md](76_Redundant_Milestone_3.md)
  
- **[77] Milestone 4 - Platform and Release Quality** - Planned hardening of build, release, operations, and validation
  - [Entry 77_Redundant_Milestone_4.md](77_Redundant_Milestone_4.md)
  
- **[80] Scraper Integration and Quality** - Plan and guidelines for scraper sources, mapping, validation, and fallback behavior
  - [Entry 80_Scraper_Integration_und_Qualitaet.md](80_Scraper_Integration_und_Qualitaet.md)

### Active
- **[81] i18n Internationalization** - Guidelines and next steps for sustainable internationalization across UI, logbook, and runtime texts
  - [Entry 81_i18n_Internationalisierung.md](81_i18n_Internationalisierung.md)

## Completed Features (today)
- **[14] Logging Module instead of print and True-Checks** - Migration to structured logging ✅
- **[34] MVP Approach and Tool Evaluation** - Early MVP-focused phase and tool tests ✅
- **[60] Branch Protection for main** - GitHub branch protection enabled ✅
- **[127] Detection of PC Games and Book Accompanying Discs** - Specific categorization ✅
- **[128] Playlist Management and UI Refinement** - Reordering, Clear, and UI fixes ✅

<!-- lang-split -->

<!-- ANKER: Features EN -->
# Features

## Purpose
- This entry is the central collection point for feature requests and feature status.

## Working rule
- Capture new feature ideas here first.
- For larger scope, move to dedicated logbook entry and link here.

## References
- For milestone-specific planning see the respective M1/M2/M3/M4 entries.

## Open Features (as of 2026-03-09)

### Planned
- **[15] Parser Pipeline Rework** - Planned parser pipeline redesign for robustness, prioritization, and better fault tolerance
  - [Entry 15_Parser_Pipeline_Rework.md](15_Parser_Pipeline_Rework.md)
  
- **[76] Milestone 3 - New GUI** - Planned UI/UX modernization with incremental migration
  - [Entry 76_Redundant_Milestone_3.md](76_Redundant_Milestone_3.md)
  
- **[77] Milestone 4 - Platform and Release Quality** - Planned hardening of build, release, operations, and validation
  - [Entry 77_Redundant_Milestone_4.md](77_Redundant_Milestone_4.md)
  
- **[80] Scraper Integration and Quality** - Plan and guidelines for scraper sources, mapping, validation, and fallback behavior
  - [Entry 80_Scraper_Integration_und_Qualitaet.md](80_Scraper_Integration_und_Qualitaet.md)

### Active
- **[81] i18n Internationalization** - Guidelines and next steps for sustainable internationalization across UI, logbook, and runtime texts
  - [Entry 81_i18n_Internationalisierung.md](81_i18n_Internationalisierung.md)

## Completed Features (today)
- **[14] Logging Module instead of print and True-Checks** - Migration to structured logging ✅
- **[34] MVP Approach and Tool Evaluation** - Early MVP-focused phase and tool tests ✅
- **[60] Branch Protection for main** - GitHub branch protection enabled ✅
- **[127] Detection of PC Games and Book Accompanying Discs** - Specific categorization ✅
- **[128] Playlist Management and UI Refinement** - Reordering, Clear, and UI fixes ✅
