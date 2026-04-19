import os
import sys
import time
from typing import Any, Dict, List
from src.core.config_master import (
    GLOBAL_CONFIG, MASTER_CAT_MAP, TECH_MARKERS,
    set_config_value as master_set
)
from src.core.logger import get_logger

# Robust Eel shell fallback
try:
    from src.core.eel_shell import eel
except ImportError:
    import eel

log = get_logger("api_config")

@eel.expose
def get_category_master():
    """Returns the centralized category mapping (v1.35.76 SSOT)."""
    log.info("[BD-AUDIT] Handshake: get_category_master requested.")
    return MASTER_CAT_MAP

@eel.expose
def get_global_config():
    """Returns the full centralized configuration (v1.41.00)."""
    log.info("[BD-AUDIT] Handshake: get_global_config requested.")
    return GLOBAL_CONFIG

@eel.expose
def get_tech_markers():
    """Returns the centralized transcoding tech markers (v1.35.76 SSOT)."""
    log.info("[BD-AUDIT] Handshake: get_tech_markers requested.")
    return TECH_MARKERS

@eel.expose
def set_hydration_mode(mode: str) -> bool:
    """Sets the hydration mode for library retrieval (v1.41.67)."""
    mode_normalized = mode.lower()
    GLOBAL_CONFIG["forensic_hydration_registry"]["mode"] = mode_normalized
    log.info(f"[HYDR-TRACE] Centralized Hydration mode updated to: {mode_normalized}")
    return True

@eel.expose
def set_ui_config_value(key: str, value: Any):
    """
    Sets a configuration value in GLOBAL_CONFIG (v1.38.05).
    Special handling for nested ui_fragments and functional modules.
    """
    log.info(f"[CONFIG] UI Request: {key} -> {value}")

    # Check if it's a nested ui_fragment toggle
    if key.startswith("ui_fragments."):
        frag_key = key.split(".")[1]
        if "ui_settings" in GLOBAL_CONFIG and "ui_fragments" in GLOBAL_CONFIG["ui_settings"]:
            GLOBAL_CONFIG["ui_settings"]["ui_fragments"][frag_key] = value
            log.info(f"[CONFIG] Fragment {frag_key} toggled: {value}")
            return True

    # Check if it's a nested footer_settings toggle (v1.41.158 Extension)
    if key.startswith("footer_settings."):
        feat_key = key.split(".")[1]
        if "ui_settings" in GLOBAL_CONFIG and "footer_settings" in GLOBAL_CONFIG["ui_settings"]:
            GLOBAL_CONFIG["ui_settings"]["footer_settings"][feat_key] = value
            log.info(f"[CONFIG] Granular Footer Feature {feat_key} toggled: {value}")
            return True

    # Generic set
    return master_set(key, value)
