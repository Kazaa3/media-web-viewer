import subprocess
import json
from pathlib import Path
from typing import Any
from src.core.config_master import GLOBAL_CONFIG
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_mkvmerge")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "MKVMerge",
        "description": "JSON-based identification tool from MKVToolNix for MKV/Matroska files.",
        "supported_tags": ["title", "duration", "muxing_app", "writing_app", "track_info"],
        "supported_codecs": ["mkv", "webm"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {
        "cli_flags": {
            "type": "string",
            "default": "",
            "description": "Additional custom CLI flags for mkvmerge -J."
        },
        "timeout": {
            "type": "integer",
            "default": 10,
            "description": "Maximum execution time in seconds."
        }
    }

def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight', settings: dict[str, Any] = None) -> dict[str, Any]:
    """
    @brief Extracts metadata using mkvmerge JSON identification.
    """
    if file_type.lower() != '.mkv':
        return tags

    if filename is None:
        filename = path.name
    if settings is None:
        settings = {}

    try:
        mkvmerge_bin = GLOBAL_CONFIG.get("program_paths", {}).get("mkvmerge", "mkvmerge")
        cmd = [mkvmerge_bin, "-J"]
        
        custom_flags = settings.get('cli_flags', '').split()
        if custom_flags:
            cmd.extend(custom_flags)
            
        cmd.append(str(path))
        
        timeout = settings.get('timeout', 10)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='ignore')
        
        if result.returncode != 0:
            log.warning(f"[MKVMerge-Parser] Failed with exit code {result.returncode} for {filename}")
            return tags
            
        data = json.loads(result.stdout)
        
        container = data.get('container', {})
        properties = container.get('properties', {})
        
        # Duration: reported in nanoseconds
        if not tags.get('duration') and 'duration' in properties:
            try:
                tags['duration'] = int(int(properties['duration']) / 1_000_000_000)
            except (ValueError, TypeError):
                pass

        # Title
        if not tags.get('title') and 'title' in properties:
            tags['title'] = properties['title']

        # Apps
        if 'muxing_application' in properties:
            tags['muxing_app'] = properties['muxing_application']
        if 'writing_application' in properties:
            tags['writing_app'] = properties['writing_application']

        # Tracks
        tracks = data.get('tracks', [])
        if mode == 'full':
            tags['track_info'] = tracks

        if not tags.get('container') and container.get('type'):
            tags['container'] = container['type'].lower()

    except subprocess.TimeoutExpired:
        log.warning(f"[MKVMerge-Parser] Timeout expired for {filename}")
    except json.JSONDecodeError as je:
        log.error(f"[MKVMerge-Parser] JSON decode failed for {filename}: {je}")
    except Exception as e:
        log.error(f"[MKVMerge-Parser] Unexpected error for {filename}: {e}", exc_info=True)

    return tags

