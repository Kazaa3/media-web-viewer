# Logbuch: UX & Frontend Fixes, Testbed & Verifikation

**Datum:** 11. März 2026

---

## UX & Frontend Fixes
- [MODIFY] app.html
  - Direct Drag Logic: 400ms Delay entfernt, mousedown auf Handle startet Picking sofort.
  - Unique Tab IDs: id-Attribute für Navigation-Buttons (playlist-btn etc.) für zuverlässige Tests.
  - Improved Item Selection: stopPropagation nur bei aktivem Drag, normale Klicks selektieren/abspielen.
  - Drag-and-Drop Support: onMouseEnter zeigt Insert-Position, mouseup auf Ziel triggert releasePick.
  - State-Sync Fix: eel.jump_to_index im play-Flow für Backend-Sync.

---

## Test Suite & Infrastructure
- [NEW] venv_testbed: Isolierte Umgebung für GUI-Tests, trennt Test-Abhängigkeiten vom Hauptprojekt.
- [MODIFY] test_utils.py
  - Smart Discovery: find_running_project_sessions findet IDE-Session zuverlässig.
  - Strict No-Spawn: manage_app_instance priorisiert bestehende Sessions, kein unnötiges Spawning.
  - Robustness: robust_action für automatische Retries bei StaleElementReferenceException.
- [MODIFY] run_gui_tests.py: Führt alle Tests im Kontext von venv_testbed aus.

---

## Verification Plan
- Automated Tests
  - python3 tests/run_gui_tests.py mit IDE-Python.
  - Reordering funktioniert ohne manuelle Eingriffe im Testlauf.
- Manual Verification
  - Manuelles Testen des Pickings in der Playlist.
  - App bleibt responsiv während initialem Media-Scan.
