## Phase 9: Advanced Transcoding & Multi-Engine Player Support
**Datum:** 12. März 2026

- Implementierung einer matrixbasierten Player-Architektur: Verschiedene Backend-Engines (FFmpeg, VLC, mkvmerge) liefern Inhalte an diverse Frontend-Ausgaben (Chrome Native, Embedded Stream).

### Komponenten

**Transcoding & Streaming Matrix**
- Audio-Matrix: serve_media in app_bottle.py erweitert für generische Zielformate:
    - file.mp3_transcoded: Any → MP3 (libmp3lame)
    - file.aac_transcoded: Any → AAC (native/aac)
    - file.opus_transcoded: Any → Opus (libopus)
- Video-Matrix: VLC-basierter Streaming-Endpunkt (/vlc-stream/): Streamt browser-kompatible Container (TS, MP4/MJPEG) via VLC --sout.
- main.py: start_vlc_transcode_stream implementiert, startet VLC-Prozess für Streaming.

**Universal Player UI**
- app.html: Video-mode-select als Engine/Output-Paare:
    - Chrome (Native): Direkte Datei.
    - FFmpeg Engine → Chrome: Live-Transcode zu fragmented MP4.
    - VLC Engine → Chrome: VLC-Transcode zu HTTP-Stream.
    - mkvmerge Engine → VLC (Local): Pipe zu externem VLC.
    - VLC (Local): Direktes Öffnen in VLC.
- CSS/UI: Anpassung für "VLC Embedded" Look & Feel bei integrierten Streams.

### Verifikation
- Automatisierte Tests: FFmpeg/VLC-Streaming-Prozesse starten korrekt mit gültigen Argumenten.
- Audio Routing: Alle *_transcoded-Suffixe liefern korrekten MIME-Type und Stream.
- Manuelle Tests: "VLC Engine → Chrome" Pipeline stabil, Embedded-UI bleibt konsistent.

*Entry created: 12. März 2026*
---