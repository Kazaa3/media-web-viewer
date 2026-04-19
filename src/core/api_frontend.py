import os
import time
from src.core.eel_shell import eel
from pathlib import Path
from src.core.config_master import GLOBAL_CONFIG, EEL_SETTINGS, LAUNCH_PROFILE
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
    
    return EEL_SETTINGS.get("mode", "chrome")

@eel.expose
def get_frontend_settings():
    """Exposes window size and resolution settings to the UI."""
    return {
        "window_size": EEL_SETTINGS["size"],
        "settings": EEL_SETTINGS,
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

# --- UI & Event Orchestration (Migrated from main.py v1.54.018) ---

@eel.expose
def report_spawn():
    """Reports workstation boot readiness."""
    try:
        from src.core.main import spawn_event
    except ImportError:
        # Fallback for circular imports during refactor
        return False
    if not spawn_event.is_set():
        spawn_event.set()

@eel.expose
def log_gui_event(category, action, details=""):
    """General purpose GUI event logging for forensic analysis."""
    log.info(f"[JS-NAV] [{category}] {action} | {details}")

@eel.expose
def log_spawn_event(component_id, status):
    """Logs the instantiation/hydration of a UI component (v1.46.03)."""
    log.info(f"🚀 [SPAWN-LOG] {component_id.upper()} -> {status}")
    return True

@eel.expose
def get_footer_registry():
    """ Returns a merged dict of primary flat flags and granular footer sub-settings. """
    settings = GLOBAL_CONFIG.get("ui_settings", {})
    flat_keys = [
        "enable_diagnostics_hud", "enable_dom_auditor", "enable_technical_hud",
        "enable_sync_anchor", "enable_footer_hud_cluster", "enable_zen_mode",
        "enable_footer_db_status"
    ]
    resp = {k: settings.get(k, False) for k in flat_keys}
    resp.update(settings.get("footer_settings", {}))
    return resp

@eel.expose
def set_footer_element_state(element_key: str, is_active: bool):
    """ Dedicated high-level bridge to toggle footer components and persist state. """
    log.info(f"[UI-ORCHESTRATION] Requesting state change for footer component: {element_key} -> {is_active}")
    from src.core.api_config import set_ui_config_value
    return set_ui_config_value(element_key, is_active)

@eel.expose
def report_items_spawned(count, source="frontend"):
    """ Formal DOM test reporting. """
    log.info(f"[DOM-TEST] [{'SUCCESS' if count > 0 else 'EMPTY'}] Items in DOM: {count} (Source: {source})")
    return {"status": "counts_logged", "timestamp": time.time()}

@eel.expose
def report_playback_state(is_playing, item_name, current_time):
    """ Reports the current playback state from the frontend. """
    log.info(f"[DOM-TEST] [PLAYBACK] {'Playing' if is_playing else 'Stopped'} | Item: {item_name} | Pos: {current_time:.1f}s")
    return {"status": "playback_logged"}
