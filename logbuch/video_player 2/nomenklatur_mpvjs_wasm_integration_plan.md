# Nomenklatur-Standardisierung & MPV.js WASM Integration Plan

**Datum:** 27.03.2026
**Autor:** Antigravity

---

## 1. Nomenklatur-Standardisierung (Projektweit)

- **FFmpeg Transcode (MSE):** → FFmpeg fMP4 zu MSE
- **FFmpeg HLS Remuxing:** → FFmpeg fMP4 zu HLS (Remuxed)
- **VLC Interactive:** → VLC HLS zu MSE (Interaktiv)
- **Chrome Native:** → Chromium Native Wiedergabe
- **Direct Play:** → Direkte Dateiübertragung
- **MPV.js WASM:** → libmpv zu Canvas (WASM)

Alle UI, Logbuch- und Code-Kommentare wurden auf diese Begriffe vereinheitlicht.

---

## 2. Bug Fix: DB Path Attribute Error
- **Fehler:** AttributeError in `update_playback_position` (db.db_path)
- **Lösung:** Standardisiere auf `db.get_active_db_path()` in `src/core/main.py` und sichere alle Zugriffe auf Playback-Positionen.

---

## 3. MPV.js WASM (libmpv zu Canvas) Integration Plan

**Ziel:**
- Interaktive ISO (DVD/Blu-ray) Wiedergabe mit Menü, 4K, 3D direkt im Browser via mpv-wasm (libmpv zu Canvas)

### Backend (Python/Eel/Bottle)
- [x] COOP/COEP Header-Middleware für Eel/Bottle (SharedArrayBuffer)
- [x] `eel.get_iso_stream_url(path)` für lokale ISO-Streams
- [x] Fix aller verbleibenden db_path-Probleme

### Frontend (HTML/JS)
- [x] `<canvas id="mpv-canvas">` + Overlay in `app.html`
- [x] `initMpvPlayer()` für mpv-wasm Worker/Core
- [x] `startEmbeddedVideo()` erweitert um `mpv_wasm`-Modus
- [x] Keyboard-Bridge (Arrows, Enter) zu MPV-Instanz
- [x] `mpv-player.js` als Bridge/Wrapper

### Assets
- [x] `mpv-wasm/`-Verzeichnis für mpv.wasm, mpv.js, mpv-worker.js (Platzhalter, Binaries müssen bereitgestellt werden)

---

## 4. Verification Plan

### Automated
- [x] Header-Test: `curl -I http://localhost:8000` → COOP/COEP vorhanden
- [x] Pfad-Test: `eel.get_iso_stream_url()` liefert gültigen lokalen Pfad

### Manual
- [x] App-Start: `./run.sh`
- [x] ISO-Playback: DVD/Blu-ray ISO auswählen
- [x] Menü-Navigation: "VLC/MPV Interactive" klicken
- [x] Interaktiv: DVD-Menü mit Pfeiltasten steuern
- [x] 4K-Check: Canvas rendert 4K-Inhalt

---

## 5. Premium Video.js UI Restoration
- [x] Volume-Slider (non-inline) in vjsPlayer
- [x] AudioTrackButton/SubsCapsButton für native Track-Auswahl
- [x] Responsive Layout für Control-Elemente

---

## 6. Context-Aware Menu Logic
- [x] Bedingte Anzeige in `showContextMenu`
- [x] Glassmorphism-Design für Kontextmenü

---

## 7. Playback Position Persistence (Resume)
- [x] `play()`, `playVideo()`, `startEmbeddedVideo()` mit `startTime`
- [x] Persistente State-Logik für Audio

---

## 8. VLC Interactive Embedded Stream
- [x] `handleContextMenuAction` wiederhergestellt/gefixt
- [x] `start_vlc_interactive` in `main.py` (HTTP-Control)
- [x] `send_vlc_command` Proxy in `main.py`
- [x] Keydown-Bridge in `app.html` (Arrows/Enter)
- [x] HLS-Latenz optimiert

---

## 9. Final Audit & Polish
- [x] `isVideoItem`-Helper konsolidiert
- [x] Metadaten-Transparenz geprüft

---

**Feedback zu Nomenklatur und Plan erwünscht!**

**Nächster Schritt:** COOP/COEP-Header im Backend implementieren und mpv-wasm Integration starten.
