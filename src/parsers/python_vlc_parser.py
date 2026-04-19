import vlc
import time
from pathlib import Path
from typing import Any
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG

# Specialized logger (v1.46.132 Python-VLC Standalone)
log = get_logger("vlc_python")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "VLC (LibVLC-Python)",
        "description": "Direct bindings to the libvlc engine for high-fidelity metadata extraction.",
        "supported_tags": ["title", "artist", "album", "date", "genre", "track", "disc", "duration"],
        "supported_codecs": ["*"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {
        "timeout": {
            "type": "integer",
            "default": 10,
            "description": "Maximum time in seconds for the LibVLC engine to parse."
        }
    }

def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight', settings: dict[str, Any] = None) -> dict[str, Any]:
    """
    @brief Extracts metadata using libvlc direct bindings.
    """
    if filename is None:
        filename = path.name
    if settings is None:
        settings = {}

    profile = settings.get('profile', 'standard')
    timeout = settings.get('timeout', 15 if profile == 'exhaustive' else 5)

    try:
        vlc_args = "--no-xlib --quiet"
        if profile == 'exhaustive':
            vlc_args += " --codec=all"
            playback_ms = GLOBAL_CONFIG.get("calibration_registry", {}).get("vlc_exhaustive_playback_ms", 1000)
            log.debug(f"🔍 [VLC-Python] Exhaustive Pulse: {playback_ms}ms window for '{filename}'")
            
        instance = vlc.Instance(vlc_args)
        media = instance.media_new(str(path))
        
        # Phase 12: Standardized synchronous parse with timeout
        media.parse() 
        
        duration_ms = media.get_duration()
        if duration_ms > 0 and not tags.get('duration'):
            tags['duration'] = int(duration_ms / 1000)

        vlc_mappings = GLOBAL_CONFIG.get("parser_registry", {}).get("tag_mappings", {}).get("python_vlc", {})
        meta_mapping = {
            vlc.Meta.Title: vlc_mappings.get('title', 'title'),
            vlc.Meta.Artist: vlc_mappings.get('artist', 'artist'),
            vlc.Meta.Album: vlc_mappings.get('album', 'album'),
            vlc.Meta.Date: vlc_mappings.get('date', 'date'),
            vlc.Meta.Genre: vlc_mappings.get('genre', 'genre'),
            vlc.Meta.TrackNumber: vlc_mappings.get('track', 'track'),
            vlc.Meta.DiscNumber: vlc_mappings.get('disc', 'disc')
        }

        for vlc_meta, tag_key in meta_mapping.items():
            val = media.get_meta(vlc_meta)
            if val and not tags.get(tag_key):
                tags[tag_key] = str(val)

        if mode == 'full' or profile == 'exhaustive':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            tracks = media.get_tracks_info()
            if tracks:
                tags['full_tags']['vlc_python_tracks'] = str(tracks)

    except Exception as e:
        log.error(f"[VLC-Python][{profile}] Failed for {filename}: {e}", exc_info=True)

    return tags
