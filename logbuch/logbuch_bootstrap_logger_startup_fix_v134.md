# Logbuch – Bootstrap Logger & Startup-Fix (v1.34)

## Problem
Beim Start der Anwendung trat ein `NameError: name 'log' is not defined` auf, weil `log.info()`-Aufrufe im allerersten Bootstrap-Guard von main.py standen – noch bevor der zentrale Logger initialisiert war.

---

## Lösung
- **Bootstrap Logger:**
  - Am absoluten Anfang von main.py wurde eine Minimal-Klasse eingeführt, die `log.info`, `log.error` und `log.warning` sicher auf STDOUT mapped.
  - Diese Klasse übernimmt alle Logging-Aufrufe während der frühen Environment-Guards und Initialisierung.
  - Sobald die App vollständig gestartet ist, übernimmt der professionelle Logger automatisch.

---

## Vorteile
- **Keine Crashes mehr:** Die Anwendung startet jetzt immer stabil, auch wenn Logging im Bootstrap-Guard benötigt wird.
- **Konsistentes Logging:** Der Code verwendet von Anfang an das `log`-Interface – keine Sonderfälle oder Workarounds nötig.
- **Bessere Auditierbarkeit:** Auch Bootstrap-Events sind jetzt sauber formatiert und werden von System-Logs erfasst.

---

## Status
- Fehler behoben, Anwendung startet wieder normal (`python3.14 src/core/main.py`)
- Logging ist ab der ersten Zeile konsistent und robust
