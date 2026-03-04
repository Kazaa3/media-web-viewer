import traceback
from pymediainfo import MediaInfo

def parse(path, file_type, tags, mode='lightweight'):
    """
    Parses container-level metadata specifically designed to identify
    embedded details such as MKV streams or nested audio.
    """
    if file_type not in ('.mkv', '.mp4', '.m4v', '.webm', '.avi', '.mov'):
        return tags

    try:
        media_info = MediaInfo.parse(path)
        
        # General Track analysis
        general_track = next((t for t in media_info.tracks if t.track_type == 'General'), None)
        if general_track:
            if not tags.get('duration') and general_track.duration:
                tags['duration'] = int(general_track.duration / 1000)
            if not tags.get('container') and general_track.format:
                tags['container'] = general_track.format.lower()
                
            tags['title'] = general_track.title or tags.get('title')
            tags['date'] = tags.get('date') or general_track.recorded_date

        # Look for inner streams (Audio primarily for MKV nested AAC)
        audio_tracks = [t for t in media_info.tracks if t.track_type == 'Audio']
        
        if audio_tracks:
            # Typically pick the first audio stream or preferred language if later logic allows
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
            
            # Additional tags from primary_audio if missing
            if primary_audio.language:
                tags['language'] = primary_audio.language

        if mode == 'full':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            for i, track in enumerate(media_info.tracks):
                tags['full_tags'][f"container_track_{i}_{track.track_type}"] = track.to_data()

    except Exception:
        pass

    return tags
