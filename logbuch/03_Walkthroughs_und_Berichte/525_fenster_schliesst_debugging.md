# Test- und Debugging-Strategien: "Fenster schließt sich sofort"

**Datum:** 2026-03-15

## Problemstellung
Nach dem Start des Media Web Viewer schließt sich das Fenster sofort wieder. Das Backend startet augenscheinlich fehlerfrei (Exit Code 0), aber das Frontend bleibt nicht offen.

## Test- und Debugging-Strategien

### 1. Log- und Fehleranalyse
- **Backend-Log prüfen:**
  - logs/ Verzeichnis auf neue Logdateien oder Tracebacks durchsuchen.
  - Konsole/Terminal-Ausgabe auf Fehler, Tracebacks oder Warnungen prüfen.
- **Frontend-Log prüfen:**
  - Browser-Entwicklertools (F12) öffnen, Konsole auf Fehler/Exceptions prüfen.
  - Eel-Logausgaben beachten (werden oft im Backend-Log oder Terminal angezeigt).

### 2. Typische Fehlerquellen
- **ImportError / fehlende Pakete:**
  - psutil, eel, bottle, etc. installiert?
  - `pip list` im aktiven venv prüfen.
- **Syntax-/IndentationError:**
  - Python-Dateien auf Einrückungsfehler oder Tippfehler prüfen.
- **Exception in @eel.expose:**
  - Fehler in einer Eel-API-Funktion kann das Frontend sofort crashen lassen.
- **Fehlerhafte Rückgabe an das Frontend:**
  - None/Fehlerobjekte werden nicht abgefangen und führen zu JS-Fehlern.
- **Port-Konflikte:**
  - Läuft bereits eine Instanz? Ist der Port blockiert?

### 3. Schrittweise Tests
- **Backend isoliert starten:**
  - Nur das Backend im Terminal starten, prüfen ob es "wartet" oder sofort beendet.
- **Frontend im Browser manuell öffnen:**
  - http://localhost:PORT (siehe Log) im Browser öffnen, um JS-Fehler zu sehen.
- **Minimalstart:**
  - Alle neuen Features (PID-Logik etc.) temporär auskommentieren, dann Schritt für Schritt wieder aktivieren.
- **Eel im Debug-Modus starten:**
  - Eel-Start mit debug=True, um mehr Ausgaben zu erhalten.

### 4. Tools & Hilfsmittel
- **pytest** für Unit- und Integrationstests.
- **ruff/mypy** für Linting und Typprüfung.
- **psutil**-Test: `python -c "import psutil; print(psutil.__version__)"`
- **requirements.txt**/`pip freeze` prüfen.

### 5. Dokumentation & Nachvollziehbarkeit
- Alle Test- und Debugging-Schritte im Logbuch dokumentieren.
- Fehler und deren Behebung als eigene .md-Dateien ablegen.

## Empfehlung
- Zuerst Backend- und Frontend-Logs prüfen.
- Dann Schrittweise die neuen Features isolieren und testen.
- Fehlerquellen systematisch ausschließen.

---
*Diese Datei dient als Leitfaden für die Fehlersuche bei "Fenster schließt sich sofort"-Problemen im Media Web Viewer.*
