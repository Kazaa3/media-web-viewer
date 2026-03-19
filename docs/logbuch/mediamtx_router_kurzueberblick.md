# MediaMTX als Streaming-Router: Kurzüberblick

MediaMTX (früher rtsp-simple-server) ist der zentrale „Streaming-Router“ zwischen FFmpeg/VLC/Kameras und Browser/Player:

- **Eingänge:** RTSP, RTMP, SRT, WebRTC, HLS, MPEG-TS/RTP
- **Ausgänge:** RTSP, RTMP, SRT, HLS, WebRTC (z.B. für VLC, ffplay, Browser, OBS)
- **Features:**
  - Automatisches Protokoll-Umschalten (z.B. RTSP rein, HLS/WebRTC raus)
  - Mehrere Pfade/Streams parallel
  - Aufnahme (fMP4/TS)
  - HTTP-API für Überwachung und Konfiguration

**Praxis für deine App:**
- Per ffmpeg eine Datei/Kamera als RTSP zu MediaMTX schicken
- Den Stream dann wahlweise konsumieren:
  - Im Browser als HLS/WebRTC
  - In VLC/mpv/ffplay als RTSP/SRT/RTMP
- Kein eigener komplexer Streaming-Server nötig – MediaMTX übernimmt das Routing und Protokollhandling.
