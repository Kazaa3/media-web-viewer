# Implementation Plan – v1.41.109 Legacy Evolution

## Ziel
Reaktivierung der legacy app.html-Shell und Upgrade auf den "Atomic Standard" v1.41.109. Die Multi-Panel-Tiefe der alten App wird mit der forensischen Observability der neuen Architektur kombiniert.

---

## Phase 1: Legacy Shell Modernization
- **[MODIFY] app.html**
  - ID Alignment: Benenne die View-Container nach Atomic-Standard um:
    - `state-orchestrated-active-queue-list-container` → `player-panel-container`
    - `coverflow-library-panel` → `library-panel-container`
  - DOM Observability: Füge `data-mwv-category` und `data-mwv-tab` zum <body>-Tag hinzu.
  - HUD Update: Harmonisiere die Diagnose-IDs (`diag-pid`, `diag-boot`, `diag-up`) in Header und Footer mit der Logik in app_core.js.

## Phase 2: Backend Activation
- **[MODIFY] main.py**
  - Entry Pivot: Schalte eel.start() zurück auf app.html.

## Phase 3: Stability Restoration
- **[MODIFY] ui_nav_helpers.js**
  - Geometry Sync: Stelle sicher, dass die legacy `refreshUIVisibility()` nicht mit den neuen DOM-Attributen kollidiert.

---

## Verification Plan
- **Bootstrap Success:** App startet mit app.html und zeigt korrekte PID/BOOT-Infos an.
- **Hydration Check:** Alle Multi-Panels (Player, Library, etc.) laden korrekt in die umbenannten Container.
- **Observability Check:** document.body-Attribute werden beim Tab-Wechsel in der Legacy-Shell korrekt aktualisiert.

---

**Review erforderlich nach Umsetzung!**
