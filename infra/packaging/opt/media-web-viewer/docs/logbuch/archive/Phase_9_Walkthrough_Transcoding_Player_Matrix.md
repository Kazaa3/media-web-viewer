## Phase 9: Walkthrough – Transcoding & Multi-Engine Player Matrix
**Datum:** 12. März 2026

- Die Transkodierungs- und Player-Logik wurde massiv erweitert und als Matrix umgesetzt.

### Audio-Transkodierungs-Matrix
- Flexible Matrix für Audio-Ausgabeformate:
    - MP3 (192k): Maximale Kompatibilität für alle Browser (.mp3_transcoded)
    - AAC (128k): Moderner Standard für Web-Player (.aac_transcoded)
    - Opus/OGG: Hocheffizientes verlustbehaftetes Format (.opus_transcoded / .ogg_transcoded)
    - FLAC: Verlustfreie Wiedergabe im Browser (.flac_transcoded)

### Multi-Engine Video Player Matrix
- Video-Player als Source/Output-Matrix:
    - FFmpeg Engine → Chrome: Live-Transkodierung zu Fragmented MP4 (Browser)
    - VLC Engine → Chrome: VLC als Backend-Engine für Browser-Stream
    - mkvmerge → VLC (Lokal): Pipe zu lokaler VLC-App (Direct Play)
    - Chrome Native: Direkte Wiedergabe ohne Engine-Eingriff
- UI angepasst, um zwischen den Modi im Video-Tab zu wechseln.

*Entry created: 12. März 2026*
---