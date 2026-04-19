# Implementation Plan – Multi-Level UI Restoration & Hard Diagnostics (v1.41.134)

## Ziel
Behebung des Routing- und Fragment-Problems bei der STATUS-Kategorie durch Einführung eines dedizierten Status-Panels als "Atomic Command Center" für forensische Diagnostik.

---

## Phase 1: UI Orchestration
- **[MODIFY] app_core.js**
  - Registriere den Debug-Tab explizit im WindowManager.
  - Verknüpfe ihn mit `status-panel-container`.
  - Setze den Fragment-Pfad auf `fragments/status_panel.html`.
  - Füge einen `onActivate`-Hook hinzu, der beim Öffnen des Status-Tabs automatisch `runUiIntegrityCheck()` auslöst.

- **[MODIFY] ui_nav_helpers.js**
  - Harmonisiere die Category-to-Tab-Mappings.
  - Stelle sicher, dass `switchMainCategory('status')` die Debug-Tab-Registrierung korrekt triggert.

## Phase 2: New Fragment – Hard Diagnostics
- **[NEW] status_panel.html**
  - Erstelle ein hochdichtes forensisches Status-Panel.
  - Integriere einen Bereich für die 7+1 Stages of UI Integrity.
  - Füge einen Live Sentinel Log Stream (minimierte Sidebar) hinzu.
  - Buttons für:
    - FORCE RE-HYDRATION
    - NUCLEAR VISIBILITY FIX
    - CLEAR LOCALSTORAGE

---

## Verification Plan
- **Automated Tests:**
  - Browser Probe: `WM.activate('debug')` lädt das Status-Panel.
  - UI Probe: Level-2-Buttons wechseln zu "Logs" und "Health", wenn STATUS aktiv ist.
- **Manual Verification:**
  - STATUS klicken: Schwarzer Viewport wird durch die neue Diagnostik-Konsole ersetzt.
  - PLAYER klicken: UI kehrt korrekt zur Media Queue zurück.

---

**Review erforderlich nach Umsetzung!**
