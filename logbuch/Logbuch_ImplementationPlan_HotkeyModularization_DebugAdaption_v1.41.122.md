# Implementation Plan – v1.41.122 Hotkey Modularization & Debug Adaption

## Ziel
Entkopplung der Keyboard-Interaktionsschicht und Wiederherstellung des forensischen Hydration-Debug-Tools für die moderne Player-Architektur.

---

## Phase 1: Modularization
- **[NEW] mwv_hotkeys.js**
  - Dedizierter Event Listener für alle globalen Alt-Toggles (Alt+H/N/M/F/R/S).
  - Zentrale Verwaltung aller MWV_UI-Toggle-Aufrufe.
- **[MODIFY] ui_nav_helpers.js**
  - Cleanup: Entferne den redundanten keydown-Listener und den legacy toggleMenuBar()-Call.
- **[MODIFY] app.html**
  - Script Link: Füge `<script src="js/mwv_hotkeys.js"></script>` im Head/Body-Bereich hinzu (nach ui_core.js).

## Phase 2: Debugging & Stabilization
- **[MODIFY] gui_diagnostics.js**
  - Adaption: Implementiere `MWV_Diagnostics.forceHydrationTest()`, das:
    - Einen Satz Mock-Media-Items hardcodiert.
    - Diese in `window.currentPlaylist` injiziert.
    - Ein Re-Rendern von `#active-queue-list-render-target-warteschlange` erzwingt.
    - Die Player-Ansicht auf `display: flex` setzt.

---

## Open Questions
- Soll `forceHydrationTest` per Hotkey (z.B. Alt+D) oder nur über die Konsole/Diagnose-Overlay ausgelöst werden? **Annahme:** Über Button im Diagnostics-Overlay oder Alt+D.

---

## Verification Plan
- **Module Check:** Hotkeys funktionieren nach Auslagerung in die neue Datei.
- **Debug Check:** `MWV_Diagnostics.forceHydrationTest()` ausführen → Items erscheinen, "Black Screen" wird durch gefüllte Queue ersetzt.
- **Boot Integrity:** App startet korrekt ohne Hotkey-Interferenz.

---

**Review erforderlich nach Umsetzung!**
