# Media Web Viewer (v1.2.21)

Media Web Viewer is a sleek, modern desktop application for browsing and playing media libraries (music, audiobooks, and basic video support). Built with Python (Eel) and Vanilla JS/HTML/CSS, it prioritizes a premium user experience and detailed metadata extraction.

---

## 🚀 Quick Start

### Installation via .deb (Debian / Ubuntu)
Download the latest `.deb` from [Releases](https://github.com/MasterX360/media-web-viewer/releases) and run:
```bash
sudo dpkg -i media-web-viewer_1.2.21_amd64.deb
sudo apt-get install -f   # Installs missing system dependencies
media-web-viewer          # Start the app
```

### Run from Source
```bash
# Clone and enter directory
git clone https://github.com/Kazaa3/media-web-viewer.git
cd media-web-viewer

# Install dependencies and run
mamba env create -f environment.yml
mamba activate media-web-viewer
python main.py
```

---

## ✨ Key Features
- **Smart Metadata Extraction**: Multi-parser pipeline (`mutagen`, `pymediainfo`, `ffmpeg`).
- **Audiobook Support**: Specialized `.m4b` handling with chapter navigation.
- **On-the-Fly Transcoding**: Transparent ALAC/WMA → FLAC/OGG conversion.
- **Modern UI**: Glassmorphism design with responsive Vanilla JS/CSS.
- **Integrated Tools**: Built-in test suite, dev-logbook, and metadata editor.

---

## 🛠️ Technical Overview
- **Backend**: Python 3.11+ using the **Bottle** framework and **Eel** bridge.
- **Frontend**: Responsive HTML5/CSS3 and Vanilla JavaScript.
- **Persistence**: SQLite database (`media_library.db`) with optimized JSON storage.
- **Packaging**: Native Debian packaging for deep Linux integration.

---

## 📖 Documentation
For a deep dive into the technical architecture, database schema, and development standards, please refer to:
👉 **[DOCUMENTATION.md](DOCUMENTATION.md)**

---

## 🏗️ Project Structure
```text
media-web-viewer/
├── VERSION               ← Central version number
├── Doxyfile              ← Doxygen configuration
├── environment.yml       ← Conda/Mamba environment setup
├── main.py               ← App entry point & Backend API
├── models.py             ← MediaItem data model
├── db.py                 ← Persistence layer layer
├── parsers/              ← Metadata extraction pipeline
│   ├── media_parser.py   ← Parser orchestrator
│   ├── filename_parser.py
│   ├── container_parser.py
│   ├── mutagen_parser.py
│   ├── ffmpeg_parser.py
│   ├── pymediainfo_parser.py
│   └── format_utils.py   ← Config & formatting
├── web/                  ← Frontend (HTML/CSS/JS)
│   ├── app.html          ← Main UI
│   └── app_bottle.py     ← API & Streaming
├── tests/                ← Unit & Integration tests
├── logbuch/              ← Dev-log entries
└── packaging/            ← .deb build files
```

---

## ⚖️ License
This project is licensed under the **GNU General Public License v3 (GPL-3.0)**. See [LICENSE.md](LICENSE.md) for details.

Developed by **kazaa3**.
