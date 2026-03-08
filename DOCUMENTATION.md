# Media Web Viewer - Comprehensive Documentation

**Version:** 1.2.23  
**License:** GNU General Public License v3 (GPL-3.0)  
**Author:** kazaa3 | Germany  
### Global Versioning

The application uses a centralized versioning system defined in the `VERSION` file in the project root:

```text
1.2.23
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
- **VLC Integration:** Import VLC playlists (m3u8/m3u) into your library and export your library as VLC-compatible playlists

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
- **Environment Monitor:** Python version, virtual environment status, and system info displayed in Options tab
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
- **Dual File Picker API:** 
  - GUI-based file/folder selection with native OS dialogs (Tkinter)
  - CLI-based alternatives for SSH/headless environments (no GUI dependencies)

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
sudo dpkg -i media-web-viewer_1.2.23_amd64.deb

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
git clone https://github.com/kazaa3/media-web-viewer.git
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
sudo dpkg -i media-web-viewer_1.2.23_amd64.deb
sudo apt-get install -f
```

---

## .deb Package Creation

The project is built as a Debian package (.deb) for Debian/Ubuntu systems to enable easy installation. The build script `build_deb.sh` automates the entire process.

### Prerequisites for Building

- Bash shell
- `dpkg-deb` (part of dpkg, standard on Debian/Ubuntu)
- `rsync` (for copying files)

### Build Process in Detail

1. **Prepare Staging Area:** The script creates or empties the `packaging/` folder and sets up the structure.
2. **Copy Source Code:** Using `rsync`, the entire project code is copied to `packaging/opt/media-web-viewer/`, excluding unwanted files like `.git`, `.venv`, `__pycache__`, build artifacts, and media files.
3. **Make Scripts Executable:** The DEBIAN scripts (`postinst`, `prerm`) and the start script (`usr/bin/media-web-viewer`) are made executable with `chmod 755`.
4. **Build Package:** `dpkg-deb --build --root-owner-group packaging/ media-web-viewer_VERSION_amd64.deb` creates the final .deb package.

### Package Structure

The .deb package follows Debian standards:
- `DEBIAN/control`: Package metadata (name, version, dependencies, etc.)
- `DEBIAN/postinst`: Post-installation script (e.g., for setup)
- `DEBIAN/prerm`: Pre-removal script (e.g., for cleanup)
- `opt/media-web-viewer/`: The complete application code
- `usr/bin/media-web-viewer`: Start script in PATH
- `usr/share/applications/media-web-viewer.desktop`: Desktop menu entry

### Installation and Usage

After building, install the package with:
```bash
sudo dpkg -i media-web-viewer_VERSION_amd64.deb
sudo apt-get install -f  # If dependencies are missing
```

Start: `media-web-viewer`

Uninstall: `sudo apt remove media-web-viewer` (keeps config) or `sudo apt purge media-web-viewer` (removes everything).

### Adjustments

- **Version:** Adjust the `VERSION` variable in `build_deb.sh`.
- **Architecture:** Default is `amd64`, can be changed.
- **Contents:** The rsync excludes in `build_deb.sh` can be adjusted to include or exclude additional files.
- **Dependencies:** Update the `Depends` line in `packaging/DEBIAN/control` if new dependencies are added.

For more details, see the script `build_deb.sh` and Debian packaging documentation.

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

**Debug Files:**
- **Project-Local Log:** When started with `--debug`, a detailed log is written to `logs/debug.log` in the project directory.
- **User-Data Log:** General application logs are always written to `~/.media-web-viewer/app.log`.

**Log Suppression:**
To keep the console and log files clean, noisy third-party logs (e.g., `geventwebsocket`) are automatically suppressed (set to `WARNING` level) while the application is running.

#### VLC Playlist Integration

Media Web Viewer includes bidirectional integration with VLC Media Player:

**Import VLC Playlists:**
1. Navigate to **Video Player** tab (🎬)
2. Scroll to **VLC Playlist Integration** section
3. Click **📥 Playlist importieren** (Import Playlist)
4. Select your `.m3u8` or `.m3u` playlist file from VLC
5. Tracks are automatically parsed and added to your library

**Export to VLC:**
1. Open **Video Player** tab
2. Click **📤 Als Playlist exportieren** (Export as Playlist)
3. Choose save location for the `.m3u8` file
4. Open the exported playlist in VLC: `Media → Open File`

**Creating VLC Playlists:**
- In VLC: `View → Playlist → Right-click → Save Playlist to File`
- Choose format: M3U8 UTF-8 Extended (recommended)
- Supported formats: `.m3u8`, `.m3u` (m3u with UTF-8 support preferred)

**Features:**
- ✅ Preserves track order and metadata (duration, title, artist)
- ✅ Handles relative and absolute file paths
- ✅ Skips duplicates automatically (tracks already in library)
- ✅ Error reporting for missing files
- ✅ Full m3u8 extended format support with `#EXTINF` metadata

---

### π©πͺ Deutsch (German)

Ein lokaler Desktop-Medienplayer und Bibliotheksverwalter mit einer eingebetteten webbasierten GUI. Entwickelt mit Python, [Eel](https://github.com/python-eel/Eel) und dem [Bottle](https://bottlepy.org/) Web-Framework. Unterstützt eine Vielzahl von Audioformaten, darunter MP3, M4A, M4B (Hörbücher), FLAC, OGG, WAV, ALAC und WMA.

Die Installer richtet automatisch eine Python Virtual Environment ein und installiert alle Abhängigkeiten.

**Deinstallation:**
```bash
# Konfiguration beibehalten
sudo apt remove media-web-viewer

# Alles entfernen (purge)
sudo apt purge media-web-viewer
```

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

### Technology Tree

```
Media Web Viewer (v1.1.14)
├── Frontend Layer
│   ├── HTML5 / CSS3 (Glassmorphism)
│   ├── Vanilla JavaScript (ES6+)
│   ├── i18n.json (German/English)
│   └── Responsive Design
│
├── Communication Bridge (EEL)
│   ├── WebSocket Server
│   ├── @eel.expose API Decorators
│   └── JSON Serialization
│
├── Backend Layer
│   ├── Python 3.11+
│   ├── Eel Framework (GUI Bridge)
│   ├── Bottle Web Server (localhost:8888)
│   │   ├── Media Routes (/media/<file>)
│   │   └── Cover Art Routes (/cover/<file>)
│   └── Bottle WebSocket Plugin
│
├── Data Processing
│   ├── Parser Pipeline
│   │   ├── Filename Parser (Pure Python)
│   │   ├── Container Parser (Format Detection)
│   │   ├── Mutagen Parser (Tag Extraction)
│   │   ├── FFmpeg Parser (CLI Codec Detection)
│   │   └── pymediainfo Parser (Metadata Supplement)
│   └── Transcoding Engine
│       ├── FFmpeg CLI (ALAC→FLAC, WMA→OGG)
│       └── Cache Management (~/.media-web-viewer/transcoded_cache/)
│
├── Data Persistence
│   ├── SQLite Database (media_library.db)
│   ├── JSON Metadata Storage
│   ├── Config Files (config.json, parser_config.json)
│   └── Debug Flags (debug_flags.json)
│
├── System Integration
│   ├── .deb Packaging (Debian/Ubuntu)
│   ├── System File Dialogs (python3-tk)
│   ├── FFmpeg CLI (Audio/Video Processing)
│   └── mediainfo Library
│
└── Development & Testing
    ├── pytest Unit Tests
    ├── pytest-cov Coverage
    ├── Black Code Formatter
    ├── Flake8 Linter
    └── Git Version Control
```

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

## Bottle Web Framework

Bottle is a minimalist WSGI web framework for Python that runs in a single file with no dependencies other than the standard library. It's perfect for small APIs or apps like Media Web Viewer, where you need routing and templates quickly.

### Core Features

- **Routing:** Decorators like `@route('/path/<name>')` map URLs to functions.
- **Templates:** Built-in engine for simple HTML templates (supports Jinja2/Mako).
- **HTTP Tools:** Access to forms, cookies, uploads, and JSON.
- **Simple Example:**

```python
from bottle import route, run, template, request

@route('/hello/<name>')
def greet(name):
    return template('<h1>Hello {{name}}!</h1>', name=name)

@route('/add', method='POST')
def add_track():
    title = request.forms.get('title')
    # Here you could use mutagen for audio metadata
    return f'Track "{title}" added!'

run(host='localhost', port=8080, debug=True, reloader=True)
```

Start with `python app.py` – visit localhost:8080/hello/Peter. For production: Use Gunicorn.

---

## EEL Framework

EEL is a Python library for Electron-like desktop apps with HTML/JS/CSS frontend and Python backend – ideal for Media Web Viewer, since you have JS knowledge. It starts a local server, loads HTML in the browser, and connects via `@eel.expose` Python functions (e.g., mutagen) with JS.

### Setup and Structure

Install with `pip install eel`. Folder structure:

```
app.py          # Python backend
web/            # Frontend
  index.html
  style.css
  script.js
```

EEL serves `/eel.js` automatically for bidirectional calls.

### Simple Example

**app.py:**

```python
import eel

eel.init('web')  # Web folder

@eel.expose
def scan_media(path):
    # Here use mutagen/FFmpeg for FLAC/MKV etc.
    return f"Found: {len(os.listdir(path))} files"

eel.start('index.html', size=(1000, 600))
```

**web/index.html:**

```xml
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
```

Start: `python app.py` – Browser opens automatically.

---

## Python as Backend

Python serves as the robust backend for Media Web Viewer, handling all core logic, metadata parsing, database operations, and system integration. The architecture leverages Python's strengths in data processing and library ecosystem while providing a seamless bridge to the web-based frontend via EEL.

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

#### Player Tab

The **Player** tab is the primary interface for media playback and library browsing.

**Main Components:**

1. **Itemlist (Left Panel)**
   - Displays all indexed media items
   - Shows: Title, Artist, Album, Duration
   - Sorted by category (Album, Single, Compilation, Classical, Audiobook)
   - Real-time search and filtering
   - Context menu for quick actions (Play, Edit, Delete)

2. **Player Controls (Center)**
   - **Play/Pause Button:** Toggle playback
   - **Previous/Next Buttons:** Navigate tracks
   - **Progress Bar:** Seek to any position
   - **Volume Slider:** Adjust playback volume
   - **Time Display:** Current / Total duration

3. **Premium Sidebar (Right Panel)**
   - **Cover Art:** Embedded album artwork (fallback to default icon)
   - **Metadata Display:** 
     - Title, Artist, Album
     - Year, Genre, Track Number
     - Codec, Bitrate, Sample Rate
     - Container Format
   - **Related Info:** Album year, artist image (if available)

4. **Now Playing Footer**
   - Currently playing track information
   - Mini player controls
   - Volume indicator
   - Playback time slider

**Playback Features:**

- **Continuous Playback:** Automatically plays next track in queue
- **Repeat Modes:** Off, Repeat All, Repeat One
- **Shuffle:** Randomize track order
- **Volume Control:** 0-100%, mute option
- **Seek Precision:** Millisecond-accurate seeking
- **Transcoding Status:** Shows when playing converted files (ALAC→FLAC, WMA→OGG)

**Playlist Management:**

1. **Create Playlist**
   - Select one or more tracks using **Ctrl+Click**
   - Click **Create Playlist** button
   - Name your playlist and confirm
   - Playlist appears in dropdown list

2. **Save/Load Playlists**
   - Access from **Playlists** dropdown
   - Change playback order dynamically
   - Playlists persist in database

3. **Edit During Playback**
   - Reorder tracks via drag-and-drop
   - Remove tracks from current queue
   - Add new tracks from library

**Keyboard Shortcuts:**

- **Space:** Play/Pause
- **N:** Next Track
- **P:** Previous Track
- **M:** Mute/Unmute
- **+/-:** Volume Up/Down
- **Delete:** Remove from library

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

## GUI via EEL with Web Frontend

The user interface is implemented using EEL, which provides a seamless bridge between the Python backend and a modern web-based frontend. This approach eliminates the need for Electron while maintaining a native desktop application feel.

### Architecture Overview

- **Backend:** Python with EEL and Bottle servers
- **Frontend:** Vanilla JavaScript, HTML5, CSS3 with Glassmorphism effects
- **Communication:** Bidirectional via WebSocket (EEL) and HTTP (Bottle)
- **Styling:** Responsive design with dynamic event handling

### Key Components

**main.py:** Entry point with EEL setup and all backend API functions  
**web/app.html:** Complete UI with tabs (Player, Browser, Edit, Tests, Logbook, Options)  
**web/app_bottle.py:** Routes for media serving (`/media/<file>`) and cover art  
**web/script.js:** Frontend logic and EEL bridge calls  
**web/i18n.json:** Localization strings for German and English

### Wording & Terminology

Consistent terminology across the user interface:

#### UI Elements

- **Itemlist:** List of all playable media items
- **Item Modal:** Detail view/edit dialog for individual media file
- **Player Footer:** Bottom playback control bar
- **Premium Sidebar:** Right-side metadata display panel
- **Cover Art:** Embedded album artwork image
- **Browse/Browser Tab:** File navigator for adding media

#### Media Categories

- **Album:** Collection of tracks by artist(s)
- **Single:** Individual track or multiple versions of same song
- **Compilation:** Various artists collection
- **Klassik (Classical):** Orchestral/classical music with composer detection
- **Hörbuch (Audiobook):** Long-form audio with chapter navigation
- **Film/Serie:** Movie or TV series content

#### Technical Terms

- **Container:** File wrapper format (MP4, MKV, OGG, etc.)
- **Codec:** Audio/video compression algorithm
- **Parser:** Metadata extraction tool/method
- **Transcoding:** On-the-fly format conversion for browser compatibility
- **Tag:** Metadata field (title, artist, album, etc.)
- **Bitrate:** Audio encoding quality (kbps)
- **Sample Rate:** Audio sampling frequency (Hz)

#### Action Buttons

- **Scan Now:** Force immediate library re-indexing
- **Add Directory:** Include new folder in media library
- **Play:** Start playback
- **Create Playlist:** Group selected tracks
- **Save Changes:** Persist metadata edits to database

### Item Modal (Detail View)

The **Item Modal** provides comprehensive media file information and editing capabilities:

**Read-Only Fields:**

- **File Name:** Full filename with extension
- **File Path:** Complete file system path
- **File Size:** Total file size in bytes/MB
- **Duration:** Total playback time (HH:MM:SS)
- **Container:** Detected file container format
- **Codec:** Audio/video compression method
- **Bitrate:** Encoded data rate
- **Sample Rate:** Audio sampling frequency
- **Bit Depth:** Audio quantization level
- **Parser Times:** Performance metrics for each parser

**Editable Fields:**

- **Title:** Track or album name
- **Artist:** Creator/performer name
- **Album:** Album title
- **Year:** Release year (YYYY)
- **Genre:** Music category
- **Track Number:** Position in album
- **Total Tracks:** Album size
- **Disc Number:** Multi-disc position
- **Comments:** User notes or metadata

**Functional Buttons:**

- **Save Changes:** Persist edits to database and file tags
- **Test Stream:** Verify playback compatibility
- **Analyze:** Re-run parser pipeline for updated metadata
- **Delete:** Remove from library
- **Cancel:** Discard unsaved changes

### Initialization Sequence

```javascript
loadLibrary();
loadParserConfig();
loadDebugFlags();
loadTestSuites();
```

### Data Flow

1. User interaction triggers JavaScript event
2. JavaScript calls `eel.function_name(args)`
3. Python function processes request (database, parsing, etc.)
4. Result returned via callback, UI updates

---

## MediaItem Class

The `MediaItem` class represents individual media files with comprehensive metadata handling.

### Core Attributes

- `name`: Filename identifier
- `path`: Full file path
- `duration`: Formatted duration string
- `tags`: Dictionary of metadata tags
- `type`: File extension
- `category`: Auto-detected category (Album, Audiobook, etc.)
- `is_transcoded`: Boolean for transcoding requirement
- `transcoded_format`: Target format if transcoded

### Key Methods

**get_category():** Determines media category based on metadata patterns  
**to_dict():** Serializes object to dictionary for JSON storage

```python
def to_dict(self):
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
```

---

## Dictionary and JSON Storage

Media metadata is stored as Python dictionaries internally and serialized to JSON for database persistence and API communication.

### Storage Format

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
    "has_art": true
}
```

### Import/Export

```python
import json

# Load from database
tags = json.loads(db_row['tags'])

# Save to database
db_row['tags'] = json.dumps(tags)
```

---

## media_library.db

The SQLite database stores all media metadata and application state.

### Tables

- **media:** Main table with file information and JSON tags
- **playlists:** Playlist definitions
- **playlist_media:** Many-to-many relationship for playlist contents

### Database Operations

```python
import sqlite3
import os
import json
from pathlib import Path

# Use user-writable path
DB_DIR = Path.home() / ".media-web-viewer"
DB_FILENAME = str(DB_DIR / "media_library.db")

def init_db():
    # Create tables if not exist

def get_known_media_names():
    # Return list of indexed filenames

def clear_media():
    # Remove all media entries

def insert_media(item_dict):
    # Add new media item

def get_all_media():
    # Retrieve all media with filtering

def get_media_path(name):
    # Get full path for filename

def update_media_tags(name, tags_dict):
    # Update metadata for item

def rename_media(old_name, new_name):
    # Rename media entry

def delete_media(name):
    # Remove media entry

def get_db_stats():
    # Return database statistics
```

---

## Backend API Functions

The following functions are exposed via `@eel.expose` decorators and can be called from the frontend JavaScript.

### VLC Integration API

#### `import_vlc_playlist(m3u_path: str)`
Imports a VLC playlist (m3u8/m3u/XSPF) into the media library.

**Parameters:**
- `m3u_path` (str): Absolute path to the playlist file

**Returns:**
```python
{
    "status": "ok",
    "imported": [MediaItem, ...],  # List of imported items
    "skipped": ["file1.mp3", ...],  # Already in library
    "errors": ["error1", ...],       # Files not found or parse errors
    "count": 5                       # Number of imported items
}
```

**Example:**
```javascript
const result = await eel.import_vlc_playlist('/home/user/my_playlist.m3u8')();
if (result.error) {
    console.error('Import failed:', result.error);
} else {
    console.log(`Imported ${result.count} tracks`);
}
```

#### `export_playlist_to_vlc(media_names: list, output_path: str)`
Exports selected media items to a VLC-compatible m3u8 playlist.

**Parameters:**
- `media_names` (list): List of media item names from database
- `output_path` (str): Target path for the .m3u8 file

**Returns:**
```python
{
    "status": "ok",
    "path": "/home/user/exported.m3u8",
    "exported": 10,                  # Number of tracks
    "missing": ["file2.mp3", ...]    # Files not found
}
```

**Example:**
```javascript
const library = await eel.get_library()();
const mediaNames = library.media.map(item => item.name);
const result = await eel.export_playlist_to_vlc(mediaNames, '/home/user/export.m3u8')();
console.log(`Exported to: ${result.path}`);
```

### File Picker API (GUI - Tkinter)

#### `pick_folder()`
Opens a native folder selection dialog using Tkinter.

**Returns:**
- (str): Selected folder path or `None` if cancelled

**Example:**
```javascript
const folder = await eel.pick_folder()();
if (folder) {
    console.log('Selected folder:', folder);
}
```

**System Requirements:**
- Requires `python3-tk` system package on Linux
- Native OS dialogs (GTK on Linux, Aqua on macOS, Win32 on Windows)

#### `pick_file(title: str, filetypes: list)`
Opens a native file picker dialog (Tkinter-based).

**Parameters:**
- `title` (str): Dialog window title
- `filetypes` (list): List of `[description, extension]` tuples

**Returns:**
- (str): Selected file path or `None` if cancelled

**Example:**
```javascript
const filePath = await eel.pick_file('Select Playlist', [
    ['M3U8 Playlists', '*.m3u8'],
    ['All Files', '*.*']
])();
```

#### `pick_save_file(title: str, filetypes: list, default_name: str)`
Opens a native save file dialog.

**Parameters:**
- `title` (str): Dialog window title
- `filetypes` (list): List of file type filters
- `default_name` (str): Default filename

**Returns:**
- (str): Selected file path or `None`

**Example:**
```javascript
const savePath = await eel.pick_save_file(
    'Save Playlist',
    [['M3U8', '*.m3u8']],
    'my_playlist.m3u8'
)();
```

### File Picker API (CLI - No GUI Dependencies)

#### `pick_folder_cli(prompt: str)`
Terminal-based folder selection without GUI dependencies (SSH/Headless compatible).

**Parameters:**
- `prompt` (str): Input prompt text (default: "Ordnerpfad eingeben")

**Returns:**
- (str): Validated folder path or `None` if cancelled/invalid

**Example:**
```python
folder = pick_folder_cli("Bitte Scan-Verzeichnis angeben")
# User sees:
# > Bitte Scan-Verzeichnis angeben:
# > (Standard: /home/user)
# > /path/to/folder
```

**Features:**
- Validates folder existence
- Supports `~` for home directory (via `expanduser()`)
- Keyboard interrupt handling (Ctrl+C)
- Only Python stdlib (no tkinter required)

#### `pick_file_cli(prompt: str, extensions: list)`
Terminal-based file selection with optional extension filter.

**Parameters:**
- `prompt` (str): Input prompt text
- `extensions` (list): Optional list of allowed extensions (e.g., `['.m3u8', '.m3u']`)

**Returns:**
- (str): Validated file path or `None`

**Example:**
```python
file = pick_file_cli("Playlist importieren", ['.m3u8', '.m3u'])
# User sees:
# > Playlist importieren (Erlaubte Formate: .m3u8, .m3u):
# > /home/user/playlist.m3u8
```

**Features:**
- Validates: file exists, is a file, has correct extension
- Case-insensitive extension check
- User feedback on validation errors

#### `pick_save_file_cli(prompt: str, default_name: str, extensions: list)`
Terminal-based save file dialog with overwrite protection.

**Parameters:**
- `prompt` (str): Input prompt text
- `default_name` (str): Default filename if user presses Enter
- `extensions` (list): Optional list of allowed extensions

**Returns:**
- (str): Save path or `None`

**Example:**
```python
path = pick_save_file_cli("Playlist exportieren", "library.m3u8", ['.m3u8'])
# User sees:
# > Playlist exportieren (Formate: .m3u8):
# > (Standard: library.m3u8)
# > /home/user/export.m3u8
# > Datei 'export.m3u8' existiert. Überschreiben? (j/n): j
```

**Features:**
- Automatic extension addition if missing
- Overwrite confirmation for existing files
- Directory creation prompt if parent doesn't exist
- Empty input uses default filename

### System Information API

#### `get_environment_info()`
Returns detailed information about the Python runtime environment.

**Returns:**
```python
{
    "python_version": "3.11.2",
    "python_executable": "/opt/media-web-viewer/.venv/bin/python3",
    "python_prefix": "/opt/media-web-viewer/.venv",
    "python_base_prefix": "/usr",
    "in_venv": True,                      # Boolean: virtual environment active
    "venv_path": "/opt/media-web-viewer/.venv",  # or None
    "platform": "Linux-6.1.0-amd64-x86_64-with-glibc2.36",
    "platform_system": "Linux",
    "platform_release": "6.1.0"
}
```

**Example:**
```javascript
const env = await eel.get_environment_info()();
console.log(`Python ${env.python_version}`);
console.log(`Virtual Env: ${env.in_venv ? 'Yes' : 'No'}`);
if (env.venv_path) {
    console.log(`venv Path: ${env.venv_path}`);
}
```

**Use Cases:**
- Debugging deployment issues
- Displaying environment info in Options tab
- Verifying virtual environment activation
- System diagnostics

### VLC Player Control

#### `play_vlc(file_path: str)`
Plays a media file in an external VLC window using python-vlc bindings.

**Parameters:**
- `file_path` (str): Absolute path to media file

**Returns:**
```python
{"status": "ok"} or {"error": "error message"}
```

#### `stop_vlc()`
Stops the currently playing VLC instance.

**Returns:**
```python
{"status": "ok"}
```

---

## Parser Details

### Efficiency Mode (Fast)

Optimized for speed with basic metadata extraction:
- Focuses on essential tags (title, artist, album, codec)
- Stops parsing when critical information is found
- Ideal for large libraries

### Detail Mode (Full)

Comprehensive extraction including extended metadata:
- Runs all parsers regardless of existing data
- Includes comments, lyrics, technical details
- Trade-off: Slower but more complete

### Basic Tags

Core metadata fields extracted:
- artist
- title
- album
- year
- track
- totaltracks

### Chapters

For audiobooks and long-form content:
- Automatic chapter detection in M4B files
- Natural sorting for chapter order
- Navigation support in player

### Extended Tags

Additional metadata stored in `full_tags`:
- Container-specific information
- Technical codec details
- Track-level metadata from media containers

```python
if mode == 'full':
    if 'full_tags' not in tags:
        tags['full_tags'] = {}
    for i, track in enumerate(media_info.tracks):
        tags['full_tags'][f"container_track_{i}_{track.track_type}"] = track.to_data()
```

---

## File Format Guide

### Supported Formats

**Audio:**
- MP3, M4A, M4B, FLAC, OGG, WAV, ALAC, WMA, AIFF, DSD

**Video:**
- MP4, MKV, WebM

**Documents:**
- EPUB, PDF

### Whitelist

Allowed metadata fields for storage:
```python
whitelist = {
    'title', 'artist', 'album', 'year', 'genre', 'track', 'totaltracks',
    'disc', 'codec', 'bitdepth', 'samplerate', 'bitrate', 'size',
    'has_art', 'container', 'tagtype', '_parser_times', 'releasetype', 'compilation'
}
```

### Blacklist

Filtered out system and junk files:
- cover, thumb, captcha, etc.

---

## Doxygen Documentation

Doxygen works well with Python – perfect for GPL-3.0 Media Web Viewer project (EEL/Bottle). It parses standard docstrings (""") and generates HTML docs with indices, diagrams.

### Setup Steps

Install: `sudo apt install doxygen graphviz python3-pip` (MX Linux).  
For better Python support: `pip install doxypy` (filter for docstrings).

Create `Doxyfile`: `doxygen -g` in `/docs` folder.

### Important Doxyfile Adjustments

```
PROJECT_NAME = "Media-Library"
INPUT = ../src
FILE_PATTERNS = *.py
EXTRACT_ALL = YES
EXTRACT_PRIVATE = YES
OPTIMIZE_OUTPUT_JAVA = NO  # For Python
INPUT_FILTER = "python doxypy_filter.py"  # With doxypy
GENERATE_HTML = YES
```

### Python Docstring Example

```python
def scan_files(path: str) -> list:
    """
    Scan media files with mutagen/FFmpeg.

    @param path Path to folder
    @return List of files
    """
    pass
```

Run `doxygen Doxyfile` – open `html/index.html`.

Perfect for GitHub README or Pages! Great for GPL-3.0 project documentation.

---

## Formats, Containers, and Tags

### Audio Formats

- **OGG:** Container for Vorbis/Opus audio
- **FLAC:** Lossless audio codec
- **MP3:** MPEG-1 Audio Layer III
- **M4A:** MPEG-4 AAC audio
- **WAV:** Uncompressed PCM audio

### Containers

- **None:** Raw audio files
- **MKV:** Matroska multimedia container
- **MP4:** MPEG-4 multimedia container

### Tags

Metadata standards supported:
- ID3v2 (MP3)
- Vorbis comments (FLAC, OGG)
- MPEG-4 tags (M4A, MP4)
- RIFF INFO (WAV)

### File Extensions

- Audio: .mp3, .flac, .ogg, .m4a, .m4b, .wav, .alac, .wma, .aiff
- Video: .mp4, .mkv, .webm
- Documents: .epub, .pdf

---

## Environment Configuration

### environment.yml

For conda/pixi environments:

```yaml
name: media-web-viewer
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - ffmpeg
  - mediainfo
  - pip:
    - eel
    - bottle
    - mutagen
    - pymediainfo
    - pytest
```

---

## Feature Modal Refinements

The Feature Modal has been cleaned up for better UX.

**Duplication Removed:** Redundant "Project Documentation" button at top removed.  
**Categorization Improved:** Entries separated into:
- Latest Updates: Last 3 logbook entries
- Open Bugs: Dynamic from `logbuch/00_Known_Issues.md`
- Open Features: Non-completed features
- Project Documentation: Direct link
- Completed: Archive of finished tasks

---

## Debug Log Fixes

Debug logs from media parser now respect `parser` flag strictly.

```python
# parsers/media_parser.py
if debug and mode == 'full':
    logger(f"[Debug-Parser] 🚀 Full Mode activated for '{filename}' – collecting ALL tags!")
```

### Verification

1. **Build Verification:** Ran `bash build_deb.sh` and confirmed package: `media-web-viewer_1.2.23_amd64.deb`

2. **UI Verification:** Version 1.1.19 displayed correctly, Feature Modal shows latest entry 42_Wording.

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

#### Audio Formats
- **WAV (Plain):** Raw PCM audio, no metadata tags
- **MP3 (Plain):** Basic MPEG-1 Audio Layer III, minimal tags
- **MP3 (with ID3v2.2):** Enhanced metadata using ID3v2.2 standard
- **MP3 (with ID3v2.3/2.4):** Modern ID3 standards with full UTF-8 support
- **M4A (AAC):** MPEG-4 Audio with iTunes-compatible tags
- **M4B (Audiobooks):** MPEG-4 audiobook format, chapter-aware
- **FLAC:** Free Lossless Audio Codec with Vorbis comments
- **OGG (Vorbis/Opus):** Theora container with Vorbis/Opus audio
- **WAV (RIFF):** RIFF INFO tags support

#### Container Formats
- **MKV (with AAC):** Matroska container with Advanced Audio Coding
- **MKV (with FLAC):** Matroska with lossless FLAC audio
- **MP4 (with H.264):** MPEG-4 video container with H.264 codec
- **WebM:** VP8/VP9 video codec in WebM container

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

### Debug Flags Details

Debug flags enable detailed logging for specific application components:

- **parser**: Logs metadata parsing pipeline operations, parser chain execution, tag extraction
- **ui**: Logs user interface updates, event listeners, DOM modifications
- **db**: Logs database operations, SQLite queries, data persistence
- **system**: Logs system file operations, directory scanning, file I/O
- **player**: Logs playback operations, transcoding processes, audio stream handling

Enable with: `python main.py --debug` (activates all flags)

Or toggle individual flags in **Options → Debug Console**

### Options Window: General & Debug

The **Options** tab provides access to critical application settings, split into two sections:

#### Left Panel: General Settings
- Language selection (German/English)
- Library directories management
- Parser mode selection (Lightweight/Full)
- UI theme preferences
- Auto-scan intervals

#### Right Panel: General & Debug (Technical Parameters)

Manage technical parameters and debug flags here:

```
SYSTEM
├── Scan Directory
├── Clear Database
└── Reset Application

SCAN
├── Parser Mode
├── Auto-Index Interval
└── Blacklist Management

PARSER
├── Chain Configuration
├── Enable/Disable Parsers
├── Parser Reordering
└── Performance Metrics

PLAYER
├── Playback Settings
├── Transcoding Options
├── Cache Management
└── Stream Quality

DATABASE (DB)
├── Database Statistics
├── Optimize Database
├── Backup Configuration
└── Recovery Options
```

---

## Development

### Setting Up Development Environment

```bash
# 1. Clone and enter directory
git clone https://github.com/Kazaa3/media-web-viewer.git
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
- **Dictionary & JSON Storage:** Comments are stored as dictionaries and imported as JSON
  - Dictionary storage for metadata tags (Python native `dict` type)
  - JSON import/export for database persistence (`json.dumps()` / `json.loads()`)
  - Seamless bidirectional type conversion between Python objects and JSON strings
  - Type validation and schema enforcement for metadata fields
  - Automatic encoding/decoding with UTF-8 support for file storage

**Dictionary/JSON Conversion Pattern:**

```python
import json
from pathlib import Path

# Internal storage (Python dictionary)
tags = {
    'title': 'Song Title',
    'artist': 'Artist Name',
    'codec': 'MP3',
    '_parser_times': {
        'filename': 0.001,
        'mutagen': 0.045
    }
}

# Database storage (JSON string)
tags_json = json.dumps(tags, ensure_ascii=False)  # Serialize to JSON
db.insert_media(name, path, tags_json)

# Retrieval from database
tags_loaded = json.loads(db_row['tags'])  # Deserialize from JSON
# Now tags_loaded is a Python dict again for processing
```

**Best Practices:**

- Always use `json.dumps()` before database storage
- Always use `json.loads()` after database retrieval
- Validate data types before conversion
- Use `ensure_ascii=False` for internationalization support
- Implement schema validation for expected metadata fields
- Handle exceptions during JSON serialization/deserialization

**Database Layer:** [db.py](db.py)
- SQLite initialization and migrations
- CRUD operations for media items and playlists
- Query optimization and data filtering

**Parser System:** [parsers/](parsers/)
- Modular parser chain system
- Individual parsers for different metadata sources
- Configuration management and performance tracking

### Parser Architecture Details

Each parser accesses specific libraries and contributes to internal testing:

- **Filename Parser:** Pure Python string processing, no external libraries. Parses filename patterns for metadata hints.
- **Container Parser:** Uses `os.path.splitext()` and custom format detection for container type identification.
- **Mutagen Parser:** Accesses `mutagen` library for ID3/Vorbis/MP4 tag reading. Supports multiple audio formats.
- **FFmpeg Parser:** Calls `ffmpeg` CLI tool via `subprocess`, parses JSON output for codec and bitrate information.
- **pymediainfo Parser:** Uses `pymediainfo` library (MediaInfo wrapper) for supplementary container and track information.

Internal tests validate each parser's output against known test files, ensuring reliability and performance metrics.

#### Library Access Pattern

```python
# Each parser receives tags dict, never overwrites existing values
def parse(path, file_type, tags, mode='lightweight'):
    # Only add missing keys
    if 'title' not in tags:
        tags['title'] = extract_title(path)
    return tags
```

### Standards & Good Practice

This section outlines development standards and best practices for contributing to Media Web Viewer.

#### Code Style

**Python (Backend):**
- **Formatter:** Black (line length: 88 characters)
- **Linter:** Flake8 (E501 line length disabled for Black)
- **Type Hints:** Recommended for function signatures
- **Docstrings:** Use Google-style docstrings for all functions
- **Naming:** `snake_case` for functions/variables, `PascalCase` for classes

```python
# Good practice example
def extract_metadata(file_path: Path, mode: str = 'lightweight') -> dict:
    """
    Extract metadata from media file.
    
    Args:
        file_path: Path to media file
        mode: Parsing mode ('lightweight' or 'full')
        
    Returns:
        Dictionary containing metadata tags
    """
    tags = {}
    # Implementation
    return tags
```

**JavaScript/Frontend:**
- **Format:** Use semicolons and 2-space indentation
- **Naming:** `camelCase` for variables/functions
- **i18n:** Always use localization keys for user-facing strings
- **Comments:** Use `//` for inline comments

```javascript
// Good practice example
async function loadMediaLibrary() {
    try {
        const items = await eel.get_all_media()();
        renderItemlist(items);
    } catch (error) {
        console.error('Failed to load library:', error);
    }
}
```

#### Architecture Patterns

**Parser Chain Pattern:**
- Never overwrite existing metadata
- Always check `if key not in tags` before adding
- Return the modified tags dict
- Support both `lightweight` and `full` modes

**Database Operations:**
- Use parameterized queries to prevent SQL injection
- Always handle JSON serialization/deserialization
- Implement proper error handling with try/except
- Log database operations in debug mode

**EEL Function Exposure:**
- Use `@eel.expose` decorator for all backend functions
- Return JSON-serializable data (dicts, lists, primitives)
- Implement error handling with meaningful error messages
- Document function signatures in comments

####Testing & Quality Assurance

**Unit Tests:**
- Write tests in `tests/` directory
- Use pytest framework with fixtures for setup
- Aim for >80% code coverage
- Test both success and failure cases

```bash
# Run tests with coverage
pytest tests/ --cov=. --cov-report=html
```

**Code Quality Checks:**
```bash
# Format code with Black
black --line-length 88 .

# Check style with Flake8
flake8 --max-line-length=88 .

# Type checking with mypy
mypy --strict parsers/ models.py
```

**Before Committing:**
1. Run all code quality tools
2. Pass all tests (>80% coverage)
3. Update documentation
4. Write descriptive commit messages

#### Configuration Management

**Configuration Files:**
- Store all settings in JSON files (not hardcoded)
- Use clear, descriptive key names
- Include comments for complex settings
- Version your schema when changing structure

**Environment Variables:**
- Use for sensitive data (API keys, credentials)
- Prefix with `MEDIA_WEB_VIEWER_` for clarity
- Document all environment variables in README

#### Documentation Standards

**Markdown Files:**
- Use ATX-style headings (`#`, `##`, etc.)
- Include code examples for complex topics
- Use consistent terminology (see Wording section)
- Keep lines <100 characters for readability

**Docstrings:**
- Document public functions and classes
- Include type hints in docstring
- Provide usage examples for complex functions
- Reference related functions with links

#### Error Handling

**Best Practices:**
- Catch specific exceptions, not generic `Exception`
- Log errors with appropriate severity level
- Provide user-friendly error messages in UI
- Include debugging information for developers

```python
# Good practice
try:
    result = parse_media(file_path)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise UserError("Media file not found")
except Exception as e:
    logger.exception(f"Unexpected error parsing {file_path}: {e}")
    raise
```

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
- Check GitHub issues: https://github.com/kazaa3/media-web-viewer/issues

---

### Deutsch Troubleshooting

#### Von vorne anfangen
Falls du die App zuvor aus dem Quellcode ausgeführt hast oder alle Einstellungen zurücksetzen möchtest, beachte, dass `apt purge` **keine** Dateien in deinem Home-Verzeichnis entfernt. Um wirklich "von Null" zu starten:

```bash
# 1. Alte Benutzerkonfiguration und Datenbank entfernen
rm -rf ~/.config/gui_media_web_viewer ~/.media-web-viewer

# 2. Saubere Version neu installieren
sudo dpkg -i media-web-viewer_1.2.23_amd64.deb

# 3. Abhängigkeiten bei Bedarf reparieren
sudo apt-get install -f
```

---

## License

Media Web Viewer is licensed under the **GNU General Public License v3 (GPL-3.0)**. 

This means:
- ✅ You can freely use, modify, and distribute the software
- ✅ You must include the license text and copyright notice
- ✅ Any modifications or derived works must also be GPL-3.0
- ✅ Source code must be made available to users

See [LICENSE.md](LICENSE.md) for the complete license text.

### Python Dependencies for Media Web Viewer

This project is licensed under GNU General Public License v3 (GPL-3.0)  
See LICENSE.md and DEPENDENCIES.md for details

#### PYTHON PACKAGE DEPENDENCIES AND THEIR LICENSES:
- **MIT License:** eel, bottle, bottle-websocket, pymediainfo, gevent, gevent-websocket, pytest, pytest-cov
- **GPL v2:** mutagen (compatible with GPL v3)
- **BSD 3-Clause:** psutil
- **BSD 2-Clause:** future

#### SYSTEM DEPENDENCIES (must be installed separately):
- **ffmpeg:** LGPL v2.1 / GPL - Audio/Video transcoding and metadata extraction ✅ GPL-3.0 compatible
- **libmediainfo0v5:** BSD 2-Clause - Media information library (via apt/package manager) ✅ GPL-3.0 compatible
- **python3-tk:** Python Software Foundation - Python Tkinter for system file dialogs ✅ GPL-3.0 compatible

All dependencies are compatible with GPL-3.0

#### Installation:
```bash
sudo apt install ffmpeg libmediainfo0v5 python3-tk  # Debian/Ubuntu
pip install -r requirements.txt
```

#### Web Framework & Desktop GUI
- eel>=0.18.2                    # MIT License - Electron-like GUI framework
- bottle>=0.13.0                 # MIT License - Lightweight web framework
- bottle-websocket>=0.2.9        # MIT License - WebSocket plugin for Bottle

#### Audio/Media Metadata Parsing
- mutagen>=1.47.0                # GPL v2 - Audio metadata manipulation
- pymediainfo>=7.0.1             # MIT License - Media information library

#### Async & WebSocket Support
- gevent>=25.9.1                 # MIT License - Coroutine-based networking
- gevent-websocket>=0.10.1       # MIT License - WebSocket implementation for gevent

#### Testing & Coverage
- pytest>=8.0.0                  # MIT License - Test framework
- pytest-cov>=4.1.0              # MIT License - Coverage plugin for pytest

#### System & Utilities
- psutil>=5.9.0                  # BSD 3-Clause License - System and process utilities
- future>=1.0.0                  # BSD 2-Clause License - Python 2/3 compatibility

---

### GPL-3.0 Compatibility

Ja, du kannst absolut GPL-3.0 für dein GitHub-Projekt mit Python, Eel und Bottle verwenden – es ist voll kompatibel. Eel und Bottle sind beide MIT-lizenziert (permissiv), was mit GPL-3.0 harmoniert: Dein Projekt wird GPL, Dependencies bleiben unberührt.

Warum kompatibel?
MIT + GPL: Erlaubt Linking/Import in GPL-Projekte ohne Lizenzkonflikt – dein Code dominiert.

Python-spezifisch: Importe (z. B. import eel) triggern kein automatisches Lizenz-Upgrading der Libs.

Copyleft-Effekt: Nur dein App-Code muss GPL-konform bleiben; Eel/Bottle können weiterhin separat genutzt werden.

Dein GitHub-Nickname geht absolut für den Copyright in der GPL-3.0 – Pseudonyme sind legal und üblich. Es zählt als gültiger Identifikator, solange du nachweisbar der Autor bist (z. B. bei Streit via GitHub-Account).

Tipps für dein Repo
Füge LICENSE mit GPL-3.0 hinzu (wie zuvor beschrieben).

In requirements.txt oder README: Erwähne Dependencies und ihre MIT-Lizenzen.

Header in Python-Dateien: # Copyright (c) 2026 kaaza3\n# Licensed under GPL-3.0.

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

### Technical Stack

- **Backend:** Python 3.11+ with Eel and Bottle
- **Frontend:** Vanilla JavaScript, HTML5, CSS3 (Glassmorphism)
- **Database:** SQLite with JSON metadata storage
- **Metadata Parsing:** Mutagen, FFmpeg, pymediainfo
- **Packaging:** Debian .deb with automatic dependency resolution
- **Localization:** Bilingual i18n (German/English)

### Features Summary

- Multi-format audio/video support (MP3, FLAC, M4B, MKV, and more)
- Intelligent metadata extraction with custom parser chain
- Audiobook support with chapter detection
- Automatic transcoding for incompatible codecs
- Real-time library indexing with SQLite backend
- Integrated testing suite and debug tools
- Full GPL-3.0 open-source license

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

### Git Author Configuration

**Problem:** When committing changes (even from VS Code), the author appears as "Antigravity" instead of your username.

**Cause:** This project may have been worked on by an AI assistant (Antigravity) that set its own Git configuration in the repository. This configuration overrides your global Git settings and persists even when committing from VS Code.

**Solution - Set Repository-Specific Author:**
```bash
cd /path/to/gui_media_web_viewer

# Set your author name and email for this repository only
git config user.name "kazaa3"
git config user.email "kazaa3@local"

# Verify the change
git config user.name
# Output: kazaa3
```

**Solution - Set Global Author (affects all repositories):**
```bash
# Set author for all Git repositories on your system
git config --global user.name "kazaa3"
git config --global user.email "kazaa3@example.com"

# Verify
git config --global user.name
```

**Why This Happens:**
- Git uses a 3-tier config hierarchy: **system** → **global** → **local (repository)**
- Repository-local config (`.git/config`) has highest priority
- AI assistants or automated tools may set repository-specific config
- VS Code uses the Git CLI under the hood, so it respects `.git/config`

**How to Check Current Configuration:**
```bash
# Show all config values and their source
git config --list --show-origin

# Expected output includes:
# file:.git/config    user.name=kazaa3
# file:.git/config    user.email=kazaa3@local
```

**Permanent Fix:**
```bash
# Remove repository-specific author override (falls back to global)
git config --unset user.name
git config --unset user.email

# Then ensure your global config is set
git config --global user.name "kazaa3"
git config --global user.email "kazaa3@example.com"
```

### Git Branch Management & Cleanup

**Problem:** Multiple branches exist (e.g., `main`, `master`, `feature/xyz`) and you want to consolidate everything into `main` and remove outdated branches.

**Common Scenario:**
- Started with `master` as default branch
- Later switched to `main` as primary branch
- Feature branches from old development cycles still exist
- Need to clean up local and remote branches

**Step 1: Check Current Branch Status**
```bash
cd /path/to/gui_media_web_viewer

# Show all branches (local and remote)
git branch -a

# Example output:
#   feature/db-playlists
# * main
#   master
#   remotes/origin/feature/db-playlists
#   remotes/origin/main
#   remotes/origin/master
#   remotes/public-origin/main
```

**Step 2: Compare Branches**
```bash
# Check how many commits main is ahead/behind master
git rev-list --left-right --count main...origin/master

# Example output: "60  0" means:
# - main is 60 commits ahead
# - master has 0 unique commits
# - Safe to delete master

# Show visual commit history
git log --oneline --graph --all --decorate -20
```

**Step 3: Delete Local Branches**
```bash
# Delete merged local branches (safe)
git branch -d feature/db-playlists master

# Force delete unmerged branches (use with caution!)
git branch -D feature/db-playlists

# Example output:
# Branch feature/db-playlists entfernt (war 6ed929b).
# Branch master entfernt (war 29a6a09).
```

**Step 4: Push Main Branch with All Changes**
```bash
# Ensure all commits are on origin/main
git push origin main

# Example output:
# Objekte aufzählen: 71, fertig.
# Zähle Objekte: 100% (71/71), fertig.
# ...
# 320d10d..bc89e63  main -> main
```

**Step 5: Delete Remote Branches**
```bash
# Delete remote feature branches (works immediately)
git push origin --delete feature/db-playlists

# Example output:
# To https://github.com/Kazaa3/media-web-viewer.git
#  - [deleted]         feature/db-playlists

# Try to delete remote master branch
git push origin --delete master
```

**Step 6: Handle Protected Default Branch**

If you get this error:
```
! [remote rejected] master (refusing to delete the current branch: refs/heads/master)
Fehler: Fehler beim Versenden einiger Referenzen
```

**Cause:** The `master` branch is still the **default branch** on GitHub/GitLab.

**Solution - Change Default Branch on GitHub:**
1. Go to GitHub repository: `https://github.com/yourusername/media-web-viewer`
2. Click **Settings** tab
3. Click **Branches** in left sidebar
4. Under "Default branch", click the switch icon ↔️
5. Select `main` from dropdown
6. Click **Update** and confirm the warning
7. Now you can delete the old default branch:
   ```bash
   git push origin --delete master
   # Output: - [deleted]  master
   ```

**Step 7: Verify Final State**
```bash
# Check remaining branches
git branch -a

# Expected output (clean):
# * main
#   remotes/origin/main
#   remotes/public-origin/main
```

**Migration Status (8. März 2026):**
- Old repository `Kazaa3/gui_media_web_viewer` was deleted.
- Canonical repository is now `Kazaa3/media-web-viewer`.
- Only `main` branch remains on the active remote.
- Full commit history is preserved in `main`.

**Current Verification Commands:**
```bash
git remote -v
git branch -a
git ls-remote --symref origin HEAD
```

**Common Branch Management Commands:**
```bash
# List all branches with last commit
git branch -v

# List only remote branches
git branch -r

# Prune remote-tracking branches that no longer exist on remote
git remote prune origin

# Delete all local branches except main
git branch | grep -v "main" | xargs git branch -D

# Rename current branch
git branch -m old-name new-name

# Push renamed branch and delete old one on remote
git push origin new-name :old-name
```

**Best Practices:**
- ✅ Use `main` as primary branch (modern standard since 2020)
- ✅ Delete feature branches after merging into main
- ✅ Verify branch differences with `git rev-list --count` before deleting
- ✅ Always push main first, then delete old branches
- ✅ Change default branch on GitHub before deleting old default
- ⚠️ Never force-delete branches with unique commits without backing up
- ⚠️ Use `git branch -D` only when you're certain commits are elsewhere

### Git and Build Artifacts Management

**Problem:** After Git operations (clone, pull, branch cleanup), build artifacts like `.deb` packages and compiled binaries are missing.

**Cause:** Build artifacts are **intentionally excluded** from version control via `.gitignore` to keep the repository clean and focused on source code.

**Understanding Build Artifacts:**
Build artifacts are generated files that can be recreated from source code:
- `.deb` packages (e.g., `media-web-viewer_1.2.23_amd64.deb`)
- Compiled binaries and executables
- `build/` and `dist/` directories
- Python bytecode (`__pycache__/`, `*.pyc`)
- Generated documentation (`docs/html/`)

#### What Gets Excluded from Git (`.gitignore`)

**Build and Packaging:**
```gitignore
# Packaging and Build
build/
dist/
*.spec
*.deb
packaging/opt/media-web-viewer/media/
packaging/opt/media-web-viewer/Screens/
```

**Python Artifacts:**
```gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.mypy_cache/
```

**Media and Data:**
```gitignore
media/*
media_library.db
*.db
Screens/
*.log
```

**Why Exclude Build Artifacts:**
- ✅ Keeps repository size small (binaries are large)
- ✅ Makes Git history clean and focused on code changes
- ✅ Prevents merge conflicts on generated files
- ✅ Avoids tracking platform-specific binaries (Linux vs Windows)
- ✅ Forces developers to build from source (ensures reproducibility)
- ✅ Separates source code from distribution artifacts

#### Handling Missing Binaries After Git Operations

**Scenario 1: Fresh Clone**
```bash
# After cloning repository
git clone https://github.com/Kazaa3/media-web-viewer.git
cd media-web-viewer

# No binaries present - this is normal!
ls *.deb
# Output: ls: cannot access '*.deb': No such file or directory

# Solution: Build from source
bash build_deb.sh
# Creates: media-web-viewer_1.2.23_amd64.deb
```

**Scenario 2: After Branch Switch or Pull**
```bash
# Switch branches
git checkout main

# Binaries might be gone if they were in build/
ls build/
# Output: ls: cannot access 'build/': No such file or directory

# Solution: Rebuild
bash build_deb.sh
```

**Scenario 3: After Branch Cleanup**
```bash
# After deleting old branches
git branch -D feature/old-build

# Old build artifacts are local - still present unless manually deleted
ls *.deb
# Output: media-web-viewer_1.2.23_amd64.deb (current version)

# Solution: Clean and rebuild for current version
rm *.deb
bash build_deb.sh
```

#### Build Management Best Practices

**1. Local Build Workflow:**
```bash
# Always build in a clean virtual environment
source .venv/bin/activate

# Clean old builds before new build
rm -rf build/ dist/ *.deb

# Build fresh
bash build_deb.sh

# Output directory: Current directory
# Output file: media-web-viewer_<VERSION>_amd64.deb
ls -lh *.deb
# Expected: media-web-viewer_1.2.23_amd64.deb
```

**2. Version Management:**
```bash
# Build artifacts should match version in code
grep "VERSION =" main.py
# Output: VERSION = "1.2.23"

# Filename should match version
ls media-web-viewer_*.deb
# Expected: media-web-viewer_1.2.23_amd64.deb
```

**3. Storage and Distribution:**
```bash
# DO NOT commit binaries to Git
# Instead use GitHub Releases for distribution

# Option A: Manual upload to GitHub Releases
# 1. Go to https://github.com/Kazaa3/media-web-viewer/releases
# 2. Click "Create a new release"
# 3. Upload the .deb file
# 4. Add release notes

# Option B: Keep local backups outside Git repo
mkdir -p ~/releases/media-web-viewer
cp *.deb ~/releases/media-web-viewer/
```

**4. Clean Build Directory:**
```bash
# Remove all build artifacts (safe - can be regenerated)
git clean -fdX

# Explanation:
# -f = force
# -d = remove directories
# -X = only remove ignored files (.gitignore entries)

# This removes:
# - build/
# - dist/
# - *.deb
# - __pycache__/
# - *.pyc
# Does NOT remove: source code, configuration, .venv/
```

#### Checking Ignored Files

**See what Git ignores:**
```bash
# List all ignored files
git status --ignored

# Example output:
# Ignored files:
#   build/
#   dist/
#   media-web-viewer_1.2.23_amd64.deb
#   __pycache__/
#   .venv/
```

**Check if specific file is ignored:**
```bash
# Test if a file is ignored
git check-ignore -v media-web-viewer_1.2.23_amd64.deb

# Output:
# .gitignore:33:*.deb    media-web-viewer_1.2.23_amd64.deb
# Explanation: Line 33 of .gitignore excludes this file
```

#### Recovery and Backup Strategies

**If You Need to Preserve Old Builds:**
```bash
# BEFORE Git operations, backup important builds
mkdir -p ~/backup/builds
cp *.deb ~/backup/builds/
cp -r build/ ~/backup/builds/build-$(date +%Y%m%d)/

# After Git operations, restore if needed
cp ~/backup/builds/*.deb ./
```

**Create Release Archive:**
```bash
# Archive build with metadata
tar -czf media-web-viewer_1.2.23_build.tar.gz \
    media-web-viewer_1.2.23_amd64.deb \
    packaging/DEBIAN/control \
    build_deb.sh

# Store in safe location
mv media-web-viewer_1.2.23_build.tar.gz ~/releases/
```

#### Rebuilding from Clean Repository

**Complete rebuild from scratch:**
```bash
# 1. Clone fresh repository
git clone https://github.com/Kazaa3/media-web-viewer.git
cd media-web-viewer

# 2. Install system dependencies
sudo apt install ffmpeg libmediainfo0v5 python3-tk python3-dev build-essential python3-venv

# 3. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Build package
bash build_deb.sh

# 6. Verify build
ls -lh media-web-viewer_*.deb
dpkg-deb --info media-web-viewer_*.deb
```

**Expected build output:**
```
media-web-viewer_1.2.23_amd64.deb
Size: ~15MB (depends on version)
Architecture: amd64
```

#### Common Issues and Solutions

**Issue 1: "Binary missing after git pull"**
- ✅ **Expected behavior** - binaries are not in Git
- ✅ **Solution:** Run `bash build_deb.sh`

**Issue 2: "Old version .deb still present"**
- ⚠️ **Cause:** Manual builds leave old versions
- ✅ **Solution:** `rm *.deb` before building or rename old versions

**Issue 3: "Build fails after branch switch"**
- ⚠️ **Cause:** Contaminated build directory from old branch
- ✅ **Solution:** Clean build: `rm -rf build/ dist/` then rebuild

**Issue 4: "Accidentally committed .deb to Git"**
```bash
# If you committed a binary by mistake
git rm --cached media-web-viewer_*.deb
git commit -m "fix: Remove accidentally committed binary"

# Ensure .gitignore is correct
grep "*.deb" .gitignore
# Should output: *.deb
```

**Issue 5: "Want to track specific binary"**
```bash
# Force add despite .gitignore (NOT recommended)
git add -f media-web-viewer_1.2.23_amd64.deb

# Better: Use GitHub Releases or external storage
# Reason: Binaries bloat repository and history
```

#### CI/CD Considerations

**Automated Building:**
```bash
# In CI/CD pipeline (GitHub Actions example)
name: Build Package
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: sudo apt install -y ffmpeg libmediainfo0v5 python3-tk
      - name: Build package
        run: bash build_deb.sh
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: deb-package
          path: "*.deb"
```

**Benefits:**
- ✅ Consistent builds across environments
- ✅ Automated version tagging
- ✅ Automatic GitHub Release creation
- ✅ Source code remains clean in Git

#### Summary: What to Track vs. What to Ignore

**✅ Track in Git (Source Code):**
- Python source files (`*.py`)
- Configuration files (`*.json`, `*.yaml`)
- Documentation (`*.md`, `DOCUMENTATION.md`)
- Build scripts (`build_deb.sh`)
- Requirements (`requirements.txt`)
- Package metadata (`packaging/DEBIAN/control`)
- Tests (`tests/*.py`)

**❌ Ignore in Git (Generated/Build):**
- Compiled binaries (`*.deb`, executables)
- Build directories (`build/`, `dist/`)
- Python bytecode (`__pycache__/`, `*.pyc`)
- Virtual environments (`.venv/`, `venv/`)
- User data (`media/`, `*.db`, `Screens/`)
- IDE files (`.vscode/`, `.idea/`)

**🔰 Rule of Thumb:**
*"If it can be generated from source code, don't commit it to Git."*

---

## Auto-Launcher Script (run.sh)

### Overview

The `run.sh` script is a convenience launcher that automatically handles environment setup and dependency management. It eliminates the need for manual virtual environment activation and provides clear diagnostics about the Python environment being used.

**Location:** `/path/to/media-web-viewer/run.sh`

### Features

- ✅ **Automatic venv Detection & Creation**: Creates `.venv` if it doesn't exist
- ✅ **Dependency Management**: Checks and installs missing dependencies from `requirements.txt`
- ✅ **Environment Reporting**: Displays Python version, environment type (system/venv/conda), and paths
- ✅ **Clear Status Indicators**: Color-coded output (🟢 green for success, 🔴 red for errors)
- ✅ **One-Command Startup**: No manual activation required

### Usage

**Basic startup:**
```bash
cd /path/to/media-web-viewer
./run.sh
```

**With debug flag:**
```bash
./run.sh --debug
```

### What run.sh Does

1. **Checks for `.venv`** in the project directory
   - If missing: Creates new virtual environment with `python3 -m venv .venv`
   - If present: Skips creation

2. **Activates the environment**
   - Sources `source .venv/bin/activate`
   - Logs activation status

3. **Checks dependencies**
   - Reads `requirements.txt`
   - Tests if critical modules (mutagen, eel, bottle) are installed
   - Installs missing packages via `pip install -r requirements.txt` if needed

4. **Reports environment information**
   - Displays Python version
   - Shows environment path
   - Indicates environment type (.venv, conda, or system)
   - Shows executable location

5. **Launches the application**
   - Executes `python main.py` with any passed arguments

### Output Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 Media Web Viewer - Auto Launcher
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Aktiviere Umgebung...
✅ Umgebung bereit
Python 3.14.0
📦 /path/to/media-web-viewer/.venv
🚀 Starte Anwendung...
```

### Error Handling

If dependencies are missing or environment detection fails, run.sh provides clear error messages:

```
❌ Abhängigkeit 'mutagen' nicht installiert!
────────────────────────────────────────────
Installiere fehlende Abhängigkeiten...
pip install -r requirements.txt
```

---

## Logging System

### Overview

The Media Web Viewer uses a centralized, multi-destination logging system that captures application events both to the console and persistent log files.

### Log Locations

**Primary Log File:**
```
~/.media-web-viewer/app.log
```

**Log Configuration:**
- **Maximum File Size**: 5 MB (automatic rotation)
- **Backup Files**: Up to 3 rotated backups maintained
- **Encoding**: UTF-8
- **Format**: `YYYY-MM-DD HH:MM:SS [LEVEL] [MODULE] Message`

### Startup Logging

When the application starts, it automatically logs environment information:

```
════════════════════════════════════════════════════════════
[Startup] Application started - Environment Information
────────────────────────────────────────────────────────────
  Environment Type: Virtual Environment (venv)
  Environment Name: .venv
  Environment Path: /home/user/media-web-viewer/.venv
  Python Version: 3.14.0
  Python Executable: /home/user/media-web-viewer/.venv/bin/python
════════════════════════════════════════════════════════════
```

This information is helpful for:
- Verifying that the correct virtual environment is active
- Debugging environment-related issues
- Confirming Python version compatibility
- Troubleshooting import errors

### What Gets Logged

**Startup Events:**
- Environment detection results (venv/conda/system)
- Python version and paths
- Debug mode activation status
- Module initialization

**Runtime Events:**
- User interactions (file selection, playback)
- Database operations
- Media file scanning results
- Playback events
- API calls

**Error Events:**
- Missing dependencies (ModuleNotFoundError)
- File access errors
- Database errors
- Configuration issues

### Debug Mode

Enable detailed logging with the `--debug` flag:

```bash
./run.sh --debug
# or directly:
python main.py --debug
```

In debug mode:
- All `logging.debug()` calls are captured
- Additional diagnostic information is logged
- All debug flags are enabled
- Verbose output in console and log file

### Accessing Logs

**View real-time logs (console):**
```bash
./run.sh
# or
python main.py
```

**View all logged entries:**
```bash
cat ~/.media-web-viewer/app.log
```

**Monitor logs in real-time:**
```bash
tail -f ~/.media-web-viewer/app.log
```

**View only errors:**
```bash
grep "\[ERROR\]" ~/.media-web-viewer/app.log
```

**View debug entries:**
```bash
grep "\[DEBUG\]" ~/.media-web-viewer/app.log
```

### Log Rotation

When `app.log` reaches 5 MB, it automatically:
1. Renames current log to `app.log.1`
2. Renames `app.log.1` to `app.log.2`
3. Renames `app.log.2` to `app.log.3` (oldest, will be deleted)
4. Starts fresh `app.log` file

This ensures logs don't consume excessive disk space while maintaining recent history.

### Development Tips

**Adding Logging to Your Code:**
```python
import logging

logger = logging.getLogger(__name__)

# Information level (general flow)
logging.info("[ComponentName] Something happened")

# Debug level (detailed diagnostics)
logging.debug("[ComponentName] Detailed state: x=123, y=456")

# Warning level (potential issues)
logging.warning("[ComponentName] This might be a problem")

# Error level (something went wrong)
logging.error("[ComponentName] Operation failed: %s", error_message)
```

**Accessing logs from application code:**
```python
from logger import get_ui_logs

# Get all buffered logs as list
logs = get_ui_logs()

# Log is also available via the REST API:
# GET /api/debug/logs → Returns JSON array of log entries
```

---

## Contact & Support

**Developer:** kazaa3  
**Location:** Germany  
**Repository:** https://github.com/Kazaa3/media-web-viewer

---

**Last Updated:** 8. März 2026  
**Current Version:** 1.2.23

---

## Verification

### Build Verification
Ran `bash build_deb.sh` and confirmed the generated package: `media-web-viewer_1.2.23_amd64.deb`

### Version Consistency Verification
Ran `pytest -q tests/test_version_consistency.py` and confirmed that all central version references are derived from `VERSION` and no stale `.deb` version examples remain in the documentation.

### UI Verification
The version 1.2.23 is correctly displayed in the application and the Feature Modal shows the latest entries including VLC Integration (43), File-Picker API (44), Environment Info Display (45), Conda Environment Support (46), and Version Consistency Test (47).

---

## Tools Used

During development, the following commands and tools were used:

### Text Processing & Search
- **grep:** For searching text patterns in files (e.g., `grep -r "version" .`)
- **sed:** For text replacement and stream editing in files
- **awk:** For pattern scanning and processing text

### File & Directory Management
- **find:** For locating files (e.g., `find . -name "*.py"`)
- **ls:** For listing directory contents
- **mkdir:** For creating directories (e.g., `mkdir -p packaging/`)
- **rsync:** For efficient file synchronization and backup

### Python Tools & Commands
- **python -m py_compile:** For syntax checking Python files
- **pytest:** For running unit tests and test suites
- **python -m venv:** For creating virtual environments
- **pip:** For package management and dependency installation

### Version Control & Build
- **git:** For version control, diff checking, and branch management
- **bash:** For shell scripting and build automation (build_deb.sh)
- **dpkg-deb:** For building Debian packages
- **chmod:** For setting file permissions (e.g., `chmod 755`)

### Development & Testing
- **black:** For Python code formatting
- **flake8:** For linting and style checking
- **mypy:** For static type checking
- **pytest-watch:** For continuous test running
- **pytest-cov:** For test coverage reporting
