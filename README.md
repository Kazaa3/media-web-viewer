# Media Web Viewer

A local desktop media player and library manager with an embedded web-based GUI. Built with Python, [Eel](https://github.com/python-eel/Eel), and the [Bottle](https://bottlepy.org/) web framework. Supports a wide range of audio formats including MP3, M4A, M4B (Audiobooks), FLAC, OGG, WAV, ALAC, and WMA.

## Technology Stack

```
Media Web Viewer
├── Backend (Python 3.11+)
│   ├── Eel Framework (Electron-like GUI)
│   ├── Bottle Web Framework (Media streaming)
│   ├── SQLite Database (Local storage)
│   └── FFmpeg (Transcoding)
├── Frontend (Web Technologies)
│   ├── HTML5/CSS3 (Responsive UI)
│   ├── Vanilla JavaScript (No frameworks)
│   └── Web Audio API (Playback)
├── Parsers (Metadata Extraction)
│   ├── Mutagen (Audio tags)
│   ├── pymediainfo (Media info)
│   └── FFmpeg (Fallback parsing)
└── Packaging
    ├── .deb (Debian/Ubuntu)
    └── PyInstaller (Standalone exe)
```

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

## Installation

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
sudo dpkg -i media-web-viewer_1.1.14_amd64.deb

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
sudo dpkg -i media-web-viewer_1.1.14_amd64.deb
```

---

## Features

- **Web-based GUI:** Modern HTML/CSS/JS interface powered by Eel (no Electron needed)
- **Player Tab:** Real-time playback with item list and player sidebar
- **Item Modal:** Detailed view for media items with metadata editing
- **Smart Metadata Extraction:** Multi-parser pipeline using `mutagen`, `pymediainfo`, and `ffmpeg` fallback
- **Audiobook Support:** Automatic chapter detection and correct sorting for `.m4b` and long MP3 files
- **On-the-Fly Transcoding:** ALAC → FLAC and WMA → OGG via `ffmpeg` with transparent caching
- **Embedded Cover Art:** Extracts and displays cover images from MP3, FLAC, M4A, and MP4 containers
- **Media Library:** SQLite-backed library with an in-app metadata editor
- **File Browser:** Navigate your filesystem and add media directly from the app
- **Integrated Tests:** Run backend pytest suites from the "Tests" tab in the UI
- **Parser Configuration:** Drag-and-drop reordering of the parser chain with enable/disable toggles
- **Debug Tools:** Real-time log viewer and configurable debug flags
- **Logbook:** Built-in development log and documentation viewer
- **Automatic Blacklist:** Built-in filter to ignore system files and junk (e.g., 'captcha', 'thumb', 'cover art')
- **Smart Categorization:** Advanced logic to distinguish between Albums, Singles, and Compilations
- **Native System Integration:** Fully packaged `.deb` with auto-resolution of dependencies like `ffmpeg`

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
├── VERSION               ← Central version number (e.g. 1.1.19)
├── main.py               ← Entry point, Eel setup, all backend API functions
├── models.py             ← MediaItem data model (parsing, transcoding flags)
├── db.py                 ← SQLite database logic (init, insert, query, clear)
├── requirements.txt      ← Python dependencies
├── build_deb.sh          ← Script to build a .deb package
├── parsers/              ← Metadata extraction pipeline
│   ├── filename_parser.py
│   ├── mutagen_parser.py
│   ├── ffmpeg_parser.py
│   ├── pymediainfo_parser.py
│   └── format_utils.py   ← Parser config persistence
├── web/                  ← Frontend + Bottle web server
│   ├── app.html          ← Full UI (tabs: Player, Browser, Edit, Tests, Logbook, …)
│   ├── app_bottle.py     ← Routes: /media/<file>, /cover/<file>
│   └── script.js         ← Additional JavaScript
├── tests/                ← pytest unit tests
├── logbuch/              ← Development logbook (Markdown entries)
├── packaging/            ← .deb packaging files (DEBIAN/, usr/)
└── media/                ← Your media files go here (gitignored)
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

## Transcoding

Files with ALAC or WMA codec cannot be played natively in browsers. The app detects this and:

1. Sets `is_transcoded = True` in the database when codec = ALAC/WMA
2. The frontend appends `.flac_transcoded` or `.ogg_transcoded` to the URL
3. `app_bottle.py` intercepts the route, transcodes via `ffmpeg`, and caches the result in `media/.cache/`
4. The UI shows a warning that the file is being streamed as a transcoded format

---

## License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for the full license text.

The MIT License is a permissive open-source license that allows you to use, modify, and distribute the software freely, as long as the original copyright notice and license are included in all copies or substantial portions of the software.
