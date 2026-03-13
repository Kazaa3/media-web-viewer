#!/bin/bash
# build_deb.sh – Baut ein .deb-Paket für Media Web Viewer
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGE_NAME="media-web-viewer"
# Version aus zentraler Datei lesen
VERSION=$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")
ARCH="amd64"
DEB_NAME="${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
STAGING="$SCRIPT_DIR/packaging"
BUILD_DIR="$ROOT_DIR/build"
mkdir -p "$BUILD_DIR"

# Clean legacy fragments in packaging dir
if [ -d "$STAGING/opt" ]; then
    echo "==> Bereinige alte Staging-Reste..."
    rm -rf "$STAGING/opt/"*
fi

# Build-Test-Gate (default: enabled)
# Set SKIP_BUILD_TESTS=1 to skip this gate explicitly.
SKIP_BUILD_TESTS="${SKIP_BUILD_TESTS:-0}"

# Update control file version
sed -i "s/^Version:.*/Version: $VERSION/" "$STAGING/DEBIAN/control"

echo "==> Bereite Staging-Bereich vor..."

if [ "$SKIP_BUILD_TESTS" != "1" ]; then
    echo "==> Führe Build-Test-Gate aus..."
    # ... (skipping python discovery for brevity - keeping existing logic)
    if [ -n "$VIRTUAL_ENV" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
        PYTHON_BIN="$VIRTUAL_ENV/bin/python"
    elif [ -x "$ROOT_DIR/.venv_build/bin/python" ]; then
        PYTHON_BIN="$ROOT_DIR/.venv_build/bin/python"
    elif [ -x "$ROOT_DIR/.venv_dev/bin/python" ]; then
        PYTHON_BIN="$ROOT_DIR/.venv_dev/bin/python"
    elif [ -x "$ROOT_DIR/.venv_core/bin/python" ]; then
        PYTHON_BIN="$ROOT_DIR/.venv_core/bin/python"
    else
        PYTHON_BIN="python3"
    fi

    "$PYTHON_BIN" -m pytest -q \
        "$ROOT_DIR/tests/integration/performance/test_performance_probes.py" \
        "$ROOT_DIR/tests/integration/tech/bottle/test_bottle_health_latency.py" \
        "$ROOT_DIR/tests/integration/category/ui/test_installed_packages_ui.py" \
        "$ROOT_DIR/tests/integration/basic/env/test_environment_packages_fallback.py" \
        "$ROOT_DIR/tests/integration/category/ui/test_ui_session_stability.py"
    echo "==> Build-Test-Gate: OK"
else
    echo "==> Build-Test-Gate übersprungen (SKIP_BUILD_TESTS=1)"
fi

# Sauber starten
# Erstelle einen echten Staging-Bereich in /tmp für sauberen Build ohne Seiteneffekte
BUILD_ROOT=$(mktemp -d)
echo "==> Erstelle Build-Umgebung in $BUILD_ROOT..."

mkdir -p "$BUILD_ROOT/pkg"
# Kopiere das Packaging-Template (DEBIAN/, usr/bin/)
cp -a "$STAGING"/* "$BUILD_ROOT/pkg/"

# Zielverzeichnis im Staging-Bereich
STAGED_APP_DEST="$BUILD_ROOT/pkg/opt/$PACKAGE_NAME"
mkdir -p "$STAGED_APP_DEST"

# Quellcode kopieren (ohne .git, .venv, Tests, Build-Artefakte und Medien)
echo "==> Sammle Quellcode (Zero-Leak Mode)..."
rsync -a \
    --exclude '.git/' \
    --exclude '.github/' \
    --exclude '.vscode/' \
    --exclude '.idea/' \
    --exclude '.venv*/' \
    --exclude 'venv/' \
    --exclude '**/__pycache__/' \
    --exclude '*.pyc' \
    --exclude 'build/' \
    --exclude 'dist/' \
    --exclude 'infra/packaging/' \
    --exclude 'media/' \
    --exclude 'doc*/' \
    --exclude 'tests/' \
    --exclude '.gitignore' \
    --exclude '*.spec' \
    --exclude '*.deb' \
    --exclude '.pytest_cache/' \
    --exclude '.mypy_cache/' \
    --exclude 'reinstall_deb.sh' \
    --max-size=50M \
    "$ROOT_DIR/" "$STAGED_APP_DEST/"

# Update control file version im temporären Staging
sed -i "s/^Version:.*/Version: $VERSION/" "$BUILD_ROOT/pkg/DEBIAN/control"

# Sicherheitsprüfung: Staging-Bereich darf nicht zu groß sein
STAGING_SIZE=$(du -sm "$BUILD_ROOT/pkg" | cut -f1)
if [ "$STAGING_SIZE" -gt 1500 ]; then
    echo "❌ Error: Staging area is still too large ($STAGING_SIZE MB)!"
    rm -rf "$BUILD_ROOT"
    exit 1
fi

# DEBIAN-Skripte ausführbar machen
chmod 755 "$BUILD_ROOT/pkg/DEBIAN/postinst"
chmod 755 "$BUILD_ROOT/pkg/DEBIAN/prerm"
chmod 755 "$BUILD_ROOT/pkg/DEBIAN/postrm"
chmod 755 "$BUILD_ROOT/pkg/usr/bin/$PACKAGE_NAME"

echo "==> Baue .deb Paket: $DEB_NAME"
dpkg-deb --build --root-owner-group "$BUILD_ROOT/pkg" "$BUILD_DIR/$DEB_NAME"

# Aufräumen
rm -rf "$BUILD_ROOT"
echo ""
echo "Fertig! Paket: build/$DEB_NAME"
echo ""
echo "Installieren:   sudo dpkg -i build/$DEB_NAME"
echo "Starten:        media-web-viewer"
echo "Vollst. löschen: sudo apt purge $PACKAGE_NAME"
