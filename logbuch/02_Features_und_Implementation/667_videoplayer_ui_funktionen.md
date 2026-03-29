# Logbuch: Video Player Tab UI & Funktionen

## Stand März 2026

### Features & UI
- Auswahl verschiedener Wiedergabemodi:
  - Chrome Native
  - FFmpeg Engine → Chrome
  - VLC Engine → Chrome
  - mkvmerge → VLC (Local)
  - VLC (Extern)
  - Drag&Drop (Extern)
- Eingebetteter <video>-Player für native und gestreamte Wiedergabe
- Drag&Drop-Panel für externes Öffnen in VLC
- Stream-Panel für VLC-Streams (HLS, RTSP, RTMP)
- Playlist-Import/Export für m3u/m3u8
- Statusanzeigen für Fehler, laufende VLC-Instanz, Stream-Status

### Wichtige Funktionen
- `updateVideoMode()`: Synchronisiert UI und Panels je nach Modus
- `playVideo(item, path)`: Startet Video, entscheidet Player-Modus (smartes Routing)
- `startEmbeddedVideo(item, path)`: Setzt eingebetteten Player, Fehlerhandling
- `runBatchRemux()`: Batch-Remux von Ordnern
- `showUnsupportedVideoHint()` / `hideUnsupportedVideoHint()`: Fehlerhinweise
- `playVLCStream()`: Startet Stream im VLC-Modus
- Playlist-Import/Export: m3u/m3u8-Handling

### Backend-Integration
- `eel.open_video_smart(item.path, mode)`: Smartes Routing im Backend
- `eel.remux_mkv_batch(folder)`: Batch-Remux
- `eel.stop_vlc()`: Stoppt VLC

### Noch offen
- Erweiterte Timeline/Seek-Controls für HLS/WebRTC/FFmpeg
- Feedback für Streaming-Modi

---
Dieses Logbuch dokumentiert den aktuellen Stand der Video-Player-Tab UI, die wichtigsten Funktionen und die Backend-Integration. Offene Punkte sind klar benannt und können gezielt weiterentwickelt werden.
