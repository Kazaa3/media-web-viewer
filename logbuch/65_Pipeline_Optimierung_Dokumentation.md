## Logbuch-Eintrag: media_format.py

Ab 10.03.2026 gibt es eine zentrale Datei `media_format.py`, die das Format-Objekt für jede Mediendatei bereitstellt. Die Klasse `MediaFormat` erkennt und klassifiziert Typ, Format und Content für alle gängigen Medien:

- Audio-CD, PAL DVD, NTSC DVD, WMV DVD, HD DVD, Blu-ray, Daten-Disc, ISO-Image
- Audio/Video/Dokument/E-Book: Standardformate (MP3, FLAC, MKV, PDF, EPUB ...)

Die Content-Erkennung erfolgt anhand typischer Merkmale wie Volume-ID, Container oder Dateiendung. Das Format-Objekt kann in allen Modulen genutzt werden und sorgt für eine zentrale, nachvollziehbare Klassifikation und Trennung von Typ, Format und Inhalt.

Die Erweiterung ist dokumentiert, getestet und für UI, Datenbank und weitere Verarbeitung verfügbar.
### Dateiformat: Zentrale Definition und Standardisierung

Ab 10.03.2026 wird das Dateiformat für jede Mediendatei zentral über die Funktion `detect_file_format(path, tags)` definiert und standardisiert. Diese Funktion erkennt und benennt das Format für alle Typen (Audio, Video, ISO, Dokumente, E-Books) und Spezialfälle wie PAL DVD oder Blu-ray.

- Audio: z.B. MP3, FLAC, OGG, WAV, M4A, ALAC, OPUS, AAC, WMA, M4B
- Video: z.B. MP4, AVI, MOV, MKV, WEBM, FLV, WMV, MPG, MPEG, M4V, 3GP, 3G2, OGV, MTS, M2TS
- ISO: ISO, PAL DVD (ISO), Blu-ray (ISO) – Content wird über Volume-ID erkannt
- E-Book/Dokument: EPUB, MOBI, AZW, FB2, PDF, DOC, DOCX, TXT, MD, HTML, HTM

Die MediaItem-Klasse nutzt diese Funktion für das Feld `file_format`, sodass die Formatdefinition für alle Typen einheitlich und nachvollziehbar ist. Die Trennung und Definition ist dokumentiert und im Code umgesetzt.
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

## Meilenstein: Logische Trennung von Typ, Format und Inhalt

Ab 10.03.2026 ist die Parser-Pipeline so erweitert, dass eine klare logische Trennung zwischen Dateipfad (Path-Objekt), Dateiformat und dem tatsächlichen Inhalt besteht. Dies ermöglicht z.B. die Unterscheidung:

- Typ: Image (logisch, z.B. ISO)
- Format: ISO (Dateiformat)
- Inhalt: PAL DVD (detektiert durch Parser, z.B. pycdlib Volume-ID)

Diese Felder werden im MediaItem als `logical_type`, `file_format` und `content_type` geführt und stehen für UI, Datenbank und weitere Verarbeitung zur Verfügung. Die Trennung erleichtert die Klassifikation und gezielte Behandlung komplexer Medien wie ISO-Images mit spezifischem Inhalt (PAL DVD, Blu-ray etc.).

Die neue Architektur ist dokumentiert und getestet. Empfehlungen und Benchmarks berücksichtigen ab sofort diese logische Trennung.

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
