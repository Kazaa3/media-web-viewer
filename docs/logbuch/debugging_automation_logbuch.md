---

# Logbuch-Eintrag: Debugging & Testautomatisierung (März 2026)

## Ziel

Robuste Debug- und Teststrategie für die Mediathek-GUI und das Backend, um strukturelle Fehler, UI-Probleme und Backend-Instabilitäten frühzeitig zu erkennen und automatisiert zu beheben.

---

## 1. Backend-Prozessmanagement
- **Start:**
  - Backend wird mit `setsid nohup python3 src/core/main.py > backend.log 2>&1 &` im Hintergrund gestartet, um Terminalbindung/Suspension zu vermeiden.
- **Stop:**
  - Nach Tests: `pkill -f src/core/main.py`
- **Log:**
  - Fehler und Ausgaben werden in `backend.log` geschrieben und regelmäßig geprüft.

---

## 2. GUI-Validierung & Strukturprüfung
- **scripts/gui_validator.py:**
  - Prüft HTML-Struktur (DIV-/Tag-Tiefen, Bracket-Balance, orphaned Tags)
  - Vor und nach jeder Änderung ausführen, Ziel: "Final TAG stack size: 0"
- **app.html:**
  - Negative DIV-Tiefen, Bracket-Ungleichgewichte und verschachtelte Skript-Tags werden mit dem Validator identifiziert und repariert.

---

## 3. Selenium-Tests & UI-Regression
- **scripts/test_gui_structure_selenium.py:**
  - Kombiniert Selenium-UI-Tests (Tabs, ISBN-Button) mit gui_validator.py
  - Prüft Sichtbarkeit und Funktionalität der wichtigsten UI-Elemente
- **Workflow:**
  - Backend starten → Selenium-Test ausführen → Backend stoppen
  - Fehler werden direkt im Testlauf und in backend.log sichtbar

---

## 4. Typische Fehlerquellen & Debugging-Tipps
- **ReferenceError (z.B. appendUiTrace):**
  - Ursache: Fehlende JS-Funktion oder falsche Einbindung
  - Lösung: Funktion implementieren oder Referenz entfernen, Browser-Konsole prüfen
- **DIV/Tag-Probleme:**
  - Mit gui_validator.py und Context Trace gezielt verschachtelte oder offene Tags finden
- **Eel/Verbindungsfehler:**
  - backend.log auf Tracebacks prüfen, ggf. Port/Firewall kontrollieren

---

## 5. Best Practices
- Vor jedem Commit: gui_validator.py und Selenium-Tests laufen lassen
- Nach jedem Fix: `git diff`/`git status` sichern und committen
- Fehlerquellen und Debugging-Schritte im Logbuch dokumentieren

---

## Fazit

Mit automatisierten Struktur- und UI-Tests, robustem Backend-Start und konsequenter Log- und Fehleranalyse ist die Mediathek-Entwicklung stabil, reproduzierbar und effizient debugbar.
