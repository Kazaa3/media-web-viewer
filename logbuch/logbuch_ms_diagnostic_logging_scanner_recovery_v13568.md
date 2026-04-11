# Logbuch MS: High-Fidelity Diagnostic Logging & Scanner Recovery (v1.35.68)

## Ziel
Behebung des "0 items in library"-Problems durch eine Echtzeit-Diagnosekonsole und tiefgehende Instrumentierung des Backend-Scanners. Jeder Schritt des Indexing-Prozesses wird für den Nutzer sichtbar gemacht.

## Umsetzungsschritte

### 1. Frontend: Diagnostic UI Extension
- **options_panel.html:**
  - Scrollbares Terminal im "Centralized Diagnostic Hub" (ID: diagnostic-log-terminal).
  - VS Code-Style, Syntax-Highlighting für INFO, WARN, ERROR.

### 2. Frontend: Eel Bridge Implementation
- **options_helpers.js:**
  - `append_debug_log(msg, level)` für Eel exponieren.
  - DOM-Injektion für das Terminal implementieren.
  - "Clear Logs"-Button für Health-Management.

### 3. Backend: Deep Instrumentation
- **main.py:**
  - `_scan_media_execution` mit granularen Log-Reports instrumentieren:
    - [SCAN-STEP] Checking directory: {path}
    - [SCAN-STEP] Matching file: {name} (Ext: {ext})
    - [SCAN-STEP] SKIPPING: {name} (Reason: {reason})
    - [DB-STEP] Inserting ID: {id} | Result: {status}
  - Logging der all_exts-Logik zur Verifikation der Extension-Matches.

### 4. Stability Check: super_kill.py
- Sicherstellen, dass das Skript die aktuelle Umgebung erkennt und die AI-Session nicht beeinträchtigt (bestehende Version verwenden).

## Offene Fragen
- Sollen die Logs zusätzlich in eine lokale Datei geschrieben werden oder reicht der UI-Stream?
- Soll "Parser Chain"-Timing in den Echtzeit-Stream aufgenommen werden?

## Verifikation
### Automatisierte Tests
- `eel.run_direct_scan()` aus der UI ausführen.
- Prüfen, ob Logs im neuen Terminal erscheinen.
- Sicherstellen, dass Items erfolgreich in database.db eingefügt werden.

### Manuelle Verifikation
- Prüfen, dass aus "0 items" wieder "57 items" werden (Anzahl in ./media).
- Terminal muss auch bei hoher Log-Last stabil bleiben.

## Status
- **Bereit:** Plan und Instrumentierung dokumentiert.
- **Warten auf:** User-Feedback zu Log-Persistenz und Parser-Timing vor Ausführung.
