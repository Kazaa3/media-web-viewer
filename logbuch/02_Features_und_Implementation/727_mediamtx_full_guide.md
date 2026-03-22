# MediaMTX Full Guide for Local Media Apps

## Überblick
MediaMTX (früher rtsp-simple-server) ist ein vielseitiger, leichtgewichtiger Streaming-Router für lokale und hybride Medien-Apps. Er verbindet verschiedene Quellen (FFmpeg, Kameras, VLC) mit modernen Playern (Browser, VLC, mpv, OBS) und übernimmt Protokollwandlung, Routing, Recording und Monitoring.

---

## Installation

### Binary
- [Releases](https://github.com/bluenviron/mediamtx/releases) herunterladen (Linux, Windows, Mac)
- Entpacken, ausführbar machen: `chmod +x mediamtx`
- Starten: `./mediamtx` (Standard: liest `mediamtx.yml` im gleichen Verzeichnis)

### Docker
- Offizielles Image: `docker pull bluenviron/mediamtx`
- Startbeispiel:
  ```sh
  docker run -it --rm -p 8554:8554 -p 8888:8888 -p 8889:8889 -p 8890:8890 -p 1935:1935 -p 9997:9997 \
    -v "$PWD/mediamtx.yml:/mediamtx.yml" bluenviron/mediamtx
  ```

---

## Konfiguration (`mediamtx.yml`)
- YAML-Datei, steuert alle Protokolle, Pfade, Auth, Recording, API, Hooks
- Beispiel:
  ```yaml
  protocols: [rtsp, rtmp, hls, webrtc, srt]
  api: yes
  apiAddress: :9997
  hlsAlwaysRemux: yes
  hlsSegmentCount: 3
  hlsSegmentDuration: 2s
  paths:
    all:
      source: publisher
      record: yes
      recordFormat: fmp4
      runOnReady: echo "Stream ready: $RTSP_PATH"
  ```
- Doku: [mediamtx.org/docs](https://mediamtx.org/docs/)

---

## Unterstützte Protokolle
- **Eingänge:** RTSP, RTMP, SRT, WebRTC, HLS, MPEG-TS/RTP
- **Ausgänge:** RTSP, RTMP, SRT, HLS, WebRTC
- **Browser:** HLS (m3u8), WebRTC (niedrige Latenz)
- **VLC/mpv/ffplay:** RTSP, SRT, RTMP

---

## Recording, Auth, API, Metrics, Hooks
- **Recording:**
  - `record: yes` pro Pfad, Format: fmp4/ts
  - Automatische Speicherung im `recordings/`-Verzeichnis
- **Auth:**
  - Basic-Auth pro Pfad (`username`, `password`)
  - IP-Whitelist/Blacklist
- **API:**
  - HTTP-API (default Port 9997), z.B. `/v3/paths`, `/v3/metrics`, `/v3/rtspconns`
  - Status, Steuerung, Monitoring
- **Metrics:**
  - Prometheus-kompatibel auf `/metrics`
- **Hooks:**
  - `runOnReady`, `runOnDemand`, `runOnRecordStart` etc. für Automatisierung

---

## Typische Integrationsmuster

### 1. HLS/WebRTC für Browser
- **HLS:**
  - ffmpeg → RTSP zu MediaMTX
  - Browser: `/hls/<stream>/index.m3u8` (z.B. mit video.js)
- **WebRTC:**
  - Browser: `/webrtc/<stream>` (niedrige Latenz, z.B. für Live-Kameras)

### 2. RTSP/SRT für VLC/mpv
- **RTSP:**
  - VLC/mpv: `rtsp://<host>:8554/<stream>`
- **SRT:**
  - mpv/ffplay: `srt://<host>:8890?streamid=...`

### 3. Recording/Monitoring
- Recording aktivieren, Streams werden automatisch gespeichert
- API/Prometheus für Health-Checks, Monitoring, Integration in Test-Suites

---

## Best Practices
- HLS als Default für Browser, RTSP/SRT für Power-User/Player
- WebRTC für niedrige Latenz (Live, Interaktiv)
- Recording gezielt pro Pfad aktivieren
- API/Prometheus für Monitoring und Automatisierung nutzen
- Hooks für Benachrichtigungen/Automatisierung (z.B. Slack, E-Mail)

---

## Links & Ressourcen
- [MediaMTX GitHub](https://github.com/bluenviron/mediamtx)
- [Offizielle Docs](https://mediamtx.org/docs/)
- [Docker Hub](https://hub.docker.com/r/bluenviron/mediamtx)
- [API Doku](https://mediamtx.org/docs/api/)
- [Prometheus Metrics](https://mediamtx.org/docs/metrics/)
