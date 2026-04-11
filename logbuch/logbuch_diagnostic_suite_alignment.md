# Implementation Plan – Diagnostic Suite Alignment & GUI Fix

## Ziel

Behebung des gemeldeten "JS ERRRO ON STARTUP" durch Nutzung der internen Testinfrastruktur (Diagnostic Engines) anstelle externer Tools wie Playwright oder Selenium.

---

## User Review Required – WICHTIG

- Die interne Diagnostic Suite (suite_quality.py) ist aktuell defekt (TypeError bei run_all). Zuerst wird die Testinfrastruktur repariert, dann erfolgt die Fehlersuche.
- Playwright und Selenium werden wie gewünscht NICHT für die Verifikation verwendet. Es kommen ausschließlich repo-native Diagnostic Engines (Ultimate, UI, Quality, etc.) zum Einsatz.

---

## Proposed Changes

### Diagnostic Engine Infrastructure Fixes
- [MODIFY] suite_quality.py: run_all() durch modernes run() ersetzen (automatische Stage-Discovery)
- [MODIFY] suite_ui.py: slug_map und Identifikation auf neues id="tools"-Schema anpassen
- [MODIFY] run_all.py: PlaywrightEngine im Master-Runner deaktivieren ("No Playwright"-Vorgabe)

### GUI Fixes (app.html)
- [MODIFY] app.html: script-Tags auf Syntaxfehler (unbalancierte Klammern/Braces) prüfen
- switchTab- und switchToolsView-Calls auf korrekte IDs abgleichen

### Build Process Verification
- [RUN] build.sh: Build-Prozess ausführen, um die "Test Gates" in infra/build_deb.sh zu prüfen

---

## Verification Plan

### Automated Tests
- Primäres Tool: python3 tests/run_all.py
- Erfolgskriterien:
  - Master Diagnostic Report zeigt FAIL: 0
  - Alle 80+ Stages (Ultimate, UI, Quality, etc.) liefern PASS

### Manual Verification
- Terminalausgabe auf [DOM TEST] ITEM SIND GESPAWNED-Bestätigung prüfen

---

*Alle Schritte und Ergebnisse werden im Logbuch und Walkthrough dokumentiert.*
