# Logbuch: Implementation Plan – Expanded Playback & Mini-Video Overlay

**Datum:** 16. März 2026

## Player Overhaul Strategy

Wir implementieren eine Dual-Player-Strategie:

- **Player 1: Chrome Native (Video.js):** Für mobile Kompatibilität und effiziente Browser-Wiedergabe.
- **Player 2: Desktop / Standalone (VLC, ffplay, pyvidplayer2):** Für volle Formatunterstützung, ISO-Menüs und Power-Features.

### Technische Modus-Beschreibungen

| Modus              | Strategie         | Backend Engine         | Frontend Player         | Ideal Use Case                  |
|--------------------|------------------|------------------------|-------------------------|----------------------------------|
| Direct Play        | Static File      | Bottle                 | Video.js                | MP4/WebM (H.264/VP9)             |
| MediaMTX HLS       | Transcode/Stream | MediaMTX (ffmpeg)      | Video.js                | Alle Formate, mobilfreundlich    |
| MediaMTX WebRTC    | Low Latency      | MediaMTX (ffmpeg)      | Video.js (Plugin)        | Instant Playback                 |
| FFmpeg Browser     | FragMP4 Stream   | ffmpeg                 | Video.js                | Live-Transcoding zu HTML5        |
| VLC TS Detection   | TS HTTP Stream   | cvlc (headless)        | Video.js (mp2t)         | Hochwertiger TS-Stream           |
| cvlc solo          | Direct Pipe      | cvlc                   | VLC Plugin/vjs          | Raw TS Pipe                      |
| ffplay             | Standalone UI    | ffplay                 | N/A                     | Schneller Desktop-Check           |
| ISO Live           | Native Protocol  | VLC                    | VLC / Standalone        | DVD/Blu-ray Menüs                |

## Vorgeschlagene Änderungen

### Backend (`main.py`)
- `open_video` um folgende Modi erweitern:
  - `ffmpeg_browser`: Gibt Pfad zu `/video-stream/` zurück.
  - `ffplay`: Startet ffplay standalone.
  - `mkvmerge_standalone`: Remux zu temp MKV, öffnet in VLC.
  - `mediamtx_hls` & `mediamtx_webrtc`: Varianten bereitstellen.
  - `vlc_ts`: Startet cvlc mit TS-Muxing.
- Neue Helfer:
  - `vlc_ts_mode(file)` und `detect_ts_stream(port)`
  - `mediamtx_mode(file, variant)` für GUI-Integration
- `stream_to_vlc` für dvd:// und bluray:// weiter verfeinern.
- ffprobe-Pre-Check für automatische Moduswahl (Direct Play vs Fallback).

### Frontend (`app.html`)
- **Player-Update:** Video.js als primären HTML5-Player integrieren.
- **Kontextmenü & Selector:**
  - Optgroup "Chrome Native": Direct Play, MediaMTX (HLS/WebRTC), ffmpeg FragMP4
  - Optgroup "VLC / Standalone": cvlc solo, VLC TS Detection, DVD ISO Live, ffplay Standalone
- **Mini-Video Overlay (PiP):**
  - Draggable/resizable `.mini-player`-Container
  - JS für Dragging/Resizing
  - PiP-Toggle-Logik zum Umschalten des Streams ins Overlay
  - Platzhalter für swyh-rs (Systemaudio-Sync) & Chromecast

### Test
- `test_dvd_iso.py`: Spezialintegrationstest für `media/Going Raw - JUDITA_169_OPTION.ISO`

## Verifikationsplan

- **Automatisierte Tests:**
  - `python3 tests/integration/basic/playback/test_dvd_iso.py`
  - `python3 tests/integration/basic/playback/test_playback_modes.py`
- **Manuelle Verifikation:**
  - Alle neuen Wiedergabemodi im Kontextmenü testen
  - Mini-Video-Overlay auf Dragging, Resizing, Always-on-Top prüfen

---

Weitere Details siehe implementation_plan.md.
