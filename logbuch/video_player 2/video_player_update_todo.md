# TODO: Video Player Update – Architektur & Features

**Datum:** 27.03.2026
**Autor:** Antigravity

---

## Offene Aufgaben für das Video Player Update

### 1. Architektur-Überarbeitung
- [ ] Modularisierung der Backend-Streams (direct_play, mse_stream, hls_stream, vlc_bridge)
- [ ] Zentrale Routing-Logik in mode_router.py implementieren
- [ ] ffprobe_analyzer.py für erweiterte Medienanalyse erstellen

### 2. Hardware & Docker
- [ ] Dockerfile mit FFmpeg (VAAPI/NVENC) und VLC erstellen
- [ ] docker-compose.yml für /dev/dri Mapping und HW-Accel vorbereiten

### 3. Frontend-Modernisierung
- [ ] <video-js id="universal-player"> als zentrale Player-Komponente einführen
- [ ] universal-player.js: Wrapper für Mode-Negotiation und Source-Switching
- [ ] stats-overlay.js: Echtzeit-Overlay für GPU, Bitrate, FPS, RTT
- [ ] Glassmorphism-Overlays für DVD-Menü und Stats vereinheitlichen

### 4. Feature-Checks & Tests
- [ ] Automatisierte Tests für Routing, Transcode-Integrität, Backend-Connectivity
- [ ] Manuelle Verifikation: 4K HEVC, ISO/DVD, Direct Play, Overlay-Funktion

### 5. WASM & MPV.js Integration
- [ ] mpv.js, mpv.wasm, mpv-worker.js nach web/js/mpv-wasm/ deployen
- [ ] Integration und Test von libmpv zu Canvas (WASM)

---

**Hinweis:**
- Bestehende Routen und Features bleiben als Proxy erhalten ("nichts entfernen nur erweitern").
- Nach jedem Schritt: Logbuch-Eintrag und Test durchführen!

---

**Nächster Schritt:**
- Modularisierung starten und WASM-Binaries bereitstellen.
