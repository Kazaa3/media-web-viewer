import shutil
from pathlib import Path
from typing import Any


def get_capabilities() -> dict[str, Any]:
    return {
        "name": "PyMKV",
        "description": "Matroska container analysis and manipulation via the 'pymkv' library and mkvmerge.",
        "supported_tags": ["pymkv_tracks"],
        "supported_codecs": ["mkv", "webm"]
    }


def get_settings_schema() -> dict[str, Any]:
    return {}


def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    @brief Extracts MKV metadata using the pymkv library.
    """
    if file_type not in [".mkv", ".webm"]:
        return tags

    if settings is None:
        settings = {}

    try:
        import pymkv
        from src.core.config_master import GLOBAL_CONFIG
        
        mkvmerge_bin = GLOBAL_CONFIG["program_paths"].get("mkvmerge", "mkvmerge")
        if not shutil.which(mkvmerge_bin):
            return tags # Fallback: let other parsers handle it or report error
            
        mkv = pymkv.MKVFile(str(path_obj), mkvmerge_path=mkvmerge_bin)
        tags['pymkv_tracks'] = mkv.tracks
    except ImportError:
        pass
    except Exception:
        pass

    return tags
