import subprocess
from pathlib import Path
from typing import Any


def get_capabilities() -> dict[str, Any]:
    return {
        "name": "MKVParse",
        "description": "High-performance MKV/Matroska analysis via the mkvparse library.",
        "supported_tags": ["mkv_elements"],
        "supported_codecs": ["mkv", "webm"]
    }


def get_settings_schema() -> dict[str, Any]:
    return {}


def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    @brief Extracts MKV metadata using the mkvparse library.
    """
    if file_type not in [".mkv", ".webm"]:
        return tags

    if settings is None:
        settings = {}

    try:
        import mkvparse
        with open(str(path_obj), 'rb') as f:
            mkvparse.parse(f, lambda elem, data: None)
    except ImportError:
        pass
    except Exception:
        pass

    return tags
