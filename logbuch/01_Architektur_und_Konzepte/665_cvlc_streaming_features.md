# Logbuch: cvlc + Video Streaming – RTSP/HLS/HTTP Streams

## Stand März 2026

### Features & Architektur
- cvlc streamt alles: RTSP, HLS, HTTP, UDP, Dateien – ideal für Remote-Playback, NAS, Docker.
- Streaming Panel im UI: Stream-Input, Status, Output-URL, Copy-Button.
- JS: Stream Controls (Play, Status, Copy), Routing zu anderen Playern.
- Backend: cvlc Streaming Controller (RTSP/HLS/HTTP), Multi-Input, Transcoding.
- Docker: cvlc Streaming Container, Ports für HLS/HTTP/RTSP.

### Beispiel-Implementierung
#### HTML (Panel)
```html
<div id="cvlcStreamPanel" class="sub-panel">
  <h4>cvlc Streaming</h4>
  <div class="stream-input">
    <input id="cvlcStreamUrl" placeholder="rtsp://... | http://... | file://...">
    <button id="cvlcStreamPlay">Stream ▶️</button>
  </div>
  <div id="cvlcStreamStatus"></div>
  <div class="stream-output">
    <input id="cvlcStreamOut" readonly placeholder="RTSP Output">
    <button id="cvlcCopyStream">📋 Copy</button>
  </div>
</div>
```

#### JS (Controls)
```js
// ...existing code...
```

#### Python (Backend)
```python
# ...existing code...
```

#### Docker Compose
```yaml
services:
  cvlc-streamer:
    image: linuxserver/vlc:latest
    ports:
      - "8080:8080"  # HLS/HTTP
      - "8554:8554"  # RTSP
    volumes:
      - /media:/media:ro
    command: >
      cvlc --intf dummy 
      --sout-keep 
      --loop 
      /media/{{ .Path }}
```

### Streaming-Beispiele
- RTSP Input → RTSP Output: `cvlc_stream('rtsp://camera.local/stream', 'rtsp')` → `rtsp://localhost:8554/stream`
- File → HLS: `cvlc_stream('/path/to/video.mkv', 'hls')` → `http://localhost:8080/stream.m3u8`
- RTMP → HTTP MP4: `cvlc_stream('rtmp://live.youtube/stream', 'http-mp4')` → `http://localhost:8081/stream.mp4`

### Features cvlc Streaming
- ✅ RTSP ↔ HLS ↔ HTTP (bi-directional)
- ✅ Live Logs + PID
- ✅ Transcoding (MKV → H.264 on-the-fly)
- ✅ Docker-ready
- ✅ Multi-Input (File/RTSP/RTMP/UDP)

---
cvlc = Streaming-Superheld! Stream-URL kopieren → in FFplay/MTX/Chrome Native wiederverwenden!
