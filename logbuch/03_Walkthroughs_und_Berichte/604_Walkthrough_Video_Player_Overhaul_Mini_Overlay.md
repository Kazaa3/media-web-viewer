# Walkthrough: Video Player Overhaul & Mini-Video Overlay

**Datum:** 16. März 2026

## Key Accomplishments

### 1. Dual-Player Strategy
- **Chrome Native (Video.js):** Optimiert für browser-native Formate und mobile Geräte.
- **Desktop Standalone:** Nutzt VLC, ffplay und pyvidplayer2 für maximale Formatkompatibilität und lokale Performance.

### 2. Expanded Playback Modes
| Mode                  | Engine                  | Status        |
|-----------------------|-------------------------|---------------|
| MediaMTX (HLS/WebRTC) | ffmpeg + MediaMTX       | ✅ Integrated |
| cvlc TS-Stream        | cvlc + manual port check| ✅ Integrated |
| Fragmented MP4        | ffmpeg browser stream   | ✅ Integrated |
| pyvidplayer2          | Python Desktop Player   | ✅ Integrated |
| ffplay                | FFmpeg Native Standalone| ✅ Integrated |

### 3. Mini-Video Overlay (PiP)
- Resizable und verschiebbarer Floating-Player in `app.html`.
- **Interaktivität:** Sanftes Dragging mit mousedown/mousemove.
- **Controls:** Play, Pause, Fullscreen direkt im Overlay.
- **UI:** Glassmorphism-Design für moderne Optik.

### 4. Smart Routing & Localisation
- **i18n:** Neue Keys für alle Modi (Deutsch/Englisch).
- **ffprobe:** Backend-Pre-Check für optimale Strategie (Direct vs. Transcode).

## Technical Details

### Backend (`main.py`)
- Neue Funktionen: `vlc_ts_mode`, `mediamtx_mode`, `pyvidplayer2_mode`, `mkvmerge_standalone_mode`.
- `open_video` mit smarter Dispatch-Logik erweitert.

### Frontend (`app.html`)
- Video.js als primärer Player integriert.
- Responsive Playback-Selector und Kontextmenü.

## Verification

### Automated Benchmark
- Neues Skript `playback_benchmark.py` misst Start-Latenz für verschiedene Engines.

### Manual Verification
- Bibliothek öffnen, Rechtsklick auf Medien → erweiterte Wiedergabemodi sichtbar.
- Mini-Video Overlay aktivieren und Multitasking testen.

---

Weitere Details siehe Quellcode und vorherige Logbuch-Einträge.
