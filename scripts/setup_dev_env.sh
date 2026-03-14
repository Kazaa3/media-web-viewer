#!/bin/bash
# Media Web Viewer - Clean Development Environment Setup
# Automates the creation/refresh of virtual environments and verifies health.

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$PROJECT_ROOT"

# --- Configuration ---
VENVS=("venv_core" "venv_dev" "venv_testbed" "venv_selenium" "venv_build")
REQ_FILES=("requirements-core.txt" "requirements-dev.txt" "requirements-test.txt" "requirements-selenium.txt" "requirements-build.txt")

# --- Detect Python ---
if command -v python3.14 &>/dev/null; then
    PYTHON="python3.14"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "❌ Error: Python 3 not found."
    exit 1
fi

echo "🚀 Starting Dev Environment Setup using $PYTHON"
echo "📂 Project Root: $PROJECT_ROOT"

# --- Functions ---

clean_venvs() {
    echo "🧹 Cleaning existing virtual environments..."
    for venv in "${VENVS[@]}"; do
        if [ -d ".$venv" ]; then
            echo "  - Removing .$venv"
            rm -rf ".$venv"
        fi
    done
}

setup_venv() {
    local name=$1
    local req_file=$2
    local dir=".$name"
    
    echo "--------------------------------------------------------------------------------"
    echo "📦 Setting up $name environment in $dir..."
    echo "--------------------------------------------------------------------------------"
    
    if [ ! -d "$dir" ]; then
        "$PYTHON" -m venv "$dir"
    fi
    
    source "$dir/bin/activate"
    echo "  - Upgrading pip..."
    pip install --quiet --upgrade pip
    
    if [ -f "$req_file" ]; then
        echo "  - Installing requirements from $req_file..."
        pip install --quiet -r "$req_file"
    else
        echo "  ⚠️ Warning: $req_file not found. Skipping dependency installation."
    fi
    
    # Install local package in editable mode if venv_core
    if [ "$name" == "venv_core" ]; then
        echo "  - Installing local package in editable mode..."
        pip install -e .
    fi
    
    deactivate
    echo "✅ $name setup complete."
}

verify_environments() {
    echo "--------------------------------------------------------------------------------"
    echo "🔍 Verifying Environments..."
    echo "--------------------------------------------------------------------------------"
    
    # Basic health check using venv_core
    if [ -d ".venv_core" ]; then
        echo "Testing venv_core..."
        source ".venv_core/bin/activate"
        python -c "import sys; print(f'  • Python Version: {sys.version.split()[0]}')"
        python -c "import eel; print('  • Eel: Installed')"
        deactivate
    fi
    
    # Run environment tests if requested
    if [ "$1" == "--test" ]; then
        echo "Running automated environment tests..."
        source ".venv_testbed/bin/activate"
        PYTHONPATH="$PROJECT_ROOT" pytest tests/basic/env/test_dependency_probe.py -v
        deactivate
    fi
}

# --- Main Execution ---

CLEAN=false
RUN_TESTS=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --clean) CLEAN=true ;;
        --test) RUN_TESTS=true ;;
        --help) 
            echo "Usage: $0 [--clean] [--test]"
            echo "  --clean  Remove existing venvs before setup"
            echo "  --test   Run verification tests after setup"
            exit 0
            ;;
    esac
done

if [ "$CLEAN" = true ]; then
    clean_venvs
fi

for i in "${!VENVS[@]}"; do
    setup_venv "${VENVS[$i]}" "${REQ_FILES[$i]}"
done

if [ "$RUN_TESTS" = true ]; then
    verify_environments "--test"
else
    verify_environments
fi

echo "================================================================================"
echo "✨ Development environment is ready!"
echo "To activate core env: source .venv_core/bin/activate"
echo "================================================================================"
