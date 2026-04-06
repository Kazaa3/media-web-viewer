from pathlib import Path
from typing import Any


def get_capabilities() -> dict[str, Any]:
    return {
        "name": "eyeD3",
        "description": "High-fidelity ID3v1/v2 tagging extraction using the 'eyed3' library.",
        "supported_tags": ["eyed3_title", "eyed3_artist", "eyed3_album", "eyed3_duration"],
        "supported_codecs": ["mp3"]
    }


def get_settings_schema() -> dict[str, Any]:
    return {}


def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    @brief Extracts audio metadata using the eyed3 library.
    """
    if file_type != ".mp3":
        return tags

    if settings is None:
        settings = {}

    try:
        import eyed3
        audiofile = eyed3.load(str(path_obj))
        if audiofile and audiofile.tag:
            if not tags.get('title') and audiofile.tag.title: tags['title'] = audiofile.tag.title
            if not tags.get('artist') and audiofile.tag.artist: tags['artist'] = audiofile.tag.artist
            if not tags.get('album') and audiofile.tag.album: tags['album'] = audiofile.tag.album
            if not tags.get('duration') and audiofile.info: tags['duration'] = int(audiofile.info.time_secs)
            
            tags['eyed3_title'] = audiofile.tag.title
            tags['eyed3_artist'] = audiofile.tag.artist
            tags['eyed3_album'] = audiofile.tag.album
            tags['eyed3_duration'] = audiofile.info.time_secs if audiofile.info else None
    except ImportError:
        pass
    except Exception:
        pass

    return tags
