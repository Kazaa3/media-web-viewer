import os
from pathlib import Path
from typing import Dict, Any, Optional

from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT
from src.parsers.media_parser import extract_metadata as _parse_media
from src.core.logger import get_logger

log = get_logger("api_parsing")

@eel.expose
def get_media_metadata(file_path: str, mode: str = "lightweight", **kwargs) -> Dict[str, Any]:
    """
    High-level API to extract metadata from a media file.
    Orchestrates the parser chain based on the requested forensic mode.
    """
    abs_path = os.path.abspath(file_path)
    filename = os.path.basename(abs_path)
    
    log.info(f"[API-Parsing] Requesting metadata for '{filename}' (Mode: {mode})")
    
    try:
        tags = _parse_media(abs_path, filename, mode=mode, **kwargs)
        return tags
    except Exception as e:
        log.error(f"[API-Parsing] Failed to parse '{filename}': {e}")
        return {"error": str(e), "name": filename, "path": abs_path}

@eel.expose
def probe_forensic_depth(file_path: str, depth: str = "standard") -> Dict[str, Any]:
    """
    Performs a deep forensic audit with varying scan depths.
    Mapped to: quick (lightweight), standard (full), deep (ultimate).
    """
    depth_map = {
        "quick": "lightweight",
        "standard": "full",
        "deep": "ultimate"
    }
    mode = depth_map.get(depth, "lightweight")
    return get_media_metadata(file_path, mode=mode)

@eel.expose
def get_parser_chain_info() -> Dict[str, Any]:
    """Returns the currently active parser chain configuration."""
    registry = GLOBAL_CONFIG.get("parser_registry", {})
    return {
        "default_chain": registry.get("default_chain", []),
        "ultimate_chain": registry.get("ultimate_chain", []),
        "active_mode": GLOBAL_CONFIG.get("parser_mode", "lightweight")
    }
