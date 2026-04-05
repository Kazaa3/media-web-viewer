# Implementation Plan: Restoration of Library Sub-Tabs

## Datum: 2026-03-29

### Problemstellung
- Die Sub-Navigationstabs (Coverflow, Grid, Details, etc.) im Bibliotheken-Tab waren nach einem UI-Refactor entfernt oder versteckt.
- Die Logik und Views existieren weiterhin, aber die Trigger-Buttons fehlten.

---

## Geplante Änderungen

### web/app.html
- **Restore View Switchers:**
  - Neue Navigationsleiste innerhalb des `coverflow-library-panel` einfügen.
  - Diese Zeile enthält Buttons für alle Library-View-Modi.
- **Button-Definitionen:**
  - lib-tab-btn-coverflow: `switchLibrarySubTab('coverflow')`
  - lib-tab-btn-grid: `switchLibrarySubTab('grid')`
  - lib-tab-btn-details: `switchLibrarySubTab('details')`
  - lib-tab-btn-streaming: `switchLibrarySubTab('streaming')`
  - lib-tab-btn-database: `switchLibrarySubTab('database')`
  - Optional: Buttons für Alben und Folge ich, falls gewünscht.
- **Styling:**
  - Verwendung der Klasse `options-subtab` für einheitliches Design (wie Debug, Parser, Reporting).

---

## Verifikationsplan

### Automatisierte Verifikation
- **Audit Suite:**
  - `tests/engines/suite_ui_integrity.py` ausführen.
  - Level 16 (Navigation Coverage): Prüft, ob die neuen Buttons als Navigationstrigger erkannt werden.
  - Level 14 (Subtab Structural Audit): Prüft, ob die Buttons korrekt zu den lib-view-* Containern gemappt sind.

### Manuelle Verifikation
- Anwendung starten und zum Bibliothek-Tab navigieren.
- Sicherstellen, dass die neue Subtab-Leiste (Coverflow, Grid, etc.) sichtbar ist.
- Jeden Subtab anklicken und prüfen:
  - Der Content-Bereich aktualisiert sich korrekt.
  - Der Button erhält die `.active`-Klasse.
  - Im Backend-Log erscheint ein `[JS-NAV] [SUBTAB-LIB]`-Event.

---

## Status
- Plan bereit zur Umsetzung. Nach Implementierung: vollständige UI- und Diagnostik-Absicherung.
