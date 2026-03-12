import vlc
import time
from pathlib import Path
from typing import Any


def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight') -> dict[str, Any]:
    """
    @brief Extracts metadata using libvlc (python-vlc).
    @details Extrahiert Metadaten mittels libvlc (python-vlc).
    @param path Absolute path / Absoluter Pfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    try:
        instance = vlc.Instance("--no-xlib --quiet")
        media = instance.media_new(str(path))
        media.parse()  # Synchronous parse
        
        # Duration: reported in milliseconds
        duration_ms = media.get_duration()
        if duration_ms > 0 and not tags.get('duration'):
            tags['duration'] = int(duration_ms / 1000)

        # Meta identification
        meta_mapping = {
            vlc.Meta.Title: 'title',
            vlc.Meta.Artist: 'artist',
            vlc.Meta.Album: 'album',
            vlc.Meta.Date: 'date',
            vlc.Meta.Genre: 'genre',
            vlc.Meta.TrackNumber: 'track',
            vlc.Meta.DiscNumber: 'disc'
        }

        for vlc_meta, tag_key in meta_mapping.items():
            val = media.get_meta(vlc_meta)
            if val and not tags.get(tag_key):
                tags[tag_key] = str(val)

        # Track information
        if mode == 'full':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            # Basic track stats
            tracks = media.get_tracks_info()
            if tracks:
                tags['full_tags']['vlc_tracks'] = str(tracks)

    except Exception:
        pass

    return tags
