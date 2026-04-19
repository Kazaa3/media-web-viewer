#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Build Config Master (Centralized Build Metadata)
v1.41.00 - Unified source of truth for packaging and distribution.
"""

import os
from pathlib import Path

# --- PROJECT PATH CALCULATION ---
MAIN_FILE = Path(__file__).resolve()
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, DATA_DIR, MEDIA_DIR, LOGS_DIR
VERSION_FILE = PROJECT_ROOT / "VERSION"

def get_current_version() -> str:
    """Reads the central version from the VERSION file."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding='utf-8').strip()
    return "1.35.0"

# --- CENTRALIZED BUILD METADATA ---
BUILD_PACKAGE_NAME = "media-web-viewer"
BUILD_ARCH = os.environ.get("MWV_BUILD_ARCH", "amd64")
BUILD_VERSION = get_current_version()
BUILD_MAINTAINER = "Media Web Viewer Team <team@media-web-viewer.org>"
BUILD_DESCRIPTION = "A powerful, premium-grade desktop media browser and player orchestration shell."

# Destinations (Internal Staging)
STAGING_SUBDIR = "opt/media-web-viewer"
BIN_SUBDIR = "usr/bin"

# --- CENTRALIZED TEST ORCHESTRATION ---
BUILD_GATE_TESTS = [
    "tests/integration/performance/test_performance_probes.py",
    "tests/integration/tech/bottle/test_bottle_health_latency.py",
    "tests/integration/category/ui/test_installed_packages_ui.py",
    "tests/integration/basic/env/test_environment_packages_fallback.py",
    "tests/integration/category/ui/test_ui_session_stability.py"
]

# --- ZERO-LEAK RSYNC EXCLUSIONS ---
RSYNC_EXCLUDES = [
    ".git/", ".github/", ".vscode/", ".idea/", ".venv*/", "venv/",
    "**/__pycache__/", "*.pyc", "build/", "dist/", "infra/packaging/",
    "media/", "doc*/", "tests/", ".gitignore", "*.spec", "*.deb",
    ".pytest_cache/", ".mypy_cache/", "reinstall_deb.sh", "data/", "packages/"
]

def get_build_summary():
    """Returns a dictionary of build metadata."""
    return {
        "package": BUILD_PACKAGE_NAME,
        "version": BUILD_VERSION,
        "arch": BUILD_ARCH,
        "maintainer": BUILD_MAINTAINER
    }

if __name__ == "__main__":
    import sys
    # If run directly, print metadata for shell scripts
    if len(sys.argv) > 1 and sys.argv[1] == "--tests":
        print("\n".join(BUILD_GATE_TESTS))
    elif len(sys.argv) > 1 and sys.argv[1] == "--excludes":
        print(" ".join([f"--exclude '{ex}'" for ex in RSYNC_EXCLUDES]))
    else:
        print(f"VERSION={BUILD_VERSION}")
        print(f"PACKAGE={BUILD_PACKAGE_NAME}")
        print(f"ARCH={BUILD_ARCH}")
