import sys
import shutil
import os
import eel
from pathlib import Path
from src.core.config_master import GLOBAL_CONFIG, FRONTEND_SETTINGS, WINDOW_SIZE, LAUNCH_PROFILE
from src.core.logger import get_logger

log = get_logger("api_frontend")

def discover_browser():
    """
    Aggressively discover a compatible browser for the Eel engine.
    Returns the absolute path to the binary or None.
    """
    # 1. Check MWV_BROWSER_PATH env var
    env_path = os.environ.get("MWV_BROWSER_PATH")
    if env_path and os.path.exists(env_path):
        return env_path

    # 2. Check Registry (v1.46.136)
    browsers = GLOBAL_CONFIG.get("browsers", ["google-chrome", "chromium", "microsoft-edge", "firefox"])
    for b in browsers:
        path = shutil.which(b)
        if path:
            return path
    
    return None

def get_eel_mode():
    """
    Determines the Eel launch mode based on LAUNCH_PROFILE and browser availability.
    """
    if LAUNCH_PROFILE["no_gui"]:
        return False
    if LAUNCH_PROFILE["connectionless"]:
        return None
    
    browser_path = discover_browser()
    if not browser_path:
        log.warning("[Frontend] No compatible browser found for 'chrome' mode. Falling back to default.")
        return None
    
    return FRONTEND_SETTINGS.get("mode", "chrome")

@eel.expose
def get_frontend_settings():
    """Exposes window size and resolution settings to the UI."""
    return {
        "window_size": WINDOW_SIZE,
        "settings": FRONTEND_SETTINGS,
        "launch_profile": LAUNCH_PROFILE
    }

@eel.expose
def get_browser_metadata():
    """Forensic metadata about the active/discovered browser."""
    path = discover_browser()
    return {
        "path": path,
        "found": path is not None,
        "type": os.path.basename(path) if path else "none",
        "eel_mode": get_eel_mode()
    }
