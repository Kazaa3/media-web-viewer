# Implementation Plan: Perfect Video Player Architecture Overhaul

**Datum:** 27.03.2026
**Autor:** Antigravity

---

## Ziel
Restructure the media player into a unified, high-performance architecture with smart routing and modular backends. **(nichts entfernen, nur erweitern!)**

---

## Proposed Changes

### [Component] Backend: Intelligence & Routing
- **[NEW] ffprobe_analyzer.py**
  - Erweiterte Analyse: PAL/NTSC, 4K/HDR/Atmos, ISO/DVD/BD, HW-Accel (VAAPI/Arc/NVENC)
- **[NEW] mode_router.py**
  - Zentrale Entscheidungslogik für Playback-Mode:
    1. Direct Play (MP4/H.264)
    2. MSE fMP4 (Low-Latency)
    3. HLS fMP4 (4K/Kompatibilität)
    4. VLC Bridge (ISO/DVD-Menüs)
    5. Desktop Fallback

### [Component] Backend: Modular Streams
- **[NEW] streams/**
  - direct_play.py: Optimiertes statisches Serving
  - mse_stream.py: Fragmented MP4 (WS/Pipe)
  - hls_stream.py: Apple HLS fMP4
  - vlc_bridge.py: VLC CLI Streaming/Control
  - (Logik aus main.py modularisieren, alte Routen als Proxy belassen)

### [Component] Docker & Hardware Acceleration
- **[NEW] docker-compose.yml**
  - /dev/dri Mapping für Intel Arc
  - ENV-Variablen für FFmpeg HW-Accel
- **[NEW] Dockerfile**
  - Multi-Stage Build: FFmpeg (VAAPI/NVENC), VLC, alle Libs

### [Component] Frontend: Unified UI
- **[MODIFY] app.html**
  - Ein <video-js id="universal-player"> ersetzt alle Player-DIVs
  - Overlays (DVD, Stats) als einheitliche Glassmorphism-Layer
- **[NEW] universal-player.js**
  - Wrapper-Klasse UniversalPlayer:
    - Backend-Mode-Negotiation
    - Dynamisches Source-Switching
    - Video.js-Plugins (DVD, Quality, Tracks)
- **[NEW] stats-overlay.js**
  - Echtzeit-Dashboard: GPU-Typ, Bitrate, FPS, RTT

---

## Verification Plan

### Automated Tests
- **Backend Routing:** pytest tests/test_mode_router.py (Mapping-Logik)
- **Transcode Integrity:** python3 tests/test_video_performance_benchmark.py (FFmpeg Output)
- **Eel Connectivity:** python3 tests/test_backend_connection.py

### Manual Verification
- **4K HEVC:** Route zu HLS fMP4, "Intel Arc"/"NVENC" im Overlay
- **ISO:** VLC Bridge/MPV WASM, DVD-Simulator-Overlay aktiv
- **Direct Play:** 0% CPU bei MP4

---

## Hinweise
- **Bestehende Routen bleiben als Proxy erhalten, Logik wird modularisiert.**
- **"nichts entfernen nur erweitern"-Prinzip wird eingehalten.**

---

**Startbereit für die Umsetzung!**
