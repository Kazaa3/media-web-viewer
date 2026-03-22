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

**Milestone: Buildsystem, Environment, DB, Hygiene**

**build_system.py**
Komplexes Buildsystem für Media Web Viewer. Automatisiert Tests, Lint, Typprüfung, PyInstaller- und Debian-Builds, Clean, Info, Pipeline. CLI mit epilog, targeted pre-build gate, Banner-Ausgabe, Version-Handling, Artefakt-Cleaning, Info-Display. Modular, robust, dokumentiert.

**check_environment.py**
Schnelles Environment-Check-Skript. Prüft Python-Version, venv/conda, kritische und optionale Dependencies, System-Tools (ffmpeg, mediainfo, browser), tkinter, main.py-Import. Gibt Zusammenfassung und empfohlene Fixes aus. CLI mit --list-missing-pip/apt/conda.

**db.py**
SQLite-Datenbankmodul. Initialisiert DB, Migration für neue Felder, Insert/Update/Delete/Query für Medien und Playlists, Legacy-DB-Cleanup, Statistiken, Tag-Update, Rename, Delete. Nutzt user-writable Pfad (~/.media-web-viewer). Robust, migrationssicher, dokumentiert.

**env_handler.py**
Umfassendes Environment- und Hygiene-Management. Validiert exklusive venv/conda, prüft kritische Python- und System-Dependencies, Browser, generiert Environment-Fingerprint, gibt fehlende Pakete für pip/apt/conda aus, strikte Startup-Validierung mit Fix-Hinweis. Modular, robust, dokumentiert.
**Milestone: Logging, Main, MediaFormat**

**logger.py**
Zentrales Logging-Modul. Initialisiert Logging mit Console, File, Debug-File und UI-Buffer. Rotierende Logfiles, Debug-Flags, UI-Log-Handler für Eel, suppress noisy logs. Modular, robust, für alle Module nutzbar.

Hauptmodul, Einstiegspunkt. Initialisiert Eel, Logging, Environment-Check, Debug-Flags, Browser-Handling, Session-Management, DB-Init, Scan, API-Expose für Frontend. Automatische venv/conda-Erkennung und Re-Exec, robustes Environment- und Dependency-Handling, Threaded Media-Scan, flexible CLI-Modi (no-gui, connectionless-browser), Feature- und Logbuch-API.

**media_format.py**
Zentrale Definition und Standardisierung von Dateiformaten. MediaFormat-Klasse erkennt Typ, Format und Content für alle Medientypen (Audio, Video, ISO, Dokument, E-Book). Content-Erkennung für Spezialfälle (PAL DVD, Blu-ray, Daten-Disc, Audio-CD). Modular, für UI, DB und Parser nutzbar.
---
**Milestone: Build Scripts, Config, Versioning**

**build_deb.sh**
Baut .deb-Paket, prüft Build-Test-Gate, kopiert Quellcode ins Staging, setzt Version, macht DEBIAN-Skripte ausführbar, erzeugt Paket, gibt Installationshinweise aus. Robust, automatisiert, für Release und QA.

**build_exe.sh**
Baut standalone EXE für Windows/Linux mit PyInstaller, aktiviert venv, installiert PyInstaller, nutzt Spec-File, prüft Build-Erfolg. Automatisiert, für portable Distribution.

**install_launcher.sh**
Installiert globalen Launcher (media-viewer) in ~/.local/bin, prüft PATH, macht ausführbar, bietet automatische PATH-Konfiguration, gibt Usage und Test aus. Benutzerfreundlich, robust.

**run.sh**
Automatischer Environment-Setup und Launcher. Erkennt Python-Version, aktiviert venv, prüft und installiert fehlende Dependencies (pip/apt/conda), zeigt Umgebung, startet App mit CLI-Optionen (--debug, --ng, --n, --rebuild). Robust, benutzerfreundlich, für alle Plattformen.

**update_version.py**
Synchronisiert Version über alle konfigurierten Dateien (VERSION_SYNC.json), prüft und ersetzt Version-Strings, dry-run möglich, gibt Update-Summary aus. Automatisiert, robust, für Release-Management.

**requirements.txt**
Zentrale Python-Abhängigkeitsliste mit Lizenzhinweisen, System-Dependencies, Installationshinweisen. Kompatibel mit GPL-3.0, dokumentiert, für pip/apt/conda.

**.flake8**
Konfiguriert Flake8-Linter: max-line-length, exclude, ignore, per-file-ignores. Für saubere Codequalität und flexible Lint-Regeln.

**.gitignore**
Umfassende Ignore-Liste für Python, Tests, venv, Build, Logs, Datenbanken, Medien, Screenshots, User-Data, Benchmarks, Packaging. Schützt sensible und temporäre Dateien, hält Repo sauber.

---
**Milestone: Environment, Install, License, Spec, Project Config**

**environment.yml**
Conda-Umgebungsdatei: definiert Python-Version, System- und Pip-Abhängigkeiten, Channels, für schnelle Setup und reproduzierbare Umgebung. Kompatibel mit requirements.txt.

**INSTALL.md**
Installationsanleitung: Systemvoraussetzungen, Methoden (Debian-Paket, Standalone, Source, Conda), Troubleshooting, CI/CD, Build- und Run-Befehle. Detailliert, benutzerfreundlich, für alle Plattformen.

**LICENSE.md**
GPL-3.0 Lizenztext, vollständige Rechte und Pflichten, Kompatibilitätshinweise, Schutz der Nutzerfreiheit, für alle Programmteile und Abhängigkeiten.

**MediaWebViewer.spec / MediaWebViewer-1.3.2.spec / MediaWebViewer-1.3.3.spec**
PyInstaller-Spec-Files: Definieren Build-Konfiguration, Daten, Hidden-Imports, Name, Console-Optionen, für portable Executables. Versioniert, flexibel, für Release und QA.

**pyproject.toml**
Projektweite Konfiguration für Mypy (Type Checking), Python-Version, Warnungen, Import-Overrides. Für saubere Typprüfung und flexible Projektstruktur.
---
Konfiguriert Doxygen für Python und zweisprachige Dokumentation, HTML-Output, Graphviz, private/static extraction, optimiert für Projektstruktur und Docstring-Parsing.

**VERSION_SYNC.json**
Zentrale Version-Sync-Konfiguration: definiert alle zu synchronisierenden Version-Strings, Regex-Pattern, Update-Instructions, Metadaten. Für automatisierte Versionierung und Release-Consistency.
---
