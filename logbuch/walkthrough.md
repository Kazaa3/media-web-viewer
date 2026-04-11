# Walkthrough: Video Player UI Cleanup & Test Suite Refactoring (26.03.2026)

## Zusammenfassung der Änderungen

### Video Player UI
- Horizontalen Split und alle redundanten Info-Panels (vlc-info, status-strip, vlc-extern-fallback-bar) aus `app.html` entfernt.
- Der Player nutzt jetzt die volle verfügbare Fläche für maximale Sichtbarkeit und ein aufgeräumtes Layout.
- Audio-Queue-Redirection: Klick auf Video-Dateien in der Audio-Queue leitet korrekt zum Video-Tab weiter.

### Test Suite Reorganisation
- Neuer Ordner `tests/scr` für Utility- und Maintenance-Skripte.
- Folgende Dateien wurden verschoben:
  - `src/core/test_media_factory.py` → `tests/unit/core/test_media_factory.py`
  - `src/core/curate_logbuch*.py` → `tests/scr/`
  - `src/core/fix_logbuch_numbers*.py` → `tests/scr/`
  - `src/core/reorganize_logbuch.py` → `tests/scr/`
  - `src/core/foundational_restoration.py` → `tests/scr/`
  - `src/core/final_history_fix.py` → `tests/scr/`
  - `src/core/final_history_polish.py` → `tests/scr/`
  - `inspect_db.py` → `tests/scr/`
  - Ausgewählte Dateien aus `scripts/` (z.B. `gui_validator.py`, `performance_test.py`) → `tests/scr/`
- Import-Logik in `inspect_db.py` angepasst, damit das Skript auch am neuen Ort funktioniert.

## Verifikation
- `pytest tests/` ausgeführt: Alle Kern-Tests laufen erfolgreich.
- Manuelle Prüfung: Video Player Tab ist aufgeräumt, keine Split/Info-Panels mehr sichtbar, Player nutzt volle Fläche.
- Audio-Queue-Redirection funktioniert wie erwartet.

## Fazit
Die UI ist jetzt deutlich übersichtlicher und die Test-/Utility-Skripte sind sauber im Projekt organisiert. Weitere Optimierungen können auf dieser Basis einfach umgesetzt werden.