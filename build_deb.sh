#!/bin/bash
# build_deb.sh – Baut ein .deb-Paket für Media Web Viewer
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_NAME="media-web-viewer"
VERSION="1.1.16"
ARCH="amd64"
DEB_NAME="${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
STAGING="$SCRIPT_DIR/packaging"
APP_DEST="$STAGING/opt/$PACKAGE_NAME"

echo "==> Bereite Staging-Bereich vor..."

# Sauber starten
rm -rf "$APP_DEST"
mkdir -p "$APP_DEST"

# Quellcode kopieren (ohne .git, .venv, Tests, Build-Artefakte und Medien)
rsync -a \
    --exclude '.git' \
    --exclude '.venv' \
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
