# Media Web Viewer - Comprehensive Documentation

**Version:** 1.1.19  
**License:** GNU General Public License v3 (GPL-3.0)  
**Author:** kazaa3 | Germany  
### Global Versioning

The application uses a centralized versioning system defined in the `VERSION` file in the project root:

```text
1.1.19
```

This version is automatically loaded and used across:
- Application backend (`main.py`)
- .deb package metadata (`packaging/DEBIAN/control`) – automatically updated by `build_deb.sh`
- Build scripts (`build_deb.sh`)
- Application GUI (Help/About/Footer)

To update the version:
1. Edit the `VERSION` file in the project root.
2. Run `bash build_deb.sh` to build the package with the new version.
3. The documentation and application will reflect the change automatically.
---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Project Structure](#project-structure)
6. [Architecture](#architecture)
7. [Usage Guide](#usage-guide)
8. [Parser Pipeline](#parser-pipeline)
9. [Transcoding System](#transcoding-system)
10. [Database Schema](#database-schema)
11. [Configuration](#configuration)
12. [Development](#development)
13. [Troubleshooting](#troubleshooting)
14. [License](#license)

---

## Overview

**Media Web Viewer** is a sophisticated, modern desktop media player and library manager with an embedded web-based graphical user interface. It combines the power of Python backend processing with a responsive HTML/CSS/JavaScript frontend to provide a premium user experience for managing and playing large media collections.

### Design Philosophy

- **Local-First Architecture:** All data stays on your machine. No cloud synchronization, no external servers.
- **Performance-Oriented:** Multi-parser pipeline optimizes metadata extraction speed and accuracy.
- **User-Centric**: Bilingual interface (German/English) with intuitive navigation and real-time feedback.
- **Internationalization (i18n):** Full support for German and English localization via `i18n.json`. See [Wikipedia: Internationalisierung](https://de.wikipedia.org/wiki/Internationalisierung_(Softwareentwicklung)) for details.
- **Open Source:** Licensed under GPL-3.0 for transparency and community contribution.

### Supported Formats

**Audio:** MP3, M4A (AAC), M4B (Audiobooks), FLAC, OGG (Vorbis/Opus), WAV, ALAC, WMA, AIFF, DSD  
**Video:** MP4, MKV, WebM (basic support)  
**Documents:** EPUB, PDF (unsupport)

---

## Key Features

### 🎵 Core Media Capabilities
- **Multi-Format Playback:** Supports MP3, FLAC, OGG, M4A, M4B, WAV, and more
- **Audiobook Support:** Intelligent chapter detection and natural sorting for long-form audio
- **Automatic Categorization:** Smart detection of Albums, Singles, Compilations, Classical music, and Audiobooks
- **Cover Art Extraction:** Automatically detects and displays embedded album artwork
- **On-Demand Transcoding:** ALAC → FLAC and WMA → OGG transcoding with intelligent caching

### 🧠 Metadata Intelligence
- **Multi-Parser Pipeline:** Combines filename parsing, Mutagen, FFmpeg, and pymediainfo for maximum accuracy
- **Intelligent Fallbacks:** Gracefully handles missing metadata by using alternative sources
- **Parser Configuration:** Drag-and-drop reordering of parser chain with enable/disable toggles
- **Full-Mode Analysis:** Optional deep metadata extraction for detailed tag inspection

### 🎨 User Interface
- **Modern Web-Based GUI:** Built with Vanilla JS, CSS3 Glassmorphism effects, responsive design
- **Multiple Tabs:** Player, File Browser, Media Editor, Test Suite, Logbook, Options
- **Real-Time Library:** SQLite-backed media library with instant search and filtering
- **Embedded File Browser:** Navigate your filesystem and add media directly from the app
- **Live Metadata Editor:** Edit tags and organize your library without external tools

### 🔧 Developer & Testing Tools
- **Test Suite:** Integrated pytest runner directly in the UI
- **Debug Tools:** Real-time log viewer with configurable debug flags
- **Logbook System:** Built-in development documentation and feature tracking in Markdown (Planning/Planung, All/Alle, summary texts in both languages)
- **Parser Performance Metrics:** Track timing and efficiency of each metadata parser
- **Features Modal:** Refactored GUI for displaying feature updates and development notes (auto-loads from logbuch/ if files missing)

  - **English:** Latest feature updates and development notes
  - **Deutsch:** Neueste Feature-Updates und Entwicklungsnotizen
### 📦 System Integration
- **Native Packaging:** Full `.deb` package for seamless Debian/Ubuntu installation
- **Automatic Dependency Resolution:** Missing system libraries are auto-installed via apt
- **Virtual Environment Isolation:** Optional self-contained Python environment
- **Desktop Integration:** Desktop menu entry and system file dialogs via Tkinter

---

## Installation

### Prerequisites

Before installing Media Web Viewer, ensure your system meets these requirements:

#### System Dependencies (Linux/Debian/Ubuntu)
```bash
sudo apt update
sudo apt install ffmpeg libmediainfo0v5 python3-tk python3-dev build-essential
```

#### Alternative Platforms
**Fedora/RHEL:**
```bash
sudo dnf install ffmpeg mediainfo python3-tkinter python3-devel gcc
```

**macOS:**
```bash
brew install ffmpeg mediainfo python@3.11
```

### Installation Methods

#### Option A: Install Pre-Built .deb Package (Recommended for Users)

The easiest way to install Media Web Viewer on Debian/Ubuntu:

```bash
# 1. Download the latest .deb from releases page
# https://github.com/kazaa3/media-web-viewer/releases

# 2. Install the package
sudo dpkg -i media-web-viewer_1.1.18_amd64.deb

# 3. Resolve any missing dependencies
sudo apt-get install -f

# 4. Launch the application
media-web-viewer
```

**Installing Updates:**
```bash
sudo apt update
sudo apt upgrade media-web-viewer
```

#### Option B: Run from Source (For Developers)

Installation for development and customization:

```bash
# 1. Clone the repository
git clone https://github.com/MasterX360/media-web-viewer.git
cd media-web-viewer

# 2. Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py

# 5. Access via browser (usually opens automatically)
# http://localhost:8888
```

#### Option C: Build Your Own .deb Package

For creating a custom .deb package:

```bash
# 1. Install build dependencies
sudo apt install dpkg-deb rsync

# 2. Edit version and scripts as needed in build_deb.sh
# 3. Run the build script
bash build_deb.sh

# 4. Install your custom package
sudo dpkg -i media-web-viewer_1.1.18_amd64.deb
sudo apt-get install -f
```

---

## Quick Start

### First Run

1. **Start the Application**
   ```bash
   media-web-viewer
   ```
   The application window will open automatically in your default browser.

2. **Add Media Library Directory**
   - Click the **Options** tab
   - Select the **Add Directory** button
   - Choose a folder containing your media files
   - The app will begin indexing automatically

3. **View Your Library**
   - Click the **Player** tab to see your indexed media
   - Browse by category (Album, Audiobook, Classical, etc.)
   - Select a track to see detailed metadata in the sidebar

4. **Play Media**
   - Click any track to start playback
   - Use the player controls in the footer
   - Skip tracks with next/previous buttons

### Configuration

#### Selecting Directories

By default, Media Web Viewer indexes files from `/opt/media-web-viewer/media/`. To add more directories:

1. Go to **Options** tab
2. Click **+ Add Directory**
3. Select your media folders
4. Changes apply immediately with automatic re-indexing

#### Debug Mode

Enable debug logging for troubleshooting:

```bash
python main.py --debug
```

This activates all debug flags and logs detailed information about parsing, system operations, and UI events.

---

## Project Structure

```
media-web-viewer/
│
├── main.py                  # Entry point, Eel setup, backend API functions
├── models.py                # MediaItem class with parsing and transcoding logic
├── db.py                    # SQLite database operations
├── requirements.txt         # Python package dependencies
├── DEPENDENCIES.md          # Complete dependency list with licenses
├── LICENSE.md               # GNU General Public License v3
│
├── parsers/                 # Metadata extraction pipeline
│   ├── media_parser.py      # Central parser orchestrator
│   ├── filename_parser.py   # Extract info from filename patterns
│   ├── mutagen_parser.py    # Audio tag extraction (ID3, Vorbis, MP4, etc.)
│   ├── ffmpeg_parser.py     # FFmpeg-based fallback parsing
│   ├── pymediainfo_parser.py# pymediainfo supplementary parsing
│   ├── container_parser.py  # Container format detection (MKV, MP4)
│   └── format_utils.py      # Codec formatting, parser configuration
│
├── web/                     # Frontend assets and Bottle server
│   ├── app.html             # Complete web UI (all tabs and modals)
│   ├── app_bottle.py        # Bottle routes for media serving, cover art
│   ├── script.js            # Frontend JavaScript logic
│   ├── i18n.json            # German/English localization strings
│   └── __init__.py
│
├── tests/                   # pytest unit test suite
│   ├── test_*.py            # Individual test modules
│   ├── parser_tests/        # Parser-specific tests
│   └── integration_tests/   # End-to-end tests
│
├── logbuch/                 # Development logbook (Markdown)
│   ├── 01_Features.md       # Feature descriptions with bilingual titles
│   ├── 00_Known_Issues.md   # Current and resolved issues
│   └── *.py                 # Scripts for logbook management
│
├── packaging/               # .deb package structure
│   ├── DEBIAN/
│   │   ├── control          # Package metadata
│   │   ├── postinst         # Post-installation script
│   │   └── prerm            # Pre-removal script
│   ├── opt/media-web-viewer/# Application files
│   └── usr/
│       ├── bin/             # Executable launcher
│       └── share/           # Desktop integration
│
├── build_deb.sh             # Script to build .deb package
├── build.py                 # PyInstaller build script
├── MediaWebViewer.spec      # PyInstaller specification
│
└── media/                   # Default media library directory (user-writable)
    └── .cache/              # Transcoded file cache
```

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                  User Interface (Browser)               │
│        HTML/CSS/JavaScript with Eel Bridge              │
└────────────────┬────────────────────────────────────────┘
                 │ eel.expose() calls / event listeners
                 ▼
┌─────────────────────────────────────────────────────────┐
│              Python Backend (Eel + Bottle)              │
│  main.py - API routes (@eel.expose decorated)           │
│            - Bottle web server (localhost:8888)         │
└────────┬──────────────────────┬──────────────┬──────────┘
         │                      │              │
         ▼                      ▼              ▼
    ┌────────────┐      ┌──────────────┐  ┌──────────┐
    │  Parser    │      │   Database   │  │ Bottle   │
    │  Pipeline  │      │   (SQLite)   │  │ Routes   │
    │ (metadata) │      │              │  │ (/media) │
    └────────────┘      └──────────────┘  └──────────┘
         │
    ┌────┴────┬────────┬──────────┬──────────┐
    ▼         ▼        ▼          ▼          ▼
  Filename  Mutagen  FFmpeg  pymediainfo Container
  Parser    Parser   Parser    Parser      Parser
```

### Communication Flow

1. **User Interaction → Frontend (JavaScript)**
   - User clicks button, enters text, or scrolls list
   - JavaScript event handler prepares data

2. **Frontend → Backend (Eel Bridge)**
   - JavaScript calls `eel.function_name(args)(callback)`
   - Eel serializes to JSON and sends over WebSocket

3. **Backend Processing (Python)**
   - `@eel.expose` decorated function receives call
   - Function processes data (parsing, database queries, etc.)
   - Returns result

4. **Backend → Frontend (WebSocket)**
   - Eel sends result back to JavaScript callback
   - Frontend updates DOM with new data

---

## Usage Guide

### Media Library Operations

#### Adding Files to Library

**Automatic (Recommended):**
1. Place media files in configured directories
2. Use **Options → Scan Now** to trigger re-indexing
3. Files are automatically detected and added

**Manual (From Browser):**
1. Go to **Browser** tab
2. Navigate to your media directory
3. Click the **+ Add** button next to any file
4. File is immediately indexed and searchable

#### Editing Metadata

1. Click any track in the library to select it
2. Go to **Edit** tab
3. Modify fields: Title, Artist, Album, Genre, Year, etc.
4. Click **Save Changes**
5. Metadata is updated in both database and file tags (where applicable)

#### Creating Playlists

1. Go to **Player** tab
2. Select tracks using **Ctrl+Click** (multiple selection)
3. Click **Create Playlist** button
4. Name your playlist and confirm
5. Save/Load playlists from **Playlists** dropdown

### Advanced Features

#### Parser Configuration

Customize how metadata is extracted:

1. Go to **Options → Parser Configuration**
2. View the current parser chain order
3. Drag parsers to reorder priority
4. Toggle parsers on/off with checkboxes
5. Save configuration

**Parser Modes:**
- **Lightweight:** Fast extraction, basic metadata only
- **Full:** Comprehensive extraction, all available tags

#### Debug & Logging

Monitor application behavior and troubleshoot issues:

1. Go to **Options → Debug Console**
2. Select debug flags to enable:
   - `parser`: Metadata parsing operations
   - `ui`: User interface updates
   - `db`: Database operations
   - `system`: System and file operations
3. View real-time logs and performance metrics

#### Running Tests

Execute automated tests directly from the UI:

1. Go to **Tests** tab
2. Select test suite or individual test
3. Click **Run Tests**
4. View results with pass/fail indicators
5. Check coverage percentage if enabled

---

## Parser Pipeline

The parser pipeline is Media Web Viewer's core metadata extraction system. Each parser runs in sequence, adding missing information without overwriting existing data.

### Parser Order & Specialization

| Priority | Parser | Input | Specialization | Speed |
|:--------:|--------|-------|-----------------|-------|
| 1 | **Filename Parser** | Filename string | Extracts artist, album, track number from standardized filename patterns | ⚡ Instant |
| 2 | **Container Parser** | File container | Determines container format (MP4, MKV, OGG, etc.) | ⚡ Instant |
| 3 | **Mutagen Parser** | Audio tags (ID3, Vorbis, MP4) | Deep tag extraction, cover art detection, codec information | 🟡 Fast (50-500ms) |
| 4 | **FFmpeg Parser** | FFmpeg probe output | Fallback codec detection, bit depth, container format | 🟠 Moderate (500ms-2s) |
| 5 | **pymediainfo Parser** | mediainfo library | Supplementary metadata, container details | 🟠 Moderate (200-800ms) |

### Supported Data Types

The parser pipeline handles various audio/video container formats and tag standards:

- **WAV (Plain):** Raw PCM audio, no metadata tags
- **MP3 (Plain):** Basic MPEG-1 Audio Layer III, minimal tags
- **MP3 (with ID3v2.2):** Enhanced metadata using ID3v2.2 standard
- **MKV (with AAC):** Matroska container with Advanced Audio Coding
- **M4B (with M4A tags):** Audiobook format with MPEG-4 metadata

### Configuration Schema

Parser configuration is stored in `~/.media-web-viewer/parser_config.json`:

```json
{
  "parser_mode": "lightweight",
  "parser_chain": [
    "filename",
    "container",
    "mutagen",
    "pymediainfo",
    "ffmpeg"
  ],
  "enabled_parsers": {
    "filename": true,
    "container": true,
    "mutagen": true,
    "pymediainfo": true,
    "ffmpeg": true
  },
  "mutagen_prefer_albumartist": false
}
```

### Parser Behavior

**Lightweight Mode (Default):**
- Stops parsing when critical tags are found (codec, bitrate, samplerate)
- Optimal for large libraries (1000+ files)
- Trade-off: Some rare metadata may be missed

**Full Mode:**
- All parsers run regardless of existing data
- Gathers complete metadata including comments, lyrics, metadata versions
- Trade-off: Slower indexing, not needed for typical usage

### Parser Architecture Details

Each parser accesses specific libraries and contributes to internal testing:

- **Filename Parser:** Pure Python string processing, no external libraries
- **Container Parser:** Uses `os.path.splitext()` and custom format detection
- **Mutagen Parser:** Accesses `mutagen` library for ID3/Vorbis/MP4 tag reading
- **FFmpeg Parser:** Calls `ffmpeg` CLI tool via `subprocess`, parses JSON output
- **pymediainfo Parser:** Uses `pymediainfo` library (MediaInfo wrapper)

Internal tests validate each parser's output against known test files, ensuring reliability and performance metrics.

---

## Transcoding System

### Why Transcoding?

Some audio codecs (ALAC, WMA) cannot be played directly in web browsers. The transcoding system automatically converts these to browser-compatible formats with intelligent caching.

### Supported Conversions

| Source Codec | Reason | Target Codec | Quality |
|--------------|--------|--------------|---------|
| ALAC (Apple Lossless) | Not browser-supported | FLAC (lossless) | Lossless |
| WMA (Windows Media Audio) | Not browser-supported | OGG Opus (lossy) | High-quality lossy |

### How Transcoding Works

1. **Detection Phase**
   - App analyzes file codec during import
   - Sets `is_transcoded` flag in database if ALAC or WMA detected

2. **Request Phase**
   - Frontend URL includes transpile hint (e.g., `.flac_transcoded`)
   - Bottle route receives request for transcoded stream

3. **Transcoding Phase**
   - FFmpeg spawns background process
   - Original file decoded, re-encoded to target format
   - Output written to cache: `~/.media-web-viewer/transcoded_cache/`

4. **Serving Phase**
   - Cached file streamed to browser with appropriate MIME type
   - Subsequent plays use cached version (instant)
   - Automatic cache cleanup for old files

### Performance Metrics

- **ALAC Transcoding:** ~2-3x file duration (e.g., 60-min file → 2-3 min transcoding)
- **WMA Transcoding:** ~1-2x file duration
- **Cache Hit:** Instant serve from SSD cache
- **Network:** Efficient streaming suitable for local networks

### User Feedback

The UI displays a transcoding indicator:
```
⚠️ This file is streamed in compressed format (FLAC from ALAC)
```

---

## Database Schema

Media Web Viewer uses SQLite for local data persistence. All data is stored in:
```
~/.media-web-viewer/media_library.db
```

### Table: `media`

```sql
CREATE TABLE media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,                  -- Filename (unique identifier)
    path TEXT,                         -- Full file path
    type TEXT,                         -- File extension (.mp3, .flac, etc.)
    duration TEXT,                     -- Formatted duration (HH:MM:SS)
    category TEXT,                     -- Auto-detected category
    is_transcoded BOOLEAN,             -- Whether file requires transcoding
    transcoded_format TEXT,            -- Target format if transcoded
    tags TEXT                          -- JSON-serialized metadata tags
);
```

### Table: `playlists`

```sql
CREATE TABLE playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE                   -- Playlist name
);
```

### Table: `playlist_media`

```sql
CREATE TABLE playlist_media (
    playlist_id INTEGER,               -- FK to playlists
    media_id INTEGER,                  -- FK to media
    position INTEGER,                  -- Track order in playlist
    FOREIGN KEY(playlist_id) REFERENCES playlists(id),
    FOREIGN KEY(media_id) REFERENCES media(id)
);
```

### Tags Storage

The `tags` column stores metadata as JSON. Example:

```json
{
    "title": "Song Title",
    "artist": "Artist Name",
    "album": "Album Name",
    "year": "2024",
    "genre": "Rock",
    "track": "3",
    "totaltracks": "12",
    "codec": "MP3",
    "bitrate": "320 kbps",
    "samplerate": "44.1 kHz",
    "bitdepth": "16 bit",
    "container": "mp3",
    "has_art": true,
    "_parser_times": {
        "filename": 0.001,
        "mutagen": 0.045,
        "ffmpeg": 0.000
    }
}
```

---

## Configuration

### Configuration Locations

**Application Config:**
```
~/.media-web-viewer/config.json
```

**Parser Configuration:**
```
~/.media-web-viewer/parser_config.json
```

**Database:**
```
~/.media-web-viewer/media_library.db
```

**Transcoding Cache:**
```
~/.media-web-viewer/transcoded_cache/
```

### Configuration Files

#### config.json (User Preferences)

```json
{
    "language": "de",                  // "de" for German, "en" for English
    "library_dirs": [
        "/home/user/Music",
        "/mnt/external_drive/Audio"
    ],
    "parser_mode": "lightweight",
    "ui_theme": "dark",
    "auto_scan_interval": 3600
}
```

#### parser_config.json (Parser Settings)

```json
{
  "parser_mode": "lightweight",
  "parser_chain": ["filename", "container", "mutagen", "pymediainfo", "ffmpeg"],
  "enabled_parsers": {
    "filename": true,
    "container": true,
    "mutagen": true,
    "pymediainfo": true,
    "ffmpeg": true
  },
  "mutagen_prefer_albumartist": false
}
```

#### debug_flags.json (Debug Configuration)

```json
{
  "parser": false,      // Metadata parsing operations
  "ui": false,          // User interface updates
  "db": false,          // Database operations
  "system": false,      // System and file operations
  "player": false       // Playback and transcoding operations
}
```

---

## Development

### Setting Up Development Environment

```bash
# 1. Clone and enter directory
git clone https://github.com/MasterX360/media-web-viewer.git
cd media-web-viewer

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dev dependencies
pip install -r requirements.txt

# 4. Install additional dev tools (optional)
pip install black flake8 mypy pytest-watch

# 5. Run tests
pytest tests/

# 6. Start in debug mode
python main.py --debug
```

### Code Structure

**Backend Entry Point:** [main.py](main.py)
- Initializes Eel and Bottle servers
- Exposes API functions to frontend
- Handles library scanning and database operations

**Data Models:** [models.py](models.py)
- `MediaItem` class for individual media files
- Metadata extraction and transcoding logic
- Category detection and serialization

**Database Layer:** [db.py](db.py)
- SQLite initialization and migrations
- CRUD operations for media items and playlists
- Query optimization and data filtering

**Parser System:** [parsers/](parsers/)
- Modular parser chain system
- Individual parsers for different metadata sources
- Configuration management and performance tracking

### Adding New Features

**Example: Add a new parser**

1. Create `parsers/my_parser.py`:
```python
def parse(path, file_type, tags, mode='lightweight'):
    \"\"\"Parse metadata using custom logic\"\"\"
    # Extract metadata
    tags['my_field'] = 'value'
    return tags
```

2. Register in `parsers/format_utils.py`:
```python
PARSER_CONFIG['parser_chain'].append('my_parser')
```

3. Use in pipeline - it will be called automatically

---

## Troubleshooting

### Common Issues & Solutions

#### Application Won't Start

**Error:** `NameError: module not found` or `ImportError`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version (requires 3.11+)
python3 --version
```

#### Files Not Appearing in Library

**Cause:** Directory not added or not indexed

**Solution:**
1. Go to **Options → Add Directory**
2. Select your media folder
3. Click **Scan Now** to force indexing
4. Wait for scanning to complete (watch debug console)

#### Playback Issues (Audio Not Playing)

**Cause:** Browser codec support or file encoding

**Solution:**
1. Enable transcoding for ALAC/WMA files (automatic)
2. Check file format support in browser
3. Try playing from **Edit** tab → **Test Stream** button
4. Check debug logs for FFmpeg errors

#### Database Corrupted / Duplicate Entries

**Cause:** Interrupted operations or version mismatch

**Solution:**
```bash
# Clear and rebuild database
# Go to Options → Danger Zone → Clear Database
# Then: Options → Scan Directory (re-index all files)

# Or via terminal:
rm ~/.media-web-viewer/media_library.db
python main.py
```

#### High CPU Usage During Scanning

**Cause:** Too many files or slow storage device

**Solution:**
1. Enable **Lightweight** parser mode (default)
2. Disable unnecessary parsers in **Parser Configuration**
3. Scan larger directories separately
4. Monitor with `top` command during scanning

#### Metadata Not Updating in UI

**Cause:** Browser cache or session state stale

**Solution:**
1. Hard refresh browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (macOS)
2. Clear browser cache for localhost:8888
3. Restart application

### Getting Help

- Check **logbuch/00_Known_Issues.md** for documented problems
- Review debug logs: **Options → Debug Console**
- Run test suite: **Tests tab → Run All Tests**
- Check GitHub issues: https://github.com/MasterX360/media-web-viewer/issues

---

## License

Media Web Viewer is licensed under the **GNU General Public License v3 (GPL-3.0)**. 

This means:
- ✅ You can freely use, modify, and distribute the software
- ✅ You must include the license text and copyright notice
- ✅ Any modifications or derived works must also be GPL-3.0
- ✅ Source code must be made available to users

See [LICENSE.md](LICENSE.md) for the complete license text.

### Dependencies

All third-party dependencies are compatible with GPL-3.0:

- **MIT License:** Eel, Bottle, Gevent, pytest, chardet
- **GPL v2:** Mutagen
- **BSD Licenses:** psutil, future
- **LGPL:** FFmpeg, libmediainfo

For complete information, see [DEPENDENCIES.md](DEPENDENCIES.md).

---

## Imprint

**Media Web Viewer**  
Developed by kazaa3  
Germany  

This application is provided as-is under GPL-3.0 license.  
For support, see Contact & Support section below.

## About

**Media Web Viewer v1.1.14**  
A modern desktop media player and library manager.  
Built with Python, Eel, and Bottle.  
Licensed under GNU GPL-3.0.

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

## Contact & Support

**Developer:** kazaa3  
**Location:** Germany  
**Repository:** https://github.com/kaaza3/media-web-viewer

---

**Last Updated:** 7. März 2026  
**Current Version:** 1.1.19

---

## Tools Used

During development, the following commands and tools were used:

- **grep:** For searching text patterns in files (e.g., `grep -r "version" .`)
- **sed:** For text replacement in files
- **find:** For locating files (e.g., `find . -name "*.py"`)
- **python -m py_compile:** For syntax checking Python files
- **pytest:** For running unit tests
- **git:** For version control and diff checking
