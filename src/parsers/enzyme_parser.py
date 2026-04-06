from pathlib import Path
from typing import Any


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

    if settings is None:
        settings = {}

    try:
        import enzyme
        with path_obj.open('rb') as f_enz:
            movie = enzyme.MKV(f_enz)
            res = {
                'enzyme_tracks': (movie.audio_tracks + movie.video_tracks)[:settings.get('max_tracks', 50)],
                'enzyme_duration': movie.info.duration.total_seconds() if movie.info and movie.info.duration else None
            }
            tags.update(res)
    except ImportError:
        pass
    except Exception:
        pass

    return tags
