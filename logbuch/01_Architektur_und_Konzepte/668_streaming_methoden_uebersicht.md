# Logbuch: Streaming-Methoden Übersicht

## Stand März 2026

### Unterstützte Streaming-Methoden
- **HLS (MediaMTX):**
  - Backend-Routing über open_video_smart
  - Wiedergabe im Browser (Chrome Native, MediaMTX)
- **WebRTC (MediaMTX):**
  - Backend-Routing über open_video_smart
  - Wiedergabe im Browser
- **FragMP4 (MediaMTX):**
  - Backend-Routing über open_video_smart
  - Wiedergabe im Browser
- **RTSP, RTMP, MMS (VLC-Stream):**
  - Stream-Panel im UI
  - playVLCStream() Funktion für externe Streams
- **Remux-Streaming (mkvmerge/ffmpeg):**
  - On-the-fly Remux über /video-remux-stream/<item_id>
  - Backend nutzt mkvmerge oder ffmpeg
- **Direkte Wiedergabe (Browser):**
  - Chrome Native Mode
- **Externe Player:**
  - VLC, FFplay
  - Drag&Drop-Panel im UI

### Backend-Integration
- `open_video_smart(path, mode)`: Entscheidet Streaming-Methode und Routing
- `/video-remux-stream/<item_id>`: Remux-Streaming
- `/media/<filepath:path>`: Live-Transkodierung

### UI-Integration
- Modus-Auswahl im Video-Player-Tab
- Stream-Panel für URL-Eingabe
- Statusanzeigen für Fehler und laufende Streams

### Noch offen
- Feedback/Status für Streaming-Modi (HLS/WebRTC/FragMP4) im UI
- Erweiterte Timeline/Seek-Controls für Streams

---
Dieses Logbuch dokumentiert alle implementierten Streaming-Methoden, deren Routing und Integration im UI und Backend. Offene Punkte sind klar benannt.
