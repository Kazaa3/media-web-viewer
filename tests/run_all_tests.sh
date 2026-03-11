# MASTER TEST RUNNER - Refactored for Systematic Test Stages
################################################################################

# set -e removed to allow collecting multiple failures

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Help
show_help() {
    echo "Usage: ./tests/run_all_tests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --stage 1    Core Health (API, Env, Exposure)"
    echo "  --stage 2    Backend Logic (DB, Parsers, Processes)"
    echo "  --stage 3    UI & i18n Interaction"
    echo "  --stage 4    E2E & Automation (Requires display)"
    echo "  --stage 5    Quality & Security"
    echo "  --all        Run all stages (requires resources)"
    echo "  --help       Show this help"
}

STAGE=0
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --stage) STAGE="$2"; shift ;;
        --all) STAGE="all" ;;
        --help) show_help; exit 0 ;;
        *) echo "Unknown parameter: $1"; show_help; exit 1 ;;
    esac
    shift
done

if [ "$STAGE" == "0" ]; then
    echo -e "${YELLOW}No stage specified. Defaulting to Stage 1 (Core Health).${NC}"
    STAGE=1
fi

run_test() {
    local file=$1
    echo -e "${BLUE}Running: $file...${NC}"
    if python "$file"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        return 1
    fi
}

echo "================================================================================"
echo "🧪 Media Web Viewer - Systematic Runner: Stage $STAGE"
echo "================================================================================"

FAILED=0
TOTAL=0

case $STAGE in
    1)
        TESTS=("tests/test_eel_exposure_unit.py" "tests/test_api_health_endpoints.py" "tests/test_env_handler.py" "tests/test_logbuffer_api.py")
        ;;
    2)
        TESTS=("tests/test_db_logic.py" "tests/test_parser_registry.py" "tests/test_process_manager_basic.py" "tests/test_transcoding_fixed.py")
        ;;
    3)
        TESTS=("tests/test_i18n_completeness.py" "tests/test_i18n_deep_scan.py" "tests/test_ui_events.py")
        ;;
    4)
        TESTS=("tests/test_pyautogui_integration.py" "tests/test_launcher.py" "tests/test_vlc_integration.py")
        ;;
    5)
        TESTS=("tests/test_subprocess_safety.py" "tests/test_version_sync.py" "tests/test_build_integrity.py")
        ;;
    "all")
        TESTS=("tests/test_eel_exposure_unit.py" "tests/test_api_health_endpoints.py" "tests/test_db_logic.py" "tests/test_i18n_completeness.py" "tests/test_subprocess_safety.py")
        ;;
    *)
        echo "Invalid stage: $STAGE"
        exit 1
        ;;
esac

for t in "${TESTS[@]}"; do
    ((TOTAL++))
    if ! run_test "$t"; then
        ((FAILED++))
    fi
done

echo "================================================================================"
echo "📊 Results $TOTAL tests, $FAILED failed."
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}SUCCESS: Stage $STAGE complete.${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: Stage $STAGE failed.${NC}"
    exit 1
fi

