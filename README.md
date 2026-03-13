# dict – Web Media Player & Library
1.34

Kompakte Projektübersicht. Das vollständige Technical Manual liegt in [DOCUMENTATION.md](docs/DOCUMENTATION.md).

## Quick Start

### Debian/Ubuntu (.deb)
```bash
sudo dpkg -i media-web-viewer_1.34_amd64.deb
sudo apt-get install -f
media-web-viewer
```

### From Source (⭐ EMPFOHLEN: venv_core)
```bash
git clone https://github.com/Kazaa3/media-web-viewer.git
cd media-web-viewer
python3 -m venv .venv_core
source .venv_core/bin/activate
pip install -r requirements.txt
python main.py
```

## Core Stack
- Backend: Python 3.11+, Bottle, Eel
- Frontend: HTML5/CSS3, Vanilla JavaScript (Glassmorphism)
- Database: SQLite (`media_library.db`)
- Media Tooling: Mutagen, pymediainfo, FFmpeg
- VLC Support: m3u8 (playlist import/export), python-vlc, vlc
- 📦 **Venv Management**: Centralized logic for coordinated virtual environments.
- 🔍 **Build Monitoring**: Integrated watchdog system for stable DEB and EXE builds.


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

Note on build quality gate:
- `build_deb.sh` runs a mandatory targeted test gate before packaging.
- `build_system.py --build deb|pyinstaller|all` runs the same targeted gate before artifact creation.
- `build.py` (PyInstaller helper) also runs the same gate.
	- `tests/test_performance_probes.py`
	- `tests/test_bottle_health_latency.py`
	- `tests/test_installed_packages_ui.py`
	- `tests/test_environment_packages_fallback.py`
	- `tests/test_ui_session_stability.py`
- Explicit override (not recommended):

```bash
SKIP_BUILD_TESTS=1 bash build_deb.sh
python build_system.py --build deb --skip-build-gate
python build_system.py --build pyinstaller --skip-build-gate
SKIP_BUILD_TESTS=1 python build.py
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

# Optional emergency override for targeted pre-build gate
python build_system.py --pipeline --skip-build-gate

# Manual checks (if needed)
python tests/test_version_sync.py
python tests/test_reinstall_deb.py
RUN_DESTRUCTIVE_TESTS=1 python tests/test_reinstall_deb.py
```

Pipeline order in `build_system.py`:
1. Environment check
2. Version sync test
3. Debian build (with targeted pre-build gate by default)
4. Safe reinstall validation
5. Optional destructive reinstall validation

## Version Update (Automated)

```bash
# 1) Update VERSION + all configured sync locations
python update_version.py --new-version 1.34

# 2) Verify sync is fully consistent
python tests/test_version_sync.py
```

## CI/CD Pipelines

### Main Branch Artifacts (no GitHub Release)
On every push to `main`, the workflow [ci-artifacts.yml](.github/workflows/ci-artifacts.yml) builds and uploads:
- Linux executable (`dist/MediaWebViewer`)
- Debian package (`media-web-viewer_*_amd64.deb`)

### Tagged Release (auto-publish to GitHub Releases)
When you push a tag like `v1.34`, the workflow [release.yml](.github/workflows/release.yml):
- builds Linux executable + Debian package + Windows `.exe`
- creates/updates the GitHub Release
- uploads all binaries as release assets

```bash
git tag -a v1.34 -m "Release v1.34"
git push origin main --tags
```

### Release Checklist (recommended)
```bash
# 1) Update project version
python update_version.py --new-version 1.34

# 2) Verify version consistency
python tests/test_version_sync.py

# 3) Run release validation pipeline
python build_system.py --pipeline

# 4) Commit release-related changes
git add VERSION VERSION_SYNC.json update_version.py
git add main.py README.md docs/DOCUMENTATION.md
git add .github/workflows/release.yml .github/workflows/ci-artifacts.yml
git commit -m "Release v1.34"

# 5) Create and push release tag
git tag -a v1.34 -m "Release v1.34"
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

If generated artifacts were already committed in the past, remove them from the Git index once (files stay local):

```bash
git rm -r --cached -- packaging/opt/media-web-viewer
git rm --cached -- __pycache__/main.cpython-314.pyc
git rm --cached -- media-web-viewer_v1.34_amd64.deb
git commit -m "chore: untrack generated packaging/cache artifacts"
```

## Docs & Logbuch
- Technical Manual: [DOCUMENTATION.md](docs/DOCUMENTATION.md)
- Logbuch-Zentrum: [docs/logbuch/000_Index.md](docs/logbuch/000_Index.md) (17 Kern-Dokumente)
- Programm-Historie (Archiv): [docs/logbuch/archive/](docs/logbuch/archive/) (290+ Forschungs-Logs)
- Dependencies & licenses: [DEPENDENCIES.md](docs/DEPENDENCIES.md)
- License: [LICENSE.md](docs/LICENSE.md)

Developed by **kazaa3**.
