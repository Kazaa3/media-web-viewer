# Erklärung der PID-Variablen (Backend/Frontend)

## Backend (main.py, get_environment_info_dict)
- **pid**: Die Prozess-ID (PID) des aktuell laufenden Hauptprozesses (Media Web Viewer Backend).
- **testbed_pid**: Die PID eines laufenden Python-Prozesses aus der Testumgebung `.venv_testbed` (falls vorhanden, sonst `None`).
- **selenium_pid**: Die PID eines laufenden Python-Prozesses aus der Selenium-Testumgebung `.venv_selenium` (falls vorhanden, sonst `None`).
- **browser_pid**: Die PID des vom Backend gestarteten Browser-Prozesses (z.B. für Eel/Frontend).

## Frontend (app.html, script.js)
- **env-main-pid**: Anzeigeelement für die Hauptprozess-PID (`pid`).
- **env-testbed-pid**: Anzeigeelement für die Testbed-PID (`testbed_pid`).
- **env-selenium-pid**: Anzeigeelement für die Selenium-PID (`selenium_pid`).

## Verhalten
- Ist eine Umgebung nicht aktiv, wird "nicht aktiv" angezeigt.
- Die Werte werden dynamisch beim Laden der Systeminfo aus dem Backend übernommen.

## Zweck
- Transparenz über laufende Prozesse und Umgebungen.
- Schnellere Fehlerdiagnose bei Test- und E2E-Problemen.

---
*Stand: 2026-03-15*
