# Logbuch Meilenstein: Restoration Plan – Parser Settings & Logbook Editor (v1.35.68)

## Ziel
Behebung der UI-Fragmentierung im Parser-Bereich und Aktivierung des Logbuch-Editors für eine moderne, konsolidierte Bedienung.

## Maßnahmen & geplante Änderungen

### 1. Parser Tab Konsolidierung
- Entfernen des hardcodierten parser-panel-container aus app.html (DOM-Kollisionen vermeiden)
- Neuer Fragment: parser_panel.html
  - 2-Spalten-Layout
    - Links: Kern-Einstellungen (Parser-Intensität, Scan-Depth), Parser-Architektur (draggable/toggleable Grid aller Parser)
    - Rechts: Advanced Config (FFmpeg-Pfade, Regex-Excludes, Deep-Analysis), Live-Metrics (Parsing-Log)
- Anpassung ui_nav_helpers.js: Parser-Button lädt Fragment korrekt
- Anpassung options_helpers.js: loadAllOptions/saveAllOptions unterstützen beide Views

### 2. Logbuch Editor Integration
- logbuch_panel.html: + Neuer Eintrag (Sidebar), Edit (Content-Header)
- logbook_helpers.js:
  - openLogbookEditor(name, filename): Modal-Felder befüllen, Modal anzeigen
  - saveLogbookEntry(): Daten sammeln, an Backend senden (eel.save_logbook_entry), Refresh triggern

### 3. Backend-Check
- Prüfen, ob save_logbook_entry in main.py existiert, ggf. robusten Fallback implementieren

## Verifikation
- Automatisiert: Keine ReferenceErrors bei Edit, PARSER_CONFIG wird nach Save aktualisiert
- Manuell: Alle Parser im neuen Tab togglebar, Logbuch-Einträge können erstellt/editiert werden

---

**Freigabe zur Umsetzung: Parser Settings & Logbook Editor Restoration.**
