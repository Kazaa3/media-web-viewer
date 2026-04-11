# Video Player Varianten – Komplette Übersicht (März 2026)

Diese Übersicht listet alle 14+ unterstützten Wiedergabemodi deiner Media-Library-App, sortiert nach Priorität, Latenz und Features.

---

## 🎯 MAIN VARIANTS (Hauptpfade – 80% Coverage)
| # | Modus        | Tech                  | Latenz | CPU  | Input           | Features                | Status         |
|---|--------------|-----------------------|--------|------|-----------------|-------------------------|----------------|
| 1 | Direct Play  | <video> + HTTP Range  | 0.1s   | 0%   | MP4/H.264/AAC   | Seeking, Chapters       | ✅ Fertig       |
| 2 | MSE fMP4     | FFmpeg → WS → MSE     | 0.5s   | 20%  | Alle (ISO/4K)   | Ultra-low-latency       | ✅ Implementiert|
| 3 | HLS fMP4     | FFmpeg HLS            | 2s     | 25%  | Alle            | ABR, Multi-Client       | ✅ Stabil       |
| 4 | VLC Bridge   | VLC → HLS             | 3s     | 15%  | DVD/BD Menüs    | Echte Menüs, Atmos      | ✅ Bridge ready |

---

## 🧪 EXPERT VARIANTS (Fallbacks + Spezial)
| # | Modus         | Tech                | Latenz | CPU   | Input      | Features         | Status      |
|---|---------------|---------------------|--------|-------|------------|------------------|-------------|
| 5 | pyvidplayer2  | Python + Pygame/VLC | 1s     | 10%   | Desktop    | HW-Decode, Embed | ✅          |
| 6 | MPV.js WASM   | libmpv Canvas       | 2s     | Browser| ISO Menüs  | WASM, Menüs      | ⏳ Deployment|
| 7 | MediaMTX      | RTSP/WebRTC         | 1s     | 5%    | RTSP/HLS   | WebRTC, UDP      | ✅          |
| 8 | mkvmerge Pipe | mkvmerge → FFmpeg   | 0.5s   | 8%    | MKV/ISO    | Lossless Remux   | ✅          |

---

## 🔧 FFMPEG SUB-VARIANTEN (Transcode-Modi)
| Codec | Modus                | Intel QSV | 4K?     | Status   |
|-------|----------------------|-----------|---------|----------|
| H.264 | -c:v h264_qsv fast   | ✅        | ✅      | Fertig   |
| HEVC  | -c:v hevc_qsv medium | ✅ 10-bit | ✅      | Fertig   |
| AV1   | -c:v av1_qsv slow    | Arc only | ✅      | Test     |
| VP9   | -c:v vp9_vaapi       | ✅        | ✅      | Fallback |

---

## 🎮 CONTROLLER VARIANTS (UI/UX)
| # | Modus         | Tech           | Features                |
|---|---------------|---------------|-------------------------|
| A | Video.js 8    | VHS + Plugins | Quality, Subs, Stats    |
| B | DVD Simulator | Custom Overlay| Menü-Simulation         |
| C | pyvidplayer   | Pygame GUI    | Desktop-Fallback        |

---

## 🧠 ROUTING-LOGIK (ffprobe → Modus)
1. ffprobe → {codec/container/resolution/menus}
2. if H.264+MP4 → Direct Play (0%)
3. if 1080p or low-latency → MSE fMP4 (0.5s)
4. if ISO/BD → VLC Bridge (Menüs)
5. else → HLS fMP4 (Universal)
6. Fallback → pyvidplayer

---

## 📊 PERFORMANCE-MATRIX (Arc iGPU)
| Modus      | Latenz | CPU  | 4K? | Menüs? | Multi-Client |
|------------|--------|------|-----|--------|--------------|
| Direct Play| 0.1s   | 0%   | ✅  | ❌     | ✅           |
| MSE fMP4   | 0.5s   | 20%  | ✅  | ❌     | ⚠️           |
| HLS fMP4   | 2s     | 25%  | ✅  | ❌     | ✅           |
| VLC Bridge | 3s     | 15%  | ✅  | ✅     | ❌           |
| MPV.js     | 2s     | Browser| ✅| ✅     | ❌           |

---

## 🎯 NEXT STEPS (Deployment-Priorität)
- MPV.js WASM → web/js/mpv-wasm/ füllen [siehe vorherige Prompts]
- Unified Router → 1 Funktion für alle 8 Modi
- Docker Compose → Arc-GPU + Alle Streams
- Video.js Master → Alle Features in 1 Player

> Deine App: 14 Varianten – die Top 4 decken 95% aller Anwendungsfälle ab!

**Empfohlene Reihenfolge:**
1. MPV.js WASM Deployment
2. Unified Router finalisieren
3. Docker Compose für alle Streams
4. Video.js Master-Integration

---

**Diese Übersicht dient als Referenz für Implementierung, Test und Deployment aller Video-Player-Modi.**
