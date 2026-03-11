#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

def main():
    project_root = Path(__file__).resolve().parent.parent
    venv_python = project_root / ".venv_selenium" / "bin" / "python3"
    
    if not venv_python.exists():
        print(f"Error: .venv_selenium not found at {venv_python}")
        print("Please run: python3 -m venv .venv_selenium && .venv_selenium/bin/pip install selenium webdriver-manager")
        sys.exit(1)

    # If we are not running with the venv python, re-execute
    current_python = Path(sys.executable).resolve()
    if current_python != venv_python.resolve():
        # Add project root to PYTHONPATH so imports like 'pages' work if tests are in root
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root) + ":" + env.get("PYTHONPATH", "")
        print(f"Re-executing with {venv_python}...")
        os.execv(str(venv_python), [str(venv_python), *sys.argv])

    # Now we are in the correct venv
    tests = [
        "tests/test_ui_integrity.py",
        "tests/test_parser_stalling.py",
        "tests/test_mouse_interaction.py",
        "tests/test_scenario_hammerhart.py",
    ]
    
    print("Industrial Standard GUI Test Suite")
    print("==================================")
    
    failed = []
    for test_file in tests:
        if not (project_root / test_file).exists():
            print(f"Skipping missing test: {test_file}")
            continue
            
        print(f"\n[RUN] {test_file}")
        # Run test as module or script
        # Using -m unittest might be better for imports
        result = subprocess.run([sys.executable, test_file], cwd=str(project_root))
        if result.returncode != 0:
            failed.append(test_file)
    
    print("\n==================================")
    if not failed:
        print("ALL TESTS PASSED")
    else:
        print(f"FAILED TESTS: {', '.join(failed)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
