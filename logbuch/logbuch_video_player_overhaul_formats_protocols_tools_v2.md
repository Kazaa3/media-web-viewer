# Logbuch: Video Player Overhaul – Formate, Protokolle, Advanced Tools & Player Controls (März 2026)

## Zusammenfassung
Die Video-Player-Architektur wurde weiter verfeinert, um alle Übertragungsarten (Direct, HLS, WebRTC, FragMP4) und moderne Transcoding-Tools nahtlos zu integrieren. Neue Player-Controls und ein "mkvmerge PIPE KIT" für fortgeschrittenes Streaming wurden ergänzt. Die Testinfrastruktur ist vollständig isoliert und deckt alle Varianten ab.

---

## 1. Transcoding Engine (src/core/transcoder.py)
- **WebM Progress Parsing:**
    - `_parse_progress` für FFmpeg implementiert (time= aus stderr, Vergleich mit Input-Dauer).
- **HandBrakeCLI Validation:**
    - Fehlerbehandlung für "Command not found" verbessert.

## 2. Video Player Integration (web/app.html)
- **WebRTC (WHEP) Support:**
    - videojs-whep in `startEmbeddedVideo` integriert (mediamtx_webrtc).
- **HLS / FragMP4:**
    - videojs-http-streaming für Seeking und Remux-Streams optimiert.
- **UI Feedback:**
    - Status-Badges zu einheitlichem "Playback Status"-Panel konsolidiert.
- **Player Controls [NEU]:**
    - `toggleShuffle`, `toggleRepeat`, `seekVideo`, `toggleSpeed`, `openEQ` in JS implementiert.
    - Player-State mit Backend synchronisiert (Shuffle/Repeat).
    - "mkvmerge PIPE KIT" zur Video-Mode-Auswahl hinzugefügt.

## 3. Backend Routing & Logic (src/core/main.py)
- **mkvmerge PIPE KIT [NEU]:**
    - `video_remux_stream` nutzt jetzt mkvmerge | ffmpeg Pipe für FragMP4 (Chrome Native Seeking).
    - Saubere Terminierung beider Prozesse bei Stream-Ende.
- **Multi-Player Support:**
    - open_with_ffplay, open_with_vlc, open_with_cvlc, open_with_pyvlc implementiert.
    - `open_video` unterstützt gezielt ffplay, vlc, cvlc, pyvlc.
- **Advanced Format Handling:**
    - Unterscheidung Movie-ISO (VIDEO_TS) vs. Daten-Image.
    - Direkte & transkodierte Pfade für MKV, ISO, DVD-Ordner.
    - Native Audio-Unterstützung: MP3, M4B, Opus.
- **Route Consolidation:**
    - Alle Streaming-Logik zentral in main.py (z.B. video_remux_stream, video_fragment_stream).

## 4. Test-Infrastruktur
- **Selenium Isolation [ERLEDIGT]:**
    - E2E-Tests auf Port 8346, dediziertes venv (z.B. .venv_core).
    - Alle GUI-Tests (test_playlist_ui.py, test_websocket_bridge.py, test_iso_playback_ui.py, test_mouse_interaction.py, test_scenario_hammerhart.py) nutzen diese Umgebung.
- **Mocking & Real Media:**
    - FFmpeg-Mocks und echte Medientests ("Vortrag"-MKVs) integriert.

## 5. Verifikation
- **Automatisierte Tests:**
    - test_routing_logic.py prüft alle 24 Playback-Varianten.
    - Selenium E2E auf dediziertem Port/venv.
    - verify_vortrag_playback.py für Chrome Native.
- **Manuelle Tests:**
    - "Open with..." für FFplay, VLC, CVLC geprüft.
    - DVD-ISOs, DVD-Ordner, MKVs und Audio (M4B, Opus) erfolgreich getestet.
- **Real Media:**
    - Testfile "30. Pleisweiler Gespräch ...mp4" in media/ vorhanden und 100% Chrome-kompatibel.

---

**Datum:** 18. März 2026  
**Autor:** GitHub Copilot
