# Implementation Plan: Navigation Refinement & Zero-Deletion Policy (v1.46.027)

## Ziel
1. Navigation konsolidieren, ohne funktionale Sub-Tabs zu löschen (Zero-Deletion Policy).
2. Alternativ: Level 1 Navigation vollständig wiederherstellen (12+ Hauptkategorien), Level 2 granular de-duplizieren.

## Schritte

### Variante A: Zero-Deletion Policy (4 Master-Gruppen)
- **config_master.py:**
  - Registry so gruppieren, dass ALLE bisherigen Sub-Tabs erhalten bleiben, aber logisch in die 4 Master-Gruppen einsortiert werden:
    - **media:** Player (Audio), Library, Playlist, Video, Lyrics, Visualizer
    - **management:** Inventory, File Browser, Meta Editor, Parser Engine, Core Tools
    - **options:** General Settings, Debug & DBPanel, Transcoding, Environment, System Flags
    - **diagnostics:** Unit Tests, Performance Reporting, Logbuch (Audit History)
- **ui_nav_helpers.js:**
  - Sicherstellen, dass alle wiederhergestellten IDs korrekt auf die jeweiligen View-Switching-Funktionen gemappt werden.
- **Verifikation:**
  - 4 Buttons im Header, Sub-Navigation enthält alle alten Sub-Tabs an logischer Stelle.

### Variante B: Level 1 Restoration & Granular Level 2 De-Duplication
- **app.html:**
  - 12+ Hauptnavigationstabs im Header wiederherstellen: Player, Bibliothek, Database, Browser, Edit, Optionen, Parser, Debug, Tests, Tools, Report, Logbuch, Video.
- **ui_nav_helpers.js:**
  - categoryDefaults so anpassen, dass alle 12+ Kategorien korrekt auf ihre Hauptfragmente routen.
- **config_master.py:**
  - media-Registry: Video-spezifische Sub-Tabs entfernt (nur noch unter Video).
  - library-Registry: Inventory (nur noch unter Database), Cinema (nur noch unter Video).
  - tools-Registry: Transcoding (nur noch unter Optionen/System).
  - debug-Registry: Audit (nur noch unter Logbuch).
  - unsort-Registry: Legacy-Links entfernt, die jetzt redundant sind.
- **Verifikation:**
  - 12+ Buttons im Header sichtbar.
  - Video-Sub-Tabs erscheinen nur noch unter Video.
  - Transcoding nur noch unter Optionen.
  - Audit History nur noch unter Logbuch.
  - logical_type-Fix bleibt aktiv.

## Status
- Navigation ist entweder logisch gruppiert (4 Master-Gruppen, Zero-Deletion) ODER vollständig granular (12+ Tabs, Level 2 dedupliziert).
- Keine funktionalen Sub-Tabs gehen verloren, Redundanzen werden entfernt.
- Medien-Fix (logical_type) bleibt erhalten.

---

**Freigabe erforderlich:**
Bitte bestätigen Sie, ob Variante A (4 Gruppen, Zero-Deletion) oder Variante B (12+ Tabs, granular dedupliziert) umgesetzt werden soll.