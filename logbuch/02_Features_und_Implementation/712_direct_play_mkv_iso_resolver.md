- **MKV**: direkt in `get_play_source` prüfen, ggf. einmalig nach MP4 remuxen, dann über `/direct` ausliefern.  
- **ISO**: einmalig die Hauptspur als MP4/MKV in einen Cache extrahieren → danach exakt denselben Weg wie MKV/MP4 durch deine Direct‑Play/HLS‑Logik.

---

## 🧭 Routing-Empfehlung: Browser vs. VLC

Die „nächstbeste“ Variante ist, ISO/MKV gar nicht erst für den Browser aufzubereiten, sondern sie im VLC‑Pfad zu lassen und nur „normale“ MP4/HLS durch den Direct‑Play‑Pfad zum video.js‑Player zu schicken.

**Sinnvolle Priorität für playVideo():**

**1. Chrome / video.js Direct Play (Browser‑Pfad)**

- Nur wenn Datei bereits client‑kompatibel ist: z.B. MP4 + H.264 + AAC.
- Pfad: `is_direct_play_capable(...)` → `/direct/...` (Range‑Streaming), sonst Fallback HLS.

**2. „Nächstbeste“ für komplexe MKV/ISO: VLC‑Familie statt Browser**

- MKV mit PGS‑Subs, TrueHD, HDR, oder komplette DVD/BD‑ISO:
    - Nicht mehr versuchen, diese in MP4/HLS zu pressen,
    - sondern direkt im VLC‑Modus öffnen:
        - ISO: `eel.vlc_bluray(item.path, 'iso')`
        - MKV: `eel.open_in_vlc(item.path)` / cvlc / pyvlc.
- Vorteil: volle Menü‑/Kapitel‑Unterstützung, alle Tonspuren/Untertitel, keine Zusatz‑CPU im Backend.

**3. Wenn du doch Browser‑Integration für ISO/MKV willst**

- Erstversuch (beste Variante): Hauptfilm aus ISO/MKV einmalig per FFmpeg als MP4 in Cache remuxen, dann wie Punkt 1 über /direct bzw. HLS in video.js.
- Nächstbeste dazu: ISO/MKV komplett im VLC‑Tab behandeln und im Browser‑Tab nur „einfache“ Fälle (MP4/HLS) anzeigen.

**Kurz:**

- **Browser‑Tab (video.js)** = MP4/HLS‑Welt mit Direct Play/HLS.
- **VLC‑Tab** = „alles andere“ (aufwändige MKVs, ISOs, Blu‑ray), ohne sie für den Browser zu verbiegen.
# 🟢 Direct Play: MKV/ISO → Browserfähiger Pfad

**Fehlender Schritt:** Aus MKV/ISO erst einen „browserfähigen Play‑Pfad“ machen und DEN dann durch die Direct‑Play‑Pipeline schicken. MKV kann oft direkt, ISO nie – die musst du vorher auflösen.

---

## 1. MKV → Direct‑Play‑Pfad

Für ein Library‑Item `item` mit `item.path` auf SMB:

- `full_path = /mnt/smb/media + item.path`
- ffprobe‑Check: ist es schon `mp4 + h264 + aac` → direkt `/direct/<relpath>`
- Wenn **Container = mkv, Codecs kompatibel**:
  - Option A: trotzdem remux zu MP4 (für saubere Browser‑Kompatibilität).
  - Option B: `/direct` kann auch `video/x-matroska` liefern, wenn du nur Desktop‑Browser zielst.

**Backend‑Skizze:**

```python
@eel.expose
def get_play_source(item_path, client='browser'):
    full = os.path.join(MEDIA_ROOT, item_path)

    if is_direct_play_capable(full, client):
        # MKV oder MP4, aber direkt abspielbar → Direct Play
        return {'mode': 'direct', 'src_path': item_path}

    # Nicht direkt: erst Remux nach MP4
    mp4_path = remux_to_mp4_cache(full)  # z.B. /var/cache/mp4/<hash>.mp4
    rel = os.path.relpath(mp4_path, MEDIA_ROOT)
    return {'mode': 'direct', 'src_path': rel}
```

Die Flask‑Route `/direct/<rel>` bleibt wie vorher; sie sieht nur Dateipfade, egal ob Original‑MKV oder MP4‑Remux.

---

## 2. ISO → „abspielbare Datei“ → Direct Play

Browser können **kein ISO mounten**, also musst du **vorher eine abspielbare Datei extrahieren** und die wieder wie oben behandeln.

**Pattern:**

```python
ISO_CACHE = "/var/cache/iso_main"

def extract_main_from_iso(iso_path):
    """
    ISO (DVD/BD) → eine MKV/MP4 im Cache.
    Du kannst hier deinen vorhandenen Hauptfilm-Detector nutzen.
    """
    os.makedirs(ISO_CACHE, exist_ok=True)
    base = os.path.splitext(os.path.basename(iso_path))[0]
    out = os.path.join(ISO_CACHE, base + ".mp4")

    if os.path.exists(out):
        return out

    # Einfacher Ansatz: Title 1 kopieren (DVD) / längste Spur (BD)
    cmd = [
        "ffmpeg",
        "-i", iso_path,
        "-map", "0:v:0?", "-map", "0:a:0?",
        "-c", "copy",
        "-movflags", "+faststart",
        out
    ]
    subprocess.run(cmd, check=True)
    return out
```

Und dann im selben Resolver:

```python
@eel.expose
def get_play_source(item_path, client='browser'):
    full = os.path.join(MEDIA_ROOT, item_path)

    if full.lower().endswith('.iso'):
        playable = extract_main_from_iso(full)
        rel = os.path.relpath(playable, MEDIA_ROOT)
        # ab hier wie bei MKV/MP4 weiter
        if is_direct_play_capable(playable, client):
            return {'mode': 'direct', 'src_path': rel}
        else:
            # z.B. HLS aus dem extrahierten File erzeugen
            playlist = start_hls_job(playable)
            return {'mode': 'hls', 'src_path': playlist}

    # MKV/MP4/etc.
    ...
```

---

## 3. Einhängen im Player

Im JS ändert sich wenig, du verwendest nur zusätzlich `src_path`:

```js
async function playItem(item) {
    const info = await eel.get_play_source(item.relpath, 'browser')();
    if (info.mode === 'direct') {
        player.src({
            src: `/direct/${info.src_path}`,
            type: 'video/mp4'
        });
    } else if (info.mode === 'hls') {
        player.src({
            src: info.src_path,
            type: 'application/x-mpegURL'
        });
    }
    player.play();
}
```

---


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

---

**Kurz gesagt:**

- **MKV**: direkt in `get_play_source` prüfen, ggf. einmalig nach MP4 remuxen, dann über `/direct` ausliefern.  
- **ISO**: einmalig die Hauptspur als MP4/MKV in einen Cache extrahieren → danach exakt denselben Weg wie MKV/MP4 durch deine Direct‑Play/HLS‑Logik.
