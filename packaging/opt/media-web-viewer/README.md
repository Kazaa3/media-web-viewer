# Media Web Viewer (v1.3.3)

Kompakte Projektübersicht. Das vollständige Technical Manual liegt in [DOCUMENTATION.md](DOCUMENTATION.md).

## Quick Start

### Debian/Ubuntu (.deb)
```bash
sudo dpkg -i media-web-viewer_1.3.3_amd64.deb
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
- VLC Support: m3u8 (playlist import/export), python-vlc

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

## Playback Fallback Behavior
- Browser playback errors like `NotSupportedError` (unsupported codec/source) are handled gracefully.
- The UI now shows a readable status message instead of a noisy global promise popup.
- Recommended fallback: switch to **VLC mode** for unsupported media sources.

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

## Release Verification

```bash
# Full release pipeline (sync + build + reinstall validation)
python build_system.py --pipeline

# Optional: include destructive reinstall validation
python build_system.py --pipeline --destructive

# Manual checks (if needed)
python tests/test_version_sync.py
python tests/test_reinstall_deb.py
RUN_DESTRUCTIVE_TESTS=1 python tests/test_reinstall_deb.py
```

## CI/CD Pipelines

### Main Branch Artifacts (no GitHub Release)
On every push to `main`, the workflow [ci-artifacts.yml](.github/workflows/ci-artifacts.yml) builds and uploads:
- Linux executable (`dist/MediaWebViewer`)
- Debian package (`media-web-viewer_*_amd64.deb`)

### Tagged Release (auto-publish to GitHub Releases)
When you push a tag like `v1.3.3`, the workflow [release.yml](.github/workflows/release.yml):
- builds Linux executable + Debian package + Windows `.exe`
- creates/updates the GitHub Release
- uploads all binaries as release assets

```bash
git tag -a v1.3.3 -m "Release v1.3.3"
git push origin main --tags
```

### Release Checklist (recommended)
```bash
# 1) Verify version consistency
python tests/test_version_sync.py

# 2) Run release validation pipeline
python build_system.py --pipeline

# 3) Commit release-related changes
git add VERSION main.py .github/workflows/release.yml .github/workflows/ci-artifacts.yml
git commit -m "Release v1.3.3"

# 4) Create and push release tag
git tag -a v1.3.3 -m "Release v1.3.3"
git push origin main --tags
```

### Local Build Artifact Cleanup
Use the cleanup helper to keep only recent artifacts locally:

```bash
# Preview
scripts/cleanup_build_artifacts.sh

# Execute cleanup (default: keep 5 deb, 2 dist binaries)
scripts/cleanup_build_artifacts.sh --execute
```

## Docs
- Technical Manual: [DOCUMENTATION.md](DOCUMENTATION.md)
- Dependencies & licenses: [DEPENDENCIES.md](DEPENDENCIES.md)
- License: [LICENSE.md](LICENSE.md)

Developed by **kazaa3**.
