# Logbuch: Video Player Overhaul – Formate, Protokolle & Advanced Tools (März 2026)

## Zusammenfassung
Die Video-Player-Architektur und das Transcoding-Ökosystem wurden umfassend überarbeitet, um alle Übertragungsarten (Direct, HLS, WebRTC, FragMP4) und moderne Transcoding-Tools robust und benutzerfreundlich zu integrieren.

---

## 1. Transcoding Engine (src/core/transcoder.py)
- **WebM Progress Parsing:**
    - Implementierung von `_parse_progress` für FFmpeg: Fortschritt wird über `time=` aus stderr getrackt und mit der Input-Dauer verglichen.
- **HandBrakeCLI Validation:**
    - HandBrakeCLI-Aufrufe sind jetzt fehlertolerant, "Command not found"-Fehler werden sauber abgefangen und gemeldet.

## 2. Video Player Integration (web/app.html)
- **WebRTC (WHEP) Support:**
    - Integration von videojs-whep in `startEmbeddedVideo` für mediamtx_webrtc-Modus.
- **HLS / FragMP4:**
    - videojs-http-streaming ist für Seeking und Remux-Streams optimiert.
- **UI Feedback:**
    - "VLC Information" und "Transcoding"-Badges wurden zu einem einheitlichen "Playback Status"-Panel zusammengeführt.

## 3. Backend Routing & Logic (src/core/main.py)
- **Multi-Player Support:**
    - Implementiert: open_with_ffplay, open_with_vlc, open_with_cvlc, open_with_pyvlc.
    - `open_video` unterstützt jetzt gezielt ffplay, vlc, cvlc, pyvlc.
- **Advanced Format Handling:**
    - Unterscheidung zwischen Movie-ISOs (mit VIDEO_TS) und Daten-Images.
    - Direkte und transkodierte Pfade für MKV, ISO, DVD-Ordner werden unterstützt.
    - Native Unterstützung für Audio: MP3, M4B, Opus.
- **Route Consolidation:**
    - Alle Streaming-Logik ist in main.py zentralisiert (z.B. video_remux_stream, video_fragment_stream).

## 4. Test-Infrastruktur
- **Selenium Isolation:**
    - E2E-Tests laufen auf separatem Port (8346) und ggf. separatem venv.
- **Mocking & Real Media:**
    - FFmpeg-Mocks und echte Medientests (z.B. "Vortrag"-MKVs) integriert.

## 5. Verifikation
- **Automatisierte Tests:**
    - `test_routing_logic.py` prüft alle 24 Playback-Varianten (Tiered Selection).
    - Selenium E2E auf dediziertem Port/venv.
    - `verify_vortrag_playback.py` für Chrome Native.
- **Manuelle Tests:**
    - "Open with..." für FFplay, VLC, CVLC geprüft.
    - DVD-ISOs, DVD-Ordner, MKVs und Audio (M4B, Opus) erfolgreich getestet.
- **Real Media:**
    - Testfile "30. Pleisweiler Gespräch ...mp4" in media/ vorhanden und 100% Chrome-kompatibel.

---

**Datum:** 18. März 2026  
**Autor:** GitHub Copilot
