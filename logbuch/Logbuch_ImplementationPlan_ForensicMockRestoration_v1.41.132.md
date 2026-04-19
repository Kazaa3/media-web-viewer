# Implementation Plan – Forensic Mock Restoration (v1.41.132)

## Ziel
Behebung des "Black Screen"/"Queue Black Hole"-Problems durch Re-Implementierung des bewährten High-Density-Mock-Bypass. Die GUI bleibt so auch bei Backend-/Parser-Ausfall voll funktionsfähig.

---

## Phase 1: Diagnostic Engine
- **[MODIFY] gui_diagnostics.js**
  - Erweitere `forceHydrationTest` zu einem 12-Item "Elite Mock Pack".
  - Items umfassen verschiedene Kategorien (Audio, Video, FLAC, MP3) und realistische Metadaten.
  - Jedes Item erhält das Property `is_mock: true`.

## Phase 2: Boot Orchestration
- **[MODIFY] app_core.js**
  - Erweitere `startBootWatchdog` um einen Auto-Mock-Fallback.
  - Wird `DATA-READY` nicht innerhalb von maxTicks (~8s) erreicht, wird `forceHydrationTest()` automatisch ausgelöst.
  - Zeige einen "Safety Hydration Active"-Toast zur Benachrichtigung an.

## Phase 3: UI Interaction
- **[MODIFY] mwv_hotkeys.js**
  - Stelle sicher, dass ein dedizierter Hotkey (z.B. Alt+M) als manueller Bypass erhalten bleibt.

---

## Verification Plan
- **Automated Tests:**
  - Browser Probe: Nach Watchdog-Timeout ist `window.allLibraryItems.length > 0`.
  - UI Probe: `.legacy-track-item`-Elemente werden im DOM gerendert.
- **Manual Verification:**
  - App starten und 8 Sekunden warten: Mock-Items erscheinen.
  - Alt+M drücken: Queue wird mit Mock-Daten aktualisiert.

---

**Review erforderlich nach Umsetzung!**
