# Implementation Plan – Nuclear Level 2 Global Consolidation (v1.41.137)

## Ziel
Vollständiger Neuaufbau von Level 2 (Sub-Navigation) über alle Dateien hinweg, um Cross-Effects, doppelte Menüs und inkonsistente Logik zu eliminieren. Die Navigation wird in eine einzige, robuste Engine zentralisiert.

---

## 1. Global Purge (HTML)
- **[DELETE] Fragments Sub-Menus**
  - Entferne `<div class="sub-nav-bar">` aus:
    - fragments/metadata_editor.html
    - fragments/diagnostics_suite.html
    - fragments/tools_panel.html
    - fragments/options_panel.html
    - fragments/logbuch_panel.html
    - fragments/reporting_dashboard.html
  - Level 2 wird nur noch von der Shell gerendert, der "Double-Menu"-Effekt verschwindet.

## 2. Style Unification (CSS)
- **[MODIFY] main.css**
  - Entferne alle redundanten Sub-Nav-Style-Blöcke (z.B. Zeilen 868–908, 1883–1910).
  - Definiere einen einzigen, maßgeblichen `.atomic-sub-nav`-Style für `#sub-nav-container`.

## 3. Engine Rebuild (JS)
- **[MODIFY] ui_nav_helpers.js**
  - Implementiere `AtomicNav.update(category)` als einzige Einstiegsmethode für Level 2.
  - Synchronisiere direkt mit den Labels aus `config_master.py`.
  - Entferne alle alten "active pill"-Tracker aus `audioplayer.js` und `bibliothek.js`, um State-Konflikte zu verhindern.

---

## Verification Plan
- **Automated Tests:**
  - Sweep Audit: `grep sub-nav-bar` nach dem Purge → 0 Treffer im fragments/-Verzeichnis.
  - Registry Test: `AtomicNav.update('media')` erzeugt exakt 4 Pills (Queue, Playlist, Visualizer, Lyrics).
- **Manual Verification:**
  - Durchlauf aller Haupt-Tabs (Player, Library, Status, Options): Level 2-Bar aktualisiert sich fehlerfrei und ohne Duplikate.

---

**Review erforderlich nach Umsetzung!**
