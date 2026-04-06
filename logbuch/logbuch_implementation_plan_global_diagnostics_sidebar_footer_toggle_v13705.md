# Logbuch: Implementation Plan – Global Diagnostics Sidebar & Footer Toggle (v1.37.05)

## User Review Required
**IMPORTANT**

Geplant ist eine neue globale Diagnostik-Seitenleiste als linkes Glass-Overlay mit halbtransparenter Oberfläche. Zusätzlich wird im Footer-Cluster ein neuer Toggle links neben dem Theme-Button ergänzt, damit die technische Diagnose jederzeit erreichbar bleibt.

## Zielbild
Die neue Sidebar soll das bestehende Diagnose- und Recovery-Tooling an einem zentralen Ort bündeln, ohne die aktuelle UI zu verdrängen. Sie dient vor allem dazu, den "0 item"-Bibliotheksfehler sichtbar zu machen und die Beobachtbarkeit der gesamten Pipeline zu verbessern.

## Geplante Änderungen

### 1. Core UI Structure
**Datei:** [web/app.html](web/app.html)

- Neuer Container `#global-diagnostics-sidebar` mit Klasse `diagnostic-sidebar`.
- Linkes Overlay statt klassischer, opaker Seitenleiste.
- Neue interne Reiter:
  - Übersicht
  - Tests & Benchmarks
  - Video Health
  - System-Check
  - Konsole Logs
  - Latency Profiling
  - Nuclear Recovery
- Bestehende Footer-Tools bleiben erhalten und werden nicht entfernt.
- Neuer Footer-Button im rechten `footer-icon-cluster`, direkt links vom Theme-Toggle.
- Icon-Stil: Pulse-/Heartbeat-SVG für schnelle technische Erkennbarkeit.

### 2. System Flag Toggles
**Datei:** [web/app.html](web/app.html)

Geplante Schnellschalter im Sidebar-Bereich für Laufzeitdiagnose:
- `DIAG`
- `NATV`
- `HIDB`
- `RAW`
- `BYPS`
- `AUDIT`
- `TEST`

Ziel: Diagnosemodi ohne Umweg über mehrere Ansichten erreichbar machen.

### 3. Styling & Overlay-Verhalten
**Datei:** [web/css/main.css](web/css/main.css)

- Fixierte, links ausgerichtete Overlay-Positionierung.
- Halbtransparenter Glass-Look für Sicht auf den Inhalt dahinter.
- Saubere Ein-/Ausblend-Transition.
- Stabile Layer-Reihenfolge via `z-index`.
- Zusätzliche Scroll- und Spacing-Regeln für mehr Reiter und Aktionsbereiche.

### 4. Navigation & State Logic
**Datei:** [web/js/ui_nav_helpers.js](web/js/ui_nav_helpers.js)

- Einführung von `toggleDiagnosticsSidebar()`.
- Persistenz des Open/Closed-Zustands in `localStorage`.
- Persistenz des aktiven Sidebar-Reiters in `localStorage`.
- Reiter sollen die passende Zielansicht öffnen, ohne das Overlay zwingend zu schließen.
- Mapping für Spezialfälle wie Logs und Recovery.

### 5. Cross-Sync mit Diagnostikdaten
**Datei:** [web/js/diagnostics_helpers.js](web/js/diagnostics_helpers.js)

- Sidebar-HUD und Footer-Status sollen dieselben Paritätsdaten anzeigen.
- Zusätzliche Sync-Anker für DB- und GUI-Counts.
- Gemeinsame Aktivzustände für Diagnose-Buttons zwischen alter und neuer Oberfläche.

## Verification Plan

### Manual Verification
1. **Sidebar Toggle**
   - Footer-Button anklicken.
   - Prüfen, dass die linke Diagnose-Sidebar sichtbar wird.
2. **Tab Switching**
   - Jeden Reiter anklicken.
   - Prüfen, dass die zugehörige Diagnoseansicht geladen wird.
3. **Persistence**
   - Seite neu laden.
   - Prüfen, dass Offen/Geschlossen-Zustand erhalten bleibt.
4. **Footer Layout**
   - Prüfen, dass Theme-Button, Diagnose-Toggle und bestehende Footer-Tools korrekt ausgerichtet bleiben.
5. **0-Item Debugging Flow**
   - Probe-/Sync-/Scan-Aktionen aus der Sidebar starten.
   - Prüfen, ob Drop-Stellen in der Datenpipeline sichtbar werden.

## Erwartetes Ergebnis
- Schnellzugriff auf Systemdiagnose direkt aus dem Footer.
- Zentralisierte technische Beobachtbarkeit.
- Weniger Kontextwechsel zwischen Footer, Logbuch, Debug und Recovery.
- Schnellere Analyse des "0 item"-Problems.

## Status
- Plan dokumentiert.
- Bereit für Review und finale UI-Abnahme.
