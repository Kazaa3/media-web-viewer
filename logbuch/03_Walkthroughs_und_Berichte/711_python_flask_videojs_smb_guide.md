# 🚀 **Python Backend → Video.js Frontend** – ISO/MKV/SMB Complete Guide

**Beste Lösung**: **Flask + Range Requests** (HTTP 206 Partial Content) für **Direct Play** + **FFmpeg HLS** Fallback. Funktioniert mit **SMB**! [edlitera](https://www.edlitera.com/blog/posts/serve-videos-flask-videojs)

## **1. Flask Backend (Python + Eel)**

```python
from flask import Flask, Response, request, abort, send_file
import os
import mimetypes

app = Flask(__name__)

@app.route('/video/<path:filename>')
def stream_video(filename):
    """Direct Play mit Range Requests (ISO/MKV/MP4)"""
    
    # SMB Mount (smb://server/share)
    smb_base = "/mnt/smb/media"  # smb://user@server/share → /mnt/smb/media
    video_path = os.path.join(smb_base, filename)
    
    if not os.path.exists(video_path):
        abort(404, "Video not found")
    
    # Range Requests für Seeking
    range_header = request.headers.get('Range', None)
    file_size = os.path.getsize(video_path)
    
    if not range_header:
        # Full File
        return send_file(video_path, mimetype='video/mp4')
    
    # Partial Content (Seeking)
    byte1, byte2 = parse_range(range_header, file_size)
    data = open(video_path, 'rb').read(byte2 - byte1 + 1)
    
    response = Response(data, 206,
        mimetype='video/mp4',
        headers={
            'Content-Range': f'bytes {byte1}-{byte2}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(byte2 - byte1 + 1)
        }
    )
    return response

def parse_range(range_header, file_size):
    """Range: bytes=0- → bytes=1000000-2000000"""
    match = re.search(r'bytes=(\d+)-(\d*)', range_header)
    byte1 = int(match.group(1))
    byte2 = int(match.group(2)) if match.group(2) else file_size - 1
    return byte1, min(byte2, file_size - 1)

@app.route('/hls/<path:filename>')
def hls_stream(filename):
    """FFmpeg HLS Fallback"""
    smb_path = os.path.join("/mnt/smb/media", filename)
    hls_dir = f"/tmp/hls/{os.path.basename(filename)}"
    
    # FFmpeg HLS on-demand
    cmd = [
        'ffmpeg', '-re', '-i', smb_path,
        '-c:v', 'libx264', '-preset', 'ultrafast',
        '-f', 'hls', '-hls_time', '4', '-hls_list_size', '6',
        f"{hls_dir}/playlist.m3u8"
    ]
    subprocess.Popen(cmd)
    
    return send_file(f"{hls_dir}/playlist.m3u8", mimetype='application/x-mpegURL')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
```

## **2. Video.js Frontend (Eel)**

```html
<video id="videoPlayer" class="video-js vjs-default-skin" 
       controls preload="auto" width="100%" data-setup="{}">
</video>
<script src="https://vjs.zencdn.net/8.6.1/video.min.js"></script>

<script>
const player = videojs('videoPlayer');

// Direct Play (MP4/MKV mit Range Requests)
function playDirect(smbPath) {
    player.src({
        src: `http://localhost:5000/video/${smbPath}`,
        type: 'video/mp4'  // Browser auto-detect
    });
    player.play();
}

// HLS Fallback
function playHLS(smbPath) {
    player.src({
        src: `http://localhost:5000/hls/${smbPath}`,
        type: 'application/x-mpegURL'
    });
}
</script>
```

## **3. Eel Python Bridge**

```python
# main.py (Eel App)

---

## 🔄 Direct Play als Pipeline im Player-Flow

Direct Play ist einfach eine weitere „Abspiel-Pipeline“ im bestehenden `playItem()`-Flow:

### 1. HTML: Player + Item-Liste

```html
<ul id="videoList"></ul>

<!-- Native/Video.js Player -->
<video id="videoPlayer" class="video-js vjs-default-skin" controls preload="auto"></video>

<div id="playInfo"></div>
```

Video.js initialisieren:

```js
const player = videojs('videoPlayer', { controls: true, preload: 'auto' });
let currentItem = null;
```

### 2. Items klicken → `playItem(item)`

Beim Rendern der Item-Liste:

```js
function renderItemList(items) {
    const list = document.getElementById('videoList');
    list.innerHTML = '';
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item.title;
        li.onclick = () => playItem(item);
        list.appendChild(li);
    });
}
```

`item.relpath` ist z.B. `Movies/Avatar/Avatar.mkv`.

### 3. Zentrale Logik: `playItem(item)`

Hier wird Direct Play vs. HLS entschieden:

```js
async function playItem(item) {
    currentItem = item;

    // Backend entscheidet: direct oder hls
    const info = await eel.get_play_url_checked(item.relpath, 'browser')();
    // info = { mode: 'direct' | 'hls', url: '/direct/...' oder '/hls/...', quality: ... }

    updatePlayInfo(info, item);

    if (info.mode === 'direct') {
        // Direct Play: progressive/Range
        player.src({
            src: info.url,
            type: 'video/mp4'
        });
    } else if (info.mode === 'hls') {
        // HLS: Video.js + hls.js
        player.src({
            src: info.url,
            type: 'application/x-mpegURL'
        });
    }

    player.play();
}
```

Damit ist Direct Play komplett im **gleichen Player** integriert – nur die `src` unterscheidet sich.

### 4. UI-Feedback im Video-Player-Tab

Kleines Status-Label, damit du siehst, was passiert:

```js
function updatePlayInfo(info, item) {
    const el = document.getElementById('playInfo');
    const txt = info.mode === 'direct'
        ? `Direct Play: ${item.title} (${info.quality || '?'} Score)`
        : `HLS/Transcode: ${item.title} (${info.quality || '?'} Score)`;
    el.textContent = txt;
    el.className = info.mode === 'direct' ? 'badge badge-success' : 'badge badge-warning';
}
```

Optional: Im Mode-Selector den aktiven Pfad hervorheben („Chrome Native (Direct Play)“ vs. „Video.js (HLS)“).

### 5. Zusammenspiel mit anderen Modi

In deinem bestehenden `switchPlayerMode(mode)` kannst du für Browser-Modi einfach `playItem(currentItem)` wiederverwenden:

```js
async function switchPlayerMode(mode) {
    videoMode = mode;
    // Panels umschalten …

    if (!currentItem) return;

    if (mode === 'chrome-native' || mode === 'videojs') {
        // nutzt intern get_play_url_checked → Direct vs. HLS
        await playItem(currentItem);
    } else if (mode === 'vlc') {
        await eel.open_in_vlc(currentItem.path)();
    } else if (mode === 'ffplay') {
        await eel.ffplay_bluray(currentItem.path, 'direct')();
    }
}
```

So hängt Direct Play „unsichtbar“ unter deinen Browser-Modi, ohne dass du im UI noch einen eigenen Button brauchst – der Video-Player-Tab bleibt gleich, nur der Pfad zu `src` ist smarter.

    """Direct Play über Flask"""
    return f"http://localhost:5000/video/{smb_path}"

@eel.expose
def play_video_hls(smb_path):
    """HLS Stream"""
    return f"http://localhost:5000/hls/{smb_path}"

@eel.expose
def test_suite(smb_path):
    """Pre-Stream Tests"""
    analysis = ffprobe_suite(f"/mnt/smb/media/{smb_path}")
    
    # Quality Gate
    if analysis['quality_score'] > 70:
        return {'ready': True, 'url': play_video_direct(smb_path)}
        return {'ready': False, 'fallback': play_video_hls(smb_path)}

eel.init('web')
app.run()  # Flask + Eel
```

## **4. SMB Mount (automatisch)**

```python
import smbprotocol.connection
from smb.SMBConnection import SMBConnection

def mount_smb(share_url):
    """smb://user:pass@server/share → /mnt/smb"""
    if not os.path.exists('/mnt/smb'):
    subprocess.run(cmd)

# Auto-Mount bei Start
mount_smb('smb://user:pass@nas.local/media')
```

## **5. Kompletter Workflow**

```js
async function playSmart(smbPath) {
    // 1. Test Suite
    const test = await eel.test_suite(smbPath)();
    
    if (test.ready) {
        playDirect(test.url);  // Range Requests
    } else {
        playHLS(test.fallback);  // FFmpeg HLS
    }
}

// Nutzung
playSmart('Movies/Avengers.iso');  // SMB Path!
```

## **Test-Suite Integration**

```python
@eel.expose
def pre_stream_suite(smb_path):
    full_path = f"/mnt/smb/media/{smb_path}"
    
    # ffprobe
    analysis = ffprobe_suite(full_path)
    
    # FFplay Quick
    gpu_ok = test_gpu_decode(full_path)
    
    # FFmpeg Remux Test
    remux_test = ffmpeg_mkv(full_path, 'mkv-mp4')
    
    return {
        'ffprobe': analysis,
        'gpu_ok': gpu_ok,
        'remux_ok': os.path.exists(remux_test),
        'quality': analysis['quality_score']
    }
```

## **Video.js Features**

```js
// Quality Auto-Select
player.ready(() => {
    if (test.quality > 80) {
        player.src({type: 'video/mp4'});  // Direct
    } else {
        player.src({type: 'application/x-mpegURL'});  // HLS
    }
});

// Buffering + Error Handling
player.on('error', () => {
    console.log('Direct failed → HLS Fallback');
    playHLS(smbPath);
});
```

## 🟢 Konkrete Direct Play-Implementierung (mit Quality Gate)

**Ziel:** Wenn Container/Codecs passen, Datei 1:1 via HTTP-Range ausliefern, sonst HLS/Transcode nutzen.

### 1. Voraussetzungen prüfen (Direct-Play-fähig?)

```python
import json, subprocess

def is_direct_play_capable(path, client='browser'):
    # mp4/h264/aac für Chrome/Video.js
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_streams', '-show_format', path
    ]
    info = json.loads(subprocess.check_output(cmd))
    fmt = info['format']['format_name']
    v_streams = [s for s in info['streams'] if s['codec_type'] == 'video']
    a_streams = [s for s in info['streams'] if s['codec_type'] == 'audio']
    if not v_streams or not a_streams:
        return False
    v = v_streams[0]['codec_name']
    a = a_streams[0]['codec_name']
    if client == 'browser':
        return (
            'mp4' in fmt and
            v in ('h264', 'hev1', 'avc1') and
            a in ('aac', 'mp3')
        )
    return True
```

### 2. Flask-Route für Direct Play mit Range

```python
from flask import Flask, request, Response, abort
import os, re

app = Flask(__name__)
MEDIA_ROOT = "/mnt/smb/media"

def iter_file_range(path, start, end, chunk_size=1024*1024):
    with open(path, 'rb') as f:
        f.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            chunk = f.read(min(chunk_size, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
            yield chunk

@app.route('/direct/<path:relpath>')
def direct_play(relpath):
    path = os.path.join(MEDIA_ROOT, relpath)
    if not os.path.isfile(path):
        abort(404)
    file_size = os.path.getsize(path)
    range_header = request.headers.get('Range')
    if range_header:
        m = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not m:
            abort(416)
        start = int(m.group(1))
        end = int(m.group(2) or file_size - 1)
        end = min(end, file_size - 1)
        resp = Response(
            iter_file_range(path, start, end),
            status=206,
            mimetype='video/mp4',
            direct_passthrough=True,
        )
        resp.headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        resp.headers['Accept-Ranges'] = 'bytes'
        resp.headers['Content-Length'] = str(end - start + 1)
        return resp
    else:
        return Response(
            iter_file_range(path, 0, file_size - 1),
            mimetype='video/mp4',
            headers={
                'Content-Length': str(file_size),
                'Accept-Ranges': 'bytes',
            },
            direct_passthrough=True,
        )
```

### 3. Routing im Backend: Direct Play vs. HLS

```python
@eel.expose
def get_play_url(relpath, client='browser'):
    full = os.path.join(MEDIA_ROOT, relpath)
    if is_direct_play_capable(full, client=client):
        return {'mode': 'direct', 'url': f'/direct/{relpath}'}
    else:
        playlist_url = start_hls_job(full)
        return {'mode': 'hls', 'url': playlist_url}
```

### 4. Frontend (video.js) im Video-Player-Tab

```js
const player = videojs('videoPlayer');

async function playItem(item) {
    const info = await eel.get_play_url(item.relpath, 'browser')();
    if (info.mode === 'direct') {
        player.src({
            src: info.url,
            type: 'video/mp4'
        });
    } else if (info.mode === 'hls') {
        player.src({
            src: info.url,
            type: 'application/x-mpegURL'
        });
    }
    player.play();
}
```

### 5. Test-Suite-Integration (Quality Gate)

```python
@eel.expose
def get_play_url_checked(relpath, client='browser'):
    full = os.path.join(MEDIA_ROOT, relpath)
    analysis = ffprobe_suite(full)
    if ffprobe_quality_score(analysis) < 60:
        playlist_url = start_hls_job(full)
        return {'mode': 'hls', 'url': playlist_url}
    if is_direct_play_capable(full, client):
        return {'mode': 'direct', 'url': f'/direct/{relpath}'}
    else:
        playlist_url = start_hls_job(full)
        return {'mode': 'hls', 'url': playlist_url}
```

**Fazit:**
- SMB-Files lokal gemountet
- Flask serviert MP4/H.264/AAC via Range als Direct-Play-Pfad
- Video.js bekommt je nach Analyse `/direct/...` oder eine HLS-Playlist
- Test-Suite/Quality-Gate entscheidet, ob Direct Play angeboten wird

## **SMB + Flask = Perfekt!**

```
smb://nas/media/movie.iso
  ↓ Flask Range Requests
http://localhost:5000/video/movie.iso
  ↓ Video.js Direct Play
<video src="...">  ✅ Seeking, Pause, Fullscreen!
```

**Komplett**: **SMB → Flask → Video.js** mit **Test-Suite** + **HLS Fallback**! 🚀🎥

**Eel Call**: `playSmart("Movies/movie.iso")` → **instant Video Player**! 

**Docker?** Flask + smbclient ready!

---

## ⚠️ Flask + Byte-Range + SMB: Grenzen & Best Practice

Flask-Byte-Range-Streaming über SMB funktioniert für kleine Dateien, skaliert aber bei großen ISO/MKV (>20 GB) und mehreren Nutzern nicht zuverlässig. Die wichtigsten Gründe:

1. **Sync WSGI + lange Streams**: Jeder Stream blockiert einen Worker. Mehrere parallele Nutzer → Worker-Engpass, hohe Latenz.
2. **Naive Range-Implementierung**: Viele Beispiele lesen zu viel (RAM-Problem) oder zu wenig (tausende SMB-Reads, hohe Latenz).
3. **SMB-Latenz**: Jeder `read()` ist ein Netzwerkanruf. Viele kleine Reads → Durchsatz sinkt, Latenz steigt.
4. **Range-Handling muss exakt sein**: Fehlerhafte `Content-Range`/`Accept-Ranges` führen zu Browser-Retries und I/O-Stürmen.
5. **Kein Backpressure/Rate-Limit**: Flask throttelt nicht pro Client. Schnelle Clients können SMB/Netzwerk auslasten.

**Fazit:** Mit einem Nutzer „geht’s irgendwie“, mit mehreren und großen Dateien stößt man schnell an CPU-, Worker- und I/O-Limits.

### Warum HLS-Segmentierung besser skaliert

- **Segmentiertes I/O**: HLS zerlegt große Dateien in kleine `.ts`-Segmente (4–10 s). Server liest sequentiell, Clients fordern keine willkürlichen Ranges.
- **Caching**: Segmente können als statische Dateien (nginx, Caddy, Flask static) ausgeliefert werden. OS-Cache entlastet SMB.
- **Adaptives Streaming**: HLS erlaubt mehrere Qualitätsstufen, Video.js passt sich an die Netzqualität an.
- **Günstige Parallelität**: Viele Clients = viele GETs auf kleine Dateien, kein Worker-Engpass.
- **Test-Suite-Integration**: ffprobe/FFmpeg-Tests laufen einmal pro Quelle, dann wird nur noch die Playlist ausgeliefert.

### Praxis-Architektur für skalierbares Streaming

1. **SMB immer auf dem Server mounten** (CIFS), Backend arbeitet mit lokalen Pfaden (`/mnt/media/...`).
2. **Beim Play-Request:**
    - ffprobe/ffplay-Tests (Quality Gate)
    - Bei Erfolg: FFmpeg HLS-Segmente erzeugen (oder vorhandene nutzen), Playlist-URL an Video.js zurückgeben
3. **HLS über nginx oder Flask static serven** (nicht per-Request-Python-IO)
4. **Flask/Eel nur als Control Plane** (Auswahl, Trigger, Test-Suite, URL-Expose)
5. **Progressive Byte-Range nur als Fallback/Admin** – und dann mit großem Chunking und exaktem Range-Handling

**Empfehlung:** Für wiederholtes, paralleles Streaming großer Medien: HLS-Segmentierung + statischer HTTP-Server. Flask/Eel steuert, aber streamt nicht selbst.
