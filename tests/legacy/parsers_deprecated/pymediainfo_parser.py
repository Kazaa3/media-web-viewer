from pymediainfo import MediaInfo
from typing import Any

from pathlib import Path


def parse(path: str | Path, file_type: str, tags: dict[str, Any], mode: str = 'lightweight') -> dict[str, Any]:
    """
    @brief Extracts metadata using PyMediaInfo (fallback/supplement).
    @details Extrahiert Metadaten mittels PyMediaInfo als Fallback oder Ergänzung.
    @param path Absolute path / Absoluter Pfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    if mode == 'full' and 'full_tags' not in tags:
        tags['full_tags'] = {}

    try:
        media_info = MediaInfo.parse(path)
        general_track = None
        audio_track = None
        menu_track = None

        for track in media_info.tracks:
            if track.track_type == "General":
                general_track = track
            elif track.track_type == "Audio":
                audio_track = track
            elif track.track_type == "Menu":
                menu_track = track

        if general_track:
            if not tags.get('duration') and general_track.duration:
                # duration is in ms
                tags['duration'] = int(general_track.duration / 1000)
            if not tags.get('container') and general_track.format:
                tags['container'] = general_track.format.lower()

            # Title, Artist, Album fallbacks
            path_obj = Path(path)
            if not tags.get('title') or tags.get('title') == path_obj.name:
                tags['title'] = general_track.title or tags.get('title')
            if not tags.get('artist') or tags.get('artist') == 'Unbekannt':
                tags['artist'] = general_track.performer or tags.get('artist')
            if not tags.get('album'):
                tags['album'] = general_track.album or ''
            if not tags.get('year'):
                tags['year'] = general_track.recorded_date or ''

        if audio_track:
            from .format_utils import format_codec, format_bitdepth, format_samplerate

            # Use centralized formatting for codec
            tags['codec'] = format_codec(audio_track.format, track_info=audio_track)

            if not tags.get('bitrate') and audio_track.bit_rate:
                tags['bitrate'] = f"{int(audio_track.bit_rate / 1000)} kbps"
            if not tags.get('samplerate') and audio_track.sampling_rate:
                tags['samplerate'] = format_samplerate(audio_track.sampling_rate)

            # Use centralized formatting for bitdepth
            tags['bitdepth'] = format_bitdepth(audio_track.bit_depth, codec=tags.get('codec'), file_type=file_type)

        if mode == 'full':
            for i, track in enumerate(media_info.tracks):
                tags['full_tags'][f"mediainfo_{i}_{track.track_type}"] = track.to_data()

        # Chapters from Menu track
        if menu_track and not tags.get('chapters'):
            chapters = []
            menu_data = menu_track.to_data()

            # Mediainfo formats chapters usually as "123456: Chapter 1" inside the dictionary keys
            # or sometimes as specific properties. We will iterate over the to_data keys looking for digits.
            for key, val in menu_data.items():
                # Keys are usually time formats like '00_00_00_000' or similar representing time or milliseconds
                if '_' in key and str(val).startswith('Chapter') or ':' in str(val) or len(key.split('_')) >= 3:
                    # Calculate start time from key if it's formatted like HH_MM_SS_mmm
                    parts = key.split('_')
                    try:
                        if len(parts) >= 3:
                            h = float(parts[0])
                            m = float(parts[1])
                            s = float(parts[2])
                            ms = float(parts[3]) if len(parts) > 3 else 0.0
                            start_time = h * 3600 + m * 60 + s + (ms / 1000.0)

                            chapters.append({
                                'start': start_time,
                                'title': str(val),
                                'end': 0.0
                            })
                    except ValueError:
                        pass

            if chapters:
                from .format_utils import natural_sort_key
                tags['chapters'] = sorted(chapters, key=lambda x: (
                    x.get('start', 0.0), natural_sort_key(x.get('title', ''))))

    except Exception:
        pass

    return tags
