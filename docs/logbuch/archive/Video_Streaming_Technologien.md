# Doku: Video-Streaming-Technologien im Media Web Viewer

**Datum:** 11. März 2026

---

## Überblick
Der Media Web Viewer unterstützt verschiedene Video-Streaming-Technologien, um maximale Kompatibilität und Performance zu gewährleisten. Die Auswahl erfolgt dynamisch je nach Dateiformat, Endgerät und gewünschter Latenz.

---

### 1. HLS/DASH (Adaptive Streaming)
- **Beschreibung:** Segmentiertes Streaming mit adaptiver Bitrate, ideal für Browser und mobile Geräte.
- **Umsetzung:**
  - FFmpeg mit ffmpeg_streaming-Bibliothek (`pip install python-ffmpeg-video-streaming`).
  - MKV/MP4-Dateien werden in HLS/DASH-Streams konvertiert.
  - Beispiel:
    ```python
    from ffmpeg_streaming import input, Formats
    video = input('/pfad/zur/datei.mkv')
    video.dash('/pfad/zum/output')
    video.hls('/pfad/zum/output')
    ```
- **Vorteile:** Adaptive Qualität, breite Kompatibilität, einfache Integration in HTML5-Player.

---

### 2. Direct Play
- **Beschreibung:** Direkte Wiedergabe von kompatiblen Formaten (z.B. H.264, MP4, MKV) ohne Transcoding.
- **Umsetzung:**
  - Mit ffprobe prüfen, ob das Video direkt abspielbar ist.
  - Beispiel:
    ```bash
    ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 /pfad/zur/datei.mkv
    ```
  - Bei Kompatibilität wird die Datei direkt an den Browser gestreamt.
- **Vorteile:** Keine CPU-Last, schnelle Wiedergabe, native Qualität.

---

### 3. WebRTC (Low-Latency)
- **Beschreibung:** Echtzeit-Streaming mit minimaler Latenz, geeignet für Live-Übertragungen und interaktive Anwendungen.
- **Umsetzung:**
  - Python-Bibliothek aiortc (`pip install aiortc`) für WebRTC-Server.
  - Beispiel:
    ```python
    from aiortc import RTCPeerConnection, MediaStreamTrack
    # ... WebRTC-Server-Setup ...
    ```
- **Vorteile:** Sehr geringe Latenz, bidirektionale Kommunikation, ideal für Live.
- **Nachteile:** Komplexere Integration, spezielle Browser-Unterstützung.

---

## Workflow-Empfehlung
1. Prüfe mit ffprobe, ob Direct Play möglich.
2. Falls nicht: Erstelle HLS/DASH-Stream mit FFmpeg.
3. Optional: WebRTC für Spezialfälle (Live, Interaktiv).

---

## Referenzen & Links
- [ffmpeg_streaming](https://github.com/kkroening/ffmpeg-streaming)
- [aiortc](https://github.com/aiortc/aiortc)
- [FFmpeg Doku](https://ffmpeg.org/documentation.html)

---

**TODO/FIXME:**
- Automatische Auswahl der Streaming-Technologie im Backend.
- Integration von HLS/DASH und WebRTC in die UI.
- Performance-Tests und Logging ergänzen.
