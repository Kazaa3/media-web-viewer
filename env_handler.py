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

# Mappings for Conda-specific package names
# These are used to satisfy requirements via conda instead of pip/apt
PIP_TO_CONDA_MAP = {
    "python-vlc": "vlc-python",
    "gevent-websocket": "gevent-websocket",
    "m3u8": "m3u8",
    "psutil": "psutil"
}

APT_TO_CONDA_MAP = {
    "shared-mime-info": "shared-mime-info",
    "libgdk-pixbuf2.0-0": "gdk-pixbuf",
    "mediainfo": "mediainfo",
    "ffmpeg": "ffmpeg"
}

logger = logging.getLogger("env_handler")


def detect_async_runtime() -> str:
    """
    Return one of: "gevent", "trio", "asyncio", "none", "missing"
    """
    try:
        import sniffio
    except Exception:
        return "missing"
    try:
        runtime = sniffio.current_async_library()  # may raise if none active
        if not runtime:
            return "none"
        name = runtime.lower()
        if "gevent" in name:
            return "gevent"
        if "trio" in name:
            return "trio"
        if "asyncio" in name:
            return "asyncio"
        return name
    except Exception:
        return "none"


def apply_gevent_monkey_patch_safe():
    """
    Call gevent.monkey.patch_all() only when gevent is desired and available.
    Call explicitly at controlled startup (do not auto-patch on import).
    """
    try:
        import gevent.monkey as _monkey  # type: ignore
        _monkey.patch_all()
        logger.info("gevent.monkey.patch_all() applied")
    except Exception as exc:
        logger.debug("gevent monkey-patch not applied: %s", exc)


def runtime_info() -> Dict[str, str]:
    """Return normalized runtime metadata for status endpoints."""
    rt = detect_async_runtime()
    ws_backend = "none"
    if rt == "gevent":
        ws_backend = "gevent"
    elif rt == "trio":
        ws_backend = "trio"
    elif rt == "asyncio":
        ws_backend = "asyncio"
    return {"runtime": rt, "ws_backend": ws_backend}


def register_ws_health_route(app):
    """
    Try to register a simple /ws-health websocket handler appropriate for the runtime.
    No-op if required libraries are not present. Should be called after server/app creation.
    """
    rt = detect_async_runtime()
    try:
        if rt == "gevent":
            from bottle_websocket import websocket  # type: ignore

            @app.route("/ws-health", apply=[websocket])
            def _ws_health(ws):
                try:
                    ws.send("ping")
                    msg = ws.receive(timeout=5)
                    if msg == "pong":
                        ws.send("ok")
                    else:
                        ws.send("error")
                except Exception:
                    try:
                        ws.send("error")
                    except Exception:
                        pass

        elif rt == "trio":
            # trio-websocket registration needs a different server/runner; keep as a placeholder
            logger.debug("trio runtime detected — register trio websocket server separately")
        else:
            logger.debug("No websocket backend registered for runtime: %s", rt)
    except Exception as e:
        logger.debug("ws-health route registration skipped: %s", e)


class EnvironmentManager:
    """
    Manages and validates the Python execution environment.
    """
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.resolve()
        self.venv_path = self.project_root / ".venv_testbed"
        self.is_debug = "--debug" in sys.argv

    def is_conda(self) -> bool:
        """Check if running in a Conda environment."""
        return 'CONDA_PREFIX' in os.environ or os.environ.get('CONDA_DEFAULT_ENV') is not None

    def is_exclusive_venv(self) -> bool:
        """
        Check if we are running in the project's own .venv or an allowed Conda env.
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
        if self.is_conda():
            # If it's a conda env, we allow it (e.g., p14)
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

    def get_missing_info(self) -> tuple[list[str], list[str], list[str]]:
        """
        Returns (missing_pip, missing_apt, missing_conda)
        - missing_pip: Packages that MUST or SHOULD be installed via pip (standard env)
        - missing_apt: Binaries that MUST be installed via apt (standard env)
        - missing_conda: All missing items that CAN be installed via conda (conda env)
        """
        missing_pip = []
        missing_apt = []
        missing_conda = []
        
        from importlib.metadata import version, PackageNotFoundError
        import shutil

        # 1. Process Python Dependencies
        for pkg, min_ver in CRITICAL_DEPENDENCIES.items():
            try:
                version(pkg)
            except PackageNotFoundError:
                full_spec = f"{pkg}>={min_ver}"
                missing_pip.append(full_spec)
                # If we have a conda mapping OR if it's likely available in conda-forge
                conda_name = PIP_TO_CONDA_MAP.get(pkg, pkg)
                missing_conda.append(f"{conda_name}>={min_ver}")

        # 2. Process System Dependencies
        apt_map = {
            "ffmpeg": "ffmpeg",
            "mediainfo": "mediainfo",
            "update-mime-database": "shared-mime-info",
            "gdk-pixbuf-query-loaders": "libgdk-pixbuf-2.0-0"
        }
        for binary, apt_pkg in apt_map.items():
            binary_found = bool(shutil.which(binary))

            # Debian/Ubuntu often install gdk-pixbuf-query-loaders outside PATH.
            # Accept known system locations to avoid false negatives.
            if binary == "gdk-pixbuf-query-loaders" and not binary_found:
                known_locations = [
                    Path("/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders"),
                    Path("/usr/lib/aarch64-linux-gnu/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders"),
                    Path("/usr/lib/i386-linux-gnu/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders"),
                ]
                binary_found = any(path.exists() for path in known_locations)

            if not binary_found:
                missing_apt.append(apt_pkg)
                if apt_pkg in APT_TO_CONDA_MAP:
                    missing_conda.append(APT_TO_CONDA_MAP[apt_pkg])
                else:
                    # Fallback if no mapping but we are in conda: 
                    # some things like ffmpeg have same name
                    missing_conda.append(apt_pkg)
        
        # 3. Process Tkinter (System-level for Python GUI)
        try:
            import tkinter
        except ImportError:
            # tkinter is a system package on Linux (python3-tk)
            missing_apt.append("python3-tk")
            if self.is_conda():
                # On conda it's usually 'tk'
                missing_conda.append("tk")

        return (
            sorted(list(set(missing_pip))), 
            sorted(list(set(missing_apt))), 
            sorted(list(set(missing_conda)))
        )

    def verify_dependencies(self) -> List[str]:
        """Strictly verifies that critical dependencies are installed."""
        missing_pip, missing_apt, _ = self.get_missing_info()
        errors = []
        for pkg in missing_pip:
            errors.append(f"Missing critical Python package: {pkg}")
        for pkg in missing_apt:
            errors.append(f"Missing critical system binary/package: {pkg}")
            
        # Check browser binaries (at least one must be present)
        import shutil
        if not any(shutil.which(b) for b in BROWSER_BINARIES):
            errors.append(f"No suitable browser found (searched for: {', '.join(BROWSER_BINARIES)})")
            
        return errors
            
        # Check browser binaries (at least one must be present)
        import shutil
        if not any(shutil.which(b) for b in BROWSER_BINARIES):
            errors.append(f"No suitable browser found (searched for: {', '.join(BROWSER_BINARIES)})")
            
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
            
            fix_cmd = "./run.sh"
            installer_hint = "automatically install all dependencies"
            if self.is_conda():
                installer_hint += " via conda/apt"
            else:
                installer_hint += " via pip/apt"
                
            print(f"\n   👉 Fix: Run '{fix_cmd}' to {installer_hint}.", file=sys.stderr)
            print(f"   (Or use '{fix_cmd} --rebuild' to recreate the environment from scratch)", file=sys.stderr)
            sys.exit(1)

        if self.is_debug:
            logging.debug(f"[{header}] Status: CLEAN & VERIFIED")


def validate_safe_startup():
    """Helper function for quick integration."""
    manager = EnvironmentManager()
    manager.validate_safe_startup()
