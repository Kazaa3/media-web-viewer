#!/bin/bash
# build_deb.sh – Baut ein .deb-Paket für Media Web Viewer
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_NAME="media-web-viewer"
# Version aus zentraler Datei lesen
VERSION=$(tr -d '[:space:]' < "$SCRIPT_DIR/VERSION")
ARCH="amd64"
DEB_NAME="${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
STAGING="$SCRIPT_DIR/packaging"
APP_DEST="$STAGING/opt/$PACKAGE_NAME"

# Build-Test-Gate (default: enabled)
# Set SKIP_BUILD_TESTS=1 to skip this gate explicitly.
SKIP_BUILD_TESTS="${SKIP_BUILD_TESTS:-0}"

# Update control file version
sed -i "s/^Version:.*/Version: $VERSION/" "$STAGING/DEBIAN/control"

echo "==> Bereite Staging-Bereich vor..."

if [ "$SKIP_BUILD_TESTS" != "1" ]; then
    echo "==> Führe Build-Test-Gate aus..."
    if [ -n "$VIRTUAL_ENV" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
        PYTHON_BIN="$VIRTUAL_ENV/bin/python"
    elif [ -x "$SCRIPT_DIR/.venv_testbed/bin/python" ]; then
        PYTHON_BIN="$SCRIPT_DIR/.venv_testbed/bin/python"
    else
        PYTHON_BIN="python3"
    fi

    "$PYTHON_BIN" -m pytest -q \
        "$SCRIPT_DIR/tests/test_performance_probes.py" \
        "$SCRIPT_DIR/tests/test_bottle_health_latency.py" \
        "$SCRIPT_DIR/tests/test_installed_packages_ui.py" \
        "$SCRIPT_DIR/tests/test_environment_packages_fallback.py" \
        "$SCRIPT_DIR/tests/test_ui_session_stability.py"
    echo "==> Build-Test-Gate: OK"
else
    echo "==> Build-Test-Gate übersprungen (SKIP_BUILD_TESTS=1)"
fi

# Sauber starten
rm -rf "$APP_DEST"
mkdir -p "$APP_DEST"

# Quellcode kopieren (ohne .git, .venv, Tests, Build-Artefakte und Medien)
rsync -a \
    --exclude '.git' \
    --exclude '.venv_testbed' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude 'build/' \
    --exclude 'dist/' \
    --exclude 'packaging/' \
    --exclude 'media/*.mp3' \
    --exclude 'media/*.flac' \
    --exclude 'media/*.m4a' \
    --exclude 'media/*.m4b' \
    --exclude 'media/*.ogg' \
    --exclude 'media/*.wav' \
    --exclude 'media/*.opus' \
    --exclude 'media/*.aac' \
    --exclude 'media/*.mkv' \
    --exclude 'media/*.mp4' \
    --exclude 'media/*.webm' \
    --exclude 'media/.cache' \
    --exclude '*.db' \
    --exclude '.gitignore' \
    --exclude '*.spec' \
    --exclude '*.deb' \
    --exclude '.pytest_cache' \
    "$SCRIPT_DIR/" "$APP_DEST/"

# DEBIAN-Skripte ausführbar machen
chmod 755 "$STAGING/DEBIAN/postinst"
chmod 755 "$STAGING/DEBIAN/prerm"
chmod 755 "$STAGING/usr/bin/$PACKAGE_NAME"

echo "==> Baue .deb Paket: $DEB_NAME"
dpkg-deb --build --root-owner-group "$STAGING" "$SCRIPT_DIR/$DEB_NAME"

echo ""
echo "Fertig! Paket: $DEB_NAME"
echo ""
echo "Installieren:   sudo dpkg -i $DEB_NAME"
echo "Starten:        media-web-viewer"
echo "Vollst. löschen: sudo apt purge $PACKAGE_NAME"
