# Implementation Plan – Level 2 Reconstruction & Shell Consolidation (v1.41.136)

## Ziel
Konsolidierung der Navigation in eine einzige, hochwertige Global Bar und Synchronisierung mit dem Backend-Registry. Redundante und inkonsistente Level-2-Menüs werden beseitigt.

---

## Phase 1: UI Consolidation
- **[MODIFY] app.html**
  - Entferne das redundante `<div id="player-sub-nav-shell">` (Zeilen 364–376).
  - Dadurch verschwindet der "Double Menu"-Effekt und die vertikale Integrität des Viewports wird wiederhergestellt.
  - Stelle sicher, dass `#sub-nav-container` korrekt positioniert ist, um die dynamischen Pills aufzunehmen.

## Phase 2: Style Hardening (Level 2)
- **[MODIFY] main.css**
  - Redesign von `.sub-pill-btn` für ein Premium-High-Density-Look:
    - 4px Radius, enges Padding, leuchtende aktive Zustände.
    - Transparenter Glas-Hintergrund mit subtilen Rändern.

## Phase 3: Logic Synchronization
- **[MODIFY] ui_nav_helpers.js**
  - Aktualisiere `SUB_NAV_REGISTRY` so, dass es exakt mit `src/core/config_master.py` übereinstimmt:
    - media: Queue, Playlist, Visualizer, Lyrics
    - library: Cinema, Filme
    - status: Live Logs, Core Health
    - system: Allgemein, Darstellung
  - Sorge dafür, dass `updateGlobalSubNav` Kategorie-Aliase korrekt behandelt (z.B. media → player) und das DOM für nicht getrackte Kategorien leert.

## Phase 4: Viewport Restoration
- **[MODIFY] window_manager.js**
  - Stelle sicher, dass die Kategorie media den `player-panel-container` korrekt aktiviert.
  - Synchronisiere mit den Tab-IDs in app.html, um "Black Screen"-Fragmente zu verhindern.

---

## Verification Plan
- **Automated Tests:**
  - Registry Parity Check: JS `SUB_NAV_REGISTRY` entspricht den Keys in `config_master.py`.
  - Viewport Probe: Klick auf "Player" zeigt NUR eine Level-2-Bar und einen sichtbaren Inhaltsbereich.
- **Manual Verification:**
  - "STATUS" zeigt jetzt "Gesundheit" und "Protokolle" in derselben Level-2-Bar wie "Queue".
  - Der Haupt-Viewport bleibt nach Kategorie-Wechsel sichtbar und nicht schwarz.

---

**Review erforderlich nach Umsetzung!**
