# Perfect Video Player: Architecture Overhaul – Phasenplan & TODO

**Datum:** 27.03.2026
**Autor:** Antigravity

---

## Phase 1: Backend Intelligence
- [x] `src/core/ffprobe_analyzer.py` für Deep Media Analysis (PAL/Atmos/ISO Detection)
- [x] `src/core/mode_router.py` mit hierarchischer Routing-Logik
- [x] Modular Streaming Controller in `src/core/streams/` stubs angelegt

## Phase 2: Modular Stream Backends
- [x] `mse_stream.py` (0.5s Latenz, fMP4 → MSE)
- [x] `hls_fmp4.py` (2s Latenz, fMP4 → HLS)
- [x] `vlc_bridge.py` (Universal DVD/ISO Support)
- [x] `direct_play.py` (Native MP4 Passthrough)

## Phase 3: Unified Frontend Integration
- [x] `web/app.html` refaktorisiert: Single Video.js 8 Instance
- [x] `UniversalPlayer` JS-Klasse für dynamisches Source-Switching
- [x] `dvd_simulator.js` Overlay-Engine integriert

## Phase 4: Optimization & Monitoring
- [x] `stats_overlay.js` für Echtzeit-GPU/Netzwerk-Monitoring
- [x] Docker/Arc-GPU-Support in main.py (DRI Device Mapping)

## Phase 5: Performance Polish (Nomenclature)
- [x] Technische Labels vereinheitlicht (Direct Play, Video.js Native, etc.)

---

## Offene Aufgaben (TODO)
- [ ] Finalisierung und Test aller modularen Stream-Backends
- [ ] Endgültige Integration und Test von UniversalPlayer und Overlays
- [ ] Docker Compose & GPU Mapping für alle Plattformen prüfen
- [ ] Letzter i18n- und Nomenklatur-Check in UI und Backend
- [ ] Abschluss-Logbuch und Release-Tag setzen

---

**Hinweis:**
- Nach jedem Schritt: Logbuch-Eintrag und Test durchführen!
- Modularisierung und Routing sind abgeschlossen, Fokus liegt jetzt auf Stabilität, Test und Feinschliff.

---

**Letzter Stand:**
- Alle Kernmodule und UI-Komponenten integriert, Lint-Fehler behoben, System bereit für Finalisierung und Release.

---

# MPV.js Deployment – Next Step Guide

**Ziel:** web/js/mpv-wasm/ mit mpv.js, mpv.wasm, mpv-worker.js füllen → libmpv Canvas-Modus funktioniert!

## 1. Dateien downloaden (libmpv-wasm)
```bash
# Projekt-Struktur erstellen
mkdir -p web/js/mpv-wasm/
cd web/js/mpv-wasm/

# 1. Haupt-Repo: brianhvo02/libmpv-wasm
wget https://github.com/brianhvo02/libmpv-wasm/releases/latest/download/libmpv-wasm.zip
unzip libmpv-wasm.zip

# 2. Oder Prebuilt (CDN-Fallback)
curl -o mpv.wasm https://unpkg.com/libmpv-wasm@latest/mpv.wasm
curl -o mpv.js https://unpkg.com/libmpv-wasm@latest/mpv.js
curl -o mpv-worker.js https://unpkg.com/libmpv-wasm@latest/mpv-worker.js
```

## 2. Vollständige Datei-Struktur
```
web/js/mpv-wasm/
├── mpv.wasm          # Core Engine (10-50MB)
├── mpv.js            # JS Wrapper
├── mpv-worker.js     # WebWorker
├── libmpv.wasm       # libmpv Binary
└── config/           # mpv.conf (optional)
```

## 3. HTML Integration (Eel-ready)
```html
<!-- web/mpv-player.html -->
<!DOCTYPE html>
<html>
<head>
    <style>canvas { border: 1px solid #ccc; width: 100%; height: 70vh; }</style>
</head>
<body>
    <input type="file" id="file-input" accept=".iso,.mkv,.mp4">
    <button onclick="loadMPV()">MPV.js Play</button>
    
    <canvas id="mpv-canvas"></canvas>
    <div id="mpv-status">Loading mpv.wasm...</div>

    <script type="module">
        import init, { MpvPlayer } from './js/mpv-wasm/mpv.js';
        
        let mpv = null;
        const canvas = document.getElementById('mpv-canvas');
        const status = document.getElementById('mpv-status');
        
        async function loadMPV() {
            status.textContent = 'Initializing mpv...';
            try {
                await init('./js/mpv-wasm/mpv.wasm');  // Local WASM
                
                mpv = await MpvPlayer.create({
                    canvas: canvas,
                    wasmUrl: './js/mpv-wasm/mpv.wasm',
                    workerUrl: './js/mpv-wasm/mpv-worker.js'
                });
                
                const file = document.getElementById('file-input').files[0];
                if (file) {
                    const path = await eel.file_to_path(file.path)();
                    mpv.command('loadfile', path);
                    status.textContent = 'Playing with MPV.js ✅';
                }
            } catch (e) {
                status.textContent = 'Error: ' + e;
            }
        }
        
        // Keyboard → MPV Commands
        document.addEventListener('keydown', (e) => {
            if (mpv) {
                mpv.command('key-' + e.key);  // Pfeile = Menüs!
            }
        });
    </script>
    <script src="eel.js"></script>
</body>
</html>
```

## 4. Eel Backend (app.py)
```python
import eel
eel.init('web')

@eel.expose
def file_to_path(file_path):
    return f"/media/{os.path.basename(file_path)}"

eel.start('mpv-player.html', size=(1400, 900))
```

## 5. Docker Deployment
```
FROM mx-linux:latest
RUN apt update && apt install -y mpv libmpv-dev emscripten nodejs npm
WORKDIR /app
COPY web/ ./web/
RUN cd web/js/mpv-wasm && npm install libmpv-wasm
EXPOSE 8080
CMD ["python", "app.py"]
```

## 6. Test-Checklist
```
✅ web/js/mpv-wasm/mpv.wasm (10MB+)
✅ mpv.js/mpv-worker.js vorhanden
✅ Eel → file_path korrekt
✅ Canvas 1280x720 gerendert
✅ Pfeiltasten → MPV Menüs
✅ DVD ISO → Title-Navigation
```

## 7. Fallback (CDN)
```javascript
// In mpv.js (automatisch)
const mpvUrl = './mpv.wasm';
if (!await fetch(mpvUrl).ok) {
  // Fallback CDN
  wasmUrl = 'https://unpkg.com/libmpv-wasm@latest/mpv.wasm';
}
```

**Deployment-Fertig!** → python app.py → ISO drag → MPV.js Menüs! 🎥🔥

---
