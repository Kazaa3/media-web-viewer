# Implementation Plan – v1.34 Unified Logging & DOM Diagnostics

## Ziel
Modernisierung der Diagnostik: Einheitliches Logging für Backend und Frontend, explizite DOM/UI-State-Traceability, keine Änderungen an der Tab-Struktur.

---

## Proposed Changes

### [Backend] Media Engine & Core
**[MODIFY] main.py**
- Alle print()-Aufrufe (Bootstrap, System, Restart, Watchdog etc.) werden durch log.info(), log.error(), log.debug() ersetzt.
- Beispiel: print("STDOUT: [Bootstrap] ...") → log.info("[Bootstrap] ...")
- log_gui_event und report_items_spawned auf einheitliche Log-Formate umstellen.

### [Frontend] Control Logic
**[MODIFY] ui_nav_helpers.js**
- console.log() durch mwv_trace('NAV-UI', 'EVENT', { ... }) ersetzen.
- DOM Logging: mwv_trace('DOM-STATE', 'TAB-SWITCH', { tabId }) in switchMainCategory und switchTab einbauen.
- Traces für Menü-Toggle und Layout-Anpassungen ergänzen.

**[MODIFY] bibliothek.js**
- console.log() durch mwv_trace('DATA-LIB', 'EVENT', { ... }) ersetzen.
- mwv_trace('DOM-UI', 'RENDER-START', { count: items.length }) und RENDER-COMPLETE ergänzen.

**[MODIFY] audioplayer.js**
- Playback-Logs: console.log() durch mwv_trace('PLAYER-EVENT', 'STATE-CHANGE', { track: title, isPlaying }) ersetzen.

### [Frontend] Logging Utility
**[MODIFY] trace_helpers.js**
- mwv_trace robuster machen, komplexe Detail-Objekte korrekt serialisieren.
- eel.log_ui_event nur aufrufen, wenn vorhanden.

---

## Open Questions
- Sollen mwv_trace-Messages weiterhin im Browser-Console erscheinen (console.log im Helper) oder nur Backend/DOM-Console?
- Gibt es performance-kritische Funktionen (z.B. Visualizer), wo Logging reduziert werden soll?

---

## Verification Plan
- **Automated:**
  - Source-Audit auf verbleibende print( und console.log( (z.B. grep "print(" src/core/main.py)
  - Nach App-Start: app.log prüfen, ob alle Bootstrap-Events geloggt werden
- **Manual:**
  - Nav Sync: Tabs durchklicken, strukturierte Einträge im Backend-Log (GUI-TRACE) prüfen
  - DOM Console: Debug-Konsole toggeln, "DOM-STATE"-Messages für jeden Tab-Switch sichtbar
