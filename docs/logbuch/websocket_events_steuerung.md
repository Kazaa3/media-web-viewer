# WebSocket & Events: Steuer- und Signalisierungsebene

**Empfohlene Nutzung in deiner App:**

---

## Gute Einsatzzwecke

- **Player-Events zum Backend schicken**
  - video.js-Events wie `play`, `pause`, `seeking`, `timeupdate`, `volumechange` abfangen und per WebSocket an Python senden
  - Use Cases:
    - Watch-Progress / „zuletzt gesehen“
    - Realtime-Logs für Test-Suite („HLS-Stream X läuft seit N Sekunden, keine Errors“)

- **Backend → Frontend Push**
  - Status von HLS-Jobs („Transcode fertig“, „Segmenter läuft nicht“)
  - MediaMTX-Health („RTSP-Source down“, „Reconnect läuft“) in Echtzeit anzeigen
  - Async-Aktionen wie PAL-DVD→H.264-Konvertierung per Event updaten

- **Remote-Control / Sync**
  - Ein Client startet/stoppt/seeked, andere Instanzen (oder Eel-Fenster) folgen über WebSocket-Events

---

## Was du NICHT über WebSocket machen solltest

- Kein „Video über WebSocket streamen“ – das ist ein Sonderweg (Canvas-Hacks, eigene Demuxer) und für deine Mediathek unnötig komplex
- WebSocket ist ideal als **leichtgewichtiger Event-Bus** um den Player herum, während das eigentliche Video als MP4/HLS/DASH/RTSP läuft
