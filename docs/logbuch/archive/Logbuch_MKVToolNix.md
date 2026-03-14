## MKVToolNix

MKVToolNix is a set of tools for creating, modifying, and inspecting Matroska (MKV) files. It is commonly used for batch-remuxing media files, both via GUI and command-line interface (CLI).

### Features
- Supports batch processing of MKV files
- Provides both GUI and CLI tools
- Useful for remuxing, splitting, merging, and inspecting media files

### Usage Example
- For batch-remux: `mkvmerge -o output.mkv input1.mkv input2.mkv`
- For inspecting files: `mkvinfo input.mkv`

### Integration in Media Web Viewer
- Recommended for manual jobs and batch processing workflows
- Can be automated via scripts for large-scale media management

---

## MKVToolNix: Streaming & Direct Play

Ja, MKVToolNix reicht absolut zum Streamen aus – Remux MKV zu MP4/MKV, Tracks editieren bei null CPU-Last (kein Re-Encode), perfekt für Jellyfin/Browser-Kompatibilität in deiner App. Es ist der Standard für Container-Arbeit, schneller als FFmpeg bei Remux.

### Warum reicht es?
- **Streaming:** MP4-Output Direct Play in allen Browsern/Jellyfin; MKV für fortgeschrittene Features (Chapters/Subs).
- **Funktionen:** Mux Tracks (Video/Audio/Subs), Tags/Chapters setzen, Split/Join – alles ohne Qualitätsverlust.
- **Synology:** Docker-Image verfügbar, batch-skriptbar.

### Vollständiges Python-Beispiel
```python
import subprocess, os

def remux_mkvtool(input_file, output_file=None):
    if output_file is None:
        base = os.path.splitext(input_file)[0]
        output_file = base + '.mp4' if not input_file.endswith('.mp4') else base + '_remuxed.mkv'
    cmd = ['mkvmerge', '-o', output_file, input_file]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_file

# Nutzung: remux_mkvtool('/volume1/ABC/01 Medien/film.mkv')
# Für Tracks: mkvmerge -o out.mkv -a 2 input.mkv  # Nur Audio-Track 2
```
Install: `sudo apt install mkvtoolnix` – läuft lokal oder Docker.

### Einschränkungen
- Kein Transcoding/Resize (dazu FFmpeg).
- Für 4K-Streaming: Kombiniere mit Jellyfin Direct Play.

---

## Direct Play Anforderungen
Direct Play erfordert volle Kompatibilität von Container, Video/Audio/Subtitles mit Client – keine Änderung am Stream, minimale Server-Last. Jellyfin priorisiert es, sonst Direct Stream (Remux) oder Transcode.

### Kern-Anforderungen
- Container/Video/Audio müssen client-seitig dekodierbar sein (z. B. Browser: H.264/AAC in MP4).

### Kompatibilitäts-Tabelle (Jellyfin/Browser)
- **Browser (Chrome/Edge):** H.264 8-bit + AAC in MP4 – 4K ok bei Gigabit-LAN.
- **Jellyfin Apps (VLC/AndroidTV):** Breiter (HEVC/VP9 in MKV).
- **Synology 4K:** Direct Play bei H.264/MP4; HEVC braucht HW-Decode (QuickSync).
- **Netzwerk:** >25 Mbps für 4K H.264.

### Tipps
- Remux zu H.264/AAC/MP4 maximiert Direct Play.
- Jellyfin-Dashboard zeigt Play-Methode (Direct Play ideal).

---

## App-spezifische Anforderungen
Deine Eel/Bottle-App nutzt HTML5 `<video>`-Tag für Streaming – Direct Play-Anforderungen sind identisch mit Browser-Standards (Chrome/Edge), da Eel lokalen Webserver hostet. Fokussiere H.264/AAC in MP4 für perfektes Direct Play bei null Server-Last.

### Anforderungen
- **Container:** MP4 (MOV/M4V ok, MKV oft Stream).
- **Video:** H.264 Baseline/High (8-bit) – HEVC/VP9 transcodes im Browser.
- **Audio:** AAC, MP3 – AC3/DTS nicht.
- **Subs:** SRT/WebVTT (PGS burn-in).
- **Auflösung:** 4K ok (Gigabit-LAN), Seeking via Range-Requests (dein Skript).

### Code-Optimierung
```xml
<video id="player" controls crossorigin="anonymous">
  <source src="/stream/mp4/film.mp4" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'>
</video>
```
crossorigin für CORS (NAS).
Codecs explizit für Browser-Hint.

### Test & Fallback
- ffprobe prüfen: `ffprobe -show_streams film.mp4`.
- Fallback: HLS via FFmpeg in App.

---

## Eigener Eintrag: Streaming mit Chrome – Formate & Leistungsanforderungen

### Unterstützte Formate (Chrome)
- **Video:** H.264 (AVC) 8-bit, VP9, AV1
- **Audio:** AAC, MP3, Opus
- **Container:** MP4 (empfohlen), WebM, MKV (eingeschränkt)
- **Subtitles:** SRT, WebVTT

### Leistungsanforderungen
- **4K Streaming:**
  - H.264/MP4: Direct Play möglich, benötigt Gigabit-LAN (>25 Mbps)
  - HEVC/VP9: Transcoding im Browser, höhere CPU/GPU-Anforderung
- **CPU-Last:**
  - Remux mit MKVToolNix: keine Re-Encode, null CPU-Last
  - Transcoding (FFmpeg): hohe CPU/GPU-Last
- **RAM:**
  - Für große Dateien (>10 GB): Browser benötigt ausreichend RAM für Buffering

### Streaming in deiner App (Eel/Bottle)
- Nutzt HTML5 `<video>`-Tag, identisch mit Chrome-Standards
- Fokussiere H.264/AAC in MP4 für Direct Play
- CORS beachten (`crossorigin="anonymous"`), besonders bei NAS/Synology
- Codecs explizit angeben für Browser-Kompatibilität

### Beispiel-Code
```xml
<video id="player" controls crossorigin="anonymous">
  <source src="/stream/mp4/film.mp4" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'>
</video>
```

### Tipps & Fallbacks
- Remux zu MP4/H.264/AAC maximiert Direct Play
- ffprobe prüfen: `ffprobe -show_streams film.mp4`
- Fallback: HLS via FFmpeg für inkompatible Formate

---
