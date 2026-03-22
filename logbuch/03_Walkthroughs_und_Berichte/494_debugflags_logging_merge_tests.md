# Logbuch: Debugflags & Logging – Wirkung nach Merge, Teststatus & Reparatur

**Datum:** 15.03.2026

## Kontext
Nach dem letzten Merge sollen die Wirkung der Debugflags und das Logging-System überprüft, die zugehörigen Tests ausgeführt und ggf. repariert werden.

## Überprüfung & Analyse
- **Debugflags:**
  - Initialisierung und Steuerung über `initialize_debug_flags()` in `main.py`.
  - Flags werden zentral im Dictionary `DEBUG_FLAGS` verwaltet und über die UI sowie CLI (`--debug`) gesetzt.
  - Die Funktionalität wird über `logger.set_debug_flags()` und gezielte Komponenten-Logs (`logger.debug(component, message)`) gesteuert.
- **Logging:**
  - Zentrales Logging-System in `logger.py` mit File-, Console- und UI-Handler.
  - Logbuffer für UI-Analyse und Fehlerdiagnostik.
  - Loglevel und Debug-Logfile werden dynamisch je nach Umgebung und Debugflag gesetzt.

## Teststatus (nach Merge)
- **Tests vorhanden:**
  - `tests/test_logging.py`: Testet Logging-Setup, File-Logging, UI-Buffer, Komponenten-Logger, Buffer-Limit, Debug-Logfile.
  - `tests/test_debug_flags.py` & `tests/integration/basic/logging/test_debug_flags.py`: Testen gezielte Wirkung der Debugflags auf Logausgabe.
  - `tests/integration/tech/test_debug_tab_values.py`: Testet Debug-Tab-UI und Label-Logik.
  - `tests/e2e/selenium/pages/test_debug_and_db.py`: E2E-Tests für Debug/DB-Tab (Platzhalter).
- **Fehler nach Merge:**
  - ImportError: Zwei Testdateien mit gleichem Namen (`test_debug_flags.py`) führen zu pytest-Importkonflikt.
  - Lösung: Mindestens eine Datei umbenennen, damit pytest die Module eindeutig zuordnen kann.

## Nächste Schritte
1. **Testdatei umbenennen** (`tests/integration/basic/logging/test_debug_flags.py` → z.B. `test_debug_flags_basic.py`).
2. **Tests erneut ausführen** und Fehlerprotokoll prüfen.
3. **Fehlerhafte Tests reparieren** und Wirkung der Debugflags/Logging nach Merge validieren.

## Testergebnisse nach Umbenennung und Ausführung
- **14 von 16 Tests bestanden**
- **Fehlschläge:**
  1. `test_project_debug_log_file` (tests/test_logging.py): Debug-Logfile wurde nicht wie erwartet unter `/logs/debug.log` angelegt, sondern unter `/data/logs/debug.log` (siehe Logausgabe). Ursache: Unterschiedliche Logpfad-Logik im Test vs. logger.py.
  2. `test_debug_tab_json_logic` (tests/integration/tech/test_debug_tab_values.py): Erwartete JSON-Logik (`JSON.stringify(debugConsole.env|debug_flags`) im Debug-Tab nicht gefunden. Möglicherweise wurde die UI-Logik geändert oder entfernt.

## Reparaturmaßnahmen
- **Test für Debug-Logfile**: Test anpassen, damit er den tatsächlichen Logpfad (`data/logs/debug.log`) prüft, wie von logger.py verwendet.
- **Debug-Tab-JSON-Test**: UI/JS-Code prüfen und ggf. Test und/oder Frontend anpassen, damit die Debug-Informationen wie erwartet angezeigt werden.

## Zusatz: Geckodriver-Fehler im CI – Zusammenhang mit GitHub Actions
- Der Fehler beim Installieren von `firefox-geckodriver` entsteht nicht durch GitHub selbst, sondern durch die verwendete CI-Umgebung (GitHub Actions) und das zugrundeliegende Ubuntu-Image.
- In Ubuntu 24.04 ist das Paket `firefox-geckodriver` nicht mehr verfügbar, daher schlägt die Installation im CI-Workflow fehl.
- GitHub Actions ist lediglich die Plattform, auf der das Problem sichtbar wird – die eigentliche Ursache ist die Paketänderung in Ubuntu, nicht GitHub oder Geckodriver selbst.
- Lösung: Geckodriver direkt von Mozilla herunterladen und im CI-Workflow manuell installieren (siehe separaten Logbucheintrag zum CI-Geckodriver-Problem).

## Status
- Debugflags und Logging funktionieren, aber zwei Tests müssen an neue Pfade/Logik angepasst werden.
- Nach Reparatur erneute Testausführung empfohlen.

## Fazit
- Debugflags und Logging sind nach Merge grundsätzlich funktionsfähig, aber die Testabdeckung ist durch einen Importkonflikt blockiert.
- Nach Umbenennung und erneuter Ausführung können Fehler gezielt repariert werden.
- Die Dokumentation und Teststrategie bleibt damit nachvollziehbar und reproduzierbar.
