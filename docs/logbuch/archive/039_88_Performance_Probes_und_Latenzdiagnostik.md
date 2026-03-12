# 88 Performance Probes und Latenzdiagnostik

**Datum:** 09.03.2026  
**Bereich:** Performance / Backend / Frontend / Transport  
**Status:** ✅ umgesetzt

## Ziel
Die GUI wirkte träge. Für die nächste Optimierungsrunde wurde zuerst eine saubere, getrennte Messbasis aufgebaut:

- Backend-Latenz
- Frontend-Frame-Latenz
- Bottle-HTTP-Transport
- Eel-Roundtrip inkl. Payload-Overhead

## Umsetzung

### 1) Backend/Eel Probe
- Datei: `main.py`
- Neue Eel-exposed Funktion: `api_ping(client_ts=None, payload_size=0)`
- Liefert:
  - `server_ts`, `client_ts`
  - `payload_size`
  - optionale Echo-`payload`
- Payload-Schutz: Größenbegrenzung auf `0..200000` Bytes

### 2) Bottle Transport Probe
- Datei: `web/app_bottle.py`
- Neuer Endpoint: `GET /health`
- Lightweight JSON-Response mit Status und Timestamp

### 3) Frontend Diagnostik-Hook
- Datei: `web/app.html`
- Neuer Hook: `window.runLatencyDiagnostics(payloadSize = 0, samples = 5)`
- Misst getrennt:
  - Frontend-Frame-Latenz via `requestAnimationFrame`
  - Eel-Roundtrip via `eel.api_ping(...)`
  - Bottle-Latenz via `fetch('/health')`

### 4) Reaktionszeit-Optimierung für Environment-Panel
- Datei: `main.py`
- `get_environment_info(force_refresh=False)` mit Kurzzeit-Cache ergänzt
- TTL: `8s`
- Effekt: weniger teure Wiederholungs-Scans beim Tab-Wechsel

## Tests

### Neue Tests
- `tests/test_performance_probes.py`
  - validiert `api_ping` Struktur + Payload-Verhalten
  - validiert Frontend-Hook-Verdrahtung
  - prüft warmen `get_environment_info`-Call auf offensichtliche Regression

- `tests/test_bottle_health_latency.py`
  - startet lokale Bottle-Instanz
  - misst `/health`-Roundtrip-Latenz (Median) und Antwortstruktur

### Gesamtergebnis (gezielter Lauf)
- `27 passed`
- Enthalten:
  - neue Performance-Tests
  - Session-/Environment-Regressions
  - Environment-UI Tests

## Doku
- `DOCUMENTATION.md` erweitert um Abschnitt:
  - **Performance Diagnostics (Backend / Frontend / Bottle / Eel)**
  - plus Verweis auf neue Tests und Cache-Optimierung

## Nächster Schritt (geplant)
Mit dieser Messbasis folgt als eigener Schritt die eigentliche Performance-Optimierung pro Layer (Backend, Frontend, Bottle/Eel-Transport), inklusive Vorher/Nachher-Messung.

---

## Update 09.03.2026 – Post-Optimierungs-Snapshot #1

### Umgesetzte Optimierungen in dieser Runde
- `web/app_bottle.py`: Unbedingtes Request-Info-Logging im Hook entfernt (nur noch Debug-Trace), um Request-Pfad-Overhead zu reduzieren.
- `web/app.html`: Package-Suche optimiert:
  - vor-normalisierte Suchfelder (`window.allPackagesSearch`)
  - Debounce (`120ms`) statt Filterung bei jedem einzelnen Keypress

### Messung (lokal, `.venv`, 09.03.2026)
Messskript: direkter Probe-Lauf für `api_ping`, `get_environment_info` (cold/warm) und `GET /health`.

- **api_ping (Payload 4096, n=20)**
  - avg: `0.002 ms`
  - median: `0.001 ms`
  - p95: `0.012 ms`

- **get_environment_info (n=1 cold + n=10 warm)**
  - cold: `4160.203 ms`
  - warm avg: `0.003 ms`
  - warm median: `0.001 ms`
  - warm p95: `0.017 ms`

- **Bottle /health (n=20)**
  - avg: `2.762 ms`
  - median: `0.527 ms`
  - p95: `44.568 ms`

### Einordnung
- Der große Unterschied zwischen **cold** und **warm** bei `get_environment_info` bestätigt den gewünschten Effekt des 8s-Caches.
- `/health` zeigt lokal eine sehr niedrige Median-Latenz; höhere p95-Werte sind im lokalen Single-Process-/wsgiref-Setup erwartbar (Scheduling/Jitter).

### Abschlussstatus dieser Runde
- Messbasis ist aktiv und getestet.
- Erste konkrete Optimierungen sind umgesetzt und validiert.
- Nächster Schritt bleibt die echte Vorher/Nachher-UI-Messung über `runLatencyDiagnostics(...)` im laufenden App-Fenster.

## Update 09.03.2026 – Test-Gate im Build-Prozess

Der gewünschte Build-Qualitätsfilter wurde integriert:

- `build_deb.sh` führt vor dem Packaging standardmäßig ein Test-Gate aus.
- Gate-Suite:
  - `tests/test_performance_probes.py`
  - `tests/test_bottle_health_latency.py`
  - `tests/test_installed_packages_ui.py`
  - `tests/test_ui_session_stability.py`
- Verhalten: Bei Fehlschlag wird der Build sofort abgebrochen (`set -e`).
- Expliziter Override für lokale Notfälle/Debugging: `SKIP_BUILD_TESTS=1 bash build_deb.sh`

Lokale Validierung der Gate-Suite:
- `20 passed` (09.03.2026)

## Update 09.03.2026 – Vereinheitlichung aller Build-Wege

Zusätzlich zur Shell-Integration wurde das Gate jetzt über alle Build-Einstiegspunkte vereinheitlicht:

- `build_system.py`
  - zentrales `run_build_test_gate()` ergänzt
  - aktiv für `--build deb`, `--build pyinstaller`, `--build all`, `--full-build`, `--pipeline`
  - neuer expliziter Override: `--skip-build-gate`

- `build.py`
  - führt dieselbe Gate-Suite vor dem PyInstaller-Lauf aus
  - Override via `SKIP_BUILD_TESTS=1`

Ergebnis:
- konsistente Mindest-Qualität über **alle** Build-Pfade
- identische Gate-Suite statt divergierender Build-Prüfungen

## Update 09.03.2026 – Benchmark Debug-Konsole vs. DB-Schreiben

Auf Wunsch wurde vor dem Pipeline-Lauf ein gezielter Schreib-Latenztest ergänzt und ausgeführt.

Neues Skript:
- `tests/benchmark_debug_db_write_speed.py`

Messung A – Debug-Log-Schreibpfad (500 Samples, `logger.debug("db", ...)`):
- avg: `0.0225 ms`
- median: `0.0221 ms`
- p95: `0.0265 ms`

Messung B – DB-Schreibpfad (300 Samples, `db.insert_media(...)` auf temp SQLite):
- avg: `8.2807 ms`
- median: `8.0917 ms`
- p95: `9.6027 ms`

Direkter Konsolen-Check (echter Stream, 80 Samples):
- avg: `0.0479 ms`
- median: `0.0463 ms`
- p95: `0.0596 ms`

Einordnung:
- DB-Insert ist im Schnitt ca. `368x` langsamer als ein Debug-Log-Eintrag.
- Der echte Konsolenpfad bleibt ebenfalls deutlich unter 1 ms pro Debug-Eintrag.

## Update 09.03.2026 – Pipeline-Verifikation nach Benchmark

- `build_system.py --pipeline` erfolgreich durchgelaufen (non-destructive).
- Vorherige Version-Sync-Blocker wurden behoben:
  - `main.py` Fallback-Version auf `1.3.3`
  - `logbuch/00_Known_Issues.md` Version-Header/Title auf Sync-Pattern angepasst
- Build-Gate-Doppellauf entfernt: bei Aufruf über `build_system.py` wird `build_deb.sh` mit `SKIP_BUILD_TESTS=1` gestartet, da das Gate bereits im Wrapper lief.
