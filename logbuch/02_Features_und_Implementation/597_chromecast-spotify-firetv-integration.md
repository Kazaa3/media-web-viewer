# Logbuch: Chromecast-, Spotify- und Fire TV-Integration

**Datum:** 16. März 2026

---

## Chromecast-Support in Eel/Bottle-App

Mit PyChromecast kannst du deine App als Cast-Receiver für Audio/Video-Streams nutzen. Geräte werden automatisch entdeckt, Streams gestartet und Custom-Receiver-Apps unterstützt.

### Installation
```bash
pip install pychromecast
```

### Beispiel-Code (Backend: Bottle, GUI: Eel)
```python
import pychromecast
from bottle import route, run

chromecasts, browser = pychromecast.discover()
# Für Receiver: Custom App laden via chromecasts[0].register_status_listener()

@route('/cast/<media_url>')
def cast_media(media_url):
    chromecasts[0].media_controller.play_media(media_url, 'video/mp4')
    return 'Casting...'

run(host='localhost', port=8080)
```
Das Eel-Frontend ruft `/cast/<media_url>` via AJAX auf und zeigt die Geräte-Liste.

---

## Spotify Connect
- Keine direkte Unterstützung in Eel/Bottle (proprietär, offizielle SDKs nötig).
- Workaround: Spotipy für Playback-Control, librespot-rs (Rust) als Connect-Emulator.
- Spotify kann zu PyChromecast-Ziel casten, wenn als Gerät sichtbar.

---

## Fire TV Support
- Fire TV unterstützt kein Google Cast nativ.
- Alternative: DLNA/UPnP (z.B. python-dlnap) oder HLS-Stream via MediaMTX.
- Fire TV VLC/EXO-Player kann HLS von deinem Bottle-Server abspielen.

---

## Integration mit MediaMTX
- MediaMTX (RTSP/HLS) als Bridge für Streaming zu Fire TV, Chromecast, Web-GUI.
- Docker-Service für Synology/Jellyfin-Setup möglich.

---

## Nächste Schritte
- PyChromecast separat testen, dann in Bottle/Eel-App integrieren.
- Für Spotify/Fire: MediaMTX als Bridge nutzen.
- Beispiel: app.mount('/cast', cast_app) für Bottle.

---

## DLNA/UPnP

- Media-Server mit `dlnap` oder `ryu` erstellen.
- Fire TV, VLC, BubbleUPnP entdecken Inhalte automatisch via SSDP.
- Installation:
  ```bash
  pip install dlnap
  ```
- Beispiel:
  ```bash
  dlnap play /path/to/media.mp4
  ```
- Erweiterung: Bottle-Route für dynamische Dateien.

---

## AirPlay

- Nutze `pyatv` oder `python-airplay` für Apple TV/iOS-Casting.
- Installation:
  ```bash
  pip install pyatv
  ```
- Geräte scannen, play/pause via asyncio.
- In Eel: JS-Button triggert Python-Funktion zum Streamen.

---

## Spotify Connect

- `pyspotify-connect` (veraltet, aber forkbar) macht deine App zum Connect-Player; braucht Premium und libspotify.
- Besser: Spotipy + librespot für Control, kombiniert mit DLNA/HLS für Multi-Device.

---

## Weitere Optionen

| Protokoll   | Library           | Vorteile für Eel/Bottle/Fire TV           |
|-------------|-------------------|-------------------------------------------|
| HLS/RTSP    | MediaMTX/FFmpeg   | Browser-nativ, Fire TV VLC-kompatibel, passt zu Jellyfin |
| Matter Cast | Neu (Amazon)      | Offen, Fire TV 7+ nativ, aber noch früh   |
| WebRTC      | aiortc            | Peer-to-Peer, niedrige Latenz für Live-Audio |

---

## Implementierungstipps

- In Bottle: `@route('/stream/<file>')` mit `static_file` + Protokoll-Header.
- Eel-GUI listet Geräte und startet Cast.
- Starte mit DLNA für schnellen Test auf Fire TV.

---

## ffplay RTSP Stream mit MediaMTX abspielen

Um einen RTSP-Stream mit ffplay über MediaMTX abzuspielen, verwende diese bewährten Befehle. Stelle sicher, dass MediaMTX läuft und ein Stream publiziert ist (z. B. via ffmpeg oder Kamera).

### Stream abspielen (Reader)
```bash
ffplay -rtsp_transport tcp rtsp://localhost:8554/mystream
```
- `-rtsp_transport tcp`: Vermeidet UDP-Probleme (Firewall/Paketverlust).
- `mystream`: Dein Path-Name (aus mediamtx.yml oder API `curl localhost:9997/v3/paths/list`).

### Vollständiger Test (Publisher + Player)
Stream publishen (z. B. Video-Datei):
```bash
ffmpeg -re -stream_loop -1 -i /path/to/video.mp4 -c copy -f rtsp rtsp://localhost:8554/test
```
Abspielen (neues Terminal):
```bash
ffplay -rtsp_transport tcp rtsp://localhost:8554/test
```
Drücke `q` zum Beenden.

### Häufige Probleme & Fixes
| Problem           | Lösung                                                                 |
|-------------------|------------------------------------------------------------------------|
| 404 Not Found     | Stream nicht publiziert oder falscher Path. Prüfe `curl localhost:9997/v3/paths/list` |
| Kein Video/Lag    | TCP nutzen; `ffplay -fflags nobuffer -flags low_delay ...`              |
| Auth              | `ffplay rtsp://user:pass@localhost:8554/stream` (konfiguriere in yml)  |
| Fernzugriff       | `rtsp://deine-ip:8554/stream` (Firewall Port 8554 öffnen)              |

### Alternative Player
- VLC: `vlc rtsp://localhost:8554/test`
- Browser HLS: `http://localhost:8888/test/index.m3u8`

### MediaMTX-Logs
- Fehler prüfen: `tail -f /tmp/mediamtx.log`

---

# swyh-rs: Open-Source DLNA/UPnP Audio-Bridge

swyh-rs ist eine Open-Source Rust-App als Alternative zu StreamWhatYouHear (SWYH), die System-Audio (z.B. Spotify) über UPnP/DLNA zu Renderern wie Fire TV streamt – ideal als Bridge für deine Eel/Bottle-Media-App.

## Features
- Entdeckt DLNA-Geräte automatisch (Fire TV, Sonos, Denon etc.)
- Streamt WAV über UPnP mit niedriger Latenz
- GUI-basiert, reconnect bei Start, chunked-Transfer-Optionen
- Zuverlässiger als SWYH

## Einschränkungen
- Kein AirPlay/Spotify Connect nativ, aber kombinierbar mit Python-Backends für Spotify-Control

## Integration in Eel/Bottle
- Dockerize swyh-rs (Rust-Binary)
- Steuerung via API/Unix-Socket aus Bottle
- Eel-GUI zeigt Geräte und startet Streams
- Download: GitHub-Releases (dheijl/swyh-rs)

### Beispiel-Setup
```bash
docker run -p 8080:8080 swyh-rs  # UPnP exposen
# In Bottle: requests.post('http://swyh/api/play', data={'url': media})
```
- Passt zu MediaMTX/HLS für hybrides Streaming

## Vorteile vs. DLNA-Python
- Rust ist effizienter für Echtzeit-Audio (weniger CPU als Python-DLNA)
- Erweiterbar mit librespot-rs für Spotify Connect

---

**Frage:**
Soll ich ein Docker-Compose-Beispiel mit swyh-rs + deiner Bottle-App erstellen?
