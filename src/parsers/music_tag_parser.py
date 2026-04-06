from pathlib import Path
from typing import Any


def get_capabilities() -> dict[str, Any]:
    return {
        "name": "Music-Tag",
        "description": "Unified audio metadata extraction using the 'music-tag' library. Supports a wide range of formats with a consistent API.",
        "supported_tags": ["music_tag_title", "music_tag_artist", "music_tag_album", "music_tag_duration"],
        "supported_codecs": ["mp3", "flac", "m4a", "ogg", "opus", "wav", "dsf"]
    }


def get_settings_schema() -> dict[str, Any]:
    return {}


def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    @brief Extracts audio metadata using the music_tag library.
    """
    if file_type not in [".mp3", ".flac", ".m4a", ".ogg", ".opus", ".wav", ".dsf"]:
        return tags

    if settings is None:
        settings = {}

    try:
        import music_tag
        f = music_tag.load_file(str(path_obj))
        
        if not tags.get('title') and f['title'].value: tags['title'] = str(f['title'].value)
        if not tags.get('artist') and f['artist'].value: tags['artist'] = str(f['artist'].value)
        if not tags.get('album') and f['album'].value: tags['album'] = str(f['album'].value)
        if not tags.get('duration') and f['duration'].value: tags['duration'] = int(float(f['duration'].value))
        
        tags['music_tag_title'] = str(f['title'].value)
        tags['music_tag_artist'] = str(f['artist'].value)
        tags['music_tag_album'] = str(f['album'].value)
        tags['music_tag_duration'] = float(f['duration'].value) if f['duration'].value else None
    except ImportError:
        pass
    except Exception:
        pass

    return tags
