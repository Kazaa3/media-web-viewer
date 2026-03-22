# Fehler: Falsches venv für Testausführung – .venv_testbed wird ignoriert

**Datum:** 15.03.2026

## Problem
- Die Testausführung nutzt weiterhin den Interpreter aus `.venv_run` statt aus `.venv_testbed`.
- Dadurch tritt der Fehler auf:
  ```
  /home/xc/#Coding/gui_media_web_viewer/.venv_run/bin/python: No module named pytest
  ```
- Erwartet wird, dass `.venv_testbed` (mit pytest) für Tests verwendet wird.

## Analyse
- Die Logik zur Interpreter-Auswahl erkennt oder priorisiert `.venv_testbed` nicht korrekt.
- Mögliche Ursachen:
  - Der Pfad zu `.venv_testbed` wird nicht gefunden oder falsch geprüft.
  - Die Priorisierung in der Test-Discovery-Logik ist fehlerhaft.
  - Die Debug-Ausgabe zeigt nicht, warum `.venv_testbed` übersprungen wird.

## Empfehlung
- Terminal-Logs mit den neuen Debug-Ausgaben prüfen: Welche Interpreter werden gefunden, wie wird priorisiert?
- Die Logik in `main.py` gezielt auf die Auswahl und Prüfung von `.venv_testbed` untersuchen und ggf. korrigieren.
- Sicherstellen, dass `.venv_testbed/bin/python` existiert und verwendet wird, wenn vorhanden.

## Nächste Schritte
- Debug-Ausgabe auswerten und Interpreter-Logik anpassen, bis `.venv_testbed` zuverlässig für Tests genutzt wird.

**Ergebnis:**
- Erst nach Korrektur der Auswahl-Logik wird `.venv_testbed` wie gewünscht für Testläufe verwendet und der Fehler verschwindet.
