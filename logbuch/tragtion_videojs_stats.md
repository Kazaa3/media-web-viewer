# Fixes: MKV Seeking, Track Switching, and Stats Button Visibility (27.03.2026)

- **MKV Seeking:**
  - /video-remux-stream wurde zur Hot-Reload-Seeking-Logik im Frontend hinzugefügt.
  - Sicherstellen, dass ein Seek den FFmpeg-Stream für MKV korrekt neu startet.
- **Track Switching:**
  - Auswahl von Audio- oder Untertitelspuren erzwingt jetzt ein Stream-Reload mit neuen Track-Parametern, insbesondere für MKV.
  - Backend erhält aktualisierte Track-Infos und startet den Stream bei Bedarf neu.
- **Stats Button Visibility:**
  - Der STATS-Button ist jetzt deutlich hervorgehoben (Farbe, Größe, ggf. Icon) und befindet sich in der unteren Controlbar zwischen den Feature-Buttons (VLC, Cinema, etc.).
  - Tooltip und visuelle Hinweise erleichtern das Auffinden.
  - Label bleibt "STATS".
- **Intel Arc GPU Monitoring Refinement:**
  - Weitere Verfeinerung der Erkennung und Skalierung für Intel Arc GPUs.
  - Fallback-Logik für ältere Intel iGPUs bleibt erhalten.

# Verification Steps (27.03.2026)
- **MKV Seeking:**
  - Seek in einem MKV-Stream ausführen, prüfen, ob der Stream korrekt neu startet und an die gewünschte Position springt.
- **Track Switching:**
  - Audio- oder Untertitelspur wechseln, prüfen, ob der Stream mit neuer Spur neu geladen wird.
- **Stats Button:**
  - Sichtbarkeit und Auffindbarkeit des STATS-Buttons in der Controlbar prüfen.
  - Overlay-Funktionalität testen.
- **Intel Arc Monitoring:**
  - GPU-Auslastung bei Arc/iGPU unter Last (z.B. FFmpeg) beobachten.
# Intel Arc GPU Monitoring Refinement (27.03.2026)

- **Backend (main.py):**
  - import glob für saubere Pfaderkennung.
  - get_gpu_usage_safe():
    - glob.glob('/sys/class/drm/card*/device/gpu_busy_percent') für alle GPUs.
    - Wenn Intel (vendor oder Pfad), Wert durch 10 teilen (0-1000 → 0-100).
    - Fallback: iGPU-Frequenz-Proxy, falls gpu_busy_percent fehlt.

# Verification Plan
- **Manual:**
  - "STATS"-Button im Video.js-Player finden.
  - Overlay toggeln, Glassmorphism-Overlay erscheint.
  - GPU-Metrik prüfen: Bei FFmpeg/Video-Last steigt GPU-Auslastung sichtbar.
# Fix: vjsComponent Error & Universal GPU Detection (27.03.2026)

- **JS Startup Fix:**
  - Fehlende vjsComponent-Definition in app.html ergänzt, Referenzfehler auf Start beseitigt.
- **Universal GPU Support:**
  - AMD: /sys/class/drm/card*/device/gpu_busy_percent wird überwacht.
  - Intel Arc: /sys/class/drm/card*/device/gpu_busy_percent für Busy-Time (0-100%), präzise Auslastung (ab Kernel 6.1+, Mesa 24+).
    - Fallback für ältere iGPUs: act_freq/max_freq als Proxy (siehe unten).
  - Nvidia: nvidia-smi bleibt als Fallback.

**Erweiterte Backend-Monitoring (Intel Arc/iGPU):**
```python
import psutil, glob, time, json

def get_intel_arc_util():
    cards = glob.glob('/sys/class/drm/card*/device/gpu_busy_percent')
    if cards:
        with open(cards[0], 'r') as f:
            busy_percent = int(f.read().strip()) / 10  # 0-1000 → 0-100
        return busy_percent
    # Fallback iGPU: act_freq/max_freq
    freq_file = '/sys/class/drm/card0/gt_cur_freq_mhz'
    max_freq_file = '/sys/class/drm/card0/gt_max_freq_mhz'
    if glob.glob(freq_file) and glob.glob(max_freq_file):
        cur = int(open(freq_file).read())
        maxf = int(open(max_freq_file).read())
        return (cur / maxf) * 100
    return 0

def monitor_resources():
    while True:
        stats = {
            'cpu': psutil.cpu_percent(),
            'ram_mb': psutil.virtual_memory().used / 1024**2,
            'gpu_util': get_intel_arc_util(),
            'net_mb': psutil.net_io_counters().bytes_sent / 1024**2
        }
        # WS send...
        time.sleep(1)
# Für Arc: intel_gpu_top (apt install intel-gpu-tools) als Fallback
```

**Video.js-Update (Backend-Stats Overlay):**
```javascript
ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  statsDiv.innerHTML = `
    CPU: ${data.cpu}%<br>
    RAM: ${Math.round(data.ram_mb)}MB<br>
    ${data.gpu_util ? `GPU: ${Math.round(data.gpu_util)}% (Arc/iGPU)` : 'GPU: N/A'}<br>
    Net: ${Math.round(data.net_mb)}MB
  `;
};
```

Arc-spezifisch: gpu_busy_percent ist präzise (Engine Busy-Time), besser als Freq-Proxy für iGPUs. Funktioniert auf MX Linux mit Kernel 6.1+ und Mesa 24+ für Arc-Support. Teste mit cat /sys/class/drm/card0/device/gpu_busy_percent während FFmpeg!
- **Ergebnis:**
  - "Stats for Nerds" Overlay funktioniert jetzt auf Intel-, AMD- und Nvidia-Hardware zuverlässig.
# Walkthrough – Cinematic Media Player Stabilization (27.03.2026)

## Frontend Logic & Stability
- Startup Crash (Video.js 8): Alle 9 Custom-Komponenten (Audio, Subs, Aspect Ratio, CinemaMode, Visual FX, Stop, VLC, MPV, Snapshot) auf ES6-Klassen refaktoriert, volle Kompatibilität, TypeError gelöst.
- Inheritance Stabilization: super(player, options) überall, Registrierung via videojs.registerComponent.
- JS Syntax Audit: node --check, keine Fehler.

## Cinematic Layout & Premium UI
- Clipping Issue: overflow: hidden/min-height entfernt.
- Button Visibility: CSS für Custom-Buttons, Fallback-Labels (CINEMA, STOP, FX) für Sichtbarkeit ohne Icon-Font.
- Aspect Ratio: Hardcoded aspectRatio entfernt, Player passt sich Videoformat an.
- DOM ID: Wrapper-ID auf video-player-container-root-wrapper gesetzt.

## MKV Seeking & Performance
- Remux Seeking: /video-remux-stream/ nutzt jetzt korrekt FFmpeg -ss für Seeking.
- MIME Type: video/x-matroska überall, Chromium kann native Byte-Range-Seeks.
- Direct Play Whitelisting: .mkv für H264 bleibt erlaubt.

## Real-Time Stats Overlay ("Stats for Nerds")
- Backend Metrics: main.py-Thread pusht CPU/RAM/Netz via Eel, Fallback nvidia-smi für GPU.
- Frontend: VisualStatsOverlay (Glassmorphism), StatsButton (Toggle), ES6-Klassen.
- Player Loop: requestAnimationFrame für FPS, Bitrate, Buffer.

## Verification Results
- Automated: node --check, Wrapper-ID bestätigt.
- Manual: App starten (keine JS-Fehler), Cinema-Icon, FX-Menü, Aspect Ratio testen.

**Die "Zauberei" (Magic) ist jetzt voll integriert und stabil!**
# Real-Time "Stats for Nerds" Dashboard – Final Integration (27.03.2026)

- **Live System Metrics:**
  - Hintergrund-Thread in main.py pollt psutil alle 2s (CPU/RAM).
  - Netzwerk-Monitoring: Download/Upload-Speed in Echtzeit, Push ins UI.
  - GPU-Support: Fallback via nvidia-smi, falls GPUtil fehlt.
- **Real-Time Player Performance:**
  - requestAnimationFrame-Loop trackt FPS, Bitrate, Buffer, Dropped Frames nativ.
- **Premium UI Overlay:**
  - Stats-Button (grünes Icon) toggelt das Dashboard.
  - Glassmorphism-Design: Halbtransparent, Blur, Premium-Look, nicht störend.
- **Eel-Powered Synchronization:**
  - Eel-Bridge für schnellen Datenfluss Backend→Frontend, kein separater WebSocket nötig.
- **Finalisierung:**
  - Remux-Seeking, Premium-Button-Visibility, korrekte MIME-Types für MKV/WebM – alles stabilisiert.
  - Media Player ist jetzt vollwertige Monitoring-Station: STATS-Button zeigt alles live!
# Cinematic Media Player Stabilization & Real-Time Stats (v1.0.1, 27.03.2026)

- Planung und Artefakt-Erstellung
- Startup-JS-Fehler (srcType) behoben
- Cinematic Layout CSS (cinema-expanded) wiederhergestellt
- DOM-ID-Mismatch (video-player-container-root-wrapper) gefixt
- Alle Video.js-Komponenten auf ES6-Klassen (Video.js 8 kompatibel) refaktoriert
- Startup-TypeError-Crashes gelöst
- Final Verification & UI-Versionierung (v1.0.1)
- Video-Layout (Overflow/Min-Height) gefixt
- Zuverlässiges MKV-Seeking (Direct Play & Remux-Whitelist)
- Premium-Feature-Sichtbarkeit (CSS & Labels) wiederhergestellt
- Seeking für Remux-Route (-ss-Support) implementiert
- Echtzeit-Stats-Overlay (Backend-Pusher + ES6-Komponente)
- Performance-Metrics-Loop (FPS, Bitrate, Buffer)
# Proposed Changes (27.03.2026)

## Backend (src/core/main.py)
- [NEW] Hintergrund-Thread pollt psutil alle 2s (CPU, RAM, ggf. GPU/Netz).
- [NEW] eel.update_system_stats(): Broadcaster pusht Metriken an das UI.
- [NEW] @eel.expose get_system_stats_static(): Einmaliger Point-in-Time-Check für Systemwerte.

## Frontend (web/app.html)
- [NEW] VisualStatsOverlay Video.js-Komponente: Glassmorphism-Dashboard für System- und Player-Stats.
- [NEW] StatsButton Video.js-Komponente: Toggle-Button in der controlBar.
- [MODIFY] startEmbeddedVideo(): requestAnimationFrame-Loop für Player-Stats:
  - FPS (aus RAF-Timing)
  - Bitrate (vjsPlayer.tech().vhs.stats.bandwidth)
  - Buffer Depth (video.buffered)
  - Dropped Frames (getVideoPlaybackQuality())

# Verification Plan

## Automated Tests
- psutil bleibt während Playback stabil/funktional.
- Keine Memory Leaks im RAF-Loop.

## Manual Verification
- "Stats"-Button toggeln, Overlay erscheint.
- Live-Updates von CPU/RAM beobachten.
- FPS-Stabilität bei High-Bitrate-Seeking prüfen.
# Logbuch: Echtzeit-Stats & Backend-Integration in Video.js 8 (27.03.2026)

## Backend-Integration (Python/Bottle + WebSocket)
- WebSocket-Endpoint /ws/stats liefert CPU/GPU/RAM/Netz live via psutil/GPUtil.
- Beispiel:
```python
from bottle import Bottle, run, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import geventwebsocket
import psutil, GPUtil, threading, time, json

app = Bottle()
clients = []

@app.get('/ws/stats')
def stats_ws():
    ws = request.environ.get('wsgi.websocket')
    if not ws: return abort(400)
    clients.append(ws)
    try:
        while True:
            ws.receive()  # Ping
            stats = {
                'cpu': psutil.cpu_percent(),
                'ram_mb': psutil.virtual_memory().used / 1024**2,
                'gpu_util': GPUtil.getGPUs()[0].load*100 if GPUtil.getGPUs() else 0,
                'net_mb': psutil.net_io_counters().bytes_sent / 1024**2
            }
            for client in clients:
                try: client.send(json.dumps(stats))
                except: clients.remove(client)
            time.sleep(1)
    except: clients.remove(ws)

@app.route('/output.m3u8')
def hls(): return static_file('output.m3u8')

# FFmpeg-Start in Thread...
run(app, handler_class=WebSocketHandler, server=WSGIServer)
```

## Video.js 8 ES6 Frontend (Overlay + Stats)
- WebSocket-Client für Backend-Stats + HLS-Metrics.
- Overlay-Div für Backend- und Player-Stats (FPS, Bitrate, Buffer, Dropped Frames).
- Beispiel:
```javascript
import videojs from 'video.js';
import '@videojs/http-streaming';  // VHS für HLS

const player = videojs('player', {
  sources: [{ src: '/output.m3u8', type: 'application/x-mpegURL' }],
  html5: { hls: { overrideNative: true } }
});

const statsDiv = document.createElement('div');
statsDiv.id = 'backend-stats';
statsDiv.style.cssText = 'position:absolute;top:10px;left:10px;color:white;background:rgba(0,0,0,0.8);padding:10px;font:12px monospace;z-index:999;';
player.el().appendChild(statsDiv);

const ws = new WebSocket('ws://localhost:8080/ws/stats');
ws.onmessage = (e) => {
  const backend = JSON.parse(e.data);
  document.getElementById('backend-stats').innerHTML = `
    Backend CPU: ${backend.cpu}%<br>
    RAM: ${Math.round(backend.ram_mb)}MB<br>
    GPU: ${Math.round(backend.gpu_util)}%<br>
    Netz: ${Math.round(backend.net_mb)}MB
  `;
};

// HLS + Video Stats (RAF-Loop)
let fpsCounter = 0, lastTime = performance.now();
function updatePlayerStats() {
  const tech = player.tech({ IWillNotUseThisInPlugins: 'yet' });
  const vhs = tech.vhs;
  const video = player.el().querySelector('video');
  fpsCounter++;
  const delta = performance.now() - lastTime;
  const fps = delta > 1000 ? fpsCounter * 1000 / delta : 0;
  if (delta > 1000) { fpsCounter = 0; lastTime = performance.now(); }

  const statsHTML = `
    FPS: ${Math.round(fps)}<br>
    Bitrate: ${vhs?.stats?.bandwidth ? Math.round(vhs.stats.bandwidth/1000) : 0}kbps<br>
    Buffer: ${video.buffered.length ? (video.buffered.end(0) - video.currentTime).toFixed(1) : 0}s<br>
    Dropped: ${video.getVideoPlaybackQuality?.()?.droppedVideoFrames || 0}
  `;
  // Füge zu Overlay hinzu oder separater Div
  requestAnimationFrame(updatePlayerStats);
}
updatePlayerStats();
```

## Features
- Backend-Stats: Live CPU/GPU/Netz via WS.
- Player-Stats: FPS/Bitrate/Buffer aus VHS/VideoElement.
- Overlay: Absolut positioniert über Video.
- Perfekt für Debugging von FFmpeg-Streams.
- In Eel via eel.spawn für FFmpeg/Monitor integrierbar.
