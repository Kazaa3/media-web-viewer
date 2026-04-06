from pathlib import Path
from typing import Any


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

    if settings is None:
        settings = {}

    try:
        from ebml.container import File
        with path_obj.open('rb') as f_ebml:
            ef = File(f_ebml)
            seg = next(ef.children_named("Segment"), None)
            if seg:
                ebml_data = {
                    'ebml_title': getattr(seg, 'title', None),
                    'ebml_duration': getattr(seg, 'duration', None),
                    'ebml_tracks': [
                        {
                            'type': getattr(tr, 'track_type', None),
                            'language': getattr(tr, 'language', None),
                            'codec_id': getattr(tr, 'codec_id', None)
                        }
                        for tr in getattr(seg, 'tracks', [])[:settings.get('max_tracks', 50)]
                    ]
                }
                tags.update(ebml_data)
    except ImportError:
        # Expected if dependency not installed
        pass
    except Exception:
        # Standard fallback for corrupted or non-EBML files
        pass

    return tags
