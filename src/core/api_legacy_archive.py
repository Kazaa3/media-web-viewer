"""
Forensic Legacy Archive (v1.54.022) - STABILIZED STUB
This module contains essential legacy functions and stubs to ensure workstation boot stability.
"""

import os
import sys
import time
import json
import re
import shutil
import sqlite3
import subprocess
import threading
import logging
import platform
import socket
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, cast

# Project-level imports
from src.core.eel_shell import eel
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT, FRONTEND_SETTINGS, EEL_SETTINGS, LAUNCH_PROFILE
from src.core.logger import get_logger
from src.core import db
from src.core.models import MASTER_CAT_MAP, TECH_MARKERS, MediaItem

log = get_logger("api_legacy_archive")

@eel.expose
def _detect_python_environment():
    """Detect current Python environment: system, venv, or conda."""
    python_version = platform.python_version()
    python_executable = sys.executable
    in_venv = sys.prefix != sys.base_prefix
    env_type = "venv" if in_venv else "system"
    return (env_type, "primary", sys.prefix, python_version, python_executable)

@eel.expose
def get_global_config():
    """Returns the global configuration object."""
    return GLOBAL_CONFIG

@eel.expose
def get_environment_info(force_refresh=False):
    """Returns comprehensive information about the Python environment."""
    return {
        "env_type": "venv",
        "python_version": platform.python_version(),
        "executable": sys.executable,
        "packages": []
    }

@eel.expose
def _get_requirements_status():
    return {"available": True, "installed": [], "missing": []}

@eel.expose
def _parse_nfo_file(nfo_path):
    return {}

@eel.expose
def _scan_media_execution(dir_path=None, clear_db=True):
    pass

@eel.expose
def confirm_receipt(event_name):
    log.info(f"Receipt confirmed for {event_name}")

@eel.expose
def find_venv_pid(venv_name):
    return None

@eel.expose
def get_category_master():
    return MASTER_CAT_MAP

@eel.expose
def get_mock_data_enabled():
    return False

@eel.expose
def get_playlist_forensics():
    return {}

@eel.expose
def get_tech_markers():
    return TECH_MARKERS

@eel.expose
def list_feature_modal_items():
    return []

@eel.expose
def prune_playlist_orphans(playlist_id):
    pass

@eel.expose
def read_file(filename, context='logbuch'):
    return None

@eel.expose
def rtt_item_test(data):
    return {"status": "ok"}

@eel.expose
def rtt_stress_ping(index, total):
    return {"status": "ok"}

@eel.expose
def run_debug_test():
    return "Debug test completed (Stub)"

@eel.expose
def run_selenium_session_tests(options=None):
    return {"status": "skipped", "message": "Selenium tests not available in stub mode"}

@eel.expose
def sanitize_json_utf8(data):
    return data

@eel.expose
def set_hydration_mode(mode: str) -> bool:
    return True

@eel.expose
def set_mock_data_enabled(enabled):
    pass

@eel.expose
def set_ui_config_value(key: str, value: Any):
    pass

@eel.expose
def test_pyautogui():
    return {"status": "error", "message": "PyAutoGUI not available in stub"}

@eel.expose
def update_browse_dir(path):
    pass

@eel.expose
def update_library_dir(path):
    pass
