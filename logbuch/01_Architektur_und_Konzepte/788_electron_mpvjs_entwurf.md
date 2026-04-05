# Praktisch einsetzbarer Entwurf: Electron + mpv.js + Python-Backend

## 1. Ziel-Architektur

- **Frontend-Shell:** Electron + mpv.js
- **Backend:** Bottle-Server (Python, laufender Prozess)
- **Kommunikation:**
  - Electron ↔ Python: HTTP/REST
  - mpv.js ↔ Electron-Main: ipcMain/ipcRenderer (z.B. für EQ-Steuerung/Preset-Hook)

---

## 2. Ordner-Struktur (Beispiel)

```
gui_media_electron/
  main.js                  # Electron-Main-Prozess
  preload.js               # IPC-Schnittstelle
  package.json
  index.html
  js/
    player.js              # mpv.js-Steuerung, JS-UI
    api_client.js          # Aufruf an Python-Backend (z.B. via fetch)
python_backend/
  bottle_server.py         # Bibliothek, Endpunkte
  media_lib/               # Medien-Backend
```

---

## 3. Electron-Main-Prozess (main.js)

```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
let mainWindow;
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
    },
  });
  mainWindow.loadFile('index.html');
}
app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
```

---

## 4. Preload-Skript (preload.js)

```javascript
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('electronAPI', {
  startMpv: (filePath) => ipcRenderer.send('mpv:start', filePath),
  mpvPlay: () => ipcRenderer.send('mpv:play'),
  mpvPause: () => ipcRenderer.send('mpv:pause'),
  mpvSeek: (seconds) => ipcRenderer.send('mpv:seek', seconds),
});
```

---

## 5. Frontend-Seite (index.html + js/player.js)

### index.html

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Mediaplayer mit mpv.js</title>
</head>
<body>
  <h1>Mediaplayer</h1>
  <div id="mpv-container"></div>
  <button onclick="playVideo()">Play</button>
  <button onclick="pauseVideo()">Pause</button>
  <script src="js/player.js"></script>
</body>
</html>
```

### js/player.js

```javascript
import mpv, { MPV } from 'mpv.js';
const mpvPlayer = new MPV({
  container: document.getElementById('mpv-container'),
});
function playVideo() {
  const filePath = 'file:///path/to/your/media/file.mp4';
  mpvPlayer.load(filePath);
}
function pauseVideo() {
  mpvPlayer.pause();
}
// Optional: Electron-IPC-Hook für EQ-Presets an Python-Backend
const playButton = document.querySelector('button');
playButton.addEventListener('click', async () => {
  await window.electronAPI.startMpv('/media/track.mp4');
  await mpvPlayer.load('/media/track.mp4');
});
```

Installation für mpv.js:

```bash
npm init -y
npm install mpv.js
```

(Installiere `libmpv-dev`/`mpv-dev` auf deinem System.) [github](https://github.com/Kagami/mpv.js/)

---

## 6. Python-Backend-Endpunkt (Bottle-basiert)

```python
from bottle import route, run, static_file
import subprocess
MPV_CMD = [
    "mpv",
    "--no-terminal",
    "--idle",
    "--input-ipc-server=/tmp/mpv.sock"
]
proc = subprocess.Popen(MPV_CMD)
@route('/play/<path>')
def play(path):
    import json
    msg = json.dumps({"command": ["loadfile", path]})
    with open("/tmp/mpv.sock", "w") as f:
        f.write(msg + "\n")
    return {"status": "playing", "path": path}
@route('/api/media')
def media():
    return {"tracks": [...]}
run(host='localhost', port=8080, debug=True)
```

Electron-Frontend ruft:

```js
fetch('http://localhost:8080/api/media')
  .then(response => response.json())
  .then(data => { /* Medienliste zeigen */ });
```

---

## 7. Electron-Package (package.json)

```json
{
  "name": "gui_media_electron",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "dependencies": {
    "mpv.js": "^latest"
  },
  "devDependencies": {
    "electron": "^latest"
  }
}
```

Installation:

```bash
npm install
```

Dann App starten:

```bash
npm start
```

---

## 8. Vorteile für den Use-Case

- Vollwertiger mpv-Player in Electron-App
- Equalizer/Presets via mpv-IPC steuerbar
- Python-Backend bleibt für Mediathek, EQ-Logik, REST-API
- Electron-UI für modernes Desktop-Feeling

**Tipp:** Für ein vollständiges GitHub-Template (Electron + mpv.js + Python-Backend) einfach melden!
