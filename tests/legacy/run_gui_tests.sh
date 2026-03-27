#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
./.venv_selenium/bin/python3 tests/run_gui_tests.py "$@"
