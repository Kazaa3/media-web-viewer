from pathlib import Path
from typing import Any
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_ebml")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "EBML Parser",
        "description": "Deep inspection of EBML (Matroska/WebM) container segments and tracks.",
        "supported_tags": ["ebml_title", "ebml_duration", "ebml_tracks"],
        "supported_codecs": ["mkv", "webm"]
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
    @brief Extracts deep EBML metadata using the ebml library.
    """
    if file_type not in [".mkv", ".webm"]:
        return tags

    if filename is None:
        filename = path_obj.name
    if settings is None:
        settings = {}

    try:
        from ebml.container import File
        
        # Centralized Tag Mappings (Phase 9)
        ebml_map = GLOBAL_CONFIG.get("parser_registry", {}).get("tag_mappings", {}).get("ebml", {})
        
        with path_obj.open('rb') as f_ebml:
            ef = File(f_ebml)
            seg = next(ef.children_named("Segment"), None)
            if seg:
                ebml_data = {
                    ebml_map.get('ebml_title', 'ebml_title'): getattr(seg, 'title', None),
                    ebml_map.get('ebml_duration', 'ebml_duration'): getattr(seg, 'duration', None),
                    'ebml_tracks': [
                        {
                            ebml_map.get('track_type', 'type'): getattr(tr, 'track_type', None),
                            ebml_map.get('language', 'language'): getattr(tr, 'language', None),
                            ebml_map.get('codec_id', 'codec_id'): getattr(tr, 'codec_id', None)
                        }
                        for tr in getattr(seg, 'tracks', [])[:settings.get('max_tracks', 50)]
                    ]
                }
                tags.update(ebml_data)
    except Exception as e:
        log.error(f"[EBML-Parser] Failed for {filename}: {e}", exc_info=True)

    return tags

