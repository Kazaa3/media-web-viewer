# Media Web Viewer

A local desktop media player and library manager with an embedded web-based GUI. Built with Python, [Eel](https://github.com/python-eel/Eel), and the [Bottle](https://bottlepy.org/) web framework. Supports a wide range of audio formats including MP3, M4A, M4B (Audiobooks), FLAC, OGG, WAV, ALAC, and WMA.

---

## Quick Start

### Option A: Install via .deb (Debian / Ubuntu)

> Download the latest `.deb` from [Releases](../../releases) and run:

```bash
sudo dpkg -i media-web-viewer_1.0.0_amd64.deb
sudo apt-get install -f   # installs missing dependencies if needed

# Start the app
media-web-viewer
```

The installer automatically sets up a Python virtual environment and installs all dependencies.

**Uninstall:**
```bash
sudo apt remove media-web-viewer
```

---

### Option B: Run from Source

**Requirements:**
- Python 3.11+
- `ffmpeg` in your PATH (for transcoding and metadata fallback)

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
sudo dpkg -i media-web-viewer_1.0.0_amd64.deb
```

---

## Features

- **Web-based GUI:** Modern HTML/CSS/JS interface powered by Eel (no Electron needed)
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

---

## Project Structure

```
media-web-viewer/
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
| 2 | `mutagen_parser` | Mutagen lib | ID3/MP4/Vorbis tags, bitrate, samplerate, cover detection |
| 3 | `ffmpeg_parser` | FFmpeg CLI | Container format, codec, bit depth (fallback) |
| 4 | `pymediainfo_parser` | pymediainfo | Supplementary / missing metadata |

---

## Transcoding

Files with ALAC or WMA codec cannot be played natively in browsers. The app detects this and:

1. Sets `is_transcoded = True` in the database when codec = ALAC/WMA
2. The frontend appends `.flac_transcoded` or `.ogg_transcoded` to the URL
3. `app_bottle.py` intercepts the route, transcodes via `ffmpeg`, and caches the result in `media/.cache/`
4. The UI shows a warning that the file is being streamed as a transcoded format

---

## License

This project is open source and free to use.
