# FFmpeg Modes – Vollständige Übersicht (März 2026)

## 🗂️ FFmpeg Mode-Tabelle (Media-App)

| Kategorie   | Modus         | Command                                      | Use-Case                        | Output         |
|-------------|---------------|----------------------------------------------|----------------------------------|---------------|
| Remux       | copy-mp4      | -c copy -movflags +faststart                 | MKV→MP4 (Browser)               | MP4           |
| Remux       | copy-mkv      | -c copy                                      | Container-Wechsel               | MKV           |
| Remux       | dvd-iso       | -f dvdvideo -title 1 -c copy                 | DVD-ISO → einzelner Stream      | MKV/MP4       |
| Streaming   | hls           | -f hls -hls_time 6                           | Video.js/Chrome (LAN/WAN)       | m3u8+ts       |
| Streaming   | dash          | -f dash -window_size 10                      | DASH-Player (adaptive)          | mpd+m4s       |
| Streaming   | rtsp          | -f rtsp rtsp://localhost:8554/               | MTX/FFplay/VLC                  | RTSP          |
| Transcode   | h264-fast     | -c:v libx264 -preset ultrafast               | Kompatibilität                  | H.264         |
| Transcode   | hevc-fast     | -c:v libx265 -preset fast                    | Kleinere Files                  | HEVC          |
| HW-Accel    | vaapi-h264    | -hwaccel vaapi -c:v h264_vaapi               | Intel/AMD GPU (Linux)           | H.264         |
| HW-Accel    | nvenc-h264    | -hwaccel cuda -c:v h264_nvenc                | NVIDIA GPU                      | H.264         |
| Expert      | fragmp4       | -movflags frag_keyframe+empty_moov           | Progressive DASH                | FragMP4       |

## 🛠️ Backend: Master FFmpeg Generator
- Zentrale `FFMPEG_MODES`-Dict für alle Varianten (siehe Beispiel im Code oben).
- `ffmpeg_generate(input_path, mode, output_base)` erzeugt den passenden Befehl und führt ihn aus.
- Speziallogik für DVD-ISO, HW-Accel Detection, und Streaming-Modi (RTSP/HLS/DASH) integriert.

## 🖥️ Frontend: FFmpeg-Modus-Auswahl
- UI-Details-Panel mit Buttons für alle Modi (copy-mp4, hls, dvd-iso, vaapi-h264, ...).
- JS-Handler fragt Modus ab und ruft eel.ffmpeg_generate() auf.

## 🔍 Spezialfälle
- **DVD-ISO:** Automatische Titelauswahl und Stream-Extraktion.
- **HW-Accel Detection:** Automatische Erkennung von vaapi/nvenc/software.
- **Streaming:** RTSP/HLS/DASH für Netzwerk- und adaptive Streams.

## ✅ Empfehlung: Start mit copy-mp4 (Browser) oder vaapi-h264 (GPU) für maximale Kompatibilität und Performance.

---

**Result:**
Alle FFmpeg-Modi sind jetzt zentralisiert, UI- und Backend-integriert und für Remux, Transcode, Streaming und Hardware-Beschleunigung optimiert.
