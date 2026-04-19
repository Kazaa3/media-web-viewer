# Logbuch: Expanded Playback, Mini-Video Overlay & Player Selection

**Datum:** 16. März 2026

## Aufgaben & Fortschritt

- **Erweiterte Wiedergabemodi (Backend):**
  - Neue Wiedergabemodi in `src/core/main.py` implementiert (Direct Play, MediaMTX HLS/WebRTC, FFmpeg Browser, VLC TS, cvlc solo, ffplay, ISO Live, MKVMerge Standalone).
  - ffprobe-Pre-Check für automatische Moduswahl integriert.

- **Lokalisierung:**
  - `web/i18n.json` aktualisiert, um neue Modi und UI-Elemente abzudecken.

- **Erweiterte Wiedergabemodi (Frontend):**
  - `web/app.html` um neue Modi erweitert.
  - Kontextmenü und Selector mit neuen Kategorien und Varianten aktualisiert.
  - Video.js als primären Player integriert.

- **Mini-Video Overlay (PiP):**
  - HTML/CSS/JS für ein verschiebbares und skalierbares Overlay in `web/app.html` implementiert.
  - Backend-Unterstützung für PiP-Stream hinzugefügt.

- **DVD ISO Integrationstest:**
  - `tests/integration/basic/playback/test_dvd_iso.py` erstellt, um echte DVD-ISO-Strukturen zu testen.

- **Verifikation & Benchmarking:**
  - Gesamte Implementierung überprüft und Benchmarks durchgeführt.

---

Weitere Details und technische Umsetzung siehe Implementation_Plan_Expanded_Playback_Mini_Video_Overlay.md und Chrome_Native_Videojs_Status.md.
