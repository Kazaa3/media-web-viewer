from pymediainfo import MediaInfo
from typing import Any
from pathlib import Path
from src.core.config_master import GLOBAL_CONFIG
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_mediainfo")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "PyMediaInfo",
        "description": "Python wrapper for MediaInfo library, providing exhaustive stream-level meta. Reliable for track counts and technical metadata.",
        "supported_tags": ["audio_track_count", "video_track_count", "subtitle_count", "duration", "container", "standard", "frame_rate", "chapters"],
        "supported_codecs": ["*"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {
        "full_scan": {
            "type": "boolean",
            "default": False,
            "description": "Perform a deeper scan to discover more technical details (slower)."
        }
    }

def parse(path, file_type, tags, filename=None, mode='lightweight', settings=None):
    """
    @brief Extracts metadata using PyMediaInfo (fallback/supplement).
    """
    if filename is None:
        filename = Path(path).name
    if settings is None:
        settings = {}

    try:
        full_scan = settings.get('full_scan', False)
        media_info = MediaInfo.parse(path, full=full_scan)
        general_track = None
        audio_track = None
        video_track = None
        menu_track = None

        audio_tracks = []
        video_tracks = []
        subtitle_tracks = []

        for track in media_info.tracks:
            if track.track_type == "General":
                general_track = track
            elif track.track_type == "Audio":
                audio_track = track
                audio_tracks.append(track)
            elif track.track_type == "Video":
                video_track = track
                video_tracks.append(track)
            elif track.track_type == "Text":
                subtitle_tracks.append(track)
            elif track.track_type == "Menu":
                menu_track = track

        tags['audio_track_count'] = len(audio_tracks)
        tags['video_track_count'] = len(video_tracks)
        tags['subtitle_count'] = len(subtitle_tracks)
        
        sub_langs = []
        for st in subtitle_tracks:
            lang = getattr(st, 'language', None)
            if lang and lang not in sub_langs:
                sub_langs.append(lang)
        if sub_langs:
            tags['subtitle_languages'] = ", ".join(sub_langs)

        if general_track:
            try:
                if not tags.get('duration') and hasattr(general_track, 'duration') and general_track.duration:
                    tags['duration'] = int(general_track.duration / 1000)
                if not tags.get('container') and hasattr(general_track, 'format') and general_track.format:
                    tags['container'] = general_track.format.lower()

                path_obj = Path(path)
                if not tags.get('title') or tags.get('title') == path_obj.name:
                    tags['title'] = getattr(general_track, 'title', None) or tags.get('title')
                if not tags.get('artist') or tags.get('artist') == 'Unbekannt':
                    tags['artist'] = getattr(general_track, 'performer', None) or tags.get('artist')
                if not tags.get('album'):
                    tags['album'] = getattr(general_track, 'album', '') or ''
                if not tags.get('year'):
                    tags['year'] = getattr(general_track, 'recorded_date', '') or ''
            except Exception as ge:
                log.debug(f"[Mediainfo-Track] general_track error for {filename}: {ge}")

        if audio_track:
            from .format_utils import format_codec, format_bitdepth, format_samplerate
            tags['codec'] = format_codec(audio_track.format, track_info=audio_track)

            if not tags.get('bitrate') and audio_track.bit_rate:
                tags['bitrate'] = f"{int(audio_track.bit_rate / 1000)} kbps"
            if not tags.get('samplerate') and audio_track.sampling_rate:
                tags['samplerate'] = format_samplerate(audio_track.sampling_rate)
            tags['bitdepth'] = format_bitdepth(audio_track.bit_depth, codec=tags.get('codec'), file_type=file_type)

        if video_track:
            from .format_utils import format_scan_type, format_chroma, format_color_info
            if not tags.get('standard') and hasattr(video_track, 'standard'):
                tags['standard'] = video_track.standard
            if not tags.get('frame_rate') and hasattr(video_track, 'frame_rate'):
                tags['frame_rate'] = video_track.frame_rate

            tags['video_scan_type'] = format_scan_type(
                getattr(video_track, 'scan_type', None),
                getattr(video_track, 'scan_order', None)
            )
            tags['video_chroma'] = format_chroma(getattr(video_track, 'chroma_subsampling', None))
            
            color_data = format_color_info(
                getattr(video_track, 'color_space', None),
                getattr(video_track, 'transfer_characteristics', None),
                getattr(video_track, 'matrix_coefficients', None),
                getattr(video_track, 'hdr_format', None)
            )
            tags['video_color_space'] = color_data['color_space']
            tags['video_hdr'] = color_data['hdr_format']
            if 'matrix' in color_data:
                tags['video_matrix'] = color_data['matrix']

            if hasattr(video_track, 'bit_depth') and video_track.bit_depth:
                tags['video_bit_depth'] = f"{video_track.bit_depth} Bit"

        if mode == 'full':
            for i, track in enumerate(media_info.tracks):
                tags['full_tags'][f"mediainfo_{i}_{track.track_type}"] = track.to_data()

        # Chapters from Menu track (Phase 9 Flag)
        flags = GLOBAL_CONFIG.get("parser_registry", {}).get("feature_flags", {})
        if flags.get("extract_chapters", True) and menu_track and not tags.get('chapters'):
            chapters = []
            menu_data = menu_track.to_data()
            for key, val in menu_data.items():
                if '_' in key and str(val).startswith('Chapter') or ':' in str(val) or len(key.split('_')) >= 3:
                    parts = key.split('_')
                    try:
                        if len(parts) >= 3:
                            h = float(parts[0])
                            m = float(parts[1])
                            s = float(parts[2])
                            ms = float(parts[3]) if len(parts) > 3 else 0.0
                            start_time = h * 3600 + m * 60 + s + (ms / 1000.0)
                            chapters.append({'start': start_time, 'title': str(val), 'end': 0.0})
                    except ValueError:
                        pass
            if chapters:
                from .format_utils import natural_sort_key
                tags['chapters'] = sorted(chapters, key=lambda x: (
                    x.get('start', 0.0), natural_sort_key(x.get('title', ''))))

    except Exception as e:
        log.error(f"[Mediainfo-Parser] Failed for {filename}: {e}", exc_info=True)

    return tags

