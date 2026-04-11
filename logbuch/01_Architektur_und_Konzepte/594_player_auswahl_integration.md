# Logbuch: Player-Auswahl & Integration – Backend/Frontend

## Datum
16. März 2026

---

## Übersicht: Mögliche Player für Media Web Viewer

### 1. Chrome Native (HTML5 <video>)
- MP4/H.264, WebM/VP9, HLS (MediaMTX, ffmpeg HLS)
- Vorteile: 0–5% CPU, mobilfähig, Seeking, keine Zusatztools nötig
- Limitation: Kein ISO/DVD, keine exotischen Codecs

### 2. MediaMTX (HLS/WebRTC)
- Universell, alle Formate via ffmpeg
- HLS: Browser-nativ, Seeking, stabil
- WebRTC: Ultra-low-latency, ideal für Live/Instant-Playback

### 3. ffmpeg-basierte Streams
- FragMP4 (HTTP Range, Seeking, browserkompatibel)
- HLS-Server (playlist.m3u8, .ts-Chunks)
- Vorteil: Keine VLC-Abhängigkeit, flexibel

### 4. VLC (cvlc/extern/embedded)
- Für alle Formate, ISO/DVD, Menüs, Hardware-Decoding
- Desktop-only, höhere CPU, nicht mobil

### 5. Externe Tools/Player
- mpv, PotPlayer, MPC-HC: Über Custom-URL/Kommandozeile
- Vorteil: Maximale Codec-Kompatibilität, Power-User-Features

---

## Empfehlung für Integration
- Standard: Chrome Native + MediaMTX (HLS/WebRTC) für 99% aller Fälle
- Spezialfälle: VLC/extern für ISO/DVD, exotische Codecs, Power-Features
- Optional: mpv/MPC-HC als „Öffnen mit“-Option für fortgeschrittene Nutzer

---

## Architektur
- Backend kann alle Player flexibel mappen (API, Routing)
- Frontend bietet Dropdown/Context-Menü für Player- und Moduswahl
- Automatische Fallback-Logik (ffprobe, Kompatibilitätscheck)

---

*Siehe vorherige Logbuch-Einträge für Details zu MediaMTX, ffmpeg, VLC und Smart-Modus.*

---

## Video.js (De facto Standard)

```html
<script src="https://vjs.zencdn.net/8.6.1/video.min.js"></script>
<link href="https://vjs.zencdn.net/8.6.1/video-js.css" rel="stylesheet">

<video-js id="my-player" class="vjs-default-skin" controls preload="auto" data-setup="{}">
  <source src="/mediamtx/movie.mkv/index.m3u8" type="application/x-mpegURL">
  <p class="vjs-no-js">Browser unterstützt kein Video</p>
</video-js>

<script>
var player = videojs('my-player');
player.play();
</script>
```

**Features:** HLS/DASH/MKV/ISO (via HLS), Theming, Plugins, 1M+ Sites

---

## PlayerJS.com (Online Builder)

```html
<!-- Ein‑File Player (kostenlos) -->
<script src="my-custom-player.js"></script>
<div id="player"></div>
<script>
playerjs.init({
  container: '#player',
  file: '/movie.mp4',
  poster: '/thumb.jpg'
});
</script>
```

**Vorteil:** 500+ Settings, PIP/Chromecast, kein Framework nötig

---

## Plyr (Leicht, Modern)

```html
<script src="https://cdn.plyr.io/3.7.8/plyr.js"></script>
<link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css">

<video id="player" playsinline controls>
  <source src="/direct/movie.mp4" type="video/mp4">
</video>

<script>plyr.setup(document.getElementById('player'));</script>
```

**Klein:** 24kB, YouTube/Vimeo, iOS‑optimiert

---

## Eel‑Optimierte Integration

**Video.js + Eel (Empfohlen)**

```python
# Python Backend
@eel.expose
def get_stream_url(file):
    return f"http://localhost:8888/{file}/index.m3u8"
```

```js
// Eel Frontend
eel.get_stream_url(file)().then(url => {
  player.src({src: url, type: 'application/x-mpegURL'});
  player.play();
});
```

**PlayerJS.com (Zero‑Config)**

```html
<!-- Custom Player herunterladen -->
<script src="./my-player.js"></script>
<script>
player.start({
  file: eel.selected_file()(),
  poster: '/thumb.jpg',
  pip: true
});
</script>
```

---

## Vergleich für dein Setup

| Player    | Größe | HLS | WebRTC | Theming | Eel‑Ease |
|-----------|-------|-----|--------|---------|----------|
| Video.js  | 250kB | ✅  | Plugin | Voll    | ⭐⭐⭐⭐⭐   |
| PlayerJS  | 50kB  | ✅  | ✅     | Builder | ⭐⭐⭐⭐    |
| Plyr      | 24kB  | ✅  | ❌     | Gut     | ⭐⭐⭐     |
| Native    | 0kB   | HLS | ❌     | Nein    | ⭐⭐      |

---

## Schnellstart: Video.js in Eel

```html
<!-- web/index.html -->
<!DOCTYPE html>
<html>
<head>
  <link href="https://vjs.zencdn.net/8.6.1/video-js.css" rel="stylesheet">
</head>
<body>
  <video-js id="video-player" class="vjs-big-play-centered" controls preload="auto" width="800" height="450">
    <p>Video lädt...</p>
  </video-js>
  
  <script src="https://vjs.zencdn.net/8.6.1/video.min.js"></script>
  <script src="eel.js"></script>
  
  <script>
    var player = videojs('video-player');
    
    eel.on_video_selected((file) => {
      player.src({
        src: `http://localhost:8888/${file}/index.m3u8`,
        type: 'application/x-mpegURL'
      });
      player.play();
    });
  </script>
</body>
</html>
```

---

**Fazit:**
Video.js ist perfekt für dein Backend (MediaMTX HLS) + Chrome. PlayerJS wenn du custom Design willst.

Welchen testen? Video.js Demo?
