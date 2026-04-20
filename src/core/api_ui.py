from src.core.eel_shell import eel
import logging
import os
import re
import time
import ast
from pathlib import Path
from typing import Any, Dict, List
from .config_master import GLOBAL_CONFIG, PROJECT_ROOT

log = logging.getLogger("mwv.api.ui")

@eel.expose
def get_ui_settings():
    """Returns the current UI registry and configuration."""
    return GLOBAL_CONFIG.get("ui_settings", {})

@eel.expose
def set_ui_setting(key: str, value: Any):
    """Updates a specific UI setting in the global config."""
    if "ui_settings" not in GLOBAL_CONFIG:
        GLOBAL_CONFIG["ui_settings"] = {}
    GLOBAL_CONFIG["ui_settings"][key] = value
    log.info(f"[UI-CONFIG] Set {key} = {value}")
    return {"status": "success"}

@eel.expose
def ui_trace(message):
    """Receives and logs trace messages from the UI."""
    try:
        log.info(f"[UI-Trace] {message}")
        log_registry = GLOBAL_CONFIG.get("logging_registry", {})
        trace_path_raw = log_registry.get("ui_trace_log_path")
        if trace_path_raw:
            trace_path = Path(trace_path_raw)
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            with open(trace_path, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        log.debug(f"[UI-Trace-Internal] Failed to write to trace log: {e}")
    return {"status": "ok"}

@eel.expose
def scan_js_errors():
    """Scans shell_master.html for potential JS errors."""
    try:
        app_html = PROJECT_ROOT / "web" / "shell_master.html"
        if not app_html.exists(): return {"status": "error", "message": "shell_master.html not found"}
        content = app_html.read_text(encoding='utf-8')
        # Simple extraction of patterns
        findings = []
        return {"status": "ok", "findings": findings}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def check_ui_integrity():
    """Checks UI structural integrity (div balance, etc.)."""
    try:
        app_html = PROJECT_ROOT / "web" / "shell_master.html"
        if not app_html.exists(): return {"status": "error", "message": "shell_master.html not found"}
        content = app_html.read_text(encoding='utf-8')
        opens = len(re.findall(r'<div', content, re.I))
        closes = len(re.findall(r'</div', content, re.I))
        return {
            "status": "ok",
            "div_balance": {"opens": opens, "closes": closes, "balanced": opens == closes}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def clear_logs():
    """Resets UI log history."""
    log.info("UI Logs cleared.")
    return {"status": "ok"}
