import re
from pathlib import Path
from typing import Any


def get_capabilities() -> dict[str, Any]:
    return {
        "name": "Filename Parser",
        "description": "Heuristic parser that extracts Artist, Title, and Track Number from the filename patterns.",
        "supported_tags": ["artist", "title", "track"],
        "supported_codecs": ["*"]
    }


def get_settings_schema() -> dict[str, Any]:
    return {}


def parse(
    path: str | Path,
    file_type: str,
    tags: dict[str, Any] | None = None,
    filename: str | None = None,
    mode: str = 'lightweight',
    settings: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    @brief Extracts metadata from the filename (e.g., 'Artist - Title').
    @details Extrahiert Metadaten aus dem Dateinamen (z.B. 'Artist - Title').
    @param path Absolute filesystem path / Absoluter Dateipfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param filename Current working filename / Aktueller Dateiname.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    if filename is None:
        filename = Path(path).name

    if tags is None:
        tags = {
            'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
            'codec': '', 'size': '', 'tagtype': '', 'container': '',
            'has_art': 'No', 'title': '', 'artist': '', 'album': '',
            'date': '', 'genre': '', 'track': '', 'totaltracks': '',
            'disc': '', 'totaldiscs': ''
        }

    try:
        if not tags.get('size'):
            tags['size'] = f"{Path(path).stat().st_size / (1024 * 1024):.2f} MB"
    except Exception:
        pass

    working_filename = filename
    if not tags.get('track'):
        track_match = re.match(r"^(\d+)\s+(.*)", working_filename)
        if track_match:
            tags['track'] = str(int(track_match.group(1)))  # Remove leading zeros
            working_filename = track_match.group(2)

    if " - " in working_filename:
        parts = working_filename.split(" - ", 1)
        if not tags.get('artist'):
            tags['artist'] = parts[0].strip()
        if not tags.get('title'):
            title = parts[1].rsplit(".", 1)[0].strip() if "." in parts[1] else parts[1].strip()
            tags['title'] = title
    else:
        if not tags.get('title'):
            title = working_filename.rsplit(".", 1)[0] if "." in working_filename else working_filename
            tags['title'] = title

    return tags
