## Phase 6: Advanced Data Carriers & Playability Logic
**Datum:** 12. März 2026

- Überarbeitung und Erweiterung der Implementierungsplanung für Phase 6: Fokus auf fortgeschrittene Datenträgerformate und Playability-Logik.
-Format recherchiert sowie Legacy-Videoformate.
- Playability-Filter implementiert:
    - PC-Spiele und reine Datendisks werden nur indexiert.
    - ISO-Filme und Videoformate bleiben als "playable" markiert.
- UI aktualisiert, um die Unterscheidung zwischen indexierten und abspielbaren Medien klar darzustellen.
- MediaItem-Modell mit Playability-Logik erweitert.
- is_playable-Hilfsfunktion in format_utils.py hinzugefügt und detect_file_format entsprechend angepasst.
- parse_pycdlib_isolated in media_parser.py um Konsolen- und VCD-Marker erweitert.
- ISO-Metadaten-Expansion (pycdlib) in Phase 3 ergänzt.
- Alle Änderungen und Fortschritte sind im Task- und Walkthrough-Dokument nachvollziehbar.

*Entry created: 12. März 2026*
---