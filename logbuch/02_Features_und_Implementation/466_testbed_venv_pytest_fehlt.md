# Testbed venv: Fehler beim Testlauf – pytest fehlt

**Datum:** 15.03.2026

## Problem
- Beim Starten der Tests im Testbed-venv erscheint folgender Fehler:
  ```
  /home/xc/#Coding/gui_media_web_viewer/.venv_run/bin/python: No module named pytest
  [Python Tests - Exit Code: 1]
  ```
- Die Tests werden dadurch nicht ausgeführt.

## Ursache
- Im Testbed-venv ist das Modul `pytest` (und ggf. weitere Test-Abhängigkeiten) nicht installiert.
- Das Build- und Testsystem erwartet, dass alle benötigten Testpakete in der aktiven Umgebung vorhanden sind.

## Lösung
- Installiere `pytest` (und ggf. weitere Test-Abhängigkeiten) im Testbed-venv, z. B. mit:
  ```bash
  source .venv_run/bin/activate
  pip install -r infra/requirements-test.txt
  # oder mindestens:
  pip install pytest
  ```
- Danach können die Tests erfolgreich ausgeführt werden.

## Ergebnis
- Nach Installation der fehlenden Pakete läuft der Testlauf im Testbed-venv fehlerfrei durch.
