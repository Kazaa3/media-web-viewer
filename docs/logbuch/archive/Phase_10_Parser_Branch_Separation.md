## Phase 10: Parser Branch Separation (Audio vs. Multimedia)
**Datum:** 12. März 2026

- Refactoring der parsers/media_parser.py und des parsers/-Verzeichnisses zur logischen und strukturellen Trennung von Audio-Parsing und Multimedia-Parsing (Video/ISO).

### Geplante Änderungen
- media_parser.py:
    - Definition von AUDIO_PARSER_IDS und MULTIMEDIA_PARSER_IDS.
    - extract_metadata wird so angepasst, dass zwischen "Audio Branch" und "Multimedia Branch" gewechselt wird.
    - Gruppierung von Registrierungen und Magic-Byte-Checks nach Kategorie.
- format_utils.py:
    - Konsolidierung der Kategorie-Definitionen (AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, etc.) für saubere Branch-Logik.

### Verifikation
- Automatisierte Tests: Bestehende Unit-Tests laufen ohne Regressionen.
- Neuer Testfall für "Audio Branch" mit High-Res-Audio-Samples.
- Manuelle Verifikation: Dateiscan läuft korrekt mit getrennten Branches, Logs zeigen "Audio Branch" und "Multimedia Branch" Marker.

*Entry created: 12. März 2026*
---