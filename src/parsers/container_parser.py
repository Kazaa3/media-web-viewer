from typing import Any
from pathlib import Path
from pymediainfo import MediaInfo
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_container")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "Container Parser",
        "description": "Analyzes the high-level container structure (MKV, MP4, AVI) to identify track counts, resolutions, and languages.",
        "supported_tags": ["duration", "container", "title", "size", "width", "height", "fps", "video_codec", "resolution", "audio_track_count", "codec", "samplerate", "bitrate", "bitdepth", "language", "subtitle_count", "subtitle_languages"],
        "supported_codecs": ["mkv", "mp4", "m4v", "webm", "avi", "mov", "wmv", "mpg", "mpeg"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {}

def parse(path, file_type, tags, filename=None, mode='lightweight', settings=None):
    """
    Parses container-level metadata specifically designed to identify
    embedded details such as MKV streams or nested audio.
    """
    if filename is None:
        filename = Path(path).name
        
    if file_type not in ('.mkv', '.mp4', '.m4v', '.webm', '.avi', '.mov', '.wmv', '.mpg', '.mpeg'):
        return tags

    try:
        media_info = MediaInfo.parse(path)

        # 1. General Track analysis
        general_track = next((t for t in media_info.tracks if t.track_type == 'General'), None)
        if general_track:
            if not tags.get('duration') and general_track.duration:
                tags['duration'] = int(general_track.duration / 1000)
            if not tags.get('container') and general_track.format:
                tags['container'] = general_track.format.lower()

            tags['title'] = general_track.title or tags.get('title')
            tags['date'] = tags.get('date') or general_track.recorded_date
            if general_track.file_size:
                tags['size'] = f"{int(general_track.file_size / (1024 * 1024))} MB"

        # 2. Video Track Analysis
        video_tracks = [t for t in media_info.tracks if t.track_type == 'Video']
        if video_tracks:
            primary_video = video_tracks[0]
            tags['width'] = primary_video.width
            tags['height'] = primary_video.height
            if primary_video.frame_rate:
                tags['fps'] = f"{float(primary_video.frame_rate):g}"
            if primary_video.format:
                tags['video_codec'] = primary_video.format.lower()
            
            if primary_video.width and primary_video.height:
                tags['resolution'] = f"{primary_video.width}x{primary_video.height}"

        # 3. Audio Track analysis
        audio_tracks = [t for t in media_info.tracks if t.track_type == 'Audio']
        tags['audio_track_count'] = len(audio_tracks)

        if audio_tracks:
            primary_audio = audio_tracks[0]

            from .format_utils import format_codec, format_bitdepth, format_samplerate
            tags['codec'] = format_codec(primary_audio.format, track_info=primary_audio)

            if primary_audio.sampling_rate:
                tags['samplerate'] = format_samplerate(primary_audio.sampling_rate)

            if primary_audio.bit_rate:
                tags['bitrate'] = f"{int(primary_audio.bit_rate / 1000)} kbps"

            tags['bitdepth'] = format_bitdepth(primary_audio.bit_depth, codec=tags.get('codec'), file_type=file_type)

            if primary_audio.title and not tags.get('title'):
                tags['title'] = primary_audio.title

            if primary_audio.language:
                tags['language'] = primary_audio.language

        # 4. Subtitle Track analysis
        subtitle_tracks = [t for t in media_info.tracks if t.track_type == 'Text']
        tags['subtitle_count'] = len(subtitle_tracks)
        if subtitle_tracks:
            tags['subtitle_languages'] = list(set(t.language for t in subtitle_tracks if t.language))

        if mode == 'full':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            for i, track in enumerate(media_info.tracks):
                tags['full_tags'][f"container_track_{i}_{track.track_type}"] = track.to_data()

    except Exception as e:
        log.warning(f"[Container-Parser] Failed for {filename}: {e}", exc_info=True)

    return tags

