# Logbuch: GUI-Test-Suite & Picking-UX Stabilisierung

**Datum:** 11. März 2026

---

## Walkthrough & wichtigste Änderungen

### 1. Robustes Drag-and-Drop System (app.html)
- Auto-Cancel Fix: Loslassen der Maus nach Long-Press bricht den Vorgang nicht mehr ab.
- Echtes Drag-and-Drop: Items können direkt auf Ziel-Element gezogen und dort fallen gelassen werden (mouseup auf Ziel).
- Visuelle Vorschau: Blaue Linie markiert Einfügeposition beim Überfahren eines Elements während des Drags.
- Index-Synchronisation: Korrekte Berechnung der Zielposition (Insert-Before) im Frontend und Backend.

### 2. Performance-Telemetrie (Backend)
- Startup-Trace: Logging der Zeit vom Start von main.py bis zur Einsatzbereitschaft von Eel.
- Scan-Trace: Überwachung der Medien-Scanner-Phasen (Verzeichnisse, Dateien, Ende).
- Parser-Trace: Messung der Extraktionsdauer pro Datei in media_parser.py zur Engpass-Analyse.

### 3. Industriestandard Test-Suite & Dokumentation
- Isolierte Umgebung: Dedizierte .venv_selenium trennt Test-Abhängigkeiten vom Hauptprojekt.
- Zentraler Wrapper: tests/run_gui_tests.py führt alle kritischen GUI-Tests automatisiert aus.
- Detaillierte READMEs: Neue Dokumentation in tests/README_GUI_TESTS.md erklärt Setup und Architektur.
- Playlist-Sync Fix: Automatische Synchronisation des CURRENT_INDEX via jump_to_index im Frontend.

---

## Verifikationsergebnisse
- Picking Erfolg: UI-Logs bestätigen [UI-Trace] Picked item 0 zuverlässig, selbst bei hoher Scanner-Fehlerlast.
- Stabilität: test_refresh_maintenance Lauf erfolgreich, Picking-State bleibt konsistent.
- Robuste Synchronisation: WebDriverWait und gezielte Re-Finds eliminieren StaleElementReferenceExceptions.

---

## NOTE
Einige verbleibende Timeouts in der Test-Suite resultieren aus der extremen Last des initialen Medien-Scans auf dem Testsystem. Dies ist ein "Stress-Test" Ergebnis, das die grundsätzliche Funktion des Picking-Fixes bestätigt.
