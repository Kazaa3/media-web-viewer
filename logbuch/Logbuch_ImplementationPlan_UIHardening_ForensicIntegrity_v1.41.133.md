# Implementation Plan – UI Hardening & Forensic Integrity (v1.41.133)

## Ziel
Behebung des "Black Screen"-Problems durch Aktivierung der vollständigen forensischen Diagnostik und Implementierung eines "Nuclear Visibility Fix". Die GUI wird so gegen unsichtbare oder nicht gerenderte Fragmente gehärtet.

---

## Phase 1: Application Shell
- **[MODIFY] shell_master.html**
  - Füge folgende kritische Skripte im <body>-Footer ein:
    - `js/debug_helpers.js` (Integrity Engine)
    - `js/gui_diagnostics.js` (Hydration Mock)
    - `js/mwv_hotkeys.js` (Keyboard Interactions)
    - `js/audioplayer.js` (Media Engine)

## Phase 2: Diagnostic Hardening
- **[MODIFY] debug_helpers.js**
  - Erweitere `runUiIntegrityCheck` um Stage 8: Nuclear Visibility Force.
  - Diese Stufe iteriert über alle `.deck-view`-Container und erzwingt `display: flex !important` und `opacity: 1 !important`, falls ein "Black Screen" erkannt wird.
  - Automatischer Trigger: Wenn der Watchdog in `app_core.js` einen kritischen Timeout erreicht, wird `runUiIntegrityCheck()` ausgelöst.

## Phase 3: Interaction Layer
- **[MODIFY] mwv_hotkeys.js**
  - Mappe **Alt+U** auf `runUiIntegrityCheck()` für manuelle forensische Sweeps.

---

## Verification Plan
- **Automated Tests:**
  - Browser Probe: `window.runUiIntegrityCheck` ist definiert.
  - UI Probe: `#player-panel-container` hat nach dem Sweep eine sichtbare Höhe und Inhalt.
- **Manual Verification:**
  - Alt+U drücken: "Integrity Sweep"-Toast erscheint, die UI "heilt" sich selbst.

---

**Review erforderlich nach Umsetzung!**
