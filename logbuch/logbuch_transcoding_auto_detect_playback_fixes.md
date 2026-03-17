# Logbuch: Transcoding & Auto-Detection, Playback-Fixes & UI-Optimierung (März 2026)

## Zusammenfassung
Ein umfassendes System für automatische Medienerkennung, hardware-beschleunigtes Transcoding, Playback-Stabilität und UI-Optimierung wurde implementiert. Die Media-Library-App spielt Videos jetzt stets im optimalen Modus ab, bietet eine zentrale Oberfläche für Transcoding-Aufgaben und zeigt Kapitel für Hörbücher korrekt an.

---

## 1. FFprobe-basierte Auto-Detection
- `get_video_metadata` in main.py nutzt ffprobe zur Analyse von Codec und Container vor dem Abspielen.
- Smart Routing: `open_video` unterstützt jetzt einen `auto`-Modus, der Player und Strategie intelligent auswählt (Direct Play, Transcode, VLC, ffplay).
- ISO/DVD werden automatisch an VLC weitergeleitet.

## 2. HW-beschleunigtes Transcoding (FragMP4)
- Hardware-Acceleration für On-the-fly-Transcoding im `/video-stream/`-Route integriert (NVENC, VAAPI, QSV).
- Ultrafast-Presets und zerolatency-Tuning für flüssiges Web-Playback.

## 3. VLC Streaming Stabilität & Pipe-Fallback
- fd://0- und mjpeg demux-Fehler behoben (Flag entfernt, Pipe-Management verbessert).
- Fallback: Wenn mkvmerge/ffmpeg fehlschlägt (z.B. .bin, korrupt), wird automatisch VLC im Direktmodus gestartet.
- Verzeichnisse (z.B. VIDEO_TS) werden als DVD erkannt und via dvd:// an VLC übergeben.

## 4. UI/UX-Verbesserungen
- "Auto-Detect"-Option im Video-Player für automatische Moduswahl.
- Toast-Benachrichtigungen zeigen aktiven Playback-Modus (Direct, Transcode, VLC, ffplay).
- "Advanced Tools"-Button aus Hauptnavigation entfernt und in den "Optionen"-Tab verschoben (UI-Entlastung).

## 5. Erweiterte Transcoding-Tools
- HandBrakeCLI-Integration (x264, QSV, NVENC, VAAPI)
- WebM/VP9-Konvertierung (FFmpeg)
- "Advanced Tools"-Bereich mit Fortschrittsanzeige im Options-Tab
- Transcode Manager (src/core/transcoder.py) für Hintergrundprozesse

## 6. Kapitel & Metadaten für Hörbücher
- Kapitel werden über `media_parser.extract_metadata` extrahiert und in `MediaItem.tags` gespeichert.
- Sidebar zeigt Kapitel für M4B-Hörbücher korrekt und interaktiv an.
- Bugfix: Kapitel-Navigation funktioniert jetzt für Audio- und Videoelemente.
- Metadaten-Whitelisting: Kapitel werden im Backend-Frontend-Transfer nicht mehr gefiltert.
- Suffixe wie (Hörbuch) oder (Film) werden dynamisch durch die Kategorie-Erkennung in models.py gesetzt.

## 7. Verifikation
- Media Analysis Test: verify_video_metadata.py bestätigt ffprobe-Erkennung für H.264, HEVC, MP4, MKV
- Routing-Logik: H.264/MP4 → Direct, HEVC/MKV → FragMP4, ISO/DVD → VLC, .bin → VLC Direct
- UI: "Advanced Tools" im Options-Tab, Kapitelanzeige für Hörbücher, Kontextmenü erkennt Verzeichnisse/Film
- VLC Stability: Keine fd://0-Fehler mehr, Pipe-Fallback funktioniert

---

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
