from pathlib import Path
from typing import Any
from src.core.logger import get_logger
from . import cvlc_parser
from . import python_vlc_parser

# Specialized logger (v1.46.132 Bridge Modernized)
log = get_logger("parser_vlc_bridge")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "VLC Trinity Bridge",
        "description": "Unified entry point for VLC services. Dispatches to CVLC Master and LibVLC Python bindings.",
        "supported_tags": ["*"],
        "supported_codecs": ["*"]
    }

def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight', settings: dict[str, Any] = None) -> dict[str, Any]:
    """
    @brief Dispatches extraction to the VLC Trinity modules.
    """
    if filename is None:
        filename = path.name
    if settings is None:
        settings = {}

    log.debug(f"🔗 [VLC-Bridge] Dispatching forensic analysis for '{filename}'")
    
    # 1. Primary: CVLC Master (CLI)
    tags = cvlc_parser.parse(path, file_type, tags, filename, mode, settings)
    
    # 2. Secondary: Python-VLC (LibVLC)
    # Already included in exhaustive mode within cvlc_parser, 
    # but we can force it here for standard/full modes if needed.
    if mode == 'full' and 'vlc_python_tracks' not in tags.get('full_tags', {}):
        log.info(f"🔄 [VLC-Bridge] Secondary LibVLC pass for '{filename}'")
        tags = python_vlc_parser.parse(path, file_type, tags, filename, mode, settings)

    return tags


