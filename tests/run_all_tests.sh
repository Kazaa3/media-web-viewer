#!/bin/bash
# MASTER TEST RUNNER - Dynamic Test Discovery & Categorization
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_help() {
    echo "Usage: ./tests/run_all_tests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --stage 1    Core Health (API, Env, Exposure)"
    echo "  --stage 2    Backend Logic (DB, Parsers, Processes, Models)"
    echo "  --stage 3    UI & i18n Interaction (CSS, HTML, Events)"
    echo "  --stage 4    Automation & Integration (VLC, PyAutoGUI, Selenium)"
    echo "  --stage 5    Quality & Security (Linting, Version, Build)"
    echo "  --all        Run all stages (highly recommended for full validation)"
    echo "  --list       List discovered tests per stage"
    echo "  --help       Show this help"
}

STAGE=0
LIST_ONLY=0
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --stage) STAGE="$2"; shift ;;
        --all) STAGE="all" ;;
        --list) LIST_ONLY=1 ;;
        --help) show_help; exit 0 ;;
        *) echo "Unknown parameter: $1"; show_help; exit 1 ;;
    esac
    shift
done

# Optimization: Prefer .venv_dev or .venv_testbed
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

PYTHON_EXE=""
# 1. Prefer active VIRTUAL_ENV ONLY if it exists
if [ -n "$VIRTUAL_ENV" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
    PYTHON_EXE="$VIRTUAL_ENV/bin/python"
fi

# 2. Fallback to specialized venvs
if [ -z "$PYTHON_EXE" ]; then
    if [ -x "$PROJECT_ROOT/.venv_dev/bin/python" ]; then
        PYTHON_EXE="$PROJECT_ROOT/.venv_dev/bin/python"
    elif [ -x "$PROJECT_ROOT/.venv_testbed/bin/python" ]; then
        PYTHON_EXE="$PROJECT_ROOT/.venv_testbed/bin/python"
    elif [ -x "$PROJECT_ROOT/.venv_core/bin/python" ]; then
        PYTHON_EXE="$PROJECT_ROOT/.venv_core/bin/python"
    fi
fi

# 3. System fallback
if [ -z "$PYTHON_EXE" ]; then
    if command -v python3 &>/dev/null; then
        PYTHON_EXE="python3"
    else
        PYTHON_EXE="python"
    fi
fi

# Discovery & Categorization logic
ALL_TESTS=$(ls "$PROJECT_ROOT"/tests/test_*.py)
S1_PATTERNS=("eel" "api" "env_handler" "logbuffer" "health" "network")
S2_PATTERNS=("db" "parser" "process" "transcoding" "media" "format" "models" "parse" "artwork" "mkv" "mp3" "pcm" "bitdepth" "iso" "stream" "chapter" "tag")
S3_PATTERNS=("i18n" "ui_events" "playlist" "tabs" "refresh" "integrity" "html" "css" "json" "rendering")
S4_PATTERNS=("pyautogui" "launcher" "vlc" "selenium" "browser" "session" "docker")
S5_PATTERNS=("subprocess" "version" "build" "markdown" "linting" "doxygen" "cleanup" "package" "repo" "pip")

get_stage_tests() {
    local target_stage=$1
    local results=()
    
    for t in $ALL_TESTS; do
        local filename=$(basename "$t")
        local matched=0
        
        case $target_stage in
            1) for p in "${S1_PATTERNS[@]}"; do [[ "$filename" == *"$p"* ]] && matched=1; done ;;
            2) for p in "${S2_PATTERNS[@]}"; do [[ "$filename" == *"$p"* ]] && matched=1; done ;;
            3) for p in "${S3_PATTERNS[@]}"; do [[ "$filename" == *"$p"* ]] && matched=1; done ;;
            4) for p in "${S4_PATTERNS[@]}"; do [[ "$filename" == *"$p"* ]] && matched=1; done ;;
            5) for p in "${S5_PATTERNS[@]}"; do [[ "$filename" == *"$p"* ]] && matched=1; done ;;
        esac
        
        if [ $matched -eq 1 ]; then
            results+=("tests/$filename")
        fi
    done
    echo "${results[@]}"
}

if [ "$LIST_ONLY" -eq 1 ]; then
    echo -e "${BLUE}Discovered Tests per Stage:${NC}"
    for s in {1..5}; do
        echo -e "${YELLOW}Stage $s:${NC}"
        get_stage_tests $s | tr ' ' '\n'
    done
    exit 0
fi

run_test() {
    local file=$1
    echo -ne "${BLUE}Running: $(basename "$file")... ${NC}"
    if "$PYTHON_EXE" "$file" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        return 1
    fi
}

echo "================================================================================"
echo "🧪 Media Web Viewer - Master Runner (Dynamic Discovery)"
echo "Interpreter: $PYTHON_EXE"
echo "================================================================================"

SELECTED_TESTS=()
if [ "$STAGE" == "all" ]; then
    SELECTED_TESTS=($ALL_TESTS)
    for i in "${!SELECTED_TESTS[@]}"; do
        SELECTED_TESTS[$i]="tests/$(basename "${SELECTED_TESTS[$i]}")"
    done
else
    SELECTED_TESTS=($(get_stage_tests "$STAGE"))
fi

if [ ${#SELECTED_TESTS[@]} -eq 0 ]; then
    echo -e "${RED}No tests found for Stage $STAGE${NC}"
    exit 1
fi

TOTAL=${#SELECTED_TESTS[@]}
FAILED=0
echo "Found $TOTAL tests for execution."

for t in "${SELECTED_TESTS[@]}"; do
    if ! run_test "$t"; then
        ((FAILED++))
    fi
done

echo "================================================================================"
echo "📊 Results: $TOTAL tests, $FAILED failed."
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}SUCCESS: Validation complete.${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: $FAILED tests failed.${NC}"
    exit 1
fi
