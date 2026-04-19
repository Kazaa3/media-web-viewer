# Logbuch: Level 1 Restoration & Granular Level 2 De-Duplication (v1.46.027)

## Datum
12. April 2026

## Ziel
Wiederherstellung der vollständigen Level-1-Navigation (12+ Hauptkategorien) und konsequente De-Duplizierung der Sub-Tabs auf Level 2 ("One-View-One-Home").

## Maßnahmen

### 1. Navigation Shell Restoration
- **app.html:**
  - Alle ursprünglichen 12+ Hauptnavigationstabs im Header wiederhergestellt: Player, Bibliothek, Database, Browser, Edit, Optionen, Parser, Debug, Tests, Tools, Report, Logbuch, Video.
- **ui_nav_helpers.js:**
  - categoryDefaults so angepasst, dass alle 12+ Kategorien korrekt auf ihre Hauptfragmente routen.

### 2. Granular Registry De-Duplication
- **config_master.py:**
  - media-Registry: Video-spezifische Sub-Tabs entfernt (nur noch unter Video).
  - library-Registry: Inventory (nur noch unter Database), Cinema (nur noch unter Video).
  - tools-Registry: Transcoding (nur noch unter Optionen/System).
  - debug-Registry: Audit (nur noch unter Logbuch).
  - unsort-Registry: Legacy-Links entfernt, die jetzt redundant sind.

## Verifikationsplan
- Alle 12+ Buttons sind im Header sichtbar.
- Video-Sub-Tabs erscheinen nur noch unter Video.
- Transcoding nur noch unter Optionen.
- Audit History nur noch unter Logbuch.
- logical_type-Fix bleibt aktiv und stellt die Sichtbarkeit der Medien sicher.

## Status
- Navigation ist granular, übersichtlich und ohne Redundanzen.
- Kein Funktionsverlust, alle Views haben einen klaren "Home"-Tab.
- Medien-Fix bleibt erhalten.

---

**Nächste Schritte:**
- Weitere UI- und Registry-Optimierungen nach Bedarf.
- Fortlaufende Überwachung der Navigation und Medienintegrität.
