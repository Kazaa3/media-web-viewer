# Logbuch: MediaMTX – Modularer Media-Router & Browser-Integration

## Datum
16. März 2026

## Übersicht
Dieser Logbuch-Eintrag dokumentiert den modularen Ablauf von MediaMTX, die Protokoll-Adaptation und die Integration mit Chrome als Client.

---

## Interner Ablauf
- Core + Path Manager: Lädt Config, erstellt Server (RTSP:8554, HLS:8888, WebRTC:8889).
- Jeder Stream-Pfad (z.B. /movie.mkv) hat eigenen Path mit Sources/Readers.
- Input: Lokale Datei → ffmpeg-Wrapper (runOnInit) publisht RTSP intern.
- Routing: Publisher (ffmpeg) → Path → Readers (Browser via HLS/WebRTC). Hot-Reload ohne Disconnect.
- Output:
  - HLS: http://ip:8888/movie/index.m3u8 (Chunks, Seeking, Caching)
  - WebRTC: http://ip:8889/movie (ultra-low Latency)
- Auth/API/Metrics inklusive.

---

## Chrome-Integration
- Chrome als Client reicht: Native HLS-Support (<video src="…/index.m3u8">) oder WebRTC.
- Kein JS nötig, funktioniert out-of-box.
- Beispiel:
```html
<video id="player" controls width="800" height="450" autoplay></video>
<script>
  const video = document.getElementById('player');
  video.src = 'http://nas-ip:8888/movie.mkv/index.m3u8';
  // Oder WebRTC: video.src = 'http://nas-ip:8889/movie';
</script>
```
- Seeking/Caching funktioniert automatisch.
- Codecs: H.264/AAC ideal; H.265 nur Safari/Chrome mit Flags.

---

## Limitierungen
- Dateien: ffmpeg im Container für Loop/Read nötig (Config runOnDemand).
- Browser: Chrome HLS/WebRTC top; Firefox H.264 only.

---

## Vorteile für NAS/Eel
- Docker starten, Eel lädt HLS-URL.
- Perfekte Integration für Play/Pause-API.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe walkthrough.md für vollständige Details und Proof of Work.*
