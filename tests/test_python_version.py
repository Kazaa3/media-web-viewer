#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_python_version.py - Validates Python version compatibility for Media Web Viewer.

Tests ensure:
- Minimum Python version requirement (3.10+)
- Compatibility with 3.14.x releases
- Correct version detection
"""

import sys
import platform
from pathlib import Path

# Get project root
ROOT_DIR = Path(__file__).parent.parent


def test_python_version_minimum():
    """Test that Python version meets minimum requirement (3.10+)."""
    version_info = sys.version_info
    
    # Check major.minor >= 3.10
    assert version_info.major >= 3, f"Python {version_info.major}.x is not supported"
    assert (version_info.major == 3 and version_info.minor >= 10) or version_info.major > 3, (
        f"Python {version_info.major}.{version_info.minor} is not supported. "
        f"Minimum required: 3.10.0"
    )


def test_python_version_compatible_314():
    """Test that Python version is 3.14.x for optimal compatibility."""
    version_info = sys.version_info
    
    # Check that we're using 3.14.x (major=3, minor=14)
    assert version_info.major == 3, f"Expected Python 3.x, got {version_info.major}.x"
    assert version_info.minor == 14, (
        f"Expected Python 3.14.x, got {version_info.major}.{version_info.minor}.x"
    )


def test_python_version_detection():
    """Test that Python version can be correctly detected."""
    version = platform.python_version()
    version_info = sys.version_info
    
    # Parse detected version
    parts = version.split(".")
    assert len(parts) >= 2, f"Invalid version format: {version}"
    
    detected_major = int(parts[0])
    detected_minor = int(parts[1])
    
    # Verify detected version matches sys.version_info
    assert detected_major == version_info.major, (
        f"Major version mismatch: platform.python_version()={detected_major}, "
        f"sys.version_info.major={version_info.major}"
    )
    assert detected_minor == version_info.minor, (
        f"Minor version mismatch: platform.python_version()={detected_minor}, "
        f"sys.version_info.minor={version_info.minor}"
    )


def test_python_executable_in_venv():
    """Test that Python executable is from project's virtual environment."""
    venv_dir = ROOT_DIR / ".venv"
    python_exec = Path(sys.executable)
    
    # Check that we're running from the project's venv
    assert venv_dir.exists(), (
        f"Virtual environment not found at {venv_dir}. "
        f"Run: /home/xc/anaconda3/envs/p14/bin/python -m venv .venv"
    )
    
    assert str(python_exec).startswith(str(venv_dir)), (
        f"Python executable is not from project venv!\n"
        f"Expected: {venv_dir}/bin/python\n"
        f"Got: {python_exec}\n"
        f"Run: source .venv/bin/activate"
    )


def test_all_required_modules_available():
    """Test that all critical dependencies are installed."""
    required_modules = [
        'mutagen',      # Audio metadata
        'eel',          # Web interface
        'bottle',       # Web server
        'gevent',       # Async framework
        'vlc',          # VLC integration (optional but preferred)
        'm3u8',         # M3U8 playlist support
    ]
    
    missing_modules = []
    
    for module_name in required_modules:
        try:
            __import__(module_name)
        except ImportError as e:
            # VLC is optional
            if module_name == 'vlc':
                continue
            missing_modules.append(module_name)
    
    assert not missing_modules, (
        f"Missing required modules: {', '.join(missing_modules)}\n"
        f"Run: pip install -r requirements.txt"
    )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
