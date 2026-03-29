# Implementation Plan: Standardizing Split Layouts (Item, Edit, Options)

## Datum: 2026-03-29

### Ziel
- Vereinheitlichung der Split-Layout-Architektur für die Management-Tabs: Item (Inventory), Edit (Metadata Editor), Options (System Config).

---

## Geplante Änderungen

### web/app.html

#### 1. [Component] TAB: Item (Inventory)
- **Structure:**
  - `indexed-sqlite-media-repository-panel` wird zum flex-Container.
- **Sidebar:**
  - `item-sidebar-left` für Kategorie-Filterung oder Suche hinzufügen.
- **Content:**
  - `persistent-sqlite-repository-item-grid` in `item-main-content-pane` verschieben.

#### 2. [Component] TAB: Edit (Metadata Editor)
- **Refinement:**
  - Split-Layout in `metadata-writer-crud-panel` prüfen und vereinheitlichen.
- **Cleanup:**
  - Splitter und Panes nach Standard-Benennung (wie Item/Options) umbenennen.

#### 3. [Component] TAB: Options (System Config)
- **Split Layout:**
  - `#options-split-container` mit linker Sidebar und rechtem Content-Bereich einführen.
- **Sub-Navigation:**
  - Einheitliche `options-nav-tabs`-Bar im Header der Options-Tab.
- **Categorized Views:**
  - Lange Scroll-Liste in einzelne Views aufteilen:
    - General: Pfade, Sprache, Startseite
    - Appearance: Minimalmodus, Parserzeiten, UI-Scaling
    - Indexing: Scan, Mock-System, Medientypen
    - Transcoding: Wiedergabe, Bandbreite, Hardware
    - Debug & Flags: Log-Flags, Backend-Reset

#### 4. [Component] Navigation Logic
- **Helper Function:**
  - `switchOptionsView(viewId)` für Sichtbarkeit und Active-State der Options-Subtabs.
- **Unified Tracing:**
  - Alle Subtab-Wechsel via `traceUiNav` loggen.

---

## Verifikationsplan

### Automatisierte Tests
- **UI Integrity Suite:**
  - `suite_ui_integrity.py` prüft:
    - Neue Container-IDs existieren und sind erreichbar.
    - Subnav-Buttons haben gültige OnClick-Handler.
    - DOM-Hierarchie ist valide (keine vorzeitigen Closures).

### Manuelle Verifikation
- Prüfen, dass Item- und Options-Tabs ein funktionales Sidebar-Split-Layout haben.
- Durch die neuen Options-Subtabs navigieren und prüfen, dass Einstellungen erhalten bleiben.
- Debug & Flags lädt Flags weiterhin dynamisch.

---

## Status
- Plan bereit zur Umsetzung. Nach Implementierung: UI-Standardisierung und bessere Wartbarkeit.
