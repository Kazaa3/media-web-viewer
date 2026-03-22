# Zusammenfassung: Transcoding-Varianten & Auto-Detect für Video-Player in der Media-Library-App (MX Linux, FFmpeg-basiert)

## Übersicht
Diese Logbuch-Seite fasst alle relevanten Transcoding- und Auto-Detect-Varianten für die Video-Player-Implementierung in der Media-Library-App zusammen. Sie dient als technische Referenz für Backend- und UI-Integration, Codec-Routing und Tool-Auswahl.

---

## 1. Auto-Detect & Routing (ffprobe)
- **Auto-Detect:** ffprobe analysiert Container, Streams, Codecs, Dauer, Bitrate, Tracks in Sekunden.
- **Routing:**
    - Direct Play (z.B. H.264/MP4) wird priorisiert.
    - Transcoding als Fallback (z.B. MKV/ISO/HEVC).
- **Integration:**
    - ffprobe-Wrapper (z.B. ffmpeg-python, mediascan) für Library-Scan und Backend-Routing.
    - Beispiel-Skript (Python):

```python
import subprocess
import json

def untersuche_video(datei):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', datei]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    video = next(s for s in data['streams'] if s['codec_type'] == 'video')
    return {
        'codec': video['codec_name'],
        'dauer': float(data['format']['duration']),
        'container': data['format']['format_name']
    }

print(untersuche_video('movie.mkv'))
# Ausgabe: {'codec': 'hevc', 'dauer': 7200.5, 'container': 'matroska'}
```

- **Routing-Logik:**
    - if codec == 'h264' → Direct Play (Video.js)
    - else → Transcode/Stream (MediaMTX, ffmpeg, pyhandbrake)

---

## 2. Kern-Transcoding-Modi
| Variante         | Tool/Tech         | Input→Output         | Geschwindigkeit   | CPU/GPU      | Use-Case                |
|------------------|------------------|----------------------|-------------------|--------------|-------------------------|
| FragMP4          | ffmpeg           | MKV→FragMP4          | On-the-fly        | 5–15%        | Web-Seeking HLS         |
| Auto HLS         | MediaMTX         | Alle→HLS             | <5s               | <5% HW       | Universal Streaming     |
| Batch MP4        | pyhandbrake      | HEVC→H.264/MP4       | 1–5x realtime     | NVENC        | Library-Optimierung     |
| Remux MKV        | pymkv/mkvmerge   | MKV/ISO→Clean MKV    | Sekunden          | 0%           | Subs/Tracks             |
| WebM/VP9         | towebm/ffmpeg    | H.264→VP9/WebM       | 2–10x realtime    | QSV          | Kleinste Web-Dateien    |
| x265 Batch       | HandBrake CLI    | Alle→HEVC            | 10–50x realtime   | CPU          | Archivierung            |

### Erweiterte Tools
- **HandBrake CLI:** Offline-Batch zu x265/H.265 (kleinste Dateien)
- **MKVToolNix:** Track-Extraktion/Remux (ISO→MKV)
- **ffmpeg HW-Decode:** VAAPI/NVDEC für Live-Transcode, 0–2% CPU-Boost

---

## 3. ffprobe: Untersuchung & Integration
- **Befehle:**
    - `ffprobe -v quiet -show_format -show_streams -print_format json movie.mkv > info.json`
    - `ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,duration,width,height movie.mkv`
    - `ffprobe -show_entries format=duration,format_name -v quiet -of csv=p=0 movie.iso`
- **Python-Integration:**
    - Siehe Beispiel oben (JSON parsen, Routing nach Codec/Container)
- **Alternativen:**
    - mediainfo (sudo apt install mediainfo)
    - exiftool (sudo apt install exiftool)
    - mediascan (PyPI)

---

## 4. ffplay: Test-Player & Debugging
- **ffplay** ist der integrierte FFmpeg-Player (SDL-basiert), ideal für Tests und Debugging.
- **Befehle:**
    - `ffplay movie.mkv` (Standard-Play)
    - `ffplay -fs movie.mkv` (Fullscreen)
    - `ffplay -vf "scale=1280:720" movie.mkv` (Skalierung)
    - `ffplay -loop 0 movie.mkv` (Endlosschleife)
    - `ffplay http://localhost:8888/stream.m3u8` (HLS-Test)
- **Integration:**
    - Python-Subprocess für Embedded-Preview: `subprocess.run(['ffplay', '-autoexit', datei])`

---

## 5. Produktions-Integration
- **ffprobe** prüft Codec/Container → Backend routet zu Modus (Direct Play, Transcode, Remux).
- **HW-Support:** MediaMTX, ffmpeg, pyhandbrake unterstützen HW-Decode/Encode (Nvidia/Intel/VAAPI).
- **Empfehlung:**
    - pyhandbrake für Library-Optimierung (Batch)
    - MediaMTX für Live-Streaming
    - ffmpeg/ffplay für Debugging & Tests

---

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
