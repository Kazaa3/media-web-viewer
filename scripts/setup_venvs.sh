#!/bin/bash
# Media Web Viewer - Unified Venv Setup Script
# Initializes all 5 specialized environments based on the new requirement split.

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Detect Python
if command -v python3.14 &>/dev/null; then
    PYTHON="python3.14"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "Error: Python 3 not found."
    exit 1
fi

setup_venv() {
    local name=$1
    local req_file="infra/$2"
    local dir=".$name"
    
    echo "--------------------------------------------------------------------------------"
    echo "Setting up $name environment in $dir..."
    echo "--------------------------------------------------------------------------------"
    
    if [ ! -d "$dir" ]; then
        "$PYTHON" -m venv "$dir"
    fi
    
    source "$dir/bin/activate"
    pip install --upgrade pip
    pip install -r "$req_file"
    deactivate
    
    echo "Done."
}

# 1. Core
setup_venv "venv_core" "requirements-core.txt"

# 2. Dev
setup_venv "venv_dev" "requirements-dev.txt"

# 3. Testbed
setup_venv "venv_testbed" "requirements-test.txt"

# 4. Selenium
setup_venv "venv_selenium" "requirements-selenium.txt"

# 5. Build
setup_venv "venv_build" "requirements-build.txt"

# 6. Run (Developer Primary)
setup_venv "venv_run" "requirements-run.txt"

# 7. Legacy venv (Root Compatibility)
echo "--------------------------------------------------------------------------------"
echo "Setting up legacy venv environment in venv..."
echo "--------------------------------------------------------------------------------"
if [ ! -d "venv" ]; then
    "$PYTHON" -m venv "venv"
fi
source "venv/bin/activate"
pip install --upgrade pip
pip install -r "requirements.txt"
deactivate

echo "================================================================================"
echo "All 7 environments initialized successfully."
echo "================================================================================"
