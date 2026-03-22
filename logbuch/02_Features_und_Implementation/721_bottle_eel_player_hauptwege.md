# Bottle/Eel-Player: Hauptwege & Spezialpfade

**Empfohlene Zweiteilung für deine App:**

1. **HTTP-Direktpfad (MP4) als simpler Default**
2. **HLS → video.js als Standard-Streamingmodus** für alles, was nicht direkt spielbar ist
3. **VLC/MediaMTX nur als Spezialpfad** für ISO/BD oder Experimente (RTSP/WebRTC)

---

## 1. Progressive MP4 (Direct Play)

- Für alles, was als H.264/AAC-MP4 vorliegt
- Backend: `/direct/<relpath>` mit Range-Support (`206`, `Content-Range`, `Accept-Ranges`)
- Frontend:
  ```js
  player.src({ src: url, type: "video/mp4" });
  ```
- Vorteile:
  - kein Segment-Overhead, wenig Komplexität
  - ideal für LAN/NAS-Playback und kürzere VOD-Files
- In `get_play_plan()`: erster Versuch, wenn Browser das direkt kann → `mode="http-mp4"`

---

## 2. HLS (TS/fMP4) → video.js

- Für alles, was nicht direkt passt (MKV, exotische Codecs, PAL-DVD, 4K)
- ffmpeg erzeugt `index.m3u8` + Segmente (gern fMP4/CMAF)
- Frontend:
  ```js
  player.src({
    src: hlsUrl,
    type: "application/x-mpegURL"
  });
  ```
- Vorteile:
  - hohe Browser-Kompatibilität (Web + Apple)
  - gute Integration in video.js
  - später einfach adaptives Streaming, Bitraten, Deinterlacing nachrüstbar
  - nur ein Streaming-Protokoll nötig
- DASH kann später ergänzt werden, HLS reicht für Heim-/Jellyfin-Variante völlig

---

## 3. Spezialpfade (optional)

### VLC / MediaMTX
- Für ISO/BD oder „komische“ Sachen (PAL-DVD mit Menüs, exotische Codecs):
  - Button „In VLC abspielen“ → `vlc dvd:///...` oder Dateipfad
- Für Live/RTSP/Experimente:
  - ffmpeg → MediaMTX (RTSP/SRT) → VLC/Browser-Client
- Vorteil: Web-Player bleibt schlank, Overkill in dedizierte Modi ausgelagert

---

## Fazit
- **Bestes Grundsetup:**
  - Mode 1: Direct MP4 via HTTP (einfach, robust)
  - Mode 2: HLS (ffmpeg) via video.js für alles Komplexe
- **Später/Overkill:**
  - DASH als Zusatzmodus
  - MediaMTX + VLC/mpv für Spezialfälle und Live

**Ergebnis:**
- Minimale Komplexität im Code
- Saubere Trennung der Pfade
- Genug Luft für Overkill-Player und Experimente
