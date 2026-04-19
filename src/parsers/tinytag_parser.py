from pathlib import Path
from typing import Any
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_tinytag")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "TinyTag",
        "description": "Fast, lightweight audio metadata extraction using the 'tinytag' library.",
        "supported_tags": ["tinytag_title", "tinytag_artist", "tinytag_duration"],
        "supported_codecs": ["mp3", "flac", "m4a", "ogg", "opus", "wav"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {}

def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    @brief Extracts audio metadata using the tinytag library.
    """
    if filename is None:
        filename = path_obj.name
    if settings is None:
        settings = {}

    try:
        from tinytag import TinyTag
        tag = TinyTag.get(str(path_obj))
        
        if not tags.get('title') and tag.title: 
            tags['title'] = tag.title
        if not tags.get('artist') and tag.artist: 
            tags['artist'] = tag.artist
        if not tags.get('duration') and tag.duration: 
            tags['duration'] = int(tag.duration)
        
        tags['tinytag_title'] = tag.title
        tags['tinytag_artist'] = tag.artist
        tags['tinytag_duration'] = tag.duration
    except ImportError:
        log.debug(f"[TinyTag] Library not installed, skipping.")
    except Exception as e:
        log.error(f"[TinyTag-Parser] Failed for {filename}: {e}", exc_info=True)

    return tags

