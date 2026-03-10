# Parser-Pipeline: Optimierung & Dokumentation

## Übersicht
Die Parser-Pipeline orchestriert die Metadaten-Extraktion für alle unterstützten Dateitypen. Sie ist modular, konfigurierbar und benchmark-getestet. Alle relevanten Parser werden sequenziell oder optional ausgeführt, Fehler und Laufzeiten werden protokolliert.

### Pipeline-Architektur
- Zentrale Funktion: `extract_metadata(path, filename, mode)` in `parsers/media_parser.py`
- Konfigurierbare Kette: `PARSER_CONFIG['parser_chain']` (siehe `parsers/format_utils.py`)
- Optional aktivierbare Parser: z.B. ebml, mkvparse, enzyme, pycdlib, pymkv, tinytag, eyed3, music-tag, isoparser
- Jeder Parser erhält den aktuellen Tag-Dictionary und kann Metadaten ergänzen
- Fehlerbehandlung und Logging für jeden Schritt
- Ausführungszeiten werden für Benchmark protokolliert

### Konfiguration
- Zentrale Konfigurationsdatei: `~/.config/gui_media_web_viewer/parser_config.json`
- Optionen: Aktivierung einzelner Parser, Reihenfolge, Debug-Modus, Scan-Ordner
- Beispiel:
```python
PARSER_CONFIG = {
    "parser_chain": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "isoparser"],
    "enable_isoparser_parser": True,
    ...
}
```

### Optimale Kette (Empfehlung)
- Audio: mutagen, pymediainfo, music-tag, tinytag, eyed3
- Video: ffprobe, enzyme, pymediainfo, ebml, mkvparse, pymkv
- ISO: pycdlib, isoparser
- Fallback: ffmpeg

### Erweiterbarkeit
- Neue Parser können einfach als Modul hinzugefügt und in `parser_steps` eingetragen werden
- Aktivierung über Konfigurationsoption
- Benchmark-Skript testet alle Parser auf allen Dateien

### Dokumentation & Tests
- Detaillierte Docstrings in jedem Parser-Modul
- Logbuch-Eintrag: `logbuch/64_Parser_Benchmark_Vergleich.md` (Empfehlungen, Ergebnisse, Fehler)
- Testskripte: `tests/benchmark_all_parsers.py`, `tests/test_isoparser_parser.py`, etc.
- Benchmark-Ergebnisse: `tests/parser_benchmark_results.json`

### Optimierung
- Reihenfolge und Aktivierung der Parser an Dateityp und Performance anpassen
- Fehler und Ausreißer werden im Benchmark-JSON protokolliert
- Konfigurierbare Kette für maximale Flexibilität

---
Stand: 10.03.2026
Automatisierte Dokumentation

## Parser-Abhängigkeiten & benötigte Pakete

| Parser-Modul      | Benötigtes Paket         | Bemerkung                |
|-------------------|-------------------------|--------------------------|
| filename_parser   | -                       | Nur Python-Standard      |
| container_parser  | pymediainfo             | MediaInfo-Wrapper        |
| mutagen_parser    | mutagen                 | Audio-Tag-Bibliothek     |
| pymediainfo_parser| pymediainfo             | MediaInfo-Wrapper        |
| ffprobe_parser    | ffprobe (CLI)           | Systemtool, Python-Subprocess |
| ffmpeg_parser     | ffmpeg (CLI)            | Systemtool, Python-Subprocess |
| ebml              | ebml                    | MKV/EBML-Parsing         |
| mkvparse          | mkvparse                | MKV-Parsing              |
| enzyme            | enzyme                  | Video-Parsing            |
| pycdlib           | pycdlib                 | ISO-Parsing              |
| pymkv             | pymkv                   | MKV-Parsing              |
| tinytag           | tinytag                 | Audio-Tag-Bibliothek     |
| eyed3             | eyed3                   | MP3-Tag-Bibliothek       |
| music-tag         | music-tag               | Audio-Tag-Bibliothek     |
| isoparser_parser  | isoparser, six          | ISO-Parsing, six für Kompatibilität |

Jeder Parser benötigt das jeweilige Paket (siehe requirements.txt), ggf. Systemtools (ffprobe/ffmpeg) und Zusatzpakete wie six für isoparser. Die Tabelle gibt einen schnellen Überblick, was für Tests und Betrieb installiert sein muss.
