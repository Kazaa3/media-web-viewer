from pymediainfo import MediaInfo

def parse(path, file_type, tags):
    """
    Extrahierte Metadaten mittels MediaInfo als Fallback/Ergänzung.
    """
    try:
        media_info = MediaInfo.parse(path)
        general_track = None
        audio_track = None
        
        for track in media_info.tracks:
            if track.track_type == "General":
                general_track = track
            elif track.track_type == "Audio":
                audio_track = track
                
        if general_track:
            if not tags.get('duration') and general_track.duration:
                # duration is in ms
                tags['duration'] = int(general_track.duration / 1000)
            if not tags.get('container') and general_track.format:
                tags['container'] = general_track.format.lower()
                
            # Title, Artist, Album fallbacks
            if not tags.get('title') or tags.get('title') == path.name:
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
                
    except Exception as e:
        pass

    return tags
