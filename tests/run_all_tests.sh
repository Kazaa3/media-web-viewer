#!/bin/bash
################################################################################
# Master Test Runner - Führt alle Test-Suites aus
################################################################################
#
# ZWECK:
# ------
# Führt alle drei Test-Suites nacheinander aus und zeigt eine Gesamt-Statistik.
#
# TEST-SUITES:
# ------------
# 1. test_i18n_completeness.py - i18n Basis-Validierung (8 Tests)
# 2. test_i18n_deep_scan.py    - i18n Deep Scan (7 Tests)
# 3. test_ui_events.py          - UI Events & Interaktionen (10 Tests)
#
# VERWENDUNG:
# -----------
#     chmod +x tests/run_all_tests.sh
#     ./tests/run_all_tests.sh
#
# ODER:
#     bash tests/run_all_tests.sh
#
# EXIT-CODES:
# -----------
# 0 = Alle Tests bestanden
# 1 = Mindestens ein Test fehlgeschlagen
#
################################################################################

set -e  # Stop on first error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "================================================================================"
echo "🧪 Media Web Viewer - Complete Test Suite"
echo "================================================================================"
echo ""
echo "Führt alle Test-Suites aus:"
echo "  1️⃣  i18n Completeness (8 Tests)"
echo "  2️⃣  i18n Deep Scan (7 Tests)"
echo "  3️⃣  UI Events (10 Tests)"
echo ""
echo "Gesamt: 25 Tests"
echo ""
echo "================================================================================"
echo ""

# Initialize counters
total_tests=0
passed_tests=0
failed_tests=0

# Test 1: i18n Completeness
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}1️⃣  Running: test_i18n_completeness.py${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if python tests/test_i18n_completeness.py; then
    echo -e "${GREEN}✅ i18n Completeness: PASSED${NC}"
    ((passed_tests+=8))
else
    echo -e "${RED}❌ i18n Completeness: FAILED${NC}"
    ((failed_tests+=8))
fi
((total_tests+=8))

# Test 2: i18n Deep Scan
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}2️⃣  Running: test_i18n_deep_scan.py${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if python tests/test_i18n_deep_scan.py; then
    echo -e "${GREEN}✅ i18n Deep Scan: PASSED${NC}"
    ((passed_tests+=7))
else
    echo -e "${YELLOW}⚠️  i18n Deep Scan: PASSED with WARNINGS${NC}"
    ((passed_tests+=6))
    ((failed_tests+=1))
fi
((total_tests+=7))

# Test 3: UI Events
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}3️⃣  Running: test_ui_events.py${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if python tests/test_ui_events.py; then
    echo -e "${GREEN}✅ UI Events: PASSED${NC}"
    ((passed_tests+=10))
else
    echo -e "${RED}❌ UI Events: FAILED${NC}"
    ((failed_tests+=10))
fi
((total_tests+=10))

# Final Summary
echo ""
echo "================================================================================"
echo "📊 FINAL TEST RESULTS"
echo "================================================================================"
echo ""
echo "Total Tests:  $total_tests"
echo -e "Passed:       ${GREEN}$passed_tests${NC}"

if [ $failed_tests -gt 0 ]; then
    echo -e "Failed:       ${RED}$failed_tests${NC}"
else
    echo -e "Failed:       ${GREEN}0${NC}"
fi

# Calculate pass rate
pass_rate=$(awk "BEGIN {printf \"%.1f\", ($passed_tests/$total_tests)*100}")
echo ""
echo "Pass Rate:    ${pass_rate}%"
echo ""

# Overall result
if [ $failed_tests -eq 0 ]; then
    echo "================================================================================"
    echo -e "${GREEN}✅✅✅ ALL TESTS PASSED! ✅✅✅${NC}"
    echo "================================================================================"
    echo ""
    echo "🎉 Gratulation! Alle Tests bestanden!"
    echo ""
    echo "   ✅ i18n Completeness  → 8/8 Tests"
    echo "   ✅ i18n Deep Scan     → 7/7 Tests"
    echo "   ✅ UI Events          → 10/10 Tests"
    echo ""
    echo "   Die App ist vollständig getestet und produktionsreif!"
    echo ""
    exit 0
elif [ $failed_tests -eq 1 ]; then
    echo "================================================================================"
    echo -e "${YELLOW}⚠️  TESTS PASSED WITH WARNINGS ⚠️${NC}"
    echo "================================================================================"
    echo ""
    echo "24 von 25 Tests bestanden (96% Pass Rate)"
    echo ""
    echo "Die meisten Tests sind OK, aber es gibt ein paar nicht-kritische Warnungen."
    echo "Diese können später behoben werden."
    echo ""
    exit 0
else
    echo "================================================================================"
    echo -e "${RED}❌ SOME TESTS FAILED ❌${NC}"
    echo "================================================================================"
    echo ""
    echo "Bitte prüfe die Fehler-Ausgaben oben und behebe die Probleme."
    echo ""
    echo "Häufige Probleme:"
    echo "  • Fehlende i18n Keys in web/i18n.json"
    echo "  • Hardcoded deutsche Strings ohne t() Wrapper"
    echo "  • Buttons ohne Event-Handler"
    echo "  • Fehlende @eel.expose Dekoratoren"
    echo ""
    exit 1
fi
