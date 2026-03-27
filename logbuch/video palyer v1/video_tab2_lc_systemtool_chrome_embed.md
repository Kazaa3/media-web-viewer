# Logbuch: Video Tab 2.0 – LC System-Tool & VLC/MPV Integration (27.03.2026)

## Problemstellung
- Direkter VLC/MPV-Embed im Chrome-Tab ist nativ nicht möglich (kein Plugin-Support seit Flash-Ende).
- Ziel: DVD/Blu-ray-Menüs, 4K, Atmos, Hardware-Decode, Web-Controls in moderner Media-App.

## Lösungen & Workflows

### 1. VLC → HTML5 Stream (Einfach)
- VLC streamt DVD/Blu-ray als HLS/MSE (`stream.m3u8`)
- HTML5 `<video>` spielt Stream direkt ab
- Menüs: Pfeiltasten im VLC-Fenster (oder Dummy-Interface)

**Kommando:**
```bash
vlc dvd:// /media/dvd.iso \
--intf=http --http-port=8081 \
--sout "#transcode{vcodec=h264,acodec=aac,vb=5000}:http{mux=ts,dst=:8081/stream.m3u8}" \
--no-sout-video-synchro --sout-keep
```
**HTML:**
```html
<video controls width="100%">
  <source src="http://localhost:8081/stream.m3u8" type="application/x-mpegURL">
</video>
```

### 2. Python + VLC → WebSocket Canvas
- VLC rendert Frames, Python sendet Snapshots via WebSocket an `<canvas>`
- Tastatursteuerung via WebSocket

### 3. Tauri + VLC (Native + Web, empfohlen)
- Rust-Backend startet VLC mit HTTP-Stream
- Frontend (HTML/JS) zeigt Stream im `<video>`-Tag
- Vollständige DVD/Blu-ray-Menüs, 4K, Atmos, Hardware-Decode
- Tauri-Window kann VLC-Window parenten

**Setup:**
- Rust + Tauri installieren, Projekt initialisieren
- Rust-Backend (play_vlc, stop_vlc) steuert VLC
- Frontend: Datei auswählen, Stream starten/stoppen, `<video-js>` für Web-Controls
- tauri.conf.json: Shell/Path-Allowlist, Build-Config
- Build & Run: `cargo tauri dev` (Dev), `cargo tauri build --release` (Release)

### 4. MPV.js (WASM, Browser-only)
- Siehe vorherige Logbuch-Einträge: DVD/Blu-ray-Menüs, Hardware-Decode, alles im Browser

## Features & Vorteile
- ✅ DVD/Blu-ray-Menüs (Pfeile/Enter)
- ✅ QSV Hardware-Decode, 4K/Atmos/3D
- ✅ Web-Controls (Play/Pause/Seek)
- ✅ MX Linux/Docker ready
- ✅ Chrome-Tab mit nativer Power

## Empfehlung für MX Linux
1. VLC HLS (schnell, Menüs via VLC)
2. Tauri + VLC (voll integriert, native + Web)
3. MPV.js (reines Browser-Erlebnis)

**Fazit:**
Mit VLC/Tauri/MPV.js lassen sich alle modernen Medien-Workflows (DVD, Blu-ray, 4K, Atmos, Menüs) in Chrome-Tabs und nativen Apps abbilden – 100% Linux-kompatibel, Docker-fähig, zukunftssicher.
