# Minimal-Template: "Stat + Nice GUI" für Mediaplayer

## 1. Ziel-Idee: „statt: nice GUI“

- Oben/Seitenleiste: Medien-Bibliothek / Playlist-View
- Mitte: großer Video-Player-Bereich (mpv.js / video.js)
- Unten/Seitenpanel: Statistiken & System-Status (CPU, RAM, Audio-Delay, mpv-Bitrate, etc.)

---

## 2. UI-Konzept (minimal & clean)

| Bereich                 | Inhalt                                                        |
|-------------------------|---------------------------------------------------------------|
| Header                  | App-Name, Playlists / Library / Settings Navigation           |
| Linke Sidebar           | Bibliothek, Playlists, Filter-Felder                          |
| Haupt-Playerbereich     | video.js / mpv.js-Container (Fullscreen-fokussiert)           |
| Rechte Sidebar / Footer | Stats-Panel (System + mpv-Status)                             |

**Layout-Skizze:**

```html
<div class="app">
  <nav class="navbar">...</nav>
  <div class="main-layout">
    <aside class="sidebar sidebar-left">
      <ul id="library"></ul>
    </aside>
    <main class="player-main">
      <video id="video" class="video-js vjs-default-skin" controls></video>
    </main>
    <aside class="sidebar sidebar-right">
      <div class="stat-box">
        <h4>System</h4>
        <p>CPU: <span id="cpu">?</span>%</p>
        <p>RAM: <span id="ram">?</span> MB</p>
        <p>Netzwerk: <span id="net">?</span> Mbps</p>
      </div>
      <div class="stat-box">
        <h4>mpv Player</h4>
        <p>State: <span id="mpv-state">?</span></p>
        <p>Bitrate: <span id="mpv-bitrate">?</span> kbps</p>
        <p>Buffer: <span id="mpv-buffer">?</span> ms</p>
      </div>
    </aside>
  </div>
</div>
```

**CSS-Idee:**

```css
.app { display: flex; flex-direction: column; }
.main-layout { display: flex; }
.sidebar { width: 250px; background: #f0f0f0; padding: 1rem; }
.player-main { flex: 1; background: #000; position: relative; }
.stat-box { margin-bottom: 1rem; border: 1px solid #ddd; padding: 0.5rem; }
```

---

## 3. Statistiken abrufen

### System-Stats (CPU/RAM/Netzwerk)

**Backend (Python, psutil):**

```python
# python_backend/stats.py
import psutil
from bottle import route
@route('/api/stats')
def stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    net = psutil.net_io_counters().bytes_sent / 1024  # Beispiel
    return {
        "cpu": cpu,
        "ram": ram,
        "net": net
    }
```

**Frontend (JS, alle 2s):**

```js
setInterval(async () => {
  const resp = await fetch('http://localhost:8080/api/stats');
  const data = await resp.json();
  document.getElementById('cpu').textContent = data.cpu.toFixed(1);
  document.getElementById('ram').textContent = data.ram.toFixed(1);
  // ... für Netzwerk
}, 2000);
```

### mpv-Stats

- Backend-Endpunkt, der mpv-Status (z.B. {"playing": true, "bitrate": 192, "buffer": 100}) zurückgibt.
- z.B. via mpv-IPC: sende {"command": ["get_property", "avsync"]} etc. und zeige Werte im Stat-Panel.

---

## 4. Beispielskizze für mpv.js-Integration

```html
<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
<div class="player-main">
  <video id="video-player" class="video-js vjs-default-skin" controls preload="auto"></video>
</div>
<script>
  const player = videojs('video-player', {
    autoplay: false,
    controls: true,
    sources: [{
      src: '/api/stream/hls/:id.m3u8',
      type: 'application/x-mpegURL'
    }]
  });
</script>
<!-- oder mpv.js -->
<script type="module">
  import mpv, { MPV } from 'mpv.js';
  const mpvPlayer = new MPV({
    container: document.getElementById('mpv-container')
  });
  mpvPlayer.load('file:///path/to/media/file.mp4');
</script>
```

---

## 5. Hinweise zur „Nice GUI“

- Farbschema: Dunkel für Video-Area, hellere Sidebar für Bibliothek
- Responsive-Design: @media (max-width: 768px) → Sidebars ausblenden
- Animations-Highlights: Hover-Effekte für Playlist, sanfte Opacity-Übergänge

---

## Klarstellung: Wechsel von Python-GUI zu Electron/mpv.js

Das bisherige Python-GUI-Framework (z. B. nicegui, Dash, Gradio) wird durch eine Electron-/Browser-basierte Frontend-Shell mit mpv.js als Player ersetzt. Das Python-Backend (bottle, FastAPI o. ä.) bleibt für Mediathek, Equalizer, Stats und Steuer-APIs bestehen – aber die GUI läuft nun komplett in HTML/JS (Electron oder Browser), nicht mehr als Python-GUI.

### Was konkret zu tun ist
1. Entferne das Python-GUI-Framework (z. B. nicegui) aus deinem Projekt und den Abhängigkeiten.
2. Lege eine Electron-App-Struktur an (main.js, preload.js, package.json, index.html, js/player.js, js/api_client.js).
3. Im Frontend nutzt du mpv.js als Player-Engine (siehe Beispiel unten).
4. Die Kommunikation zu deinem Python-Backend läuft über HTTP/REST (fetch-Aufrufe im JS).

**Minimalbeispiel mpv.js-Integration (player.js):**
```js
import mpv, { MPV } from 'mpv.js';
const mpvPlayer = new MPV({
  container: document.getElementById('mpv-container')
});
mpvPlayer.load('file:///path/to/media/file.mp4');
```

**Stats vom Python-Backend holen:**
```js
setInterval(async () => {
  const resp = await fetch('http://localhost:8080/api/stats');
  const data = await resp.json();
  // Update UI mit data.cpu, data.ram, ...
}, 2000);
```

**Projektstruktur:**
```
media_app_electron/
  main.js
  preload.js
  package.json
  index.html
  js/
    player.js
    api_client.js
python_backend/
  bottle_server.py
  stats.py
  media_lib/
```

**Vorteile:**
- Klare Trennung: Electron/JS-Frontend, Python-Backend.
- Moderner mpv.js-Player in der App.
- Python-Backend bleibt für Logik, Mediathek, Equalizer, Stats.

Wenn du möchtest, kann ich dir ein minimal-lauffähiges Electron/mpv.js-Template (inkl. Python-Backend-API) erstellen, das du direkt als Basis nutzen kannst. Sag einfach Bescheid!