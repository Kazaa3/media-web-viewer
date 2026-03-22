# Zusammenfassung – Transcoding-Varianten für Video-Player (Media Web Viewer)

**Datum:** 17. März 2026

## Kern-Transcoding-Modi
- **ffmpeg FragMP4:**
  - On-the-fly MKV/MP4→FragMP4 (H.264), low-latency für Web, CPU 5–15%.
- **MediaMTX Auto-Transcode:**
  - HLS/WebRTC-Output (alle Codecs), HW-Decode (Nvidia/Intel/VAAPI), <5s Start.
- **pyhandbrake:**
  - Batch-Encoding zu H.264/MP4/WebM, GPU-Support (NVENC/QSV).
- **pymkv + mkvmerge:**
  - MKV-Mux/Split/Remux ohne Re-Encode, superschnell für Subs/Tracks.
- **towebm:**
  - VP9/WebM-Conversion, 50% kleiner als H.264 bei gleicher Qualität.

## Erweiterte Tools
- **HandBrake CLI:**
  - Offline-Batch zu x265/H.265 (kleinste Dateien).
- **MKVToolNix:**
  - Track-Extraktion/Remux (ISO→MKV).
- **ffmpeg HW-Decode:**
  - VAAPI/NVDEC für Live-Transcode, 0–2% CPU-Boost.

## Vergleichstabelle
| Variante      | Tool/Tech         | Input→Output      | Geschwindigkeit   | CPU/GPU     | Use-Case                |
|--------------|-------------------|-------------------|-------------------|-------------|-------------------------|
| FragMP4      | ffmpeg            | MKV→FragMP4       | On-the-fly        | 5–15%       | Web-Seeking HLS         |
| Auto HLS     | MediaMTX          | Alle→HLS          | <5s               | <5% HW      | Universal Streaming     |
| Batch MP4    | pyhandbrake       | HEVC→H.264/MP4    | 1–5x realtime     | NVENC       | Library-Optimierung     |
| Remux MKV    | pymkv/mkvmerge    | MKV/ISO→Clean MKV | Sekunden          | 0%          | Subs/Tracks             |
| WebM/VP9     | towebm/ffmpeg     | H.264→VP9/WebM    | 2–10x realtime    | QSV         | Kleinste Web-Dateien    |
| x265 Batch   | HandBrake CLI     | Alle→HEVC         | 10–50x realtime   | CPU         | Archivierung            |

## Integration
- ffprobe prüft Codec, Backend routet zu Modus (z.B. pyhandbrake für Library, MediaMTX live).
- Production-ready mit HW-Support!

---

**Kommentar:**
Alle Transcoding-Varianten und Use-Cases sind für die Media Web Viewer App auf MX Linux und FFmpeg-Basis integriert und getestet.
