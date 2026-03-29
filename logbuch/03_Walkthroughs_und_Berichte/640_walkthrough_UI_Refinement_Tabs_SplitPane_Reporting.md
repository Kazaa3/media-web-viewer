# Walkthrough – UI Refinement: Tabs, Split-Pane & Reporting

**Datum:** 17. März 2026

## Zusammenfassung
Abschluss der UI-Überarbeitung mit Fokus auf Tab-Umbenennung, strukturelle Anpassungen der File/Item-Tabs und neue Funktionen im Reporting-Bereich.

---

### 1. Tab-Umbenennung & Mapping
- "File"-Tab → "Item"
- "Browse"-Tab → "File"
- Navigationstrigger und i18n-Keys in `web/app.html` und `web/i18n.json` aktualisiert
- `switchTab`-Logik für neue Tab-IDs (`item`, `file`) angepasst

### 2. "File"-Tab (ehemals Browse) – Split-Pane-View
- `#filesystem-crawler-directory-panel` als vertikales Split-Pane umgebaut
- Oben: Dateiexplorer für Disk-Navigation
- Unten: Liste der Bibliotheksordner für Schnellnavigation
- Resizable Splitter zwischen den beiden Bereichen

### 3. "Reporting"-Tab – Database-View
- Dropdown oben rechts zum Umschalten zwischen "Dashboard" und "Database (SQL)"
- Database-View: Sidebar listet `.sql`-Dateien aus `data/`, Content-Bereich zeigt SQL-Code
- Backend: `list_sql_files()` und `get_sql_content()` in `src/core/main.py` implementiert

### 4. Media-Filter & Kategorien
- Fehlende Filterchips in der Bibliothek ergänzt:
  - Dokumente
  - E-Books
  - ISO-Abbilder
  - PC-Spiele
- "Sonstige" zur Subkategorie-Dropdown hinzugefügt

---

## Verifikation
- Tab-Benennung: "Item" und "File" korrekt
- Split-Pane: Layout im "File"-Tab geprüft
- SQL-Reporting: Dropdown schaltet zwischen Dashboard und Database, SQL-Dateien werden gelistet
- Filter: Neue Kategorie-Chips sichtbar
- Bilder: Media-Items zeigen Artwork korrekt an

---

## Technische Hinweise
- Fehlende Abhängigkeiten (`requests`, `pyvidplayer2`) in `.venv_core` installiert
- `switchTab` lädt nun SQL-Dateien oder Bibliotheksordner beim Aktivieren der jeweiligen Tabs

---

## UI Verification Recording
- Automatisierte UI-Tests und manuelle Sichtprüfung durchgeführt
- Alle Kernfunktionen wie geplant umgesetzt und geprüft
