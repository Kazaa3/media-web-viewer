#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Global Launcher Script
======================================

This module tests the global launcher script functionality including:
- Script existence and permissions
- Environment validation
- Path configuration
- Python environment detection

Author: Media Web Viewer Team
Created: 2026-03-08
Version: 1.0.0
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pytest


# =============================================================================
# Constants
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
LAUNCHER_SCRIPT = Path.home() / ".local" / "bin" / "media-viewer"
VENV_DIR = PROJECT_ROOT / ".venv"
MAIN_SCRIPT = PROJECT_ROOT / "main.py"


# =============================================================================
# Test: Launcher Script Existence
# =============================================================================

def test_launcher_script_exists():
    """
    Test that the global launcher script exists.
    
    Validates:
        - Script file exists at ~/.local/bin/media-viewer
        - Script is a regular file (not a directory or symlink)
    
    Raises:
        AssertionError: If script doesn't exist or is not a file
    """
    print("\n" + "═" * 70)
    print("TEST: Global Launcher Script Existence")
    print("═" * 70)
    
    print(f"\n🔍 Checking launcher script: {LAUNCHER_SCRIPT}")
    
    assert LAUNCHER_SCRIPT.exists(), (
        f"Launcher script not found at {LAUNCHER_SCRIPT}\n"
        f"Expected location: ~/.local/bin/media-viewer"
    )
    print(f"  ✓ Script exists: {LAUNCHER_SCRIPT}")
    
    assert LAUNCHER_SCRIPT.is_file(), (
        f"Launcher path exists but is not a file: {LAUNCHER_SCRIPT}"
    )
    print(f"  ✓ Script is a regular file")
    
    print(f"\n✅ Launcher script found and validated")


# =============================================================================
# Test: Script Permissions
# =============================================================================

def test_launcher_script_executable():
    """
    Test that the launcher script has executable permissions.
    
    Validates:
        - Script has execute permission for user
        - Script is readable
        - File mode is appropriate (typically 755 or 744)
    
    Raises:
        AssertionError: If script is not executable
    """
    print("\n" + "═" * 70)
    print("TEST: Launcher Script Permissions")
    print("═" * 70)
    
    print(f"\n🔍 Checking permissions for: {LAUNCHER_SCRIPT}")
    
    # Check if file exists first
    assert LAUNCHER_SCRIPT.exists(), f"Script not found: {LAUNCHER_SCRIPT}"
    
    # Get file stats
    stat_info = LAUNCHER_SCRIPT.stat()
    mode = stat_info.st_mode
    
    # Check executable bit
    is_executable = os.access(LAUNCHER_SCRIPT, os.X_OK)
    print(f"  • File mode: {oct(mode)[-3:]}")
    print(f"  • Executable: {is_executable}")
    print(f"  • Readable: {os.access(LAUNCHER_SCRIPT, os.R_OK)}")
    
    assert is_executable, (
        f"Launcher script is not executable: {LAUNCHER_SCRIPT}\n"
        f"Fix with: chmod +x {LAUNCHER_SCRIPT}"
    )
    
    print(f"\n✅ Script has correct executable permissions")


# =============================================================================
# Test: Script Content Validation
# =============================================================================

def test_launcher_script_content():
    """
    Test that the launcher script contains required configuration.
    
    Validates:
        - Script contains shebang (#!/bin/bash)
        - PROJECT_DIR is correctly configured
        - VENV_DIR path is defined
        - MAIN_SCRIPT path is defined
        - Critical functions are present
    
    Raises:
        AssertionError: If required content is missing
    """
    print("\n" + "═" * 70)
    print("TEST: Launcher Script Content Validation")
    print("═" * 70)
    
    print(f"\n🔍 Reading script content: {LAUNCHER_SCRIPT}")
    
    with open(LAUNCHER_SCRIPT, 'r') as f:
        content = f.read()
    
    # Required elements
    required_elements = {
        "Shebang": "#!/bin/bash",
        "Project Dir": f'PROJECT_DIR="{PROJECT_ROOT}"',
        "Venv Reference": "VENV_DIR=",
        "Main Script": "MAIN_SCRIPT=",
        "Validate Function": "validate_environment()",
        "Launch Function": "launch_application()",
        "Test Mode": "run_tests()",
    }
    
    print(f"\n📋 Checking required elements:")
    missing_elements = []
    
    for name, pattern in required_elements.items():
        if pattern in content:
            print(f"  ✓ {name}: Found")
        else:
            print(f"  ✗ {name}: Missing")
            missing_elements.append(name)
    
    assert not missing_elements, (
        f"Launcher script is missing required elements: {', '.join(missing_elements)}"
    )
    
    print(f"\n✅ All required script elements present")


# =============================================================================
# Test: Environment Validation
# =============================================================================

def test_launcher_validates_environment():
    """
    Test that the launcher script can validate the environment.
    
    Validates:
        - Project directory exists
        - Virtual environment exists
        - Main script exists
        - Python executable is available
    
    Raises:
        AssertionError: If environment validation fails
    """
    print("\n" + "═" * 70)
    print("TEST: Environment Validation")
    print("═" * 70)
    
    checks = {
        "Project Directory": PROJECT_ROOT,
        "Virtual Environment": VENV_DIR,
        "Main Script": MAIN_SCRIPT,
        "Python Executable": VENV_DIR / "bin" / "python",
    }
    
    print(f"\n🔍 Validating environment components:")
    
    for name, path in checks.items():
        exists = path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {name}: {path}")
        assert exists, f"{name} not found at {path}"
    
    print(f"\n✅ Environment validation successful")


# =============================================================================
# Test: Launcher Test Mode
# =============================================================================

def test_launcher_test_mode():
    """
    Test that the launcher's --test flag works correctly.
    
    Executes the launcher in test mode and validates:
        - Command runs successfully (exit code 0)
        - Output contains validation messages
        - Python environment is checked
        - Dependencies are verified
    
    Raises:
        AssertionError: If test mode fails or output is missing
    """
    print("\n" + "═" * 70)
    print("TEST: Launcher Test Mode Execution")
    print("═" * 70)
    
    print(f"\n🚀 Executing: {LAUNCHER_SCRIPT} --test")
    
    try:
        result = subprocess.run(
            [str(LAUNCHER_SCRIPT), "--test"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        
        print(f"\n📤 Exit code: {result.returncode}")
        print(f"\n📄 Output:")
        print("─" * 70)
        print(result.stdout)
        if result.stderr:
            print("\n⚠️  Stderr:")
            print(result.stderr)
        print("─" * 70)
        
        # Validate exit code
        assert result.returncode == 0, (
            f"Launcher test mode failed with exit code {result.returncode}\n"
            f"Stdout: {result.stdout}\n"
            f"Stderr: {result.stderr}"
        )
        
        # Validate output content
        output = result.stdout + result.stderr
        required_patterns = [
            "Validating environment",
            "Project directory",
            "Virtual environment",
            "Python version",
        ]
        
        print(f"\n🔍 Checking for required output patterns:")
        for pattern in required_patterns:
            found = pattern.lower() in output.lower()
            status = "✓" if found else "✗"
            print(f"  {status} '{pattern}'")
            assert found, f"Expected output pattern not found: '{pattern}'"
        
        print(f"\n✅ Launcher test mode executed successfully")
        
    except subprocess.TimeoutExpired:
        pytest.fail("Launcher test mode timed out after 30 seconds")
    except Exception as e:
        pytest.fail(f"Launcher test mode execution failed: {e}")


# =============================================================================
# Test: Launcher Help Output
# =============================================================================

def test_launcher_help_output():
    """
    Test that the launcher's --help flag works correctly.
    
    Validates:
        - Help command runs successfully
        - Output contains usage information
        - Options are documented
        - Configuration paths are shown
    
    Raises:
        AssertionError: If help output is missing expected content
    """
    print("\n" + "═" * 70)
    print("TEST: Launcher Help Output")
    print("═" * 70)
    
    print(f"\n🚀 Executing: {LAUNCHER_SCRIPT} --help")
    
    try:
        result = subprocess.run(
            [str(LAUNCHER_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        
        print(f"\n📄 Help output:")
        print("─" * 70)
        print(result.stdout)
        print("─" * 70)
        
        output = result.stdout.lower()
        
        # Expected help content
        expected_content = [
            "usage",
            "media-viewer",
            "--test",
            "--n",
            "--ng",
            "--help",
            "project",
        ]
        
        print(f"\n🔍 Checking help content:")
        for item in expected_content:
            found = item in output
            status = "✓" if found else "✗"
            print(f"  {status} Contains '{item}'")
            assert found, f"Help output missing expected content: '{item}'"
        
        print(f"\n✅ Help output validated successfully")
        
    except subprocess.TimeoutExpired:
        pytest.fail("Launcher help command timed out")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Launcher help command failed: {e}")


def test_launcher_mode_ng_executes_successfully():
    """
    Test that launcher forwards --ng to main.py and exits successfully.
    """
    result = subprocess.run(
        [str(LAUNCHER_SCRIPT), "--ng"],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )

    assert result.returncode == 0, (
        f"Launcher --ng failed with exit code {result.returncode}\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )


def test_launcher_mode_n_executes_successfully():
    """
    Test that launcher forwards --n to main.py and exits successfully.
    """
    result = subprocess.run(
        [str(LAUNCHER_SCRIPT), "--n"],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )

    assert result.returncode == 0, (
        f"Launcher --n failed with exit code {result.returncode}\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )


# =============================================================================
# Test: Python Version in Launcher
# =============================================================================

def test_launcher_python_version():
    """
    Test that the launcher uses the correct Python version.
    
    Validates:
        - Python executable in venv is Python 3.14.x
        - Version matches project requirements
        - Venv Python is used (not system Python)
    
    Raises:
        AssertionError: If Python version is incorrect
    """
    print("\n" + "═" * 70)
    print("TEST: Launcher Python Version Check")
    print("═" * 70)
    
    python_exe = VENV_DIR / "bin" / "python"
    
    print(f"\n🔍 Checking Python at: {python_exe}")
    
    assert python_exe.exists(), f"Python executable not found: {python_exe}"
    
    # Get Python version
    result = subprocess.run(
        [str(python_exe), "--version"],
        capture_output=True,
        text=True,
        check=True
    )
    
    version_output = result.stdout.strip()
    print(f"  • Version output: {version_output}")
    
    # Extract version number
    import re
    match = re.search(r'Python (\d+)\.(\d+)\.(\d+)', version_output)
    assert match, f"Could not parse Python version from: {version_output}"
    
    major, minor, micro = match.groups()
    print(f"  • Parsed version: {major}.{minor}.{micro}")
    
    # Validate Python 3.14.x
    assert major == "3", f"Expected Python 3.x, got {major}.x"
    assert minor == "14", f"Expected Python 3.14.x, got 3.{minor}.x"
    
    print(f"\n✅ Python version correct: 3.14.{micro}")


# =============================================================================
# Main Test Execution
# =============================================================================

if __name__ == "__main__":
    """
    Run all launcher tests when script is executed directly.
    
    Usage:
        python test_launcher.py
        pytest test_launcher.py -v -s
    """
    print("\n" + "═" * 70)
    print("  MEDIA WEB VIEWER - GLOBAL LAUNCHER TEST SUITE")
    print("═" * 70)
    
    # Run all tests
    pytest.main([__file__, "-v", "-s"])
