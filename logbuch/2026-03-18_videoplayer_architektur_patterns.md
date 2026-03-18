# Logbuch: Video Player Tab Architektur & Patterns

## Stand März 2026

### Scope & Struktur
Der Kommentar im Code definiert den Scope für den gesamten Video Player Tab:
- Auswahl verschiedener Wiedergabemodi
- Eingebetteter <video>-Player
- Drag&Drop-Panel für VLC
- Stream-Panel für HLS/RTSP/RTMP
- Playlist-Import/Export
- Statusanzeigen
- Backend-Integration (Smart Routing, Remux, VLC)

### Sinnvolle JS-Struktur
- State-Maschine für `videoMode`:
  - `let videoMode = 'chrome-native' | 'ffmpeg' | 'vlc' | 'mkvmerge' | 'dragdrop'`
- `updateVideoMode(mode)`: Setzt Modus, CSS-Klassen, Panels sichtbar/unsichtbar, Fehlerhinweise
- `playVideo(item, path)`: Routing nach Dateityp, Metadaten, Settings; entscheidet Player-Modus und ruft Backend/Frontend-Logik
- `startEmbeddedVideo(item, path)`: Setzt <video>-Player, Fehlerhandling
- Custom Timeline/Seek für Streams: Event-Handling, Seekbar, Buffer/Live-Anzeige
- Stream-Panel: URL-Eingabe, Buttons für VLC-Stream, Stop
- Playlist-Import/Export: Frontend-Parser oder Backend-Logik
- Batch-Remux: UI-Button, Log/Progress-Panel, Eel-Callback für Fortschritt

### Smart Routing (Backend)
- `open_video_smart(path, mode)`: Entscheidet, wie das Video geöffnet wird (direkt, remux, stream, extern)
- Eel-Callbacks für Status/Progress

### Beispiel-Implementierungen (Frontend)
- updateVideoMode(mode):
  - Setzt State, CSS, Panels
- playVideo(item, path):
  - Routing, Backend-Calls, Fehlerhandling
- startEmbeddedVideo(item, path):
  - <video>-Player, Events, Fehler
- Custom Timeline/Seek:
  - timeupdate, click, Buffer/Live
- Playlist-Import/Export:
  - M3U.parse(), Blob-Download
- Batch-Remux:
  - eel.remux_mkv_batch(), Progress-Panel

### Noch offen
- Erweiterte Timeline/Seek-Controls für Streams
- Feedback für Streaming-Modi

---
Dieses Logbuch dokumentiert die Architektur, Patterns und sinnvolle Struktur für den Video Player Tab. Die wichtigsten JS-Bausteine und Backend-Integration sind beschrieben, offene Punkte benannt.
