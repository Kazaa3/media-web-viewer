#!/bin/bash
# UI Master: v1.34 Playwright Runner
# Runs the navigation and fragment integrity audit.

set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"
TEST_FILE="$PROJECT_ROOT/tests/ui/v134_tab_integrity.spec.js"

echo "[Audit] Starting v1.34 Master Integrity Suite..."
echo "[Audit] Root: $PROJECT_ROOT"
echo "[Audit] Test: $TEST_FILE"

# Install Playwright dependencies if needed (e.g. chromium)
# npx -y playwright install chromium

# Run the test
# We use --project=chromium to focus on the main engine
npx -y playwright test "$TEST_FILE" --project=chromium --reporter=list
