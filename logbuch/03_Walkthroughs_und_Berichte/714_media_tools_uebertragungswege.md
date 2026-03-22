## mpv & mpv.js – Externer Power-Player & Canvas-Engine

**mpv** ist der „VLC für Nerds“: ein extrem schlanker, skriptbarer Player, der intern auf FFmpeg aufsetzt und bei Bildqualität, Sync und Steuerbarkeit führend ist.

### 1. Desktop-Client / externes mpv

- **Integration:**
  - Wie bei VLC: Das Backend startet `mpv file.mkv` oder `mpv rtsp://...` und steuert den Player über das IPC-Socket (JSON-RPC).
  - Steuerung/Automatisierung: Über das IPC-Socket kann das Backend Play, Pause, Seek, Filter, Profile, HDR-Tonemapping etc. per JSON-RPC setzen.
  - Vorteil: Sehr gute Scriptbarkeit (Lua/JS), präzise Filterkontrolle, exzellentes HDR-Tonemapping, Profile, Audio/Video-Sync.
- **UI:**
  - In der Video-Tab-UI als weiterer „Externer Player“-Modus (neben VLC/ffplay).
  - Status/Feedback kann über das IPC-Socket zurück ins UI gespielt werden.

**Praxis:**
- mpv ist ideal, wenn du einen mächtigen Desktop-Player im Ökosystem deiner App brauchst.
- Für Power-User und Spezialfälle (z.B. komplexe Filterchains, exotische Codecs, HDR-Workflows).

### 2. Browser-ähnlich / mpv.js

- **mpv.js** bringt die mpv-Engine per WebAssembly oder Node/Electron in den „Browser“ – aber nicht als `<video>`, sondern als Canvas-Renderer.
- **Einsatz:**
  - In Electron/Tauri/Node-GUIs, nicht im klassischen Web-Browser.
  - Volle mpv-Feature-Macht (Filter, Codecs, Profile) direkt im GUI-Teil deiner App.
- **Abgrenzung:**
  - mpv.js ist kein Drop-in-Ersatz für `<video>`/video.js, sondern ein schwergewichtiger Spezialplayer für Desktop-Shells.
  - Im reinen Browser-Tab ist video.js + MP4/HLS deutlich einfacher und kompatibler.

**Kurz:**
- mpv (extern, IPC-gesteuert) ist ein sehr starker Kandidat für Desktop-Clients und Power-User.
- mpv.js lohnt sich vor allem in „Browser-ähnlichen“ Desktop-Shells (Electron, Tauri, eigene GUI), nicht als Ersatz für `<video>` im Web-Browser.

**Integrationsempfehlung:**
- Für klassische Browser-UIs: video.js + MP4/HLS.
- Für Desktop/Power-User: mpv (extern, IPC), optional mpv.js in Electron/Tauri.

// Infos
### Praxisempfehlung: mpv/mpv.js in Bottle/Eel/Vanilla-JS

**Kurz:**
- **Externes mpv: Ja!**
  - mpv lässt sich wie VLC/cvlc als externer Player aus Python/Eel starten und per IPC steuern.
  - Beispiel (Python):

    ```python
    import subprocess, json, os

    MPV_SOCKET = "/tmp/mpv-socket"

    def open_in_mpv(path):
        # mpv mit IPC-Socket starten
        cmd = [
            "mpv", path,
            f"--input-ipc-server={MPV_SOCKET}",
            "--force-window=yes"
        ]
        subprocess.Popen(cmd)

    @eel.expose
    def mpv_command(command, args=None):
        # JSON-RPC an mpv schicken
        msg = {"command": [command] + (args or [])}
        with open(MPV_SOCKET, "w") as sock:
            sock.write(json.dumps(msg) + "\n")
    ```

  - Im JS-UI einfach als weiteren Button/Modus „In mpv abspielen“ anbieten – Integration wie bei VLC.

- **mpv als Test-Client:**
  - Für Smoke-Tests in der Suite kann mpv wie ffplay/VLC genutzt werden (`mpv --no-video file` oder RTSP/HLS).

- **mpv.js im Eel-Frontend: Nein!**
  - mpv.js ist kein normales JS-Plugin wie video.js, sondern braucht spezielle Umgebungen (Electron/Node, Canvas-Rendering).
  - Eel nutzt ein eingebettetes Chromium/WebView – dort ist `<video>` + JS (video.js) der natürliche Weg.
  - Für dein Setup ist video.js + MP4/HLS technisch und vom Aufwand her die beste Lösung.

**Fazit:**
- mpv als externer Player ist für Power-User und Testzwecke sehr gut integrierbar.
- mpv.js ist im klassischen Eel/Bottle/Vanilla-JS-Frontend overkill und nicht zu empfehlen.

// Infos
---

# ▶️ Praxis: video.js-Integration mit Play-Plan & Test-Suite

## 1. HTML/JS-Grundsetup

```html
<link href="https://vjs.zencdn.net/8.6.1/video-js.css" rel="stylesheet" />
<script src="https://vjs.zencdn.net/8.6.1/video.min.js"></script>

<video
  id="videoPlayer"
  class="video-js vjs-default-skin"
  controls
  preload="auto"
  width="100%"
  data-setup="{}">
</video>

<div id="playInfo"></div>
```

```js
// Video.js-Instanz
const player = videojs('videoPlayer', {
  controls: true,
  preload: 'auto',
  fluid: true
});
let currentItem = null;
```

## 2. Anbindung an Backend (Direct vs. HLS)

```js
async function playItem(item) {
  currentItem = item;

  // Backend fragen: Direct Play oder HLS?
  const plan = await eel.get_play_url(item.relpath, 'browser')();

  updatePlayInfo(plan, item);

  if (plan.mode === 'direct') {
    player.src({
      src: plan.url,
      type: 'video/mp4'
    });
  } else if (plan.mode === 'hls') {
    player.src({
      src: plan.url,
      type: 'application/x-mpegURL'
    });
  } else {
    // z.B. „nur VLC möglich“ → in VLC-Tab weiterleiten
    eel.open_in_vlc(item.path)();
    return;
  }

  player.play();
}

function updatePlayInfo(plan, item) {
  const el = document.getElementById('playInfo');
  el.textContent =
    `${item.title} → ${plan.mode.toUpperCase()} (Score: ${plan.quality_score ?? '?'})`;
}
```

## 3. Events: Fehler/Fallbacks

```js
player.on('error', async () => {
  const err = player.error();
  console.warn('video.js error', err);

  // Beispiel: Direct Play ist gescheitert, HLS versuchen
  if (currentItem) {
    const plan = await eel.get_play_url(currentItem.relpath, 'browser')();
    if (plan.mode === 'hls') {
      player.src({ src: plan.url, type: 'application/x-mpegURL' });
      player.play();
    } else {
      // Fallback auf VLC
      eel.open_in_vlc(currentItem.path)();
    }
  }
});

// Optional: Buffering/Loading-Indikator
player.on('waiting', () => { /* Spinner zeigen */ });
player.on('playing', () => { /* Spinner ausblenden */ });
```

## 4. Zusammenspiel mit Test-Suite

```js
async function loadItemDetails(item) {
  const info = await eel.analyze_media(item.relpath)();
  // Infos im UI anzeigen (Codecs, HDR, Direct-Play-fähig, Qualität)
  // und z.B. einen Badge „Direct Play möglich“ oder „wird transkodiert“ einblenden.
}
```

**Fazit:**
- video.js kennt nur zwei Source-Typen: MP4 (Direct Play) und HLS (m3u8).
- Das Backend/Test-Suite entscheidet, welcher Modus pro Item sinnvoll ist.
---

# 🗂️ Matrix: Tools/Protokolle × Player/Usecase

| Tool/Protokoll      | Direct Play (Browser) | HLS (Browser) | VLC-Tab | FFplay-Tab | MediaMTX/RTSP | Py-Player | Download/Export | Discovery (DLNA) |
|---------------------|:---------------------:|:-------------:|:-------:|:----------:|:-------------:|:---------:|:--------------:|:----------------:|
| **ffprobe**         |   ✓ (Analyse)         |   ✓           |   ✓     |     ✓      |      ✓        |     ✓     |       ✓        |        ✓         |
| **mkvmerge**        |   (Sanitize)          | (Sanitize)    |   ✓     |     ✓      |      ✓        |     ✓     |       ✓        |        ✓         |
| **FFmpeg Remux**    |   ✓                   |               |   ✓     |     ✓      |      ✓        |     ✓     |       ✓        |        ✓         |
| **FFmpeg HLS**      |                       |   ✓           |         |     ✓      |      ✓        |           |       ✓        |        ✓         |
| **FFmpeg DASH**     |                       |   (✓)         |         |     ✓      |      ✓        |           |       ✓        |        ✓         |
| **FFmpeg RTSP**     |                       |               |   ✓     |     ✓      |      ✓        |           |                |                  |
| **MediaMTX (mtx)**  |                       |               |   ✓     |     ✓      |      ✓        |           |                |                  |
| **VLC/cvlc/pyVLC**  |                       |               |   ✓     |     ✓      |      ✓        |     ✓     |                |                  |
| **video.js**        |   ✓                   |   ✓           |         |            |               |           |                |                  |
| **nginx/caddy**     |   ✓ (static)          |   ✓ (static)  |         |            |               |           |       ✓        |                  |
| **DLNA/UPnP**       |                       |               |         |            |               |           |                |        ✓         |
| **GStreamer**       |   (Experten)          |   (Experten)  | (✓)     |   (✓)      |    (✓)        |   (✓)     |     (✓)        |      (✓)         |
| **mpv/mpv.js**      |                       |               |   ✓     |     ✓      |      ✓        |           |                |                  |
| **WebRTC (mtx)**    |                       |               |         |            |      ✓        |           |                |                  |

Legende: ✓ = Standardpfad, (✓) = optional/Expertenpfad, leer = nicht üblich

**Hinweis:** Diese Matrix zeigt, welche Tools/Protokolle in welchem Player/Tab/Usecase sinnvoll sind. Sie hilft, alle Pfade und Optionen im Setup übersichtlich zu planen und zu dokumentieren.
---

# 🧪 Multimedia-Test-Suite als Diagnose- und Routingmodul

## 1. Ziele der Suite

Für **jede Quelle** (Datei oder Stream):

- Ist die Datei **formal gültig**? (Container/Streams, keine offensichtliche Korruption)
- Welche **Codecs/Features** hat sie (H.264/HEVC, HDR, TrueHD, PGS, Channels, Chapters)?
- Was ist der **leichteste gültige Abspielpfad**? (Direct Play, HLS, RTSP/mtx)
- Lohnt sich ein **Remux** oder ist ein „Rohrbruchkandidat“?
- Optional: kurzer **Playback-Smoke-Test** (ffplay/VLC)

Am Ende kommt ein JSON raus, aus dem Routing und UI alles ableiten können.

## 2. Kernmodule und Aufgaben

### a) Analyse-Modul (ffprobe)
- Einmaliger Call: `ffprobe -show_format -show_streams -print_format json`
- Extrahiert: Container, Streams, Codecs, HDR, Chapters, Tags
- Leitet ab: direct_play_browser, is_heavy_mkv, has_subs, has_chapters, quality_score

### b) Sanitize-Modul (mkvmerge, optional)
- Nur bei MKV und nur, wenn Analyse „komisch“ aussieht
- `mkvmerge -o fixed.mkv src.mkv` – keine Re-Encodes, nur Container-Fix
- Danach laufen alle weiteren Tests gegen `fixed.mkv`

### c) Transform-Tests (FFmpeg)
- **Remux-Test**: MKV/ISO→MP4 (Direct-Play-Kandidat)
- **HLS-Test**: HLS aus Quelle
- **RTSP/mtx-Test** (optional): Publish + Probe

### d) Playback-Smoke-Tests (ffplay / VLC)
- 3–5 s Test: `ffplay -autoexit -t 5 file` oder HLS/RTSP
- Nur um grobe Korruption/Fehler zu entdecken

## 3. Beispiel: vereinheitlichte Antwort der Suite

```json
{
  "source": "/mnt/smb/media/Movies/Avatar/Avatar.mkv",
  "analysis": {
    "container": "matroska",
    "duration_min": 162.3,
    "video": { "codec": "hevc", "res": "3840x2160", "hdr": true },
    "audio": [
      { "codec": "truehd", "ch": 8, "lang": "de" },
      { "codec": "dts", "ch": 6, "lang": "en" }
    ],
    "subs": 2,
    "chapters": 24
  },
  "quality_score": 94,
  "tests": {
    "remux_ok": false,
    "hls_ok": true,
    "rtsp_ok": true,
    "ffplay_smoke_ok": true
  },
  "flags": {
    "direct_play_browser": false,
    "prefer_vlc": true
  },
  "derived_paths": {
    "fixed_mkv": "/var/cache/fixed/abc123.mkv",
    "test_hls": "/tmp/hls_test/abc/index.m3u8"
  }
}
```

## 4. Wie dein Player das nutzt

- **Browser-Tab (video.js):**
  - Wenn `direct_play_browser` und `remux_ok`: Direct Play mit Remux-MP4
  - Sonst, wenn `hls_ok`: HLS-Pfad verwenden
  - Sonst: in UI kennzeichnen „nur VLC-Modus“
- **VLC-Tab:**
  - Wenn `prefer_vlc`: direkt Datei bzw. ISO im VLC öffnen
  - Optional RTSP-Pfad über mtx
- **Py-Player-Tab:**
  - Nur, wenn Datei/Codec-Kombination pyVLC/pyvidplayer-kompatibel

Die Test-Suite bleibt ein einzelner Backend-Entry-Point (z.B. `analyze_media(path)`), alles andere hängt sich nur an das JSON-Ergebnis dran – so bleibt die Logik zentral und wartbar.
---

# 🏗️ Schichtenmodell: Der perfekte Player (Analyse, Routing, Pfade)

## 1. Ziele und Grundprinzip

- **Direct Play, wo immer möglich**: Datei 1:1 zum Client, keine Neukodierung, fast keine Server-CPU.
- **HLS nur für Browser-Streaming**: segmentiert, adaptiv, cache-bar.
- **VLC-Familie für alles „Komplizierte“**: ISO, Blu-ray, exotische Codecs, PGS-Subs, Atmos, Menüs.
- **MediaMTX als optionaler Streaming-Hub** (RTSP/WebRTC) für VLC/ffplay/Spezialfälle.
- **Test-Suite davor**: nie „blind“ abspielen, jede Datei wird geprüft.

## 2. Storage-Layer

- Alles physisch auf SMB, Backend arbeitet mit lokalen Mounts (`/mnt/smb/...`).
- Cache-Dirs für Artefakte: `/var/cache/mp4/`, `/var/cache/hls/<hash>/`, `/var/cache/iso_main/`.

## 3. Analyse- & Test-Suite-Layer

- Zentrale Funktion: `analyze_media(path)`
  - ffprobe: Container, Streams, Codecs, HDR, Subs, Chapters
  - Regeln: `can_direct_play_browser`, `is_heavy_mkv`, `is_iso`
  - Optionale Smoke-Tests: ffplay, mkvmerge-Sanitizing
- Ergebnis: JSON-Blob für Routing-Layer

## 4. Routing-Engine im Backend

- Zentrale Funktion: `get_play_plan(item, client)`
  - Input: Item, Client-Typ
  - Steps:
    1. Analyse
    2. ISO/BD: Hauptfilm extrahieren
    3. Playable bestimmen
    4. Routing nach Client/Analyse
- Rückgabe: Play-Plan-Objekt (mode, url, quality_score, notes)

## 5. Backend-Übertragungswege

### Direct-Play-Pfad (Browser)
- `/direct/<relpath>`: Range-fähig, für MP4-Remuxe/kompatible MKVs

### HLS-Pfad (Browser)
- `ensure_hls(source)`: HLS-Ordner mit Playlist+Segmenten
- `/hls/<hash>/index.m3u8`, Segmente statisch

### VLC/MediaMTX-Pfad
- ISO/BD: `vlc bluray:///...`
- RTSP: FFmpeg → mtx → VLC/ffplay

### mkvmerge-Pfad (optional)
- Problematische MKVs vorab sanieren

## 6. Frontend: Video-Player-Tab

- Mode-Selector: Chrome Native, Video.js, VLC, FFplay, MTX/RTSP, Expert-Modi
- Hauptplayer: video.js, setzt src/type nach Play-Plan
- VLC-Panel: Drag&Drop, Playlist, RTSP
- Py-Player-Panel: pyVLC/pyvidplayer
- Status/Test-Panel: zeigt Modus, Qualität, Analyse

## 7. Zusammenarbeit mit der Test-Suite

- Beim Öffnen: analyze_media im Hintergrund
- Beim Play: Routing nach Analyse, FFmpeg/HLS/mtx nur bei Bedarf
- Optionale Smoke-Tests/Expert-Buttons

**Fazit:**
- Einheitliche Test/Routing-Schicht
- Mehrere klar getrennte Abspielpfade (Direct, HLS, VLC/RTSP, Py-Player)
- Video-Tab orchestriert, implementiert aber keine Medienlogik selbst
## MediaMTX (mtx) – Streaming-Server/Transport-Hub

MediaMTX (früher rtsp-simple-server) ist ein eigenständiger Streaming-Server, der perfekt zwischen Backend und VLC/ffplay/Browser sitzt.

- **Eingänge:**
  - RTSP (FFmpeg, IP-Kameras)
  - RTMP, WebRTC, SRT, MPEG-TS/UDP (je nach Config)
- **Ausgänge:**
  - RTSP (für VLC/ffplay)
  - RTMP, WebRTC, HLS (je nach Config)

**Transport-Hub-Workflow:**

- **Backend:**
  - `ffmpeg -re -i file.mkv -c copy -f rtsp rtsp://localhost:8554/movie`
  - mtx nimmt den Stream an und hält ihn verfügbar.
- **Client:**
  - VLC: `vlc rtsp://server:8554/movie`
  - ffplay: `ffplay rtsp://server:8554/movie`
  - (optional) Browser/WebRTC: mtx-WebRTC-Endpoint

**Rolle in App/Test-Suite:**
- Alternative zum HLS-Pfad für alles, was du mit VLC/ffplay abspielen willst (High-Bitrate, exotische Codecs, ISO/BD)
- In der Test-Suite: Pfad „FFmpeg → mtx (RTSP) → ffplay/VLC“ als eigener Test:
  - klappt Publish?
  - kann ffplay/VLC den RTSP-Stream stabil öffnen?

**Fazit:**
MediaMTX ist kein Player, sondern ein kleiner Streaming-Server, den du über FFmpeg „fütterst“ und über VLC/ffplay oder Browser/WebRTC „anzapfst“.
**Kurz gesagt:**

- **MKV**: direkt in `get_play_source` prüfen, ggf. einmalig nach MP4 remuxen, dann über `/direct` ausliefern.  
- **ISO**: einmalig die Hauptspur als MP4/MKV in einen Cache extrahieren → danach exakt denselben Weg wie MKV/MP4 durch deine Direct‑Play/HLS‑Logik.
# 🗂️ Media-Tool-Überblick: Übertragungswege & App-Integration

Fokus: SMB-Storage → Python-Backend → Video-Tab (Chrome/video.js/VLC/ffplay/mtx etc.)

---

## ffprobe – nur Analyse
- **Rolle:** Metadaten & Qualitäts-Check, keine Übertragung selbst.
- **Input:** Datei (MKV, MP4, ISO, M2TS, HLS-Playlist, RTSP-URL)
- **Output:** JSON mit Streams, Dauer, Bitraten, HDR, Subs, Chapters
- **Nutzung:**
  - Vor jedem Play/Routing
  - Vor jedem FFmpeg-Job
  - Für quality_score, direct_play_* Flags

---

## mkvmerge – Container-Tool
  1. File → File (MKV → MKV):
     - Vor FFmpeg, wenn ffprobe/Tests auf kaputte Timecodes/Streams hinweisen
     - In Test-Suite als optionaler „Sanitizer-Step“
  2. File → Pipe (optional):
     - Für Expertenfälle, selten im UI

**Detail:**

- mkvmerge **re-encodiert nie** Audio oder Video, sondern multiplexed/remuxt nur Streams in/aus MKV.
- Standard: alle Tracks (Video, Audio, Subs, Attachments) werden 1:1 übernommen, außer du schließt sie explizit per `--no-*` oder Track-Selektion aus.
- **Optionale Bitstream-Eingriffe:**
  - `--reduce-to-core` (DTS): nur lossy-Core übernehmen
  - `--fix-bitstream-timing-information` (H.264/H.265): Timing-Info angleichen
  - `--compression TID:none`: Kompression für Header/Tracks steuern
- Für „verlustfreie Bitstream-Weitergabe“ ist mkvmerge die passende Stelle: MKV→MKV = Bitstream-Passthrough mit sauberem Container.
- Für HLS/MP4/Transcode ist dann FFmpeg zuständig (`-c copy` vs. Transcode).

---

## FFmpeg – Remux, Transcode, HLS, RTSP
- **1. Datei-Pfad (Remux/Transcode):**
  - Input: MKV/MP4/ISO/M2TS
  - Output: MP4 (Direct Play), MKV, M3U8+TS (HLS)
  - Nutzung: copy-mp4 für Chrome Direct Play, ISO→MP4/MKV
- **2. HTTP/HLS-Pfad:**
  - Output: HLS-Ordner (index.m3u8 + Segmente)
  - Transport: HTTP GET (nginx/Flask static)
  - Nutzung: video.js-Modus (Browser-Streaming)
- **3. RTSP-Pfad:**
  - Output: RTSP-Stream
  - Transport: FFmpeg → -f rtsp rtsp://mtx:8554/stream
  - Nutzung: RTSP-Quelle für MediaMTX, VLC/ffplay/WebRTC

---

## VLC / cvlc / pyVLC – Player & (leicht) Server
- **1. Datei-Direct-Play:**
  - Input: Dateipfad (MKV, MP4, ISO, BDMV, DVD/BD)
  - Transport: lokal
  - Nutzung: ISO/BD-Menüs, alles was nicht in Browser/HLS soll
- **2. HTTP/RTSP-Streaming aus VLC:**
  - Output: HTTP/RTSP-Stream
  - Nutzung: Expertenfall, VLC-Tab
- **3. pyVLC:**
  - Input: Dateipfad/URL
  - Transport: intern (GUI/Window)
  - Nutzung: Py-Player-Tab, Test-Suite-Status

---

## MediaMTX (mtx) – RTSP/RTMP/WebRTC-Server
- **1. Publish:**
  - FFmpeg → rtsp://mtx:8554/stream
  - RTSP-Kamera → MediaMTX
- **2. Consume:**
  - VLC/ffplay: rtsp://mtx:8554/stream
  - Browser: WebRTC von MediaMTX
- **Nutzung:**
  - RTSP-Pfad-Test, Streaming-Modus im Video-Player-Tab

---

## FFplay – reiner Client/Tester
- **Rolle:** CLI-Player für Tests
- **Eingänge:** Datei, HLS, RTSP
- **Nutzung:** Smoke-Tests, RTSP/HLS-Validierung

---

## video.js – Browser-Player
- **1. Progressive/Direct Play:**
  - src: /direct/…, type: video/mp4
  - Flask/nginx liefert MP4 mit Range
- **2. HLS:**
  - src: /hls/<hash>/index.m3u8, type: application/x-mpegURL
  - HLS-Segmente aus FFmpeg, statisch serviert
- **Nutzung:**
  - Immer HTTP-URLs (MP4 oder HLS)

---

## Flask / Backend – Steuer- und IO-Ebene
- **1. Direct-Play MP4:**
  - /direct/<relpath>: Range-fähige Route, liest aus SMB
- **2. HLS:**
  - /hls/<hash>/index.m3u8 + Segmente: static/send_from_directory
- **3. Control-API:**
  - Eel-exposed Funktionen (analyze_media, get_play_url, ensure_hls, open_in_vlc, ...)

---

## Zusammenspiel in der Test-Suite
1. Analyse: ffprobe → analysis + quality_score
2. Sanitizing (optional): mkvmerge → fixed_path
3. Test-Pfade:
   - FFmpeg Remux → MP4 (Direct-Play)
   - FFmpeg HLS → HLS-Pfad (video.js)
   - FFmpeg → MediaMTX (RTSP) → FFplay/VLC
4. Routing-Entscheid:
   - Browser: bevorzugt Direct Play, sonst HLS
   - VLC: Datei direkt oder RTSP von MediaMTX
   - Py: pyVLC/pyvidplayer

---

> Für eine Matrix (Tool × Transport-Methode × Tab) einfach melden!
