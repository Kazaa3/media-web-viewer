from pathlib import Path
from typing import Any
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_enzyme")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "Enzyme",
        "description": "High-performance MKV analysis for metadata and tracks using the 'enzyme' library.",
        "supported_tags": ["enzyme_tracks", "enzyme_duration"],
        "supported_codecs": ["mkv"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {
        "max_tracks": {
            "type": "integer",
            "default": 50,
            "description": "Maximum number of tracks to extract for safety."
        }
    }

def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    @brief Extracts MKV metadata using the enzyme library.
    """
    if file_type != ".mkv":
        return tags

    if filename is None:
        filename = path_obj.name
    if settings is None:
        settings = {}

    try:
        import enzyme
        
        # Centralized Configuration (Phase 9 SSOT)
        registry = GLOBAL_CONFIG.get("parser_registry", {})
        enzyme_map = registry.get("tag_mappings", {}).get("enzyme", {})
        
        # Centralized Limits
        limits = GLOBAL_CONFIG.get("parser_limits", {})
        max_tracks = limits.get("max_tracks", settings.get('max_tracks', 50))
        
        with path_obj.open('rb') as f_enz:
            movie = enzyme.MKV(f_enz)
            res = {
                enzyme_map.get('enzyme_tracks', 'enzyme_tracks'): (movie.audio_tracks + movie.video_tracks)[:max_tracks],
                enzyme_map.get('enzyme_duration', 'enzyme_duration'): movie.info.duration.total_seconds() if movie.info and movie.info.duration else None
            }
            tags.update(res)
    except ImportError:
        log.debug(f"[Enzyme] Library not installed, skipping.")
    except Exception as e:
        log.error(f"[Enzyme-Parser] Failed for {filename}: {e}", exc_info=True)

    return tags


