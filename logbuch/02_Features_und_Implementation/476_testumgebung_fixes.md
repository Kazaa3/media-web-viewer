# Testumgebung: Fehlerursachen & Fixes für zuverlässige Testausführung

**Datum:** 15.03.2026

## Key Actions Taken

### 1. Modul-Shadowing behoben
- Ein veraltetes `parsers`-Verzeichnis im Projekt-Root hat das eigentliche `src/parsers`-Verzeichnis überschattet.
- Ursache für ImportError: z. B. `cannot import name 'IMAGE_EXTENSIONS'`.
- Lösung: Das Root-Verzeichnis wurde in `parsers_deprecated` umbenannt.

### 2. Test-Umgebung & PYTHONPATH
- Die Funktion `run_tests` in `src/core/main.py` setzt jetzt explizit `src/core` und `src/parsers` auf den `PYTHONPATH`.
- Dadurch können Tests alle Projektmodule (z. B. `db`, `main`) unabhängig vom Verzeichnis korrekt importieren.

### 3. Syntax- und Indentation-Fehler
- Mehrere `IndentationError` und `SyntaxError` in Testdateien wurden behoben:
  - `tests/integration/basic/utils/check_item.py`
  - `tests/iso/debug_pycdlib.py`
  - `tests/unit/tech/eel/test_eel_exposure_unit.py`
  - `tests/run_all_tests_commented.py` (fehlende Klammern)

### 4. Namens-Kollisionen
- Um "import file mismatch"-Fehler in Pytest zu vermeiden, wurden doppelte Utility-Skripte im Test-Root umbenannt:
  - `check_db.py` → `check_db_root.py`
  - `check_item.py` → `check_item_root.py`
- So werden Konflikte mit spezifischeren Integrationstests in Unterordnern vermieden.

## Verifikation
- Der Import und die Initialisierung von `MediaItem` funktionieren jetzt korrekt in der `.venv_testbed`-Umgebung.

## Nächste Schritte
- Tests können jetzt zuverlässig aus dem "Test"-Tab gestartet werden.
- Bei neuen Testfehlern bitte die Logs teilen – ich unterstütze dann gezielt bei der Testlogik!
