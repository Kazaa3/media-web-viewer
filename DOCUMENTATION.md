# Media Web Viewer - Comprehensive Documentation

**Version:** 1.1.18  
**License:** GNU General Public License v3 (GPL-3.0)  
**Author:** kazaa3 | Germany  

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
- **Open Source:** Licensed under GPL-3.0 for transparency and community contribution.

### Supported Formats

**Audio:** MP3, M4A (AAC), M4B (Audiobooks), FLAC, OGG (Vorbis/Opus), WAV, ALAC, WMA, AIFF, DSD  
**Video:** MP4, MKV, WebM (basic support)  
**Documents:** EPUB, PDF (basic support)

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
- **Logbook System:** Built-in development documentation and feature tracking in Markdown
- **Parser Performance Metrics:** Track timing and efficiency of each metadata parser

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
# https://github.com/MasterX360/media-web-viewer/releases

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

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

## Contact & Support

**Developer:** kazaa3  
**Location:** Germany  
**Repository:** https://github.com/MasterX360/media-web-viewer

---

**Last Updated:** 7. März 2026  
**Current Version:** 1.1.18
---

## Quick Start

### Option A: Install via .deb (Debian / Ubuntu)

> Download the latest `.deb` from [Releases](https://github.com/MasterX360/media-web-viewer/releases) and run:

```bash
sudo dpkg -i media-web-viewer_1.1.14_amd64.deb
sudo apt-get install -f   # installs missing dependencies if needed

# Start the app
media-web-viewer
```

---

## π©πͺ Deutsch (German)

Ein lokaler Desktop-Medienplayer und Bibliotheksverwalter mit einer eingebetteten webbasierten GUI. Entwickelt mit Python, [Eel](https://github.com/python-eel/Eel) und dem [Bottle](https://bottlepy.org/) Web-Framework. UnterstΓΌtzt eine Vielzahl von Audioformaten, darunter MP3, M4A, M4B (HΓΆrbΓΌcher), FLAC, OGG, WAV, ALAC und WMA.

---

## πΊπΈ English (Default)

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
sudo dpkg -i media-web-viewer_1.1.12_amd64.deb

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
sudo dpkg -i media-web-viewer_1.1.12_amd64.deb
```

---

## Features

- **Web-based GUI:** Modern HTML/CSS/JS interface powered by Eel (no Electron needed)
- **Player tab**: Real-time playback with Itemlist and player sidebar on GUI
- **Itemlist**: All playable elements
- **Player footer**: Real-time playback
- **Premium Sidebar**: Real-time display of media metadata and covers.
- **Smart Metadata Extraction:** Multi-parser pipeline using `mutagen`, `pymediainfo`, and `ffmpeg` fallback
- **Audiobook Support:** Automatic chapter detection and correct sorting for `.m4b` and long MP3 files
- **On-the-Fly Transcoding:** ALAC β FLAC and WMA β OGG via `ffmpeg` with transparent caching
- **Embedded Cover Art:** Extracts and displays cover images from MP3, FLAC, M4A, and MP4 containers
- **Media Library:** SQLite-backed library with an in-app metadata editor
- **File Browser:** Navigate your filesystem and add media directly from the app
- **Integrated Tests:** Run backend pytest suites from the "Tests" tab in the UI
- **Smart Categorization:** Advanced logic to distinguish between Albums, Singles, and Compilations
- **Sophisticated Metadata Parsing**: Extracts deep technical info (bitrate, codecs, tags) using a custom parser chain.
- **Parser Configuration:** Drag-and-drop reordering of the parser chain with enable/disable toggles
- **Debug Tools:** Real-time log viewer and configurable debug flags
- **Dynamic Test Suite**: Integrated GUI for running and managing media parsing tests.
- **Logbook:** Built-in development log and documentation viewer
- **Automatic Blacklist:** Built-in filter to ignore system files and junk (e.g., 'captcha', 'thumb', 'cover art')
- **Native System Integration:** Fully packaged `.deb` with auto-resolution of dependencies like `ffmpeg`
- **Internationalisierung**: Full documentation and UI support for German and English.
- **Natural Sorting**: Intelligent numerical sorting for chapters and titles.

---

### Supported Media Categories

The application automatically categorizes indexed items based on metadata and file patterns:

- **π΅ Audio:** General fallback for music without specific tags.
- **πΏ Album:** Music organized by album name or track length.
- **πΏ Single:** Music organized by multiple versions for the same song.
- **π Compilation:** Detection of "Various Artists" or "compilation" tags.
- **π» Klassik (Classical):** Enhanced detection for composers like **Beethoven, Mozart, Bach, Chopin** and "Klassik" keywords.
- **π HΓΆrbuch (Audiobook):** Specialized support for `.m4b` and long audio files including chapter navigation.
- **π¬ Film / Serie:** Detection for movie files and TV show patterns (Season/Staffel).
- **π E-Book / Dokument:** Support for EPUB, PDF and other document types.


---

## Project Structure

```
media-web-viewer/
βββ main.py               β Entry point, Eel setup, all backend API functions
βββ models.py             β MediaItem data model (parsing, transcoding flags)
βββ db.py                 β SQLite database logic (init, insert, query, clear)
βββ requirements.txt      β Python dependencies
βββ build_deb.sh          β Script to build a .deb package
βββ parsers/              β Metadata extraction pipeline
β   βββ filename_parser.py
β   βββ mutagen_parser.py
β   βββ ffmpeg_parser.py
β   βββ pymediainfo_parser.py
β   βββ format_utils.py   β Parser config persistence
βββ web/                  β Frontend + Bottle web server
β   βββ app.html          β Full UI (tabs: Player, Browser, Edit, Tests, Logbook, β¦)
β   βββ app_bottle.py     β Routes: /media/<file>, /cover/<file>
β   βββ script.js         β Additional JavaScript
    - `i18n.json`: Localization strings.
βββ tests/                β pytest unit tests
βββ logbuch/              β Development logbook (Markdown entries)
βββ packaging/            β .deb packaging files (DEBIAN/, usr/)
βββ media/                β Your media files go here (gitignored)
```

---

## Parser Pipeline

Each parser receives the current `tags` dict and only fills in missing values β it never overwrites data already found by an earlier parser.

| Order | Parser | Source | Provides |
|:-----:|--------|--------|----------|
| 1 | `filename_parser` | Filename | title, artist, file size |
| 2 | `container_parser` | Container format | container format |
| 3 | `mutagen_parser` | Mutagen lib | ID3/MP4/Vorbis tags, bitrate, samplerate, cover detection |
| 4 | `ffmpeg_parser` | FFmpeg CLI | Container format, codec, bit depth (fallback) |
| 5 | `pymediainfo_parser` | pymediainfo | Supplementary / missing metadata |

---

## Transcoding

Files with ALAC or WMA codec cannot be played natively in browsers. The app detects this and:

1. Sets `is_transcoded = True` in the database when codec = ALAC/WMA
2. The frontend appends `.flac_transcoded` or `.ogg_transcoded` to the URL
3. `app_bottle.py` intercepts the route, transcodes via `ffmpeg`, and caches the result in `media/.cache/`
4. The UI shows a warning that the file is being streamed as a transcoded format

---


## Build & Release
- Packages are built using `build_deb.sh` into `.deb` format for Debian/Ubuntu systems.
- Versions are tracked in `main.py`, `build_deb.sh`, and `packaging/DEBIAN/control`.

## Reset & Recovery
- The "Danger Zone" in Options allows for:
    - **Clear DB**: Only empties the media database.
    - **App Reset**: Restores factory settings by deleting the database and config files.



## Bootle
Bottle ist ein minimalistisches WSGI-Web-Framework für Python, das in einer einzigen Datei läuft und keine Abhängigkeiten außer der Standardbibliothek braucht. Es eignet sich perfekt für kleine APIs oder Apps wie deine Media-Library, wo du Routing und Templates schnell brauchst.

Kernfeatures
Routing: Dekoratoren wie @route('/path/<name>') mappen URLs zu Funktionen.

Templates: Eingebaute Engine für einfache HTML-Vorlagen (unterstützt Jinja2/Mako).

HTTP-Tools: Zugriff auf Forms, Cookies, Uploads und JSON.

Einfaches Beispiel
python
from bottle import route, run, template, request

@route('/hello/<name>')
def greet(name):
    return template('<h1>Hallo {{name}}!</h1>', name=name)

@route('/add', method='POST')
def add_track():
    title = request.forms.get('title')
    # Hier z.B. mutagen für Audio-Metadata
    return f'Track "{title}" hinzugefügt!'

run(host='localhost', port=8080, debug=True, reloader=True)
Starte mit python app.py – besuche localhost:8080/hello/Peter. Für Prod: Gunicorn nutzen.
 EEL
Eel ist eine Python-Bibliothek für Electron-ähnliche Desktop-Apps mit HTML/JS/CSS-Frontend und Python-Backend – ideal für deine Media-Library, da du JS-Kenntnisse hast. Sie startet einen lokalen Server, lädt HTML im Browser und verbindet via @eel.expose Python-Funktionen (z.B. mutagen) mit JS.
​
​

Setup und Struktur
Installiere mit pip install eel. Ordnerstruktur:

text
app.py          # Python-Backend
web/            # Frontend
  index.html
  style.css
  script.js
Eel serviert /eel.js automatisch für Bidirektionale Calls.

Einfaches Beispiel
app.py:

python
import eel

eel.init('web')  # Web-Ordner

@eel.expose
def scan_media(path):
    # Hier mutagen für FLAC/MKV etc.
    return f"Gefunden: {len(os.listdir(path))} Dateien"

eel.start('index.html', size=(1000, 600))
web/index.html:

xml
<!DOCTYPE html>
<html>
<head><title>Media Lib</title></head>
<body>
    <input id="path" type="text">
    <button onclick="scan()">Scan</button>
    <div id="result"></div>
    <script src="/eel.js"></script>
    <script>
        async function scan() {
            let path = document.getElementById('path').value;
            let result = await eel.scan_media(path)();
            document.getElementById('result').innerHTML = result;
        }
    </script>
</body>
</html>
Starte: python app.py – Browser öffnet automatisch.
​
​## Python als Backend

## Lizenz

Das Projekt "Media Web Viewer" ist unter der GNU General Public License Version 3 (GPL-3.0) lizenziert. Diese Lizenz erlaubt es, die Software frei zu verwenden, zu modifizieren und zu verteilen, solange alle Änderungen ebenfalls unter GPL-3.0 veröffentlicht werden und der Quellcode zugänglich bleibt. Für den vollständigen Text siehe die Datei [LICENSE.md](LICENSE.md).

## .deb-Paket Erstellung

Das Projekt wird als Debian-Paket (.deb) für Debian/Ubuntu-Systeme gebaut, um eine einfache Installation zu ermöglichen. Das Build-Skript `build_deb.sh` automatisiert den gesamten Prozess.

### Voraussetzungen für den Build

- Bash-Shell
- `dpkg-deb` (Teil von dpkg, standardmäßig auf Debian/Ubuntu installiert)
- `rsync` (für das Kopieren der Dateien)

### Build-Prozess im Detail

1. **Staging-Bereich vorbereiten**: Das Skript erstellt oder leert den Ordner `packaging/` und richtet die Struktur ein.
2. **Quellcode kopieren**: Mit `rsync` wird der gesamte Projektcode nach `packaging/opt/media-web-viewer/` kopiert, wobei unerwünschte Dateien wie `.git`, `.venv`, `__pycache__`, Build-Artefakte und Medien-Dateien ausgeschlossen werden.
3. **Skripte ausführbar machen**: Die DEBIAN-Skripte (`postinst`, `prerm`) und das Startskript (`usr/bin/media-web-viewer`) werden mit `chmod 755` ausführbar gemacht.
4. **Paket bauen**: `dpkg-deb --build --root-owner-group packaging/ media-web-viewer_VERSION_amd64.deb` erstellt das finale .deb-Paket.

### Paket-Struktur

Das .deb-Paket folgt den Debian-Standards:
- `DEBIAN/control`: Metadaten des Pakets (Name, Version, Abhängigkeiten, etc.)
- `DEBIAN/postinst`: Post-Installationsskript (z.B. für Setup)
- `DEBIAN/prerm`: Pre-Remove-Skript (z.B. für Cleanup)
- `opt/media-web-viewer/`: Der gesamte Anwendungscode
- `usr/bin/media-web-viewer`: Startskript im PATH
- `usr/share/applications/media-web-viewer.desktop`: Desktop-Eintrag für das Startmenü

### Installation und Nutzung

Nach dem Build kann das Paket installiert werden mit:
```bash
sudo dpkg -i media-web-viewer_VERSION_amd64.deb
sudo apt-get install -f  # Falls Abhängigkeiten fehlen
```

Starten: `media-web-viewer`

Deinstallation: `sudo apt remove media-web-viewer` (behaltet Konfiguration) oder `sudo apt purge media-web-viewer` (entfernt alles).

### Anpassungen

- **Version**: In `build_deb.sh` die Variable `VERSION` anpassen.
- **Architektur**: Standardmäßig `amd64`, kann geändert werden.
- **Inhalte**: Die rsync-Excludes in `build_deb.sh` können angepasst werden, um weitere Dateien einzuschließen oder auszuschließen.
- **Abhängigkeiten**: In `packaging/DEBIAN/control` die `Depends`-Zeile aktualisieren, falls neue Abhängigkeiten hinzukommen.

Für weitere Details siehe das Skript `build_deb.sh` und die Packaging-Dokumentation von Debian.

##Ja, du kannst absolut GPL-3.0 für dein GitHub-Projekt mit Python, Eel und Bottle verwenden – es ist voll kompatibel. Eel und Bottle sind beide MIT-lizenziert (permissiv), was mit GPL-3.0 harmoniert: Dein Projekt wird GPL, Dependencies bleiben unberührt.

Warum kompatibel?
MIT + GPL: Erlaubt Linking/Import in GPL-Projekte ohne Lizenzkonflikt – dein Code dominiert.

Python-spezifisch: Importe (z. B. import eel) triggern kein automatisches Lizenz-Upgrading der Libs.

Copyleft-Effekt: Nur dein App-Code muss GPL-konform bleiben; Eel/Bottle können weiterhin separat genutzt werden.
​
Dein GitHub-Nickname geht absolut für den Copyright in der GPL-3.0 – Pseudonyme sind legal und üblich. Es zählt als gültiger Identifikator, solange du nachweisbar der Autor bist (z. B. bei Streit via GitHub-Account).

Tipps für dein Repo
Füge LICENSE mit GPL-3.0 hinzu (wie zuvor beschrieben).
​

In requirements.txt oder README: Erwähne Dependencies und ihre MIT-Lizenzen.

Header in Python-Dateien: # Copyright (c) 2026 kaaza3\n# Licensed under GPL-3.0.

## Python Dependencies for Media Web Viewer
# This project is licensed under GNU General Public License v3 (GPL-3.0)
# See LICENSE.md and DEPENDENCIES.md for details
# 
# PYTHON PACKAGE DEPENDENCIES AND THEIR LICENSES:
# - MIT License: eel, bottle, bottle-websocket, pymediainfo, gevent, gevent-websocket, pytest, pytest-cov
# - GPL v2: mutagen (compatible with GPL v3)
# - BSD 3-Clause: psutil
# - BSD 2-Clause: future
#
# SYSTEM DEPENDENCIES (must be installed separately):
# - ffmpeg: LGPL v2.1 / GPL - Audio/Video transcoding and metadata extraction ✅ GPL-3.0 compatible
# - libmediainfo0v5: BSD 2-Clause - Media information library (via apt/package manager) ✅ GPL-3.0 compatible
# - python3-tk: Python Software Foundation - Python Tkinter for system file dialogs ✅ GPL-3.0 compatible
#
# All dependencies are compatible with GPL-3.0
#
# Installation:
#   sudo apt install ffmpeg libmediainfo0v5 python3-tk  # Debian/Ubuntu
#   pip install -r requirements.txt

# Web Framework & Desktop GUI
eel>=0.18.2                    # MIT License - Electron-like GUI framework
bottle>=0.13.0                 # MIT License - Lightweight web framework
bottle-websocket>=0.2.9        # MIT License - WebSocket plugin for Bottle

# Audio/Media Metadata Parsing
mutagen>=1.47.0                # GPL v2 - Audio metadata manipulation
pymediainfo>=7.0.1             # MIT License - Media information library

# Async & WebSocket Support
gevent>=25.9.1                 # MIT License - Coroutine-based networking
gevent-websocket>=0.10.1       # MIT License - WebSocket implementation for gevent

# Testing & Coverage
pytest>=8.0.0                  # MIT License - Test framework
pytest-cov>=4.1.0              # MIT License - Coverage plugin for pytest

# System & Utilities
psutil>=5.9.0                  # BSD 3-Clause License - System and process utilities
future>=1.0.0                  # BSD 2-Clause License - Python 2/3 compatibility





## GUI über eel mit Web Frontend


## MediaItem

## dict

## json

#


## media_library.db

## Parser

## get_category

## to_dict
        return {
            'name': self.name,
            'path': str(self.path),
            'duration': duration_str,
            'tags': filtered_tags,
            'type': self.type[1:] if self.type.startswith('.') else self.type,
            'category': self.category,
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format
        }


## Metadata Tags (Logbook)
The application uses specific HTML comment tags in Markdown files to drive the "Features" modal:
- `Category`: Grouping (e.g., UI, Parser).
- `Title_DE / Title_EN`: Bilingual titles.
- `Summary_DE / Summary_EN`: Bilingual summaries.
- `Status`: Current state (COMPLETED, ACTIVE, PLAN, TASK, DOCS).

## Metadata Tags Tests


## Config


###AUDIO_EXTENSIONS




###VIDEO_EXTENSIONS
Video / E-Book / Document (Non-Audio)
        if ext in VIDEO_EXTENSIONS:
            if any(k in path_str for k in ['serie', 'tv', 'season', 'staffel'])
			
			
			

# Datenbank
			## import sqlite3
import os
import json

from pathlib import Path

# Use a user-writable path for the database
DB_DIR = Path.home() / ".media-web-viewer"
DB_FILENAME = str(DB_DIR / "media_library.db")

def init_db():

def get_known_media_names():

def clear_media():

def insert_media(item_dict):


def get_all_media():

def get_media_path(name):
    """Gibt den vollen Dateipfad für einen Mediennamen zurück."""

def update_media_tags(name, tags_dict):
    """Aktualisiert die Tags eines Medien-Items in der Datenbank."""


def rename_media(old_name, new_name):
    """Benennt ein Medium in der DB um (nur das Feld 'name')."""


def delete_media(name):
    """Löscht ein Medium aus der DB."""

def get_db_stats():



## GUI üner HTML / CSS / JS
            loadLibrary();
            loadParserConfig();
            loadDebugFlags();
            loadTestSuites();
			
			
##Tags			
			
Media type
    if tags.get('codec'):
        tags['codec'] = format_codec(tags['codec'])
    if tags.get('container'):
        tags['container'] = format_container(tags['container'], file_type)
    if tags.get('tagtype'):
        tags['tagtype'] = format_tagtype(tags['tagtype'])
 
 
 tags['chapters']
 
 

## Efficiency Mode (Fast)



## Detail Mode (Full)
        if mode == 'full':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            for i, track in enumerate(media_info.tracks):
                tags['full_tags'][f"container_track_{i}_{track.track_type}"] = track.to_data()


# Basic Tags
arist
title
album
year
track 
totaltracks


## Chapters


## eXTENDED Tags
EInfach zu speichern, aber doch sehr groß in Summe




##Dateiformateguide

## whitelist

        whitelist = {
            'title', 'artist', 'album', 'year', 'genre', 'track', 'totaltracks',
            'disc', 'codec', 'bitdepth', 'samplerate', 'bitrate', 'size',
            'has_art', 'container', 'tagtype', '_parser_times', 'releasetype', 'compilation'
        }
		
		
		
# blacklist
 cover usw
 
 
##doc string für Doxygen
 Doxygen funktioniert gut mit Python – ideal für Docstrings in deinem GPL-3.0-Media-Library-Projekt (Eel/Bottle). Es parst Standard-Docstrings (""" ) und erzeugt HTML-Docs mit Indizes, Diagrammen.

Setup-Schritte
Installiere: sudo apt install doxygen graphviz python3-pip (MX Linux).
​

Für bessere Python-Support: pip install doxypy (Filter für Docstrings).

Erstelle Doxyfile: doxygen -g in /docs-Ordner.
​

Wichtige Doxyfile-Anpassungen
text
PROJECT_NAME = "Media-Library"
INPUT = ../src
FILE_PATTERNS = *.py
EXTRACT_ALL = YES
EXTRACT_PRIVATE = YES
OPTIMIZE_OUTPUT_JAVA = NO  # Für Python
INPUT_FILTER = "python doxypy_filter.py"  # Mit doxypy
GENERATE_HTML = YES
Python-Docstring-Beispiel
python
def scan_files(path: str) -> list:
    """
    Scannt Medien-Dateien mit mutagen/FFmpeg.

    @param path Pfad zum Ordner
    @return Liste von Dateien
    """
    pass
Laufe doxygen Doxyfile – öffne html/index.html.

Perfekt für GitHub-README oder Pages! Willst du ein volles Doxyfile-Beispiel?


##Formate
OGG


##Container#
None
mkv
mp4

#TAgs

#Dateiendungen



##env
# environment.yml
