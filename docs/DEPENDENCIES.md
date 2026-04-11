# Third-Party Dependencies and Licenses (v1.34)

dict (v1.34) is licensed under the **GNU General Public License v3 (GPL-3.0)**.

All third-party dependencies used in this project are listed below with their respective licenses. All dependencies are compatible with GPL-3.0.

## Production Dependencies

### Web Framework & Desktop GUI

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| **eel** | >=0.18.2 | MIT | Electron-like Python GUI framework for creating desktop apps with web technologies |
| **bottle** | >=0.13.0 | MIT | Lightweight WSGI web framework for REST API and routing |
| **bottle-websocket** | >=0.2.9 | MIT | WebSocket support plugin for Bottle framework |

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| **mutagen** | >=1.47.0 | GPL v2 | Audio metadata extraction and manipulation (ID3, Vorbis, etc.) |
| **pymediainfo** | >=7.0.1 | MIT | Media file information parsing using libmediainfo |
| **m3u8** | >=4.1.0 | MIT | m3u8 playlist parsing and manipulation |
| **python-vlc** | >=3.0.18121 | MIT | VLC media player bindings for external video playback |
| **pycdlib** | >=1.14.0 | LGPL v2 | ISO/Disk Image metadata and directory structure parsing |
| **isoparser** | >=0.2.0 | MIT | ISO 9660 structure and metadata parsing |

### Async & Communication

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| **gevent** | >=25.9.1 | MIT | Coroutine-based asynchronous I/O and networking |
| **gevent-websocket** | >=0.10.1 | MIT | WebSocket implementation using gevent |

### System & Utilities

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| **psutil** | >=5.9.0 | BSD 3-Clause | Cross-platform system and process utilities |
| **future** | >=1.0.0 | BSD 2-Clause | Python 2/3 compatibility layer |
| **chardet** | >=5.0.0 | LGPL | Universal character encoding detector for text files and metadata |
| **six** | >=1.16.0 | MIT | Python 2 and 3 compatibility library (required by isoparser) |

## Development Dependencies

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| **pytest** | >=8.0.0 | MIT | Testing framework for Python |
| **pytest-cov** | >=4.1.0 | MIT | Code coverage measurement plugin for pytest |
| **flake8** | >=7.0.0 | MIT | Linting and style checks (PEP8-focused) |
| **mypy** | >=1.9.0 | MIT | Static type checking for type annotations / TypedDict |
| **markdown** | >=3.5.0 | BSD | Markdown parsing for documentation validation tests |

## License Compatibility

All dependencies are compatible with GPLv3:

- **MIT License**: Permissive, fully compatible with GPLv3 ✅
- **GPL v2**: Compatible with GPL v3 (mutagen can be used under GPLv3) ✅
- **BSD Licenses**: Permissive, fully compatible with GPLv3 ✅
- **LGPL**: Compatible with GPLv3 (chardet and pycdlib can be used under GPLv3) ✅

## System Dependencies

Besides Python packages, dict also requires the following system-level tools:

| Package | Version | License | Compatibility | Purpose | Installation |
|---------|---------|---------|---|---------|---------------|
| **ffmpeg** | latest | LGPL v2.1 / GPL | ✅ GPLv3 | Audio/video transcoding and metadata extraction | `sudo apt install ffmpeg` |
| **libmediainfo0v5** | latest | BSD 2-Clause | ✅ GPLv3 | Media file information library (required by pymediainfo) | `sudo apt install libmediainfo0v5` |
| **doxygen** | latest | GPL v2 | ✅ GPLv3 | Documentation generator | `sudo apt install doxygen` |
| **google-chrome-stable** | latest | Proprietary | ✅ Compatible | Web browser for Eel UI | `sudo apt install google-chrome-stable` |
| **shared-mime-info** | latest | LGPL-2.1+ | ✅ GPLv3 | MIME database for file type detection | `sudo apt install shared-mime-info` |
| **libgdk-pixbuf2.0-0** | latest | LGPL-2.1+ | ✅ GPLv3 | GDK Pixbuf loaders for image support | `sudo apt install libgdk-pixbuf2.0-0` |

**License Compatibility Note:** All system dependencies are compatible with GNU General Public License v3 (GPL-3.0). FFmpeg's LGPL v2.1 is compatible with GPLv3, and BSD licenses are permissive allowing use under GPLv3.

**Runtime dependency model for MediaInfo:**
- Install `pymediainfo` via `pip` in your active Python environment (venv/conda).
- Install `mediainfo` / `libmediainfo` via the OS package manager (`apt`, `dnf`, `brew`).
- The system library/CLI is not part of the Python venv; both layers are required for reliable metadata parsing.

### Installation of System Dependencies (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install ffmpeg libmediainfo0v5 doxygen google-chrome-stable shared-mime-info libgdk-pixbuf2.0-0
```

### Installation of System Dependencies (Fedora/RHEL)

```bash
sudo dnf install ffmpeg mediainfo doxygen google-chrome-stable
```

### Installation of System Dependencies (macOS)

```bash
brew install ffmpeg mediainfo doxygen
```

## Additional Information

For full license texts, refer to the individual package repositories:

- [Eel](https://github.com/python-eel/Eel/blob/master/LICENSE)
- [Bottle](https://github.com/bottlepy/bottle/blob/master/LICENSE)
- [Mutagen](https://github.com/quodlibet/mutagen/blob/master/COPYING)
- [Gevent](https://github.com/gevent/gevent/blob/master/LICENSE.rst)
- [pytest](https://github.com/pytest-dev/pytest/blob/main/LICENSE)
- [psutil](https://github.com/giampaolo/psutil/blob/master/LICENSE)
- [future](https://github.com/PythonCharm/python-future/blob/master/LICENSE.txt)
- [chardet](https://github.com/chardet/chardet/blob/master/LICENSE)
- [FFmpeg](https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md)
- [MediaInfo](https://mediaarea.net/en/MediaInfo/License)

## Installing with License Information

### Step 1: Install System Dependencies

For Debian/Ubuntu:
```bash
sudo apt update
sudo apt install ffmpeg libmediainfo0v5 doxygen google-chrome-stable shared-mime-info libgdk-pixbuf2.0-0
```

For Fedora/RHEL:
```bash
sudo dnf install ffmpeg mediainfo doxygen google-chrome-stable
```

### Step 2: Install Python Packages

```bash
pip install -r requirements.txt
```

Each package will be installed with its respective license terms. Please review the `LICENSE` or `COPYING` files in installed packages for detailed information.

### Verification

To verify all dependencies are correctly installed:
```bash
# Check Python packages
pip list

# Check lint/type tools
flake8 --version
mypy --version

# Check system tools
ffmpeg -version
mediainfo --version
```
