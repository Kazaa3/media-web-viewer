---
Title_DE: Feature-Modal Optimierung v1.1.19
Title_EN: Feature Modal Refinement v1.1.19
Status: COMPLETED
Category: UI
Version: 1.1.19
Summary_DE: Das Feature-Modal wurde vollständig dynamisiert und übersetzt. Es zeigt nun die letzten 3 Updates prominent an und bietet einen direkten Link zur Dokumentation.
Summary_EN: The feature modal has been fully dynamized and translated. It now prominently displays the last 3 updates and provides a direct link to the documentation.
---

<!-- Category: Feature -->
<!-- Title_DE: 1.1.19: Feature Modal & UI Refinement -->
<!-- Title_EN: 1.1.19: Feature Modal & UI Refinement -->
<!-- Summary_DE: Dynamische Kategorisierung im Modal, Dokumentations-Link und Test-Biling Button. -->
<!-- Summary_EN: Dynamic categorization in modal, documentation link and Test-Biling button. -->
<!-- Status: COMPLETED -->

# v1.1.19 Refinements

Diese Version konzentriert sich auf die Verbesserung der Benutzererfahrung im Dashboard und die Bereitstellung klarerer Statusinformationen.

## Änderungen am Feature Modal
- **Dynamische Kategorisierung**: Das Modal ist nun in vier klare Bereiche unterteilt:
    1. **Latest Updates**: Die letzten drei Logbuch-Einträge (basierend auf Dateipräfix).
    2. **Project Documentation**: Direkter Zugriff auf die Hauptdokumentation (`31_Project_Documentation.md`).
    3. **Features & Bugs**: Eine Zusammenfassung der offenen Punkte, inklusive der Datei `00_Known_Issues.md`.
    4. **Completed**: Alle übrigen abgeschlossenen Meilensteine.
- **Bilinguale Metadaten**: Unterstützung für sowohl Kommentar-basierte (`<!-- Tag: Value -->`) als auch Frontmatter-ähnliche Metadaten in Markdown-Dateien.

## UI Erweiterungen
- **Recent News Bar**: Die Kopfzeile zeigt nun die Titel der neuesten Entwicklungen direkt an.

## Dokumentation
- Die Hauptdatei `DOCUMENTATION.md` wurde auf Stand v1.1.19 aktualisiert.
- Der logbook-entry 32 wurde als Release-Note finalisiert.

<!-- lang-split -->


### Main Changes:
1. **Three-Section Logic**: Entries are now divided into "Latest Updates" (last 3 completed), "Open Bugs", "Planned Features", and "Completed".
2. **Direct Documentation**: A prominent button now leads directly to the project documentation.
3. **Fully Bilingual**: All labels, titles, and summaries are displayed correctly depending on the selected language (DE/EN).
4. **Interactive News Bar**: The header now displays the last 3 news entries interactively.
