# GUI Media Web Viewer

A custom media player with an embedded web-based GUI. It is built using Python, Eel, and the Bottle web framework. It supports parsing a wide range of audio formats including MP3, M4A, M4B, ALAC, FLAC, OGG, and WAV.

## Features

- **Web-based GUI:** Powered by [Eel](https://github.com/python-eel/Eel), bringing modern HTML/JS/CSS to a desktop app interface.
- **Micro Backend Server:** Uses the [Bottle](https://bottlepy.org/) WSGI micro web-framework to serve media and cover art seamlessly to the frontend.
- **Smart Metadata Extraction:** Uses multiple parser modules (`pymediainfo`, `mutagen`, and `ffmpeg` fallback) to comprehensively read audio tags (title, artist, album, bit depth, codec, sampling rate).
- **On-the-Fly Transcoding:** Automatically transcodes formats with poor browser compatibility like Apple Lossless (`ALAC`) to `FLAC` in the background utilizing lightweight `ffmpeg` caching, ensuring smooth immediate playback on the frontend.
- **Embedded Cover Art:** Identifies and displays embedded cover images inside MP4/M4A/MP3/FLAC items directly natively in the app.
- **Integrated Testing Suite:** A dedicated "Tests" tab allows running backend unit tests (Pytest) and GUI verification directly from the application.
- **Chapter Support:** Automatically parses and chronologically sorts media chapters (supported in MP3, FLAC, and MP4/M4B).
- **SQLite Database:** Media metadata is persisted in a local SQLite database with playlist support (placeholder).
- **Debug & Config:** Built-in tabs for database debugging, parser chain configuration, and experimental debug flags.

## Requirements

- Python 3.11+
- `eel`
- `bottle`
- `mutagen`
- `pymediainfo`
- A working installation of `ffmpeg` in your PATH.

## Installation / Run

```bash
# Optional: Setup virtual environment
# python -m venv .venv
# source .venv/bin/activate

# Install required python packages
pip install eel bottle mutagen pymediainfo

# Run the media viewer
python main.py
```

## Project Structure

```
gui_media_web_viewer/
├── main.py               ← Einstiegspunkt, Eel App Bootstrapping, API Exposure
├── models.py             ← Datenmodelle (MediaItem-Klasse)
├── db.py                 ← SQLite-Datenbanklogik (init, insert, query, clear)
├── parsers/              ← Metadaten-Extraktion (4 Parser in Pipeline)
│   ├── filename_parser.py
│   ├── mutagen_parser.py
│   ├── ffmpeg_parser.py
│   └── pymediainfo_parser.py
├── web/                  ← Frontend + Bottle-Webserver
│   ├── app.html          ← GUI (HTML/CSS/JS) mit Tabs (Library, Tests, Options)
│   ├── app_bottle.py     ← Bottle-Server mit Routen: /media/, /cover/
│   └── script.js         ← JavaScript für die GUI
├── tests/                ← Unit-Tests (Pytest) für DB, MediaItem und Parser
├── media/                ← Multimedia-Dateien (gitignored)
└── media_library.db      ← SQLite-DB (gitignored, wird automatisch erzeugt)
```

## Core Modules

### main.py

| Bereich | Beschreibung |
|---------|-------------|
| **API Exposure** | Exponiert Funktionen für das Frontend: `get_library`, `run_tests`, `get_debug_logs`, etc. |
| **Parser-Pipeline** | Koordiniert `filename → mutagen → ffmpeg → pymediainfo` |
| **scan_media()** | Eel-exposed: löscht DB, scannt alle Dateien neu, nutzt `MediaItem` |
| **run_tests()** | Führt ausgewählte Pytest-Suiten aus und gibt Ergebnisse an das GUI zurück. |
| **Startup** | `db.init_db()` → `eel.init()` → `eel.start()` |

### models.py

| Klasse | Beschreibung |
|--------|-------------|
| **MediaItem** | Repräsentiert ein Medium; extrahiert Dauer, Tags und Kapitel. |
| **to_dict()** | Formatiert Daten für das Frontend (inkl. Transkodierungs-Flags). |

### db.py

| Funktion | Beschreibung |
|----------|-------------|
| `init_db()` | Erstellt Tabellen `media`, `playlists`, `playlist_media` |
| `clear_media()` | Löscht alle Einträge aus `media` (für Refresh) |
| `insert_media()` | Fügt ein MediaItem-Dict ein (Tags als JSON-String) |
| `get_all_media()` | Gibt alle Medien als Liste von Dicts zurück |
| `get_known_media_names()` | Gibt Set aller bekannten Dateinamen zurück |

### Parser-Pipeline (`parsers/`)

| Reihenfolge | Parser | Quelle | Was er liefert |
|:-----------:|--------|--------|----------------|
| 1 | `filename_parser` | Dateiname | Basis-Tags: title, artist, Dateigröße |
| 2 | `mutagen_parser` | Mutagen-Lib | ID3/MP4/Vorbis-Tags, Cover-Erkennung, Bitrate, Samplerate |
| 3 | `ffmpeg_parser` | FFmpeg CLI | Container-Format, Codec, Bitdepth (Fallback) |
| 4 | `pymediainfo_parser` | pymediainfo | Ergänzende/fehlende Metadaten |

> Jeder Parser bekommt das bisherige `tags`-Dict und ergänzt fehlende Werte, ohne vorhandene zu überschreiben.

### Web-Frontend (`web/`)

| Datei | Beschreibung |
|-------|-------------|
| `app.html` | Komplette UI: Sidebar (Cover, Metadaten), Medienliste, Audio-Player, Tab-System (Library + Debug) |
| `app_bottle.py` | Bottle-Routen: `/media/<file>` (mit ALAC→FLAC Transkodierung + Caching), `/cover/<file>` (eingebettetes Cover-Art) |

## Transcoding

Dateien mit Apple Lossless (ALAC) Codec können nicht nativ im Browser abgespielt werden. Die App erkennt das und:

1. **`main.py`**: Setzt `is_transcoded = True` wenn Codec = ALAC
2. **`app.html`**: Hängt `.flac_transcoded` an die Media-URL an
3. **`app_bottle.py`**: Erkennt die Endung, transkodiert via `ffmpeg` nach FLAC, cached das Ergebnis in `media/.cache/`
4. **UI**: Zeigt `⚠️ Datei wird on-the-fly für den Webplayer transkodiert und als FLAC gestreamt.`
