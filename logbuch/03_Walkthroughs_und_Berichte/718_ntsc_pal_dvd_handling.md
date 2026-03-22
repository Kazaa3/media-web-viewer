# NTSC/PAL-DVD-Handling: Einheitliche Strategie für Web-Player

**Ziel:**
Alle SD-Video-DVDs (PAL/NTSC) einheitlich für Browser-Playback und Power-User-Pfade aufbereiten.

---

## 1. Was NTSC / PAL bei Video-DVD bedeutet
- **PAL-DVD:** MPEG-2 720×576, 25 fps, 576i (interlaced), 4:3/16:9
- **NTSC-DVD:** MPEG-2 720×480, 29.97 fps, 480i (interlaced)
- In der App als „SD-DVD-Content“ behandeln, aber unterscheiden nach:
  - `scan_type: interlaced`
  - `fps: 25` vs. `fps: 29.97`
  - `height: 576` vs. `height: 480`

---

## 2. Konvertierungs-Strategie für alle Video-DVDs
- Source: MPEG-2 VOB/MKV
- Deinterlace: yadif/bwdif
- Scale: 576p/480p (oder 720p)
- H.264 (vernünftiger CRF/Bitrate)
- Audio: AAC/AC-3/MP3, Sprach-Track beibehalten
- Ergebnis: Jede Video-DVD ist im Web-Player sauber spielbar

---

## 3. FFmpeg-Beispiele

### a) PAL-DVD (576i → 576p, 25 fps, MP4)
```bash
ffmpeg -i "pal_dvd.mkv" \
  -vf "yadif=1:-1,fps=25,scale=720:576" \
  -c:v libx264 -crf 20 -preset slow \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  "out_pal_576p25.mp4"
```

### b) NTSC-DVD (480i → 480p, 29.97 fps, MP4)
```bash
ffmpeg -i "ntsc_dvd.mkv" \
  -vf "yadif=1:-1,fps=29.97,scale=720:480" \
  -c:v libx264 -crf 20 -preset slow \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  "out_ntsc_480p2997.mp4"
```

---

## 4. Integration in deiner App
- **Backend-Analyse (ffprobe):**
  - `height = 576` & `interlaced` → PAL-DVD
  - `height = 480` & `interlaced` → NTSC-DVD
- **Konvertierungsfunktion (Python):**
```python
def is_sd_dvd_stream(meta):
    height = meta.get("height")
    is_interlaced = meta.get("scan_type") == "interlaced"
    return (height in (576, 480)) and is_interlaced

def build_dvd_ffmpeg_cmd(src, dst, is_pal=True):
    if is_pal:
        dims = "720:576"
        fps = "25"
    else:
        dims = "720:480"
        fps = "29.97"
    return [
        "ffmpeg", "-i", src,
        "-vf", f"yadif=1:-1,fps={fps},scale={dims}",
        "-c:v", "libx264", "-crf", "20", "-preset", "slow",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        dst
    ]
```
- Jedes SD-DVD-Item wird einmalig konvertiert, Web-Player spielt nur H.264-MP4 (Direct Play/HLS)

---

## 5. Fazit: Sind damit alle Video-DVDs abgedeckt?
- **Nein** für 100 % aller exotischen Cadencings
- **Ja** für die Mediathek-Praxis:
  - NTSC-DVD (480i) → H.264 480p/29.97
  - PAL-DVD (576i) → H.264 576p/25
- **Regel:**
  - „SD-DVD-MPEG-2 mit interlaced wird in H.264 deinterlaced, danach läuft es im Browser wie jede andere MP4.“
