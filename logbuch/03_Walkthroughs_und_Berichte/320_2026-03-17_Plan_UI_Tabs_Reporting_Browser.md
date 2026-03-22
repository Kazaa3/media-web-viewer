# Logbuch: Plan – UI Tabs Update (Reporting & Browser)

**Datum:** 17. März 2026

## Ziel: Verbesserte UI für Reporting- und File-Tab

---

### Backend (src/core/main.py)
- **NEU:** list_sql_files() – Gibt Liste aller .sql-Dateien im data/-Verzeichnis zurück
- **NEU:** get_sql_content(filename) – Liest und liefert Inhalt einer bestimmten SQL-Datei

### Frontend (web/app.html)
- **Reporting Tab:**
  - <select>-Dropdown oben rechts im reporting-dashboard-panel
  - Bestehende Charts in toggelbaren Container packen
  - Neuer Container für "Database"-Ansicht: Listet SQL-Dateien und zeigt Inhalt an
  - switchReportingView(view): Umschalten zwischen "Dashboard" und "Database"
- **File Tab:**
  - indexed-sqlite-media-repository-panel als Flexbox (Spaltenrichtung)
  - Oben: File-Grid (bestehend)
  - Unten: Folder-Browser
  - Synchronisation: Auswahl im Folder-Browser aktualisiert File-Grid

### Localization (web/i18n.json)
- Neue Keys: "Report Dashboard", "Database Files" und weitere Labels

---

## Verifikationsplan

### Automatisierte Tests
- list_sql_files mit Mock-Dateien in data/ testen

### Manuelle Verifikation
- Umschalten zwischen Dashboard und Database im Reporting-Tab
- Navigation im neuen Split-View des File-Tabs prüfen

---

Weitere Details siehe vorherige Logbuch-Einträge und walkthrough.md.
