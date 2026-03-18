# Logbuch: cvlc – CLI VLC Integration (Headless, Docker-ready)

## Stand März 2026

### Features & Architektur
- cvlc = VLC ohne GUI (headless, --intf dummy), ideal für Server, NAS, Docker-Container.
- Minimalistisches Panel im UI: Play, Stop, Kill, Volume, PID-Anzeige, Live-Logs.
- Drag&Drop: Files/Playlists direkt in cvlc.
- Live Log-Window: Echtzeit-Log aus stderr.
- PID-Control: Stop/Kill für laufende Prozesse.
- Volume: RC Interface (remote steuerbar).
- Docker-Integration: cvlc als Service, RC-Host für Remote-Control.

### Beispiel-Implementierung
#### HTML (Panel)
```html
<!-- cvlc Panel -->
<div id="cvlcPanel" class="player-panel" style="display: none;">
  <div class="cvlc-controls">
    <button id="cvlcPlay">▶️ Play</button>
    <button id="cvlcStop">⏹️ Stop</button>
    <button id="cvlcKill">💀 Kill</button>
    <input id="cvlcVolume" type="range" min="0" max="1024" value="256">
    <span id="cvlcPid">PID: -</span>
  </div>
  <div id="cvlcDragDrop" class="drag-zone">Drag Files/Playlists → cvlc</div>
  <div id="cvlcStatus">cvlc Ready</div>
  <pre id="cvlcLog" class="log-window"></pre>
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
  cvlc-player:
    image: linuxserver/vlc:latest
    command: cvlc --intf dummy --dvd-device /media {{ .Values.path }}
    volumes:
      - /path/to/media:/media
    ports:
      - "4212:4212"  # RC Interface
    environment:
      - PUID=1000
      - PGID=1000
```

### Vergleich: cvlc vs VLC vs PyVLC
| Feature      | cvlc (CLI) | VLC (GUI) | PyVLC (Python) |
|--------------|------------|-----------|----------------|
| Headless     | ✅         | ❌        | ✅             |
| Live Logs    | ✅         | ❌        | ✅             |
| PID Control  | ✅         | ❌        | ✅             |
| Volume       | ✅ RC Host | ✅ GUI    | ✅ API         |
| Playlists    | ✅ m3u     | ✅        | ✅ Programmatic |

### Zusammenfassung
- cvlc = Headless VLC Powerhouse für Server/Remote.
- Live Logs, PID-Control, Docker-ready.
- Alle VLC-Varianten komplett: VLC/GUI, cvlc/CLI, pyvlc/Python.

---
Perfekt für Backend, NAS, Docker – minimalistisch, robust, remote steuerbar!
