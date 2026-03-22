# PAL-DVD-MKV: Direct Play in Browser und VLC/mpv

**Kurz:**
- Für den Browser: **nein** (ohne Transcode)
- Für VLC/mpv: **ja** (direkt)

---

## 1. Direkt in VLC / externen Playern
- PAL-DVD-Bild im MKV: meist MPEG-2 Video, 720×576, 25 fps, interlaced 576i, plus AC-3/AAC
- VLC, mpv, makemkv-Player können das direkt abspielen; Deinterlacing im Player einstellbar (Yadif, Bob, etc.)
- **Fazit:** Wenn „Direct Play“ = Datei mit VLC/mpv öffnen, ohne Konvertierung → **ja, das geht sehr gut**

---

## 2. Direkt im Browser (HTTP-MP4 / Direct Play)
- Browser unterstützen **kein MPEG-2-Video** in `<video>`/video.js
- MKV-Container werden in Browsern meist nicht direkt unterstützt (nur MP4/WebM)
- **Konsequenz:** PAL-DVD-MKV mit MPEG-2 kannst du **nicht im Browser direkt abspielen**
- Lösung:
  - Vorab zu **H.264 in MP4/MKV konvertieren** (mit Deinterlace)
  - Oder on-the-fly via HLS/Transcode (ffmpeg → HLS-TS/fMP4 → video.js)

---

## 3. Praktische Empfehlung für deine App
- **Für Browser-Web-Player:**
  - Remuxe/Konvertiere PAL-DVD-MKV zu H.264/AAC + Deinterlace (576p25), dann als Direct Play/HLS im Browser
- **Für VLC-/Power-User-Pfad:**
  - UI-Button „VLC-Direct“ für das Original-MKV; dort echtes Direct Play

**Übersetzt:**
- Nicht mit PAL-DVD-MPEG-2 → Browser-Direct-Play
- Ja mit PAL-DVD-MPEG-2 → VLC/mpv-Direct-Play

---

## Beispiel: FFmpeg-Deinterlace-Remux (PAL-DVD-MKV → H.264/MP4)

```sh
ffmpeg -i input.mkv -vf yadif=mode=1 -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k -movflags +faststart output.mp4
```
- `-vf yadif=mode=1`: Deinterlacing (Bob)
- `-c:v libx264 -preset veryfast -crf 20`: H.264-Encoding, gute Qualität
- `-c:a aac -b:a 192k`: Audio zu AAC
- `-movflags +faststart`: MP4 für Web optimiert

Damit kannst du PAL-DVD-MKV für Browser-Playback fit machen und trotzdem den Originalpfad für VLC/mpv anbieten.
