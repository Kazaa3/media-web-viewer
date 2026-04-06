# Implementation Plan – v1.34 UI Finalization & Mediengalerie Restoration

## Ziel
UI-Umstrukturierung für v1.34: Aufteilung des Audio Players in Sub-Tabs, Wiederherstellung der "Mediengalerie" (Item Player), und zentrales Footer-Cluster.

---

## Proposed Changes

### [UI] Navigation & Shell

**[MODIFY] app.html**
- Sub-Nav Bar (Reihe 2) aktualisieren, um die neue Aufteilung für "Player" zu unterstützen.
- Footer-Cluster neu strukturieren:
  - **Mitte:** [SCAN] [SYNC] [RESET DB] (Admin-Cluster)
  - **Rechts:** [THEME TOGGLE] [VOLUME] [MENU]
- Platzhalter für Dual-Mode Audio Player (Queue vs. Gallery) definieren.

**[MODIFY] ui_nav_helpers.js**
- `switchMainCategory('media')` rendert die korrekten Sub-Navigation-Pills.
- `switchTab` lädt/zeigt die gewünschte Ansicht (Queue vs. Gallery).

---

### [JS] Audio Player & Source Control

**[MODIFY] audioplayer.js**
- **renderItemGallery():**
  - Holt `allLibraryItems` und rendert sie im High-Density-v1.33-Listenstil.
- **Source Selection Dropdown:**
  - media: Filtert `allLibraryItems` nach Pfad ./media.
  - library: Zeigt alle `is_mock=false` Items.
  - custom: Triggert `eel.pick_directory()`.

---

### [JS] Data Pipeline Fixes

**[MODIFY] bibliothek.js**
- **loadLibrary():**
  - Debugging für korrekte, case-insensitive Kategoriezuordnung.
- **refreshLibrary():**
  - Broadcast an beide Player-Views (Queue & Gallery).

**[MODIFY] main.py**
- **get_library():**
  - Filter-Logik prüfen, damit echte und Mock-Items nicht versehentlich entfernt werden.

---

## Verification Plan

### Automated Tests
- `python3.14 scripts/app_audit_playwright.py` prüft neue Sub-Tabs.
- `logs/app.log` auf erfolgreiche Media-Discovery und Filter-Matches überwachen.

### Manual Verification
- **Header Check:** Sub-Tabs "Warteschlange" und "Mediengalerie" erscheinen unter Player.
- **Gallery Check:** "Mediengalerie" klicken, alle echten Dateien aus ./media/ werden gelistet.
- **Source Check:** Source-Dropdown toggeln, Liste aktualisiert sich korrekt.
- **Theme Check:** Theme-Toggle funktioniert im Footer-Cluster.

---

**User Review Required:**
- Audio Player ist in Queue- und Galerie-Ansicht aufgeteilt.
- Footer-Cluster ist modern und funktionsreich.
- Mediengalerie zeigt alle echten Dateien nach Scan korrekt an.
