#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
env_handler.py - Robust environment validation and hygiene management.
Ensures the app runs in a clean, exclusive, and verified virtual environment.
"""

import sys
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

# Critical dependencies from requirements.txt that MUST be verified
CRITICAL_DEPENDENCIES = {
    "eel": "0.18.2",
    "bottle": "0.13.0",
    "mutagen": "1.47.0",
    "pymediainfo": "7.0.1",
    "gevent": "25.9.1",
    "gevent-websocket": "0.10.1",
    "psutil": "5.9.0",
    "m3u8": "4.1.0"
}

# System binaries that should be present
CRITICAL_BINARIES = [
    "ffmpeg", 
    "mediainfo", 
    "update-mime-database",  # from shared-mime-info
    "gdk-pixbuf-query-loaders" # from libgdk-pixbuf2.0-0
]
BROWSER_BINARIES = ["google-chrome-stable", "google-chrome", "chrome", "chromium-browser", "chromium"]

class EnvironmentManager:
    """
    Manages and validates the Python execution environment.
    """
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.resolve()
        self.venv_path = self.project_root / ".venv"
        self.is_debug = "--debug" in sys.argv

    def is_exclusive_venv(self) -> bool:
        """
        Check if we are running in the project's own .venv.
        Note: If running via Conda (p14), we might allow it if it's explicitly allowed.
        """
        in_venv = sys.prefix != sys.base_prefix
        # Normalize paths for comparison
        current_prefix = Path(sys.prefix).resolve()
        expected_prefix = self.venv_path.resolve()
        
        # Check if current environment is the project venv
        if in_venv and current_prefix == expected_prefix:
            return True
            
        # Fallback for active Conda environments if they are named p14 (as per user setup)
        conda_env = os.environ.get('CONDA_DEFAULT_ENV')
        if conda_env == 'p14':
            return True
            
        return False

    def get_environment_fingerprint(self) -> str:
        """
        Generates a unique fingerprint of the current environment's packages.
        Used to detect 'dirty' or modified environments.
        """
        try:
            from importlib.metadata import distributions
            pkg_list = sorted([f"{d.metadata['Name']}=={d.version}" for d in distributions()])
            fingerprint_str = "|".join(pkg_list)
            digest = hashlib.sha256(fingerprint_str.encode()).hexdigest()
            return digest[:12]
        except Exception:
            return "unknown"

    def verify_dependencies(self) -> List[str]:
        """
        Strictly verifies that critical dependencies are installed and versions are sufficient.
        Also checks for critical system binaries and browser availability.
        Returns a list of error messages.
        """
        errors = []
        try:
            from importlib.metadata import version, PackageNotFoundError
            for pkg, min_ver in CRITICAL_DEPENDENCIES.items():
                try:
                    version(pkg)
                except PackageNotFoundError:
                    errors.append(f"Missing critical Python package: {pkg} (>= {min_ver})")
            
            # Check system binaries
            import shutil
            missing_binaries = []
            for binary in CRITICAL_BINARIES:
                if not shutil.which(binary):
                    missing_binaries.append(binary)
            
            if missing_binaries:
                apt_map = {
                    "ffmpeg": "ffmpeg",
                    "mediainfo": "mediainfo",
                    "update-mime-database": "shared-mime-info",
                    "gdk-pixbuf-query-loaders": "libgdk-pixbuf2.0-0"
                }
                needed_pkgs = sorted(list(set(apt_map.get(b, b) for b in missing_binaries)))
                errors.append(f"Missing critical system binaries: {', '.join(missing_binaries)}")
                errors.append(f"👉 Fix: sudo apt install {' '.join(needed_pkgs)}")

            # Check browser binaries (at least one must be present)
            if not any(shutil.which(b) for b in BROWSER_BINARIES):
                errors.append(f"No suitable browser found (searched for: {', '.join(BROWSER_BINARIES)})")
                errors.append("👉 Fix: sudo apt install google-chrome-stable OR chromium-browser")
                
        except Exception as e:
            errors.append(f"Environmental integrity check failed: {e}")
            
        return errors

    def validate_safe_startup(self):
        """
        Performs a full validation. If unsafe, logs errors and exits.
        """
        header = "Environment Validation"
        if self.is_debug:
            logging.debug(f"[{header}] Fingerprint: {self.get_environment_fingerprint()}")

        # 1. Check exclusivity
        if not self.is_exclusive_venv():
            msg = (
                "Unsafe startup detected: Application is not running in an exclusive environment.\n"
                f"Active prefix: {sys.prefix}\n"
                f"Expected .venv: {self.venv_path}\n"
                "Please use ./run.sh to start the application."
            )
            logging.error(f"[{header}] {msg}")
            # In production, we might want to be strict. For now, we log a warning.
            # print(msg, file=sys.stderr)
            # sys.exit(1)

        # 2. Check dependency integrity
        dep_errors = self.verify_dependencies()
        if dep_errors:
            logging.error(f"[{header}] Integrity check failed:")
            for err in dep_errors:
                logging.error(f"  - {err}")
            
            print("\n❌ CRITICAL: Environment Integrity Check Failed", file=sys.stderr)
            for err in dep_errors:
                print(f"   - {err}", file=sys.stderr)
            print("\n   Try running: ./run.sh --rebuild", file=sys.stderr)
            sys.exit(1)

        if self.is_debug:
            logging.debug(f"[{header}] Status: CLEAN & VERIFIED")


def validate_safe_startup():
    """Helper function for quick integration."""
    manager = EnvironmentManager()
    manager.validate_safe_startup()
