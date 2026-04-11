## Phase 10: Parser Branch Separation – Ergänzende Infos
**Datum:** 12. März 2026

- Ziel: Klare Trennung der Parser-Logik für Audio und Multimedia (Video/ISO) zur Steigerung von Effizienz und Robustheit.

### Ergänzende Details
- AUDIO_PARSER_IDS: Enthält alle Parser, die ausschließlich Audioformate (FLAC, WAV, MP3, ALAC, DSD etc.) verarbeiten.
- MULTIMEDIA_PARSER_IDS: Umfasst Parser für Video, ISO, Containerformate (MKV, MP4, DVD, VCD, etc.).
- extract_metadata: Wählt anhand der Dateiendung und Magic-Bytes den passenden Branch (Audio oder Multimedia).
- Branch-Logik: Musikdateien werden nur von Audio-Parsern verarbeitet, Multimedia-Dateien nur von Multimedia-Parsern.
- Konsolidierte Kategorie-Definitionen in format_utils.py:
    - AUDIO_EXTENSIONS: .flac, .wav, .mp3, .alac, .dsf, .dff, .aac, .ogg, .m4a
    - VIDEO_EXTENSIONS: .mp4, .mkv, .avi, .mov, .wmv, .vob, .ts, .mpeg, .mpg
    - ISO_EXTENSIONS: .iso, .img, .bin, .cue
- Spezialisierte Entry-Points:
    - extract_metadata_audio: Für reine Musikdateien.
    - extract_metadata_multimedia: Für Video/ISO/Container.
- Magic-Byte-Checks: Branch-spezifisch, um Fehlzuordnungen zu vermeiden.
- Logging: Branch-Trace-Marker im Log ("Audio Branch", "Multimedia Branch") zur Nachvollziehbarkeit.

### Verifikation
- Automatisierte Tests: Sicherstellen, dass keine Regressionen auftreten.
- Manuelle Tests: Dateiscan und Log-Prüfung für Branch-Zuordnung.

*Entry created: 12. März 2026*
---