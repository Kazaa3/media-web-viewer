# Media Web Viewer (v1.2.22)

Kompakte Projektübersicht. Das vollständige Technical Manual liegt in [DOCUMENTATION.md](DOCUMENTATION.md).

## Quick Start

### Debian/Ubuntu (.deb)
```bash
sudo dpkg -i media-web-viewer_1.2.22_amd64.deb
sudo apt-get install -f
media-web-viewer
```

### From Source
```bash
git clone https://github.com/Kazaa3/media-web-viewer.git
cd media-web-viewer
mamba env create -f environment.yml
mamba activate media-web-viewer
python main.py
```

## Core Stack
- Backend: Python 3.11+, Bottle, Eel
- Frontend: HTML5/CSS3, Vanilla JavaScript
- Database: SQLite (`media_library.db`)
- Media Tooling: Mutagen, pymediainfo, FFmpeg

## Docs
- Technical Manual: [DOCUMENTATION.md](DOCUMENTATION.md)
- Dependencies & licenses: [DEPENDENCIES.md](DEPENDENCIES.md)
- License: [LICENSE.md](LICENSE.md)

Developed by **kazaa3**.
