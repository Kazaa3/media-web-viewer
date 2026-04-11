import subprocess
import json
from pathlib import Path
from typing import Any
from src.core.config_master import GLOBAL_CONFIG


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
    @details Extrahiert Metadaten mittels mkvmerge JSON-Identifizierung.
    @param path Absolute path / Absoluter Pfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    if file_type.lower() != '.mkv':
        return tags

    if settings is None:
        settings = {}

    try:
        # mkvmerge -J provides a nice structured JSON
        mkvmerge_bin = GLOBAL_CONFIG["program_paths"].get("mkvmerge", "mkvmerge")
        cmd = [mkvmerge_bin, "-J"]
        
        # Add custom flags if any
        custom_flags = settings.get('cli_flags', '').split()
        if custom_flags:
            cmd.extend(custom_flags)
            
        cmd.append(str(path))
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=settings.get('timeout', 10), encoding='utf-8', errors='ignore')
        
        if result.returncode != 0:
            return tags
            
        data = json.loads(result.stdout)
        
        container = data.get('container', {})
        properties = container.get('properties', {})
        
        # Duration: reported in nanoseconds
        if not tags.get('duration') and 'duration' in properties:
            try:
                # nanoseconds -> seconds
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
        # Track information
        if mode == 'full':
            # Basic track stats
            tags['track_info'] = tracks

        # Simple codec/container fallback
        if not tags.get('container') and container.get('type'):
            tags['container'] = container['type'].lower()

    except subprocess.TimeoutExpired:
        pass
    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    return tags
