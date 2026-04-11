# Walkthrough: Supercharged Diagnostics Sidebar (v1.37.05)

## Overview
Die globale Diagnostik wurde zu einer kompakten Observability-Suite ausgebaut. Kernstück ist ein linkes Glass-Overlay, das technische Navigation, Status-Parität, Flags und Sofortaktionen in einer gemeinsamen Oberfläche bündelt. Ziel ist die schnelle Aufklärung des "0 item"-Library-Bugs, ohne bestehende Footer- oder Sidebar-Flows zu verlieren.

## Umgesetzte Änderungen

### 1. Unified Diagnostic Sidebar
**Datei:** [web/app.html](web/app.html)

Die neue Sidebar `#global-diagnostics-sidebar` wurde als linkes Overlay ergänzt und enthält jetzt:
- Reiter für:
  - Übersicht
  - Tests & Benchmarks
  - Video Health
  - System-Check
  - Konsole Logs
  - Latency Profiling
  - Nuclear Recovery
- Live-HUD-Block
- Sync-Snapshot mit `FS / DB / GUI`-Parität
- System-Flags
- Quick Actions
- Observability-Sektion

Die Sidebar bleibt als eigenständige Diagnoseebene sichtbar und ergänzt die bestehende Player-/Footer-Architektur.

### 2. Footer Navigation Cluster
**Datei:** [web/app.html](web/app.html)

Im rechten Footer-Cluster wurde ein neuer Diagnose-Toggle mit Puls-/Heartbeat-SVG ergänzt:
- Button-ID: `footer-btn-diag-overlay`
- Position: links vom Theme-Button
- Verhalten: öffnet bzw. schließt das globale Diagnose-Overlay

Der bestehende Theme-Switcher bleibt erhalten. Die übrigen Footer-Tools wurden nicht verdrängt.

### 3. System Flag Toggles
**Dateien:** [web/app.html](web/app.html), [web/js/diagnostics_helpers.js](web/js/diagnostics_helpers.js)

Im Overlay wurden zentrale Laufzeit-Flags zusammengeführt:
- `DIAG`
- `NATV`
- `HIDB`
- `RAW`
- `BYPS`
- `TEST`

Die Button-Zustände werden jetzt über eine gemeinsame Sync-Logik aktualisiert, damit klassische Diagnoseflächen und das neue Overlay denselben Aktivstatus zeigen.

### 4. Action Center
**Datei:** [web/app.html](web/app.html)

Direkte Recovery- und Diagnoseaktionen im Overlay:
- `MANUAL SYNC`
- `DEEP SCAN`
- `DATA FLOW PROBE`
- `CLEAR LOGS`

Damit lassen sich Rehydrierung, Reindexing und Pipeline-Analyse ohne Navigationswechsel auslösen.

### 5. Persistente Navigation
**Datei:** [web/js/ui_nav_helpers.js](web/js/ui_nav_helpers.js)

Die Overlay-Navigation wurde erweitert:
- `toggleDiagnosticsSidebar()` verwaltet Sichtbarkeit und Persistenz.
- Sichtbarkeit wird in `mwv_diag_overlay_visible` gespeichert.
- Aktiver Diagnose-Reiter wird in `mwv_active_diag_view` gespeichert.
- Spezialrouting:
  - `logs` öffnet direkt das Logbuch.
  - `recovery` leitet in die Recovery-Ansicht unter Optionen weiter.
- Beim Wechsel eines Reiters bleibt das Overlay aktiv.

### 6. Sidebar/Footer Count Sync
**Datei:** [web/js/diagnostics_helpers.js](web/js/diagnostics_helpers.js)

`updateSyncAnchor()` synchronisiert jetzt zusätzlich die Overlay-Werte:
- `diag-db-count-sidebar`
- `diag-gui-count-sidebar`

Dadurch stimmen Footer-Status und Sidebar-Snapshot in Echtzeit überein.

### 7. Visual Polish
**Datei:** [web/css/main.css](web/css/main.css)

Die Sidebar-Navigation wurde für das erweiterte Reiter-Set angepasst:
- Scrollbarer Navigationsbereich
- Begrenzte Maximalhöhe
- Besseres Innenabstand-Verhalten
- Linksbündige Reiter-Beschriftung

Das unterstützt die größere Diagnostik-Tiefe, ohne das Overlay zu überladen.

## Warum diese Änderung das "0 item"-Problem besser sichtbar macht
Die neue Sidebar verbindet Navigation, Paritätsdaten, Systemflags und Sofortaktionen an einem Ort. Besonders relevant sind:
- `DATA FLOW PROBE` zur Drop-Analyse in der Pipeline
- `RAW` zum Umgehen potenziell fehlerhafter Kategorisierung
- Paritätsanzeige zwischen Dateisystem, Datenbank und GUI
- direkter Sprung in Logs und Recovery

Wenn `DB > 0`, aber `GUI = 0`, ist der Fehler jetzt schneller auf Filter, Mapping oder Frontend-Sync eingrenzbar.

## Diff-Fokus nach Datei
- [web/app.html](web/app.html): Overlay-Struktur, neue Reiter, Flags, Quick Actions, Footer-Toggle
- [web/js/ui_nav_helpers.js](web/js/ui_nav_helpers.js): Persistenz, Overlay-Toggle, Spezialrouting für Logs/Recovery
- [web/js/diagnostics_helpers.js](web/js/diagnostics_helpers.js): Status-Sync für Counts und Flag-Buttons
- [web/css/main.css](web/css/main.css): Scroll-/Layout-Feinschliff für die neue Sidebar-Navigation

## Manual Verification
1. Diagnose-Button im Footer anklicken.
2. Prüfen, dass die Sidebar links als Overlay erscheint.
3. Mehrere Reiter testen und bestätigen, dass die Zielansicht wechselt.
4. Seite neu laden und Persistenz von Zustand und Reiter prüfen.
5. `DATA FLOW PROBE` ausführen und mit Footer-/Sidebar-Zählern abgleichen.
6. Sicherstellen, dass Footer-Layout und Theme-Toggle unverändert sauber ausgerichtet bleiben.

## Status
- Global Diagnostics Sidebar integriert.
- Footer Navigation Cluster erweitert.
- Persistenz und Status-Sync aktiv.
- Bereit für Review und Live-Debugging des "0 item"-Falls.
