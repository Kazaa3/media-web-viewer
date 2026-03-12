#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

def main():
    """
    Main entry point for running GUI tests using venv_testbed.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    test_dir = os.path.join(project_root, "tests")
    
    # Use .venv_selenium python
    venv_python = os.path.join(project_root, ".venv_selenium", "bin", "python3")
    if not os.path.exists(venv_python):
        print(f"Error: .venv_selenium not found at {venv_python}")
        print("Please run creation script or ensure it exists.")
        sys.exit(1)

    print("Industrial Standard GUI Test Suite")
    print("==================================")
    print(f"Project Root: {project_root}")
    print(f"Python Exec:  {venv_python}")
    print("")

    # GUI Test files to run
    test_files = [
        "tests/test_ui_integrity.py",
        "tests/test_parser_stalling.py",
        "tests/test_mouse_interaction.py",
        "tests/test_scenario_hammerhart.py"
    ]

    failed_tests = []

    # Set PYTHONPATH so tests can find Page Objects and utils
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{project_root}:{test_dir}"
    # Encourage tests to use existing sessions
    # env["MWV_ONLY_EXISTING_SESSION"] = "0" # Set to 1 if we want to STRICTLY forbid spawning

    for test_file in test_files:
        abs_test_path = os.path.join(project_root, test_file)
        if not os.path.exists(abs_test_path):
            print(f"[SKIP] {test_file} (Not found)")
            continue

        print(f"[RUN] {test_file}")
        try:
            # Run test with venv_testbed
            result = subprocess.run(
                [venv_python, abs_test_path],
                env=env,
                cwd=project_root
            )
            if result.returncode != 0:
                print(f"[FAIL] {test_file} returned exit code {result.returncode}")
                failed_tests.append(test_file)
            else:
                print(f"[OK] {test_file}")
        except Exception as e:
            print(f"[ERROR] Failed to run {test_file}: {e}")
            failed_tests.append(test_file)
        print("")

    print("==================================")
    if failed_tests:
        print(f"FAILED TESTS: {', '.join(failed_tests)}")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
