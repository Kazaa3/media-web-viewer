#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Build Config Master (Centralized Build Metadata)
v1.35.68 - Unified source of truth for packaging and distribution.
"""

import os
from pathlib import Path

# --- PROJECT PATH CALCULATION ---
MAIN_FILE = Path(__file__).resolve()
PROJECT_ROOT = MAIN_FILE.parent.parent.parent
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

def get_build_summary():
    """Returns a dictionary of build metadata."""
    return {
        "package": BUILD_PACKAGE_NAME,
        "version": BUILD_VERSION,
        "arch": BUILD_ARCH,
        "maintainer": BUILD_MAINTAINER
    }

if __name__ == "__main__":
    # If run directly, print metadata for shell scripts
    print(f"VERSION={BUILD_VERSION}")
    print(f"PACKAGE={BUILD_PACKAGE_NAME}")
    print(f"ARCH={BUILD_ARCH}")
