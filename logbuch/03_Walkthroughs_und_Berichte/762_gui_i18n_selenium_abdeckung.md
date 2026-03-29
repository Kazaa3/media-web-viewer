# Logbuch: GUI/i18n Selenium Testabdeckung – 2026-03-19

## Ziel
Systematische Abdeckung und Validierung der GUI-Elemente und i18n-Tags mittels Selenium-Tests für Media Web Viewer.

## Testbereiche & Status

### 1. Haupt-Tabs
- Sichtbarkeit, Klickbarkeit und data-i18n-Tag für alle Haupt-Tabs (Player, Bibliothek, Item, Datei, Edit, Optionen, Parser, Debug, Tests, Reporting, Logbuch, Playlist, Video)
- **Test:** `test_all_tabs.py`, `test_all_tabs_i18n.py`
- **Status:** Vollständig abgedeckt

### 2. Subtabs
- Library- und Options-Subtabs: Sichtbarkeit, Klickbarkeit, data-i18n-Tag
- **Test:** `test_subtabs_i18n.py`
- **Status:** Vollständig abgedeckt

### 3. Modale
- Öffnen/Schließen, Sichtbarkeit, data-i18n-Tag am Öffnen-Button (Feature Status, Debug Flags, About/Imprint)
- **Test:** `test_modals_i18n.py`
- **Status:** Vollständig abgedeckt

### 4. Kombinierte Interaktion
- Kombinierte Tests für Tabs, Modale, Subtabs
- **Test:** `test_gui_mixed.py`
- **Status:** Abgedeckt

### 5. Einzeltests für Modale/Subtabs
- Separate Tests für Modale und Subtabs
- **Test:** `test_modals.py`, `test_subtabs.py`
- **Status:** Abgedeckt

### 6. Reporting-Subtabs
- Dropdown-Auswahl und Sichtbarkeit
- **Test:** `test_subtabs.py`
- **Status:** Abgedeckt

## Noch offene Bereiche / Empfehlungen
- Weitere Subtabs in anderen Tabs (Edit, Parser, Debug) prüfen und ggf. ergänzen
- Kontextmenüs, Dropdowns, Tooltips mit i18n validieren
- Dynamische Inhalte/Popups (Toasts, Fehlerdialoge) mit i18n testen
- Sprachwechsel und Textinhalt (i18n-Validierung) automatisieren
- Optional: Barrierefreiheit, visuelle Regression, Drag&Drop, Datei-Upload, externe Streams

## Fazit
Die Kern-GUI und i18n-Tags sind durch automatisierte Selenium-Tests weitgehend abgedeckt. Für vollständige Abdeckung sollten weitere dynamische und kontextabhängige UI-Elemente sowie Spezialfälle geprüft werden.
