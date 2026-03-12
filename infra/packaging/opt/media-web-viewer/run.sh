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

# Advanced Dependency Check (Python & System)
echo -e "${BLUE}🔍 Prüfe Abhängigkeiten...${NC}"
# Get missing dependencies from our check script
if [[ -n "$CONDA_PREFIX" ]]; then
    MISSING_CONDA=$(python check_environment.py --list-missing-conda)
else
    MISSING_PIP=$(python check_environment.py --list-missing-pip)
    MISSING_APT=$(python check_environment.py --list-missing-apt)
fi

if [[ -z "$MISSING_PIP" && -z "$MISSING_APT" && -z "$MISSING_CONDA" ]]; then
    echo -e "${GREEN}✅ Alle Abhängigkeiten erfüllt.${NC}"
else
    echo -e "${YELLOW}⚠️  Fehlende Abhängigkeiten gefunden:${NC}"
    if [[ -n "$MISSING_CONDA" ]]; then
        echo -e "   📦 Conda: $MISSING_CONDA"
    fi
    if [[ -n "$MISSING_PIP" ]]; then
        echo -e "   📦 Python (pip): $MISSING_PIP"
    fi
    if [[ -n "$MISSING_APT" ]]; then
        echo -e "   🔧 System (apt): $MISSING_APT"
    fi
    
    echo ""
    read -p "Sollen die fehlenden Abhängigkeiten jetzt installiert werden? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ -n "$MISSING_CONDA" ]]; then
            echo -e "${BLUE}📥 Installiere Abhängigkeiten via Conda (conda-forge preferiert)...${NC}"
            conda install -y -c conda-forge $MISSING_CONDA || {
                echo -e "${RED}❌ Conda installation fehlgeschlagen.${NC}"
                exit 1
            }
        fi
        if [[ -n "$MISSING_PIP" ]]; then
            echo -e "${BLUE}📥 Installiere Python-Packages via pip...${NC}"
            pip install $MISSING_PIP
        fi
        if [[ -n "$MISSING_APT" ]]; then
            echo -e "${BLUE}📥 Installiere System-Packages (sudo erforderlich)...${NC}"
            sudo apt update && sudo apt install -y $MISSING_APT
        fi
        echo -e "${GREEN}✅ Installation abgeschlossen.${NC}"
    else
        echo -e "${RED}❌ Abbruch. Die App wird möglicherweise nicht korrekt funktionieren.${NC}"
    fi
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

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo ""
    echo "Usage: ./run.sh [option]"
    echo ""
    echo "Options:"
    echo "  --debug       Start with full debug flags"
    echo "  --n           Connectionless browser mode (browser without backend session)"
    echo "  --ng          No-GUI mode (no browser, no Eel/WebSocket)"
    echo "  --rebuild     Recreate virtual environment and dependencies"
    echo "  --help, -h    Show this help"
    echo ""
    exit 0
fi

# Handle Rebuild flag
if [[ "$1" == "--rebuild" ]]; then
    echo -e "${YELLOW}♻️  Rebuilding environment as requested...${NC}"
    deactivate 2>/dev/null || true
    rm -rf "$VENV_DIR"
    echo -e "${GREEN}✅ .venv gelöscht. Starte neu...${NC}"
    exec bash "$0"
fi

if [[ "$1" == "--ng" ]]; then
    echo -e "${YELLOW}ℹ️  No-GUI mode aktiv (--ng)${NC}"
elif [[ "$1" == "--n" ]]; then
    echo -e "${YELLOW}ℹ️  Connectionless browser mode aktiv (--n)${NC}"
fi

echo ""

exec python main.py "$@"
