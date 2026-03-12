# Installation Guide - Media Web Viewer

**Version:** ${VERSION}  
**Date:** March 8, 2026

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Building from Source](#building-from-source)
4. [CI/CD Pipelines](#cicd-pipelines)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **OS:** Linux (Debian/Ubuntu), macOS 10.14+, Windows 10+
- **Python:** 3.10 or higher
- **RAM:** 512 MB
- **Disk Space:** 200 MB (application + dependencies)
- **Display:** 1024x768 or higher

### Recommended Requirements

- **OS:** Linux (Debian 11+, Ubuntu 20.04+)
- **Python:** 3.11 or higher
- **RAM:** 2 GB
- **Disk Space:** 1 GB
- **Display:** 1920x1080 or higher

### System Dependencies

The following system packages are required:

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install -y \
    ffmpeg \
    libmediainfo0v5 \
    python3 \
    python3-pip \
    python3-venv

# macOS (with Homebrew)
brew install ffmpeg mediainfo python@3.11

# Windows (with Chocolatey)
choco install ffmpeg mediainfo python
```

---

## Installation Methods

### Method 1: Debian Package (.deb) - **Recommended for Debian/Ubuntu**

**Download and Install:**

```bash
# Download latest release
wget https://github.com/Kazaa3/media-web-viewer/releases/download/v${VERSION}/media-web-viewer_${VERSION}_amd64.deb

# Install package
sudo dpkg -i media-web-viewer_${VERSION}_amd64.deb

# Install missing dependencies (if any)
sudo apt-get install -f
```

**Start Application:**

```bash
# Via command line
media-web-viewer

# Or via application menu
# Applications → Media → Media Web Viewer
```

**Uninstall:**

```bash
# Remove package (keep configuration)
sudo apt remove media-web-viewer

# Complete removal (including configuration)
sudo apt purge media-web-viewer
```

---

### Method 2: Standalone Executable

**Download:**

```bash
# Linux
wget https://github.com/Kazaa3/media-web-viewer/releases/download/v${VERSION}/MediaWebViewer-${VERSION}-Linux

# Windows
# Download MediaWebViewer-${VERSION}-Windows.exe from releases page

# macOS
# Download latest macOS build from releases page (if provided)
```

**Make Executable (Linux/macOS):**

```bash
chmod +x MediaWebViewer-${VERSION}-Linux
```

**Run:**

```bash
# Linux
./MediaWebViewer-${VERSION}-Linux

# Windows
MediaWebViewer-${VERSION}-Windows.exe

# macOS
open MediaWebViewer.app
```

**Note:** Standalone executables include all dependencies but are larger (~150 MB) than the Debian package.

---

### Method 3: From Source with Virtual Environment

**Clone Repository:**

```bash
git clone https://github.com/Kazaa3/media-web-viewer.git
cd media-web-viewer
```

**Setup Virtual Environment:**

```bash
# Create core virtual environment
python3 -m venv .venv_core

# Activate core virtual environment
source .venv_core/bin/activate

# Install core dependencies
pip install -r requirements-core.txt
```

**Run Application:**

```bash
python main.py
```

**Create Desktop Launcher (Optional):**

```bash
bash install_launcher.sh
```

---

### Method 4: Conda Environment

**Create Environment:**

```bash
# Using environment.yml
conda env create -f environment.yml
conda activate media-web-viewer

# Or manually
conda create -n media-web-viewer python=3.11
conda activate media-web-viewer
pip install -r requirements-core.txt
```

**Run Application:**

```bash
python main.py
```

---

## Building from Source

### Build Debian Package

**Quick Build:**

```bash
# Using build system (recommended)
python build_system.py --build deb

# Using legacy script
bash build_deb.sh
```

**Full Build with Tests:**

```bash
python build_system.py --full-build
```

**Output:**
- Package: `media-web-viewer_${VERSION}_amd64.deb`
- Location: Project root directory

---

### Build Standalone Executable

**All Platforms:**

```bash
# Using build system
python build_system.py --build pyinstaller

# Manual PyInstaller build
python -m PyInstaller --onefile --noconsole --name MediaWebViewer-${VERSION} --add-data "web:web" --hidden-import bottle_websocket main.py
```

**Platform-Specific Notes:**

**Linux:**
- Output: `dist/MediaWebViewer` (ELF binary)
- Size: ~100-150 MB
- Requires: glibc 2.31+ (Ubuntu 20.04+)

**Windows:**
- Output: `dist/MediaWebViewer-${VERSION}-Windows.exe`
- Size: ~120-160 MB
- Requires: Windows 10 or higher

**macOS:**
- Output: Platform-dependent bundle (if macOS build is configured)
- Size: ~110-140 MB
- Requires: macOS 10.14 (Mojave) or higher

---

## Running the Application

### Normal Startup

```bash
# From installed package
media-web-viewer

# From source
python main.py

# From executable
./dist/MediaWebViewer

---

## CI/CD Pipelines

### 1) Main Branch Artifact Pipeline

Workflow: `.github/workflows/ci-artifacts.yml`

- Trigger: push to `main` and manual dispatch
- Build outputs:
    - Linux executable (`dist/MediaWebViewer`)
    - Debian package (`media-web-viewer_${VERSION}_amd64.deb`)
- Result: artifacts are uploaded to the workflow run (without creating a GitHub Release)

### 2) Tagged Release Pipeline

Workflow: `.github/workflows/release.yml`

- Trigger: tags `v*` (e.g., `v${VERSION}`) and manual dispatch
- Build outputs:
    - Linux executable
    - Debian package
    - Windows executable
- Result: automatic GitHub Release with binaries as assets

### Release Trigger Commands

```bash
git add .
git commit -m "Release v${VERSION}"
git tag -a v${VERSION} -m "Release v${VERSION}"
git push origin main --tags
```

### Local Artifact Cleanup

```bash
# Dry-run
scripts/cleanup_build_artifacts.sh

# Execute cleanup
scripts/cleanup_build_artifacts.sh --execute
```
```

### Startup Modes

**No-GUI Mode (Headless):**
```bash
python main.py --ng
# Database initialized, stats displayed, no GUI
```

**Connectionless Mode (UI Only):**
```bash
python main.py --n
# Opens UI without backend (for UI development)
```

**Debug Mode:**
```bash
python main.py --debug
# Enables verbose logging
```

---

## Post-Installation

### Verify Installation

```bash
# Check version
python -c "from main import VERSION; print(f'Version: {VERSION}')"

# Run tests
python build_system.py --test

# Check dependencies
python -c "import eel, bottle, bottle_websocket, mutagen, pymediainfo, m3u8; print('All dependencies OK')"
```

### Configure Application

**Scan Directories:**

1. Open application
2. Navigate to **Options** tab
3. Add media directories under **Index-Verzeichnisse**
4. Click **Scan Media** to index files

**Language:**

1. Open **Options** tab
2. Select language from dropdown: German (Deutsch) or English
3. Interface updates immediately

---

## Troubleshooting

### Common Issues

**Issue:** "ModuleNotFoundError: No module named 'eel'"

**Solution:**
```bash
# Activate core virtual environment
source .venv_core/bin/activate

# Install core dependencies
pip install -r requirements-core.txt
```

---

**Issue:** Missing package like `m3u8` or `bottle_websocket`

**Typical errors:**
- `ModuleNotFoundError: No module named 'm3u8'`
- `ModuleNotFoundError: No module named 'bottle_websocket'`

**Quick fix:**
```bash
source .venv_core/bin/activate
pip install -r requirements-core.txt --upgrade --force-reinstall

# Verify
python -c "import m3u8, bottle_websocket; print('imports ok')"
```

**Feature scope note:**
- Missing `m3u8` mainly affects VLC playlist import/export.
- Missing `bottle_websocket` affects UI/backend websocket bridge features.

---

**Issue:** Dependency errors remain unclear or environment is contaminated

Use a fresh external probe environment:

```bash
# From project root
python3 -m venv /tmp/mwv_dep_probe_env

# Run probe test in clean env (outside project .venv)
/tmp/mwv_dep_probe_env/bin/python tests/test_dependency_probe.py \
    2>&1 | tee logs/dependency_probe_fresh_venv.log

# Install full requirements into probe env and re-test
/tmp/mwv_dep_probe_env/bin/pip install -r requirements.txt
/tmp/mwv_dep_probe_env/bin/python tests/test_dependency_probe.py \
    2>&1 | tee logs/dependency_probe_after_install.log
```

Probe files:
- `tests/test_dependency_probe.py`
- `logs/dependency_probe_report.json`
- `logs/dependency_probe_fresh_venv.log`
- `logs/dependency_probe_after_install.log`

---

**Issue:** "Address already in use: Port 8000"

**Solution:**
- Application uses dynamic port allocation automatically
- Check for running sessions: `python -c "from main import check_running_sessions; print(check_running_sessions())"`
- Kill existing process if needed: `pkill -f main.py`

---

**Issue:** FFmpeg not found

**Solution:**
```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

---

**Issue:** Permission denied when running executable

**Solution:**
```bash
chmod +x MediaWebViewer-${VERSION}-Linux
```

---

**Issue:** Database locked error

**Solution:**
```bash
# Close all instances
pkill -f main.py

# Remove lock file if exists
rm ~/.media-web-viewer/media_library.db-journal

# Restart application
python main.py
```

---

### Log Files

**Location:**
```
~/.media-web-viewer/app.log
```

**View Logs:**
```bash
# All logs
cat ~/.media-web-viewer/app.log

# Errors only
grep "[ERROR]" ~/.media-web-viewer/app.log

# Real-time monitoring
tail -f ~/.media-web-viewer/app.log
```

---

### Getting Help

**Documentation:**
- Technical Manual: [DOCUMENTATION.md](DOCUMENTATION.md)
- Dependencies: [DEPENDENCIES.md](DEPENDENCIES.md)
- Logbook: [logbuch/](logbuch/)

**Support:**
- GitHub Issues: https://github.com/Kazaa3/media-web-viewer/issues
- Email: [Your contact email]

---

## Uninstallation

### Debian Package

```bash
# Remove application (keep configuration)
sudo apt remove media-web-viewer

# Complete removal (including user data)
sudo apt purge media-web-viewer
rm -rf ~/.media-web-viewer
```

### Source Installation

```bash
# Remove virtual environments
rm -rf .venv_core .venv_dev .venv_testbed .venv_selenium .venv_build

# Remove application data
rm -rf ~/.media-web-viewer

# Remove launcher (if installed)
rm ~/.local/bin/media-web-viewer
rm ~/.local/share/applications/media-web-viewer.desktop
```

### Executable

```bash
# Remove executable
rm MediaWebViewer-${VERSION}-Linux

# Remove application data
rm -rf ~/.media-web-viewer
```

---

**Last Updated:** March 8, 2026  
**Version:** ${VERSION}
