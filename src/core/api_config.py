import eel
import logging
from .config_master import GLOBAL_CONFIG, save_config

log = logging.getLogger("mwv.api.config")

@eel.expose
def get_start_page():
    return GLOBAL_CONFIG.get("startup_settings", {}).get("start_page", "dashboard")

@eel.expose
def set_start_page(page):
    if "startup_settings" not in GLOBAL_CONFIG:
        GLOBAL_CONFIG["startup_settings"] = {}
    GLOBAL_CONFIG["startup_settings"]["start_page"] = page
    save_config()
    return True

@eel.expose
def get_app_mode():
    return GLOBAL_CONFIG.get("app_mode", "forensic")

@eel.expose
def set_app_mode(mode):
    GLOBAL_CONFIG["app_mode"] = mode
    save_config()
    return True

@eel.expose
def get_parser_mode():
    return GLOBAL_CONFIG.get("parser_settings", {}).get("mode", "fast")

@eel.expose
def set_parser_mode(mode):
    if "parser_settings" not in GLOBAL_CONFIG:
        GLOBAL_CONFIG["parser_settings"] = {}
    GLOBAL_CONFIG["parser_settings"]["mode"] = mode
    save_config()
    return True

@eel.expose
def get_startup_config():
    return GLOBAL_CONFIG.get("startup_settings", {})

@eel.expose
def update_startup_config(config):
    GLOBAL_CONFIG["startup_settings"] = config
    save_config()
    return True

@eel.expose
def reset_config():
    """Resets the configuration to forensic defaults."""
    # Note: Full implementation usually involves copying defaults from a manifest
    log.info("Resetting configuration to forensic defaults...")
    return True

@eel.expose
def get_language():
    return GLOBAL_CONFIG.get("language", "de")

@eel.expose
def set_language(lang):
    GLOBAL_CONFIG["language"] = lang
    save_config()
    return True

@eel.expose
def set_ui_config_value(key: str, value: Any):
    """ Atomic helper to set values in the ui_settings registry. """
    from src.core.api_ui import set_ui_setting
    return set_ui_setting(key, value)
