# Media Web Viewer (v1.1.23)

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

## Startup Modes

### Normal Mode (Full Backend)
```bash
python main.py
# → Starts Eel/WebSocket server, opens browser automatically
```

### Headless Mode (No GUI)
```bash
python main.py --ng
# → Initializes DB, shows stats, exits (for scripts/CI)
```

### Connectionless Mode (Frontend Only)
```bash
python main.py --n
# → Opens UI in browser without backend (for UI development)
```

## Build System

### Quick Build
```bash
# Build Debian package
python build_system.py --build deb

# Build standalone executable
python build_system.py --build pyinstaller

# Full build with tests
python build_system.py --full-build
```

### Development
```bash
# Run tests
python build_system.py --test

# Code quality checks
python build_system.py --lint --type-check

# Clean build artifacts
python build_system.py --clean-all
```

## Docs
- Technical Manual: [DOCUMENTATION.md](DOCUMENTATION.md)
- Dependencies & licenses: [DEPENDENCIES.md](DEPENDENCIES.md)
- License: [LICENSE.md](LICENSE.md)

Developed by **kazaa3**.
