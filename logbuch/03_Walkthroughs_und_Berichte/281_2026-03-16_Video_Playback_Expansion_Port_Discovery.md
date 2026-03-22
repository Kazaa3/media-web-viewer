# Logbuch: Video Playback Expansion & Port Discovery

**Datum:** 16. März 2026

## Aufgaben & Ergebnisse

- **Port Discovery Persistence:**
  - Implementierung des `.mwv_port` Mechanismus für zuverlässige Eel-Server-Port-Erkennung.

- **MediaMTX WebRTC Integration:**
  - MediaMTX WebRTC-Slug im Backend (`main.py`) hinzugefügt.

- **VLC Streaming Route:**
  - High-Performance-Route `/vlc-stream/` in `web/app_bottle.py` bestätigt und dokumentiert.

- **Playback Slug Standardisierung:**
  - Einheitliche Slugs für Wiedergabemodi im Frontend und Backend.

- **UI-Erweiterungen:**
  - Kontextmenü in `app.html` um neue Wiedergabemodi (MediaMTX, VLC, Native Disc) erweitert.
  - Wiedergabemodi im Selector gruppiert für bessere UX.

- **Native Disc Support:**
  - DVD/ISO/Blu-ray-Unterstützung in `stream_to_vlc` integriert.

- **Media-Kategorie-Erweiterung:**
  - `format_utils.py` mit spezialisierten Kategorien (CD-ROM, DVD Data, etc.) aktualisiert.

- **JavaScript Fehlerbehebungen:**
  - `Uncaught TypeError: i18next is not defined` behoben.
  - `null.style` Fehler in `switchTab` und `refreshLibrary` behoben.

## Verifikation

- Grep-Audit des Backend-Logics und der Frontend-Templates.
- Port Discovery Check (manuell/Skript).

---

Weitere Details und Verifikationsergebnisse siehe walkthrough.md.
