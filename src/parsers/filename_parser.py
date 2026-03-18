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
    
    # 1. Series/Episode Extraction (e.g. "Serien Name S01E01", "Show 1x01")
    series_pattern = re.compile(r'[sS](\d+)[eE](\d+)')
    episode_pattern = re.compile(r'(\d+)x(\d+)')
    
    s_match = series_pattern.search(working_filename)
    e_match = episode_pattern.search(working_filename)
    
    if s_match:
        tags['season'] = int(s_match.group(1))
        tags['episode'] = int(s_match.group(2))
        tags['is_series'] = True
    elif e_match:
        tags['season'] = int(e_match.group(1))
        tags['episode'] = int(e_match.group(2))
        tags['is_series'] = True

    # 2. Year Extraction (e.g. "Movie (2024)", "Film 1999")
    year_pattern = re.compile(r'[\(\[\s]((?:19|20)\d{2})[\)\]\s]?')
    year_match = year_pattern.search(working_filename)
    if year_match:
        tags['year'] = year_match.group(1)
        # Remove year from working filename for title extraction
        working_filename = year_pattern.sub('', working_filename).strip()
    
    # 3. Track Extraction
    if not tags.get('track'):
        track_match = re.match(r"^(\d+)\s+(.*)", working_filename)
        if track_match:
            tags['track'] = str(int(track_match.group(1)))  # Remove leading zeros
            working_filename = track_match.group(2)

    # 4. Title & Artist Extraction
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
            tags['title'] = title.strip()

    # 5. Folder-level Metadata (Parent folder as fallback)
    # Pattern: "Artist - Album (Year)"
    parent_name = Path(path).parent.name
    folder_pattern = re.compile(r'^(.*)\s+-\s+(.*)\s+[\(\[]((?:19|20)\d{2})[\)\]]$')
    f_match = folder_pattern.match(parent_name)
    if f_match:
        if not tags.get('artist'):
            tags['artist'] = f_match.group(1).strip()
        if not tags.get('album'):
            tags['album'] = f_match.group(2).strip()
        if not tags.get('year'):
            tags['year'] = f_match.group(3).strip()

    return tags
