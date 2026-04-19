import subprocess
import re
from pathlib import Path
from typing import Any
from src.core.config_master import GLOBAL_CONFIG
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_mkvinfo")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "MKVInfo",
        "description": "Standard diagnostic tool from MKVToolNix for analyzing Matroska file structures.",
        "supported_tags": ["title", "duration", "muxing_app", "writing_app"],
        "supported_codecs": ["mkv", "webm"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {
        "timeout": {
            "type": "integer",
            "default": 10,
            "description": "Maximum execution time in seconds."
        }
    }

def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight', settings: dict[str, Any] = None) -> dict[str, Any]:
    """
    @brief Extracts metadata using mkvinfo CLI.
    """
    if file_type.lower() != '.mkv':
        return tags

    if filename is None:
        filename = path.name
    if settings is None:
        settings = {}

    try:
        bin_path = GLOBAL_CONFIG.get("program_paths", {}).get("mkvinfo", "mkvinfo")
        cmd = [bin_path, str(path)]
        
        timeout = settings.get('timeout', 10)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='ignore')
        
        if result.returncode != 0:
            log.warning(f"[MKVInfo-Parser] Failed with exit code {result.returncode} for {filename}")
            return tags
            
        output = result.stdout
        
        # Centralized Tag Mappings (Phase 9 SSOT)
        mkvinfo_map = GLOBAL_CONFIG.get("parser_registry", {}).get("tag_mappings", {}).get("mkvinfo", {})

        # Parse Duration: | + Duration: 01:23:45.678 (5025.678s)
        duration_match = re.search(r"Duration: .*?\((\d+\.\d+)s\)", output)
        if duration_match and not tags.get('duration'):
            try:
                tags['duration'] = int(float(duration_match.group(1)))
            except (ValueError, TypeError):
                pass

        # Parse Title
        title_match = re.search(r"Title: (.*)", output)
        if title_match and not tags.get('title'):
            tags['title'] = title_match.group(1).strip()

        # Muxing App
        muxing_app_match = re.search(r"Multiplexing application: (.*)", output)
        if muxing_app_match:
            tags[mkvinfo_map.get('muxing_app', 'muxing_app')] = muxing_app_match.group(1).strip()

        # Writing App
        writing_app_match = re.search(r"Writing application: (.*)", output)
        if writing_app_match:
            tags[mkvinfo_map.get('writing_app', 'writing_app')] = writing_app_match.group(1).strip()

    except subprocess.TimeoutExpired:
        log.warning(f"[MKVInfo-Parser] Timeout expired for {filename}")
    except Exception as e:
        log.error(f"[MKVInfo-Parser] Unexpected error for {filename}: {e}", exc_info=True)

    return tags


