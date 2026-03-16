# Logbuch: Alle Video-Player Implementierungen (Komplettliste)

**Datum:** 16. März 2026

## 1. Browser/HTML5 Player (Chrome Native)

1. **Native <video> Tag**
   - MP4/H.264, WebM/VP9, HLS native
   - `<video src="/direct/movie.mp4" controls>`
2. **Video.js (#1 HTML5 Player)**
   - HLS/DASH/MKV/ISO via Plugins
   - CDN: vjs.zencdn.net/8.6.1/video.min.js
   - `<video-js id="player" data-setup="{}">`
3. **PlayerJS.com (Custom Builder)**
   - 500+ Settings, PIP/Chromecast
   - `<script src="my-custom-player.js">`
4. **Plyr (Leichtgewichtig)**
   - 24kB, YouTube/Vimeo, iOS
   - cdn.plyr.io/3.7.8/plyr.js

## 2. VLC‑Familie (100% Kompatibilität)

5. **python-vlc (Embedded)**
   - pip install python-vlc
   - vlc.MediaPlayer().set_hwnd(eel_id)
6. **cvlc Headless Stream**
   - cvlc file --sout '#std{http,ts,:8090/}'
   - Video.js/Video.js mit TS
7. **VLC Web Plugin (Chrome)**
   - libvlc.dll + npvlc.dll
   - Browser‑Embedded VLC
8. **VLC Extern**
   - subprocess.call(['vlc', 'http://localhost:8080/video'])

## 3. Python‑Native Desktop Player

9. **pyvidplayer2 (Top!)**
   - pip install pyvidplayer2
   - pv.VideoPlayer(file, size=(800,450))
10. **vidify**
    - pip install vidify
    - Musikvideos + YouTube
11. **tkinter + mpv**
    - mpv --wid=tkinter_canvas_id

## 4. Backend Streaming Server

12. **MediaMTX (HLS/WebRTC)**
    - Native Binary/Docker
    - http://8888/file/index.m3u8
    - http://8889/file (WebRTC)
13. **ffmpeg FragMP4**
    - ffmpeg -f mp4 -movflags frag_keyframe -listen 1
    - http://8090/stream.mp4
14. **ffmpeg HLS Server**
    - ffmpeg -f hls playlist.m3u8
15. **cvlc TS-Stream**
    - cvlc --sout '#std{http,ts,:8092/}'

## 5. Container/Format‑Converter

16. **mkvmerge Remux**
    - mkvmerge -o movie.mp4 input.mkv
    - → Direct Play
17. **ffmpeg Remux (faststart)**
    - ffmpeg -movflags +faststart movie.mp4
18. **MakeMKV (DVD/ISO)**
    - makemkvcon → MKV Rip + Menus

## 6. Legacy/Extern

19. **mpv Embedded**
    - pip install mpv
    - mpv --wid=eel_window
20. **PotPlayer/MPC-HC**
    - subprocess.call(['mpc-hc', file])
21. **SMPlayer**
    - Qt‑based VLC Alternative

## 7. Intelligente Modi

22. **Auto Detect**
    - ffprobe → Direct | MediaMTX | FragMP4
23. **Mini Overlay (PiP)**
    - Dragbar, always‑on‑top Video
24. **Playlist Mode**
    - M3U/JSON Sequential Play

---

## Ranking nach Einsatzbereich

🏆 **UNIVERSAL (99% Fälle):**
1. Video.js + MediaMTX HLS
2. Native <video> + Direct Play

⭐ **DESKTOP POWER (Alle Formate):**
3. pyvidplayer2
4. python-vlc Embedded

⚡ **LOW LATENCY:**
5. MediaMTX WebRTC
6. ffmpeg FragMP4

📱 **MOBILE/STABIL:**
7. Plyr + HLS
8. PlayerJS Custom

---

## Eel‑Integration Status

✅ Video.js (MediaMTX HLS)
✅ Native <video> (Direct Play)
✅ pyvidplayer2 (Desktop)
✅ python-vlc (Embedded)
✅ ffmpeg FragMP4 (Backend)
✅ MediaMTX (HLS/WebRTC)
✅ cvlc TS (Fallback)

⏳ TODO:
- mpv Embedded
- Mini Overlay PiP
- Playlist Sequencer

**Gesamt:** 24 Player‑Varianten → 6 Kernmodi für Production.

---

**Frage:**
Welchen als nächsten implementieren? mpv oder Mini‑Overlay?
