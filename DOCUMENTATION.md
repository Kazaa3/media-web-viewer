# Project Documentation: Media Web Viewer

## Overview
Media Web Viewer is a sleek, modern desktop application for browsing and playing media libraries (music, audiobooks, and basic video support). Built with Python (Eel) and Vanilla JS/HTML/CSS, it prioritizes a premium user experience and detailed metadata extraction.

A local desktop media player and library manager with an embedded web-based GUI. Built with Python, [Eel](https://github.com/python-eel/Eel), and the [Bottle](https://bottlepy.org/) web framework. Supports a wide range of audio formats including MP3, M4A, M4B (Audiobooks), FLAC, OGG, WAV, ALAC, and WMA.

Media Web Viewer is a comprehensive desktop application for managing, indexing, and playing media files with high-performance metadata parsing capabilities.

### Global Versioning
The application uses a centralized versioning system defined in the `VERSION` file in the project root:
```text
1.1.20
```
This version is automatically loaded and used across the backend, .deb package metadata, and the GUI.

## Key Features
- **Multi-format support**: Wide range of audio and container formats.
- **Intelligent parser chain**: Sequential metadata extraction with falling back logic.
- **Audiobook support**: Specialized handling for `.m4b` and long audio files including chapter navigation.
- **Automatic transcoding**: On-the-fly conversion for ALAC/WMA files for browser playback.
- **SQLite DB**: High-performance local storage for media metadata.
- **Integrated Test suite**: Run pytest suites directly from the GUI.
- **Bilingual Logbook**: Built-in development log and documentation viewer (DE/EN).

## Technical Architecture
- **Backend**: Python 3.11+ with Bottle server and Eel bridge.
- **Frontend**: Modern Vanilla JavaScript with declarative i18n system, CSS3 (Glassmorphism), and dynamic event handling.

### Imprint
- **Developer**: kazaa3
- **Location**: Germany
- **Privacy**: Local storage in SQLite. No data transmission to external servers.
- **License**: GNU General Public License v3 (GPL-3.0).

---

## Quick Start

### Option A: Install via .deb (Debian / Ubuntu)

> Download the latest `.deb` from [Releases](https://github.com/MasterX360/media-web-viewer/releases) and run:

```bash
sudo dpkg -i media-web-viewer_1.1.20_amd64.deb
sudo apt-get install -f   # installs missing dependencies if needed

# Start the app
media-web-viewer
```

---

## 🇩🇪 Deutsch (German)

Ein lokaler Desktop-Medienplayer und Bibliotheksverwalter mit einer eingebetteten webbasierten GUI. Entwickelt mit Python, [Eel](https://github.com/python-eel/Eel) und dem [Bottle](https://bottlepy.org/) Web-Framework. Unterstützt eine Vielzahl von Audioformaten, darunter MP3, M4A, M4B (Hörbücher), FLAC, OGG, WAV, ALAC und WMA.

---

## 🇺🇸 English (Default)

The installer automatically sets up a Python virtual environment and installs all dependencies.

**Uninstall:**
```bash
# Keep configuration files
sudo apt remove media-web-viewer

# Remove everything (purge)
sudo apt purge media-web-viewer
```

---

## Troubleshooting & Reset

### Start from Scratch
If you previously ran the app from source or want to reset all settings, note that `apt purge` does **not** remove files in your home directory. To truly start "from zero":

```bash
# 1. Remove old user configuration and database
rm -rf ~/.config/gui_media_web_viewer ~/.media-web-viewer

# 2. Reinstall the clean version
sudo dpkg -i media-web-viewer_1.1.20_amd64.deb

# 3. Fix dependencies if needed
sudo apt-get install -f
```

---

## Indexing

The app indexes `/opt/media-web-viewer/media` by default. You can add more directories in the **Options** tab using the "Add Directory" button.

---

### Option B: Run from Source

**Requirements:**
- Python 3.11+
- `ffmpeg` in your PATH (for transcoding and metadata fallback)
- `python3-tk` (for system file dialogs)
- `libmediainfo0v5` (required by pymediainfo)

```bash
# Clone the repository
git clone https://github.com/Kazaa3/media-web-viewer.git
cd media-web-viewer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

### Option C: Build the .deb yourself

```bash
bash build_deb.sh
sudo dpkg -i media-web-viewer_1.1.20_amd64.deb
```

---

## Features

- **Web-based GUI:** Modern HTML/CSS/JS interface powered by Eel (no Electron needed)
- **Player tab**: Real-time playback with Itemlist and player sidebar on GUI.
- **Itemlist**: Displays all playable elements with search and filtering.
- **Player footer**: Persistent playback controls and progress tracking.
- **Premium Sidebar**: Real-time display of media metadata and cover art.
- **Smart Metadata Extraction:** Multi-parser pipeline using `mutagen`, `pymediainfo`, and `ffmpeg` fallback.
- **Audiobook Support:** Automatic chapter detection and correct sorting for `.m4b` and long MP3 files.
- **On-the-Fly Transcoding:** ALAC → FLAC and WMA → OGG via `ffmpeg` with transparent caching.
- **Embedded Cover Art:** Extracts and displays cover images from MP3, FLAC, M4A, and MP4 containers.
- **Media Library:** SQLite-backed library with an in-app metadata editor.
- **File Browser:** Navigate your filesystem and add media directly from the app.
- **Integrated Tests:** Run backend pytest suites from the "Tests" tab in the UI.
- **Smart Categorization:** Advanced logic to distinguish between Albums, Singles, and Compilations.
- **Sophisticated Metadata Parsing**: Extracts deep technical info (bitrate, codecs, tags) using a custom parser chain.
- **Parser Configuration:** Drag-and-drop reordering of the parser chain with enable/disable toggles.
- **Debug Tools:** Real-time log viewer and configurable debug flags.
- **Dynamic Test Suite**: Integrated GUI for running and managing media parsing tests.
- **Logbook:** Built-in development log and documentation viewer (Bilingual).
- **Automatic Blacklist:** Built-in filter to ignore system files and junk (e.g., 'captcha', 'thumb', 'cover art').
- **Native System Integration:** Fully packaged `.deb` with auto-resolution of dependencies like `ffmpeg`.
- **Internationalisierung**: Full documentation and UI support for German and English.
- **Natural Sorting**: Intelligent numerical sorting for chapters and titles.

---

### Supported Media Categories

The application automatically categorizes indexed items based on metadata and file patterns:

- **🎵 Audio:** General fallback for music without specific tags.
- **💿 Album:** Music organized by album name or track length.
- **💿 Single:** Music organized by multiple versions for the same song.
- **🔀 Compilation:** Detection of "Various Artists" or "compilation" tags.
- **🎻 Klassik (Classical):** Enhanced detection for composers like **Beethoven, Mozart, Bach, Chopin** and "Klassik" keywords.
- **📚 Hörbuch (Audiobook):** Specialized support for `.m4b` and long audio files including chapter navigation.
- **🎬 Film / Serie:** Detection for movie files and TV show patterns (Season/Staffel).
- **📄 E-Book / Dokument:** Support for EPUB, PDF and other document types.

---

## Project Structure

```
media-web-viewer/
├── VERSION               ← Central version number (1.1.20)
├── main.py               ← Entry point, Eel setup, all backend API functions
├── models.py             ← MediaItem data model (parsing, transcoding logic)
├── db.py                 ← SQLite database logic (init, insert, query, clear)
├── requirements.txt      ← Python package dependencies
├── DOCUMENTATION.md      ← This comprehensive documentation
├── DEPENDENCIES.md       ← Complete dependency list with licenses
├── build_deb.sh          ← Script to build a .deb package
├── parsers/              ← Metadata extraction pipeline
│   ├── media_parser.py   ← Parser orchestrator
│   ├── filename_parser.py
│   ├── mutagen_parser.py
│   ├── ffmpeg_parser.py
│   ├── pymediainfo_parser.py
│   └── format_utils.py   ← Codec formatting, parser configuration
├── web/                  ← Frontend + Bottle web server
│   ├── app.html          ← Full UI (tabs: Player, Browser, Edit, Tests, Logbook, …)
│   ├── app_bottle.py     ← Routes for media and cover art serving
│   ├── script.js         ← Frontend JavaScript logic
│   └── i18n.json         ← Localization strings (DE/EN)
├── tests/                ← pytest unit tests
├── logbuch/              ← Development logbook (Markdown entries)
├── packaging/            ← .deb packaging files (DEBIAN/, usr/)
└── media/                ← Your media files go here (gitignored)
```

---

## Technology Tree

Hierarchische Übersicht aller Systemschichten und Abhängigkeiten:

```
Media Web Viewer (v1.1.20)
├── Frontend Layer
│   ├── HTML5/CSS3 (Responsive Design, Glassmorphism)
│   ├── Vanilla JavaScript (EEL Integration, Event Handling)
│   └── i18n System (German/English, JSON-based localization)
├── EEL Bridge
│   ├── WebSocket Communication (@eel.expose decorators)
│   ├── JSON Serialization (Python dict ↔ JS object)
│   └── Callback Handling (Async/await patterns)
├── Backend (Python 3.11+)
│   ├── Eel Framework (Desktop GUI bridge)
│   ├── Bottle Web Server (API routes, media streaming)
│   ├── Threading Support (Background tasks, indexing)
│   └── Exception Handling (Graceful error propagation)
├── Data Processing
│   ├── Parser Pipeline (Filename → Container → Mutagen → FFmpeg → pymediainfo)
│   ├── Transcoding Engine (ALAC/WMA → FLAC/OGG conversion)
│   ├── Category Detection (Smart media classification)
│   └── Cover Art Extraction (Embedded images from containers)
├── Data Persistence
│   ├── SQLite Database (media_library.db with JSON columns)
│   ├── JSON Config Files (settings.json, cache files)
│   └── Debug Flags (Per-module configuration)
├── System Integration
│   ├── .deb Packaging (Debian/Ubuntu distribution)
│   ├── FFmpeg Integration (Media transcoding, fallback parsing)
│   ├── Tkinter Dialogs (File browser, system integration)
│   └── File System Access (Media directory scanning)
└── Development & Testing
    ├── pytest Framework (Unit tests, fixtures)
    ├── Coverage Tools (Code coverage reports)
    ├── Black Formatter (PEP 8 code style)
    ├── Flake8 Linter (Code quality checks)
    └── Git Version Control (Change tracking)
```

---

## Parser Pipeline

Each parser receives the current `tags` dict and only fills in missing values – it never overwrites data already found by an earlier parser.

| Order | Parser | Source | Provides |
|:-----:|--------|--------|----------|
| 1 | `filename_parser` | Filename | title, artist, file size |
| 2 | `container_parser` | Container format | container format |
| 3 | `mutagen_parser` | Mutagen lib | ID3/MP4/Vorbis tags, bitrate, samplerate, cover detection |
| 4 | `ffmpeg_parser` | FFmpeg CLI | Container format, codec, bit depth (fallback) |
| 5 | `pymediainfo_parser` | pymediainfo | Supplementary / missing metadata |

---

## Player Tab

### Übersicht
Der Player Tab ist die Hauptoberfläche zum Durchsuchen und Abspielen deiner Mediathek. Er besteht aus mehreren Bereichen:

### Itemlist (Linkes Panel)
- **Funktion:** Zeigt alle verfügbaren Mediendateien in sortierter Liste
- **Suche:** Suchfeld zum Filtern nach Titel, Künstler, Album
- **Sortierung:** Nach Titel, Künstler, Hinzugefügt, Dauer
- **Kategorisierung:** Visuelle Symbole (🎵 Audio, 💿 Album, 📚 Hörbuch, etc.)
- **Kontextmenü:** Rechtsklick für Optionen (Wiedergeben, Löschen, Eigenschaften)

### Player Controls (Unteres Panel)
- **Play/Pause:** Spacebar oder Button zum Starten/Pausieren
- **Navigation:** Nächster/Vorheriger Track (N/P oder Buttons)
- **Fortschrittsleiste:** Klickbar zum Spulen, zeigt aktuelle/Gesamtdauer
- **Lautstärke:** Slider (0-100%) mit +/- Tasten oder Mausrad
- **Wiedergabemodus:** Repeat (Off/One/All), Shuffle

### Premium Sidebar (Rechts)
- **Cover Art:** Großes Albumcover aus Metadaten extrahiert
- **Now Playing:** Aktueller Titel, Künstler, Album
- **Track Info:** Dauer, Bitrate, Sample Rate, Codec
- **Related Items:** Andere Tracks des gleichen Künstlers/Albums
- **Playlist Info:** Aktuelle Playlist + Anzahl verbleibender Tracks

### Now Playing Footer
- **Track Name & Artist:** Ständig sichtbar beim Scrollen
- **Mini-Controls:** Play/Pause, Next, Volume im Footer
- **Progress:** Kleine Fortschrittsleiste mit Zeit
- **Status Indicator:** Transkodierungsstatus, Buffering

### Playback Features
- **Continuous Playback:** Auto-Play nächster Track nach Abschluss
- **Repeat Modes:** Off (keine Wiederholung) | One (Track wiederholen) | All (Playlist wiederholen)
- **Shuffle:** Randomisierte Wiedergabereihenfolge
- **Transcoding Indicator:** Sichtbarer Status bei ALAC/WMA-Konvertierung
- **Error Handling:** Sichtbare Fehler bei unzugänglichen Dateien

### Playlist Management
- **Create Playlist:** Neuer Eintrag via "New Playlist" Button
- **Add to Playlist:** Drag-and-drop oder Kontextmenü
- **Save/Load:** Playlists lokal speichern (JSON-Format)
- **Edit:** Einträge neu ordnen oder entfernen
- **Delete:** Komplette Playlist löschen (mit Bestätigung)

### Keyboard Shortcuts
| Taste | Funktion |
|-------|----------|
| `Space` | Play/Pause |
| `N` | Nächster Track |
| `P` | Vorheriger Track |
| `M` | Shuffle toggle |
| `+` / `-` | Lautstärke (+/-) |
| `Delete` | Aus Playlist entfernen |
| `Ctrl+S` | Playlist speichern |
| `Ctrl+L` | Playlist laden |
| `?` | Shortcuts anzeigen |

---

## Wording & Terminology

Einheitliche Terminologie für konsistente Dokumentation und UI-Texte.

### UI Elements
- **Itemlist**: Die Liste alle Mediendateien (linkes Panel)
- **Item Modal**: Detailansicht mit bearbeitbaren Feldern (Popup)
- **Player Footer**: Ständig sichtbarer Player unterhalb des Inhalts
- **Premium Sidebar**: Rechtes Panel mit Cover Art und Metadaten
- **Browse Tab**: Datei-Browser zum Hinzufügen von Verzeichnissen
- **Options Tab**: Einstellungen für Scanner, Parser, Datenbank
- **Logbook Tab**: Entwicklungs-Log und Features-Dokumentation

### Media Categories
- **🎵 Audio**: Einzelne Musikdatei ohne Album-Kontext
- **💿 Album**: Musik mit Album-Metadaten (mehrere Tracks)
- **💿 Single**: Musik mit mehreren Versionen (Remix, Cover, live)
- **🔀 Compilation**: Verschiedene Künstler, erkannt via "Various Artists"
- **🎻 Klassik**: Klassische Musik (Komponisten wie Beethoven, Mozart)
- **📚 Hörbuch**: .m4b oder lange MP3-Dateien mit Kapitelstruktur
- **🎬 Film/Serie**: Video-Dateien, erkannt via Dateiname oder Container
- **📄 E-Book**: PDF, EPUB oder andere Dokumente

### Technical Terms
- **Container**: Audio/Video-Format der Datei (MP3, M4A, FLAC, etc.)
- **Codec**: Algorithmus zum Komprimieren/Dekomprimieren von Daten
- **Parser**: Komponente zum Extrahieren von Metadaten aus Dateien
- **Transcoding**: Umwandlung von ALAC/WMA → FLAC/OGG für Browser
- **Tag**: Metadaten-Feld (Title, Artist, Album, etc.)
- **Bitrate**: Datenrate in kbps (kilobits pro Sekunde)
- **Sample Rate**: Audio-Abtastfrequenz in Hz (44.1 kHz, 48 kHz, etc.)
- **Cover Art**: Albumcover als eingebettetes Bild

### Action Buttons
- **Scan Now**: Startet sofortige Medien-Indizierung
- **Add Directory**: Fügt neues Verzeichnis zum Scanner hinzu
- **Play**: Startet Wiedergabe des ausgewählten Tracks
- **Create Playlist**: Neue leere Playlist erstellen
- **Save Changes**: Speichert Änderungen in Item Modal
- **Delete**: Löscht Item aus Datenbank
- **Test Stream**: Startet Test-Transkodierung
- **Analyze**: Startet detaillierte Metadaten-Analyse

---

## Item Modal (Detail View)

Detailansicht mit Metadaten für einzelne Mediendateien.

### Read-Only Fields (Informationen)
- **File Name**: Original-Dateiname
- **File Path**: Vollständiger Dateipfad
- **File Size**: Größe in MB
- **Duration**: Länge des Tracks
- **Container**: Format (MP3, M4A, FLAC, etc.)
- **Codec**: Audio-Algorithmus (MP3, AAC, FLAC, etc.)
- **Bitrate**: kbps (z.B. 320 kbps)
- **Sample Rate**: Hz (z.B. 44100 Hz)
- **Parser Times**: Dauer jedes Parser-Schritts (zur Performance-Analyse)

### Editable Fields (Metadaten)
- **Title**: Lied-/Kapitel-Titel
- **Artist**: Künstler-Name
- **Album**: Album-Name
- **Year**: Veröffentlichungsjahr (YYYY)
- **Genre**: Musikgenre (Rock, Pop, Pop, Jazz, etc.)
- **Track**: Track-Nummer (z.B. 5 von 12)
- **Disc**: Disc-Nummer bei Multi-CD (z.B. 1 von 2)
- **Comments**: Beliebige Notizen (als JSON gespeichert)

### Functional Buttons
- **Save Changes**: Speichert alle Außenbearbeitungen
- **Test Stream**: Testet Transkodierung (falls ALAC/WMA)
- **Analyze**: Triggert vollständige Metadaten-Neu-Analyse
- **Delete**: Entfernt Item komplett aus Datenbank (irreversibel)
- **Cancel**: Bricht Änderungen ab

---

## Transcoding

Files with ALAC or WMA codec cannot be played natively in browsers. The app detects this and:

1. Sets `is_transcoded = True` in the database when codec = ALAC/WMA.
2. The frontend appends `.flac_transcoded` or `.ogg_transcoded` to the URL.
3. `app_bottle.py` intercepts the route, transcodes via `ffmpeg`, and caches the result in `media/.cache/`.
4. The UI shows a warning that the file is being streamed as a transcoded format.

---

## Build & Release
- Packages are built using `build_deb.sh` into `.deb` format for Debian/Ubuntu systems.
- Versions are centraly managed in the `VERSION` file and automatically injected into `main.py`, `build_deb.sh`, and `packaging/DEBIAN/control`.

## Reset & Recovery
- The "Danger Zone" in Options allows for:
    - **Clear DB**: Only empties the media database.
    - **App Reset**: Restores factory settings by deleting the database and config files.

---

## Standards & Good Practice

Diese Sektion beschreibt Entwicklungsstandards und Best Practices für Contributions zu Media Web Viewer.

### Code Style

**Python (Backend):**
- **Formatter:** Black (line length: 88 characters)
- **Linter:** Flake8 (E501 line length disabled für Black)
- **Type Hints:** Empfohlen für Function Signatures
- **Docstrings:** Google-style docstrings für alle Functions
- **Naming:** `snake_case` für Functions/Variables, `PascalCase` für Klassen

```python
# Best Practice Beispiel
def extract_metadata(file_path: Path, mode: str = 'lightweight') -> dict:
    """
    Extract metadata from media file.
    
    Args:
        file_path: Path to media file
        mode: Parsing mode ('lightweight' oder 'full')
        
    Returns:
        Dictionary containing metadata tags
    """
    tags = {}
    # Implementation
    return tags
```

**JavaScript/Frontend:**
- **Format:** Semicolons und 2-space indentation
- **Naming:** `camelCase` für Variables/Functions
- **i18n:** Immer Lokalisierungs-Keys für User-facing Strings nutzen
- **Comments:** `//` für inline comments

```javascript
// Best Practice Beispiel
async function loadMediaLibrary() {
    try {
        const items = await eel.get_all_media()();
        renderItemlist(items);
    } catch (error) {
        console.error('Failed to load library:', error);
    }
}
```

### Architecture Patterns

**Parser Chain Pattern:**
- Nie bestehende Metadaten überschreiben
- Immer `if key not in tags` vor dem Hinzufügen prüfen
- Modified tags dict zurückgeben
- Beide `lightweight` und `full` Modi unterstützen

**Database Operations:**
- Parameterized Queries nutzen (SQL-Injection verhindern)
- JSON Serialisierung/Deserialisierung immer handhaben
- Proper error handling mit try/except
- Database Operations im debug mode loggen

**EEL Function Exposure:**
- `@eel.expose` Decorator für alle Backend-Functions
- JSON-serializable data zurückgeben (dicts, lists, primitives)
- Error handling mit bedeutungsvollen Error Messages
- Function signatures in Comments dokumentieren

### Testing & Quality Assurance

**Unit Tests:**
- Tests in `tests/` directory schreiben
- pytest Framework mit fixtures für Setup
- Ziel: >80% code coverage
- Sowohl success als auch failure cases testen

```bash
# Tests mit Coverage laufen
pytest tests/ --cov=. --cov-report=html
```

**Code Quality Checks:**
```bash
# Format code mit Black
black --line-length 88 .

# Style check mit Flake8
flake8 --max-line-length=88 .

# Type checking mit mypy
mypy --strict parsers/ models.py
```

**Vor dem Commit:**
1. Alle code quality tools laufen
2. Alle tests bestehen (>80% coverage)
3. Dokumentation aktualisiert
4. Aussagekräftige commit messages schreiben

### Configuration Management

**Configuration Files:**
- Alle settings in JSON files speichern (nicht hardcoded)
- Klare, beschreibende Key-Namen nutzen
- Comments für komplexe Settings
- Version schema, wenn Struktur ändert

**Environment Variables:**
- Für sensitive data (API keys, credentials) nutzen
- Prefix mit `MEDIA_WEB_VIEWER_` für clarity
- Alle environment variables in README dokumentieren

### Documentation Standards

**Markdown Files:**
- ATX-style headings nutzen (`#`, `##`, etc.)
- Code examples für komplexe Topics
- Konsistente Terminologie (siehe Wording section)
- Lines <100 characters für Readability halten

**Docstrings:**
- Public functions und classes dokumentieren
- Type hints in docstring
- Usage examples für komplexe functions
- Related functions mit Links referenzieren

### Error Handling

**Best Practices:**
- Spezifische exceptions catchen, nicht generic `Exception`
- Errors mit appropriate severity level loggen
- User-friendly error messages in UI
- Debugging information für developers

```python
# Best Practice
try:
    result = parse_media(file_path)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise UserError("Media file not found")
except Exception as e:
    logger.exception(f"Unexpected error parsing {file_path}: {e}")
    raise
```

---

## Bottle Web Framework
Bottle ist ein minimalistisches WSGI-Web-Framework für Python, das in einer einzigen Datei läuft und keine Abhängigkeiten außer der Standardbibliothek braucht. Es eignet sich perfekt für kleine APIs oder Apps wie deine Media-Library, wo du Routing und Templates schnell brauchst.

### Kernfeatures
- **Routing**: Dekoratoren wie `@route('/path/<name>')` mappen URLs zu Funktionen.
- **Templates**: Eingebaute Engine für einfache HTML-Vorlagen.
- **HTTP-Tools**: Zugriff auf Forms, Cookies, Uploads und JSON.

### Einfaches Beispiel
```python
from bottle import route, run, template, request

@route('/hello/<name>')
def greet(name):
    return template('<h1>Hallo {{name}}!</h1>', name=name)

run(host='localhost', port=8080)
```

---

## EEL Framework
Eel ist eine Python-Bibliothek für Electron-ähnliche Desktop-Apps mit HTML/JS/CSS-Frontend und Python-Backend. Sie startet einen lokalen Server, lädt HTML im Browser und verbindet via `@eel.expose` Python-Funktionen mit JS.

### Setup und Struktur
```
app.py          # Python-Backend
web/            # Frontend
  index.html
  style.css
  script.js
```
Eel serviert `/eel.js` automatisch für bidirektionale Calls.

### Beispiel
**app.py:**
```python
import eel
eel.init('web')
@eel.expose
def scan_media(path):
    return f"Gefunden: {len(os.listdir(path))} Dateien"
eel.start('index.html')
```

---

## Python als Backend
Python dient als robustes Backend für alle Kernlogiken, Metadaten-Extraktion, Datenbankoperationen und Systemintegrationen. Die Architektur nutzt Pythons Stärken in der Datenverarbeitung und bietet eine nahtlose Brücke zum Web-Frontend.

---

## .deb-Paket Erstellung
Das Projekt wird als Debian-Paket (.deb) für Debian/Ubuntu-Systeme gebaut. Das Build-Skript `build_deb.sh` automatisiert den Prozess:
1. **Staging**: Struktur in `packaging/` vorbereiten.
2. **Kopieren**: Projektcode via `rsync` synchronisieren (ohne Junk).
3. **Rechte**: `chmod 755` für Skripte.
4. **Build**: `dpkg-deb --build` mit automatischer Versionsinjektion.

---

## GPL-3.0 Compatibility
Ja, du kannst absolut GPL-3.0 für dein GitHub-Projekt mit Python, Eel und Bottle verwenden – es ist voll kompatibel. Eel und Bottle sind beide MIT-lizenziert (permissiv), was mit GPL-3.0 harmoniert: Dein Projekt wird GPL, Dependencies bleiben unberührt.

### Tipps für das Repo
- Füge `LICENSE` mit GPL-3.0 hinzu.
- Erwähne in `requirements.txt` oder `README` die Dependencies und ihre MIT-Lizenzen.
- Header in Python-Dateien: `# Copyright (c) 2026 kaaza3 | Licensed under GPL-3.0`.

---

## Python Dependencies for Media Web Viewer
Dieses Projekt ist lizenziert unter **GNU General Public License v3 (GPL-3.0)**.

### Paket-Abhängigkeiten
- **MIT License**: `eel`, `bottle`, `pymediainfo`, `gevent`, `pytest`, `pytest-cov`
- **GPL v2**: `mutagen` (kompatibel mit GPL v3)
- **BSD**: `psutil`, `future`

### System-Abhängigkeiten
- `ffmpeg`: LGPL v2.1 / GPL (Audio/Video Transcoding)
- `libmediainfo0v5`: BSD 2-Clause (Media Information Library)
- `python3-tk`: Python Software Foundation (System File Dialogs)

---

## GUI via EEL mit Web Frontend
Das User Interface wird via EEL implementiert, was eine moderne Web-Experience als Desktop-App ermöglicht. 

### Initialisierung
```javascript
loadLibrary();
loadParserConfig();
loadDebugFlags();
loadTestSuites();
```

---

## MediaItem Klasse
Die `MediaItem` Klasse repräsentiert einzelne Mediendateien mit umfassenden Metadaten-Tags.
```python
def to_dict(self):
    return {
        'name': self.name,
        'path': str(self.path),
        'duration': duration_str,
        'tags': filtered_tags,
        'category': self.category,
        'is_transcoded': is_transcoded
    }
```

---

## Dictionary & JSON Storage
Medien-Metadaten werden intern als Python-Dictionaries (`dict`) verwaltet und für die Persistenz in der Datenbank oder API-Kommunikation als JSON-Strings (`json`) serialisiert.

---

## media_library.db
Die SQLite-Datenbank speichert alle Medien-Metadaten und Playlists.
- `init_db()`: Erstellt Tabellen.
- `insert_media(item_dict)`: Fügt neue Items hinzu.
- `get_all_media()`: Ruft indexierte Medien ab.

---

## Parser Details

### get_category
Automatische Kategorisierung basierend auf Metadaten-Mustern (Audio, Album, Audiobook, Klassik, etc.).

### Efficiency Mode (Fast)
Ein ressourcenschonender Modus, der nur die wichtigsten Tags extrahiert (ideal für Erst-Indizierungen).

### Detail Mode (Full)
Ein umfassender Modus, der alle verfügbaren Tags (inkl. technischer Details wie Codecs und Kapitel) sammelt.

---

## Metadata Tags (Logbook)
Die Anwendung nutzt spezielle HTML-Kommentare in Markdown-Dateien für das Features-Modal:
- `Category`: Gruppierung (UI, Parser, Bug).
- `Title_DE / EN`: Bilinguale Titel.
- `Summary_DE / EN`: Bilinguale Zusammenfassungen.
- `Status`: Aktueller Status (COMPLETED, ACTIVE, PLAN, TASK, DOCS).

---

## Dateiformat Guide

### Whitelist
Erlaubte Metadaten-Felder: `title`, `artist`, `album`, `year`, `genre`, `track`, `totaltracks`, `disc`, `codec`, `bitrate`, `samplerate`, etc.

### Blacklist
Ignorierte Dateien: Systemdateien, Cover-Bilder (als Datei), Junk-Daten.

---

## Doxygen Dokumentation
Doxygen eignet sich hervorragend zur automatischen Generierung von Code-Dokumentationen aus Python-Docstrings.
1. Installiere `doxygen` und `graphviz`.
2. Erstelle ein `Doxyfile` mit `INPUT = ../src`.
3. Nutze standardisierte Docstrings in den Python-Skripten.
4. Führe `doxygen Doxyfile` aus, um HTML-Dokumente zu generieren.

---

## Environment Configuration
### environment.yml
Für die Verwaltung von Conda/Mamba Umgebungen:
```yaml
name: media-web-viewer
dependencies:
  - python=3.11
  - ffmpeg
  - mediainfo
  - pip:
    - eel
    - bottle
    - mutagen
```

---

## Verification
- **Build**: `bash build_deb.sh` → `media-web-viewer_1.1.20_amd64.deb` wurde erfolgreich verifiziert.
- **UI**: Die Version `1.1.20` wird korrekt angezeigt und das Logbuch lädt dynamisch.

---

## Lizenz
Das Projekt ist unter der **GNU General Public License v3 (GPL-3.0)** lizenziert. Der vollständige Text ist in der Datei `LICENSE.md` einsehbar.
