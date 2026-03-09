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
