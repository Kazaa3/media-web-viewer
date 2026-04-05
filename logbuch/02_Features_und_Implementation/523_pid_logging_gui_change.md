# Änderung: PID-Logging & GUI-Anzeige für testbed/selenium

**Datum:** 2026-03-15

## Zusammenfassung
- Die PIDs der testbed- und selenium-Umgebungen werden jetzt beim Start im Log ausgegeben und in der GUI angezeigt.
- Die Anzeige ist robust: Falls die Umgebungen nicht laufen, wird "nicht aktiv" angezeigt.

## Technische Details
### Backend (main.py)
- `get_environment_info_dict()` liefert jetzt zusätzlich `testbed_pid` und `selenium_pid` (ermittelt per psutil, None wenn nicht aktiv).
- Beim Startup werden alle relevanten PIDs (main, testbed, selenium) ins Log geschrieben.

### Frontend (web/app.html, web/script.js)
- Im Bereich "Backend" der Systeminfo werden die PIDs für Main, Testbed und Selenium angezeigt.
- Die Funktion `loadEnvironmentInfo()` setzt die neuen Felder (`env-main-pid`, `env-testbed-pid`, `env-selenium-pid`) dynamisch.
- Anzeige: PID oder "nicht aktiv".

## Motivation
- Transparenz über laufende Python-Umgebungen und deren Prozesse.
- Schnellere Diagnose bei Test-/E2E-Problemen.

## Beispiel Log-Ausgabe
```
[System] Main PID: 12345
[System] Testbed PID: nicht aktiv
[System] Selenium PID: 23456
```

## Beispiel GUI
- Main PID: 12345
- Testbed PID: nicht aktiv
- Selenium PID: 23456

## Betroffene Dateien
- src/core/main.py
- web/app.html
- web/script.js
- logbuch/2026-03-15_pid_logging_gui.md

---
*Change-Log-Eintrag für Nachvollziehbarkeit und Review.*
