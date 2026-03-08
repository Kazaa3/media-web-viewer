#!/bin/bash
# Media Web Viewer - Automatic Environment Setup & Launch Script
# This script automatically detects and activates the correct Python environment
# Requires: Python 3.14.2 (from Conda p14) or falls back to python3
# Supports: venv (primary) and conda (fallback)

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"
P14_PYTHON="/home/xc/anaconda3/envs/p14/bin/python"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🎬 Media Web Viewer - Auto Launcher${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Determine which Python to use (prefer 3.14.2)
PYTHON_CMD="python3"
if [ -f "$P14_PYTHON" ]; then
    PYTHON_CMD="$P14_PYTHON"
    echo -e "${GREEN}✅ Gefunden: Python 3.14.2${NC}"
else
    echo -e "${YELLOW}⚠️  Python 3.14.2 nicht verfügbar, nutze python3${NC}"
fi

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}📦 Virtuelle Umgebung nicht gefunden.${NC}"
    echo -e "${YELLOW}   Erstelle .venv mit $($PYTHON_CMD --version)...${NC}"
    "$PYTHON_CMD" -m venv "$VENV_DIR" || {
        echo -e "${RED}❌ Fehler beim Erstellen der venv!${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ venv erstellt${NC}"
fi

# Activate venv
echo -e "${BLUE}📍 Aktiviere Umgebung...${NC}"
source "$VENV_DIR/bin/activate" || {
    echo -e "${RED}❌ Fehler beim Aktivieren der venv!${NC}"
    exit 1
}

# Check if requirements are installed
if ! python -c "import mutagen, eel, bottle" 2>/dev/null; then
    echo -e "${YELLOW}📥 Installiere Abhängigkeiten...${NC}"
    pip install -q -r "$REQUIREMENTS" || {
        echo -e "${RED}❌ Fehler bei pip install!${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ Abhängigkeiten installiert${NC}"
fi

# Show environment info
PYTHON_VERSION=$(python --version 2>&1)
PYTHON_EXEC=$(which python)
VENV_NAME=$(basename "$(dirname "$VIRTUAL_ENV")")/$(basename "$VIRTUAL_ENV")

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Umgebung bereit${NC}"
echo -e "${GREEN}   $PYTHON_VERSION${NC}"
echo -e "${GREEN}   📦 $VENV_NAME${NC}"
echo -e "${GREEN}   Python: $PYTHON_EXEC${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Start the application
echo -e "${BLUE}🚀 Starte Media Web Viewer...${NC}"

# Handle Rebuild flag
if [[ "$1" == "--rebuild" ]]; then
    echo -e "${YELLOW}♻️  Rebuilding environment as requested...${NC}"
    deactivate 2>/dev/null || true
    rm -rf "$VENV_DIR"
    echo -e "${GREEN}✅ .venv gelöscht. Starte neu...${NC}"
    exec bash "$0"
fi

echo ""

exec python main.py "$@"
