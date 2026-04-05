# Walkthrough: Transcoding & Auto-Detection Implementation (März 2026)

## Zusammenfassung
Ein umfassendes System für automatische Medienerkennung, hardware-beschleunigtes Transcoding und fortgeschrittene Tools wurde implementiert. Die Media-Library-App spielt Videos jetzt stets im optimalen Modus ab und bietet eine zentrale Oberfläche für Transcoding-Aufgaben.

---

## 1. FFprobe-basierte Auto-Detection
- **get_video_metadata** in main.py nutzt ffprobe zur Analyse von Codec und Container vor dem Abspielen.
- **Smart Routing:**
    - `open_video` unterstützt jetzt einen `auto`-Modus, der Player und Strategie intelligent auswählt.
    - ISO/DVD werden automatisch an VLC weitergeleitet.

## 2. HW-beschleunigtes Transcoding (FragMP4)
- Hardware-Acceleration für On-the-fly-Transcoding im `/video-stream/`-Route integriert.
- **Dynamische Encoder-Auswahl:**
    - System prüft auf NVENC (Nvidia), VAAPI (Intel/AMD), QSV (Intel)
    - Reduziert CPU-Last bei Web-Playback
- **Low Latency:**
    - Ultrafast-Presets und zerolatency-Tuning für flüssiges Web-Playback

## 3. VLC Streaming Stabilität
- **fd://0- und mjpeg demux-Fehler behoben:**
    - Demuxer explizit auf mkv gesetzt (`--demux mkv`)
    - MJPEG-Autoerkennung deaktiviert (`--no-mjpeg-demux`)
    - Pipe-Management zwischen Remuxer (ffmpeg/mkvmerge) und VLC verbessert

## 4. UI/UX-Verbesserungen
- **Auto-Detect-Option:**
    - Neue Einstellung im Video-Player für automatische Moduswahl
- **Status-Feedback:**
    - Toast-Benachrichtigungen zeigen aktiven Playback-Modus (z.B. "Direct Playback", "On-The-Fly Transcoding")

## 5. Erweiterte Transcoding-Tools
- **HandBrakeCLI-Integration:**
    - Wrapper für HandBrake (x264, QSV, NVENC, VAAPI)
- **WebM/VP9-Konvertierung:**
    - Tool für ultra-kleine, web-optimierte Dateien (FFmpeg VP9)
- **Advanced Tools Tab:**
    - Zentrale Oberfläche für Transcoding-Aufgaben mit Fortschrittsanzeige
- **Transcode Manager:**
    - `src/core/transcoder.py` verwaltet Hintergrundprozesse und Task-Status

---

## Verifikation
### Media Analysis Test
- Standalone-Testskript `verify_video_metadata.py` bestätigt ffprobe-Erkennung für H.264, HEVC, MP4, MKV
- Beispielausgabe:
    ```
    Ran 3 tests in 0.002s
    OK
    ```

### Manuelle Logik-Verifikation
- Routing-Logik in main.py geprüft:
    - H.264 in MP4/MOV → Chrome Native Direct
    - VP9/AV1 in WebM → Chrome Native Direct
    - HEVC/MKV/AC3 → Chrome FragMP4 (Transcoded)
    - ISO/DVD → VLC Native

### Tools UI
- Advanced Tools Tab und Task-Listen-Dynamik in app.html geprüft

---

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
