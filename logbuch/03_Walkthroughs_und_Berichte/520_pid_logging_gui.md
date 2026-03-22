# PID-Logging und GUI-Anzeige für mehrere Python-Umgebungen

## Ziel
- Beim Start des Media Web Viewer sollen die Prozess-IDs (PIDs) aller relevanten Python-Umgebungen (main, testbed, selenium) im Log erscheinen.
- Zusätzlich sollen die PIDs von testbed und selenium in der GUI angezeigt werden.

## Umsetzung

### 1. PID-Logging beim Startup
- Die Funktion `get_environment_info_dict()` liefert bereits die PID des Hauptprozesses.
- Erweiterung: Beim Start werden die PIDs der testbed- und selenium-Umgebungen ermittelt (z.B. durch Starten eines Dummy-Prozesses in der jeweiligen venv oder durch PID-Erkennung laufender Prozesse).
- Alle PIDs werden im Log ausgegeben:
  - Main-PID
  - Testbed-PID
  - Selenium-PID

### 2. Anzeige der PIDs in der GUI
- Die PIDs werden über ein Eel-exponiertes Backend-API an das Frontend übergeben (z.B. Erweiterung von `get_environment_info_dict()` oder neue API-Methode).
- Die GUI zeigt die PIDs von testbed und selenium an (z.B. im System-/Diagnosebereich).

### 3. Beispiel Log-Ausgabe
```
[System] Main PID: 12345
[System] Testbed PID: 23456
[System] Selenium PID: 34567
```

### 4. Beispiel GUI-Anzeige
- Bereich "Systeminfo" oder "Diagnose":
  - Main PID: 12345
  - Testbed PID: 23456
  - Selenium PID: 34567

## Hinweise
- Die PIDs der venvs können sich ändern, wenn die Prozesse neu gestartet werden.
- Die Ermittlung der PIDs für testbed/selenium kann über Subprozess-Start oder durch Scannen laufender Prozesse erfolgen.
- Die Implementierung ist so gestaltet, dass sie robust gegenüber fehlenden oder nicht gestarteten venvs ist (Anzeige: "nicht aktiv" o.ä.).

## Status
- [x] Konzept dokumentiert
- [ ] Implementierung in main.py
- [ ] Erweiterung der GUI
- [ ] Test & Validierung

---
*Letzte Aktualisierung: 2026-03-15*
