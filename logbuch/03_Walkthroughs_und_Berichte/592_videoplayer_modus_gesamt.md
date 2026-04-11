# Logbuch: Vollständige Video-Player-Varianten & Backend-Mapping

## Datum
16. März 2026

---

## Übersicht: Alle Video-Player-Varianten (2026)

### 1. Browser-Native & Smart
- Direct Play (MP4/H.264+AAC, WebM/VP9+Opus, MKV/H.264)
- Chrome Native Progressive (HTTP Range, statische MP4/WebM)
- HLS Native (MediaMTX, ffmpeg HLS)
- Auto Detect (ffprobe → Smart Chain)

### 2. MediaMTX (Universal, Docker)
- MediaMTX HLS (http://localhost:8888/{file}/index.m3u8)
- MediaMTX WebRTC (http://localhost:8889/{file})
- MediaMTX RTSP → HLS Proxy

### 3. ffmpeg Solo (VLC-frei)
- ffmpeg FragMP4 (On-the-fly, HTTP Range)
- ffmpeg HLS Server (playlist.m3u8)
- ffmpeg HTTP TS (Video.js)

### 4. Container-Adapter & Pre-processing
- mkvmerge Remux → Direct Play
- ffmpeg Remux (faststart)
- MakeMKV (DVD/ISO → MKV)

### 5. VLC/cvlc Varianten (Legacy)
- cvlc Solo (TS-Stream)
- cvlc → ffmpeg Pipe
- cvlc DVD ISO
- Embedded VLC (ActiveX)
- VLC Extern

### 6. Speziallösungen & Erweiterte Modi
- HandBrake Title Extract
- Playlist Mode (M3U/JSON)
- LAN Optimized
- Low Latency Mode
- Drag & Drop → Auto-Detect

---

## Empfohlene Reihenfolge (Dropdown)
1. Auto Detect (ffprobe → Smart)
2. Direct Play (MP4/H.264)
3. MediaMTX HLS (Universal)
4. MediaMTX WebRTC (<100ms)
5. ffmpeg FragMP4 (Fallback)
6. cvlc Legacy (nur Notfall)

---

## Backend Mapping (Python/Eel)
```python
MODUS_MAPPING = {
    # Smart
    "auto_detect": "ffprobe → Smart Chain",
    "direct_play": "/direct/{file}",
    "chrome_native": "/progressive/{file}",
    # MediaMTX
    "mediamtx_hls": "http://localhost:8888/{file}/index.m3u8",
    "mediamtx_webrtc": "http://localhost:8889/{file}",
    # ffmpeg
    "ffmpeg_fragmp4": "http://localhost:8090/{file}",
    "ffmpeg_hls": "/hls/{file}/playlist.m3u8",
    # Remux
    "mkvmerge_remux": "mkvmerge -o /tmp/{file}.mp4 → /direct/",
    "ffmpeg_remux": "ffmpeg -movflags faststart → /direct/",
    # Spezial
    "dvd_iso": "handbrakecli --main-feature → MKV",
    "makemkv": "makemkvcon → MKV Rip",
    # Erweitert
    "playlist": "/playlist.m3u",
    "lan_optimized": "Direct > FragMP4 > HLS",
    "low_latency": "WebRTC > FragMP4 > Direct",
    # Legacy
    "cvlc_solo": "http://localhost:8092/",
    "vlc_embedded": "vlc://embedded",
    "vlc_extern": "vlc http://localhost:8080/video",
    "drag_drop": "Auto Detect"
}
```

---

## Visuelle Gruppierung (Dropdown)
- Optgroup-Struktur für Übersichtlichkeit, alle 18+ Modi abgedeckt.
- "Auto Detect" als Default, MediaMTX und ffmpeg als universelle Fallbacks.

---

## Fazit
Alle modernen und Legacy-Varianten sind abgedeckt, Backend-Mapping ist vorbereitet. Die Architektur ist bereit für Production und weitere Erweiterungen.

---

*Siehe vorherige Logbuch-Einträge für Details zu einzelnen Modi, Benchmarks und Setup.*
