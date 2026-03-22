# Logbuch: Proposed Changes & Test/UX-Plan

**Datum:** 11. März 2026

---

## Infrastructure
- [NEW] Selenium Virtual Environment
  - Erstelle `.venv_selenium` im Projekt-Root.
  - Installiere `selenium`, `webdriver-manager` (optional) und requirements.
  - Shell-Skripte zum Ausführen von Tests mit dieser Umgebung.

---

## Performance & Telemetry
- [NEW] Telemetrie-Layer
  - Startup-Trace: Zeitmessung von main.py-Start bis eel.start.
  - Scan-Trace: Messung der Scan-Phasen (Directories, Files, Total).
  - Parser-Trace: Messung pro Datei (Extraktionsdauer, Parser-Chain-Erfolg).

---

## UX & Frontend Fixes
- [MODIFY] app.html
  - Picking Logic: Refaktor onGrabPointerDown/Up für Unterscheidung zwischen Short Click, Long-Press Picking und Dragging.
  - Auto-Cancel Fix: Mouseup soll Pick-State nicht abbrechen, wenn es die gleiche Interaktion war.
  - Drag-and-Drop Support: onMouseEnter für Insert-Position, mouseup auf Zielitem triggert releasePick.
  - Visual Feedback: Subtiler Pulse/Overlay bei "picked" Item.
  - State-Sync Fix: eel.jump_to_index im play-Flow für Backend-Sync.
  - UI Tracing: appendUiTrace für Remote-Debugging von Reorder-Events.

---

## Test Suite Expansion
- [NEW] tests/test_parser_interaction.py
  - Simuliert langsamen/blockierenden Parser.
  - Verifiziert, dass UI interaktiv bleibt und Reordering funktioniert.
- [NEW] tests/test_ui_refresh.py
  - Verifiziert, dass pickedIndex und playlistIndex nach Refresh/Tab-Switch erhalten bleiben.

---

## Verification Plan
- Automated Tests
  - `python3 tests/run_gui_tests.py` (Wrapper für .venv_selenium)
  - Einzelverifikation des 'Hammerhart'-Szenarios.
- Manual Verification
  - Manuelles Testen des Pickings im Playlist-UI.
  - App bleibt responsiv während initialem Media-Scan.

---

## Comment
Ctrl+Alt+M
