# Logbuch: MediaMTX (HLS/WebRTC) – Dual-Stream Video-Modus

## Datum
16. März 2026

---

## Konzept: MediaMTX Dual-Stream (HLS & WebRTC)
- **HLS:** Perfekte Kompatibilität, Seeking, native <video>-Unterstützung in Chrome/Browsern.
- **WebRTC (WHEP):** Ultra-low-latency (<100ms), ideal für Live/Instant-Playback, parallel zu HLS verfügbar.
- **Browser-Auto-Select:** Beide Streams werden bereitgestellt, Browser/Frontend kann je nach Fähigkeit und Use-Case wählen.

---

## Setup
### 1. docker-compose.yml (Synology-ready)
```yaml
version: '3.8'
services:
  mediamtx:
    image: bluenviron/mediamtx:latest
    container_name: mediamtx-video
    network_mode: host
    volumes:
      - /volume1/media:/media
      - ./mediamtx.yml:/mediamtx.yml
    restart: unless-stopped
```

### 2. mediamtx.yml (HLS + WebRTC)
```yaml
api: yes
apiAddress: :9997
webrtcAdditionalMergeParams: |
  vflip=1  # Optional
paths:
  all:
    runOnInit: ffmpeg -stream_loop -1 -i file:///media/$MTX_PATH -c copy -f rtsp rtsp://localhost:8554/$MTX_PATH
    runOnDemand: ffmpeg -stream_loop -1 -i file:///media/$MTX_PATH -c copy -f rtsp rtsp://localhost:8554/$MTX_PATH
    hls: yes
    webrtc: yes
```

### 3. Start & URLs
```bash
docker compose up -d
# HLS:    http://nas-ip:8888/movie.mkv/index.m3u8
# WebRTC: http://nas-ip:8889/movie.mkv
```

---

## Eel/Bottle Integration (Dual-Mode)
- Video-Player lädt HLS als Fallback, prüft WebRTC-Verfügbarkeit via JS.
- Python-API liefert beide URLs (hls, webrtc) an das Frontend.

---

## Vorteile HLS vs WebRTC
| Feature   | HLS (8888)         | WebRTC/WHEP (8889) |
|-----------|--------------------|--------------------|
| Seeking   | Perfekt (Chunks)   | Instant (Ranges)   |
| Latency   | 4–8s Buffering     | <100ms             |
| Chrome    | Native <video>     | Native Seite       |
| ISO/MKV   | Ja (ffmpeg auto)   | Ja (H.264 only)    |
| CPU       | Minimal            | Minimal            |

---

## Modus in der App
**MediaMTX (HLS/WebRTC)**
- HLS: http://:8888/file/index.m3u8 → Native Chrome
- WebRTC: http://:8889/file → Low Latency
- Auto ffmpeg für alle Formate

---

## Empfehlung
- Beide Streams parallel anbieten, Browser/Frontend entscheidet.
- Zuerst HLS-nativ testen, dann WebRTC für Low-Latency validieren.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe vorherige Logbuch-Einträge für Backend- und Streaming-Details.*
