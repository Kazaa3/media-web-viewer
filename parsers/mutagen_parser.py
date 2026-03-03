# Audio-Tag-Bibliothek
from mutagen.mp3 import MP3  # Für MP3-Dauer
from mutagen.flac import FLAC  # Für FLAC-Dauer
from mutagen.oggvorbis import OggVorbis  # Für OGG
from mutagen.mp4 import MP4  # Für ALAC/M4A/M4B
from mutagen.oggopus import OggOpus
from mutagen.wave import WAVE
from mutagen.aac import AAC
from mutagen.asf import ASF # Für WMA
from mutagen.id3 import ID3 # statt ffmpeg
from mutagen.dsdiff import DSDIFF # DSD Interchange File Format: .dsf-Dateien
from mutagen.dsf import DSF # DSD Stream File: .dsd-Dateien

def safe_get(audio_obj, key, default=''):
    val = audio_obj.get(key)
    if not val:
        return default
    if isinstance(val, list) and len(val) > 0:
        return str(val[0])
    return str(val)

def format_samplerate(hz):
    try:
        hz = float(hz)
        khz = hz / 1000
        return f"{int(khz)} kHz" if khz.is_integer() else f"{khz:g} kHz"
    except:
        return ""

def parse(path, file_type, tags, name):
    audio_for_info = None
    
    try:
        if file_type == '.flac':
            audio = FLAC(path)
            audio_for_info = audio
            tags['artist'] = safe_get(audio, 'ARTIST', default=tags.get('artist', 'Unbekannt'))
            tags['title'] = safe_get(audio, 'TITLE', default=tags.get('title', name))
            tags['year'] = safe_get(audio, 'DATE')
            tags['genre'] = safe_get(audio, 'GENRE')
            tags['track'] = safe_get(audio, 'TRACKNUMBER')
            tags['totaltracks'] = safe_get(audio, 'TRACKTOTAL') or safe_get(audio, 'TOTALTRACKS')
            tags['album'] = safe_get(audio, 'ALBUM')
            tags['albumartist'] = safe_get(audio, 'ALBUMARTIST')
            tags['disc'] = safe_get(audio, 'DISCNUMBER')
            tags['codec'] = 'FLAC'
            if hasattr(audio.info, 'bits_per_sample') and audio.info.bits_per_sample:
                tags['bitdepth'] = f"{audio.info.bits_per_sample} Bit"
            
        elif file_type == '.mp3':
            audio = MP3(path)
            audio_for_info = audio
            art = audio.get('TPE1')
            tit = audio.get('TIT2')
            yr = audio.get('TDRC') or audio.get('TYER')
            gn = audio.get('TCON')
            tr = audio.get('TRCK')
            alb = audio.get('TALB')
            aart = audio.get('TPE2')
            dsc = audio.get('TPOS')
            
            if art: tags['artist'] = str(art.text[0]) if hasattr(art, 'text') else str(art[0])
            if tit: tags['title'] = str(tit.text[0]) if hasattr(tit, 'text') else str(tit[0])
            if yr: tags['year'] = str(yr.text[0]) if hasattr(yr, 'text') else str(yr)
            if gn: tags['genre'] = str(gn.text[0]) if hasattr(gn, 'text') else str(gn)
            if alb: tags['album'] = str(alb.text[0]) if hasattr(alb, 'text') else str(alb[0])
            if aart: tags['albumartist'] = str(aart.text[0]) if hasattr(aart, 'text') else str(aart[0])
            if dsc: tags['disc'] = str(dsc.text[0]).split('/')[0] if hasattr(dsc, 'text') else str(dsc)
            
            tr_val = str(tr.text[0]) if tr and hasattr(tr, 'text') else (str(tr) if tr else '')
            if '/' in tr_val:
                tags['track'] = tr_val.split('/')[0]
                tags['totaltracks'] = tr_val.split('/')[1]
            elif tr_val:
                tags['track'] = tr_val
                
            tags['codec'] = 'MP3'
            
        elif file_type in {'.m4a', '.alac', '.m4b'}:
            audio = MP4(path)
            audio_for_info = audio
            tags['artist'] = safe_get(audio, '\xa9ART', default=tags.get('artist', 'Unbekannt'))
            tags['title'] = safe_get(audio, '\xa9nam', default=tags.get('title', name))
            tags['year'] = safe_get(audio, '\xa9day')
            tags['genre'] = safe_get(audio, '\xa9gen')
            tags['album'] = safe_get(audio, '\xa9alb')
            tags['albumartist'] = safe_get(audio, 'aART')
            
            trkn = audio.get('trkn')
            if trkn and len(trkn) > 0 and isinstance(trkn[0], tuple):
                if len(trkn[0]) > 0 and int(trkn[0][0]) > 0: tags['track'] = str(trkn[0][0])
                if len(trkn[0]) > 1 and int(trkn[0][1]) > 0: tags['totaltracks'] = str(trkn[0][1])
            elif trkn and len(trkn) > 0:
                tags['track'] = str(trkn[0])
                
            disk = audio.get('disk')
            if disk and len(disk) > 0 and isinstance(disk[0], tuple):
                if len(disk[0]) > 0 and int(disk[0][0]) > 0: tags['disc'] = str(disk[0][0])
            elif disk and len(disk) > 0:
                tags['disc'] = str(disk[0])
                
            tags['codec'] = getattr(audio.info, 'codec', file_type[1:].upper())
                
        elif file_type in {'.ogg', '.opus', '.wav', '.aac', '.wma'}:
            if file_type == '.ogg': audio = OggVorbis(path)
            elif file_type == '.opus': audio = OggOpus(path)
            elif file_type == '.wav': audio = WAVE(path)
            elif file_type == '.aac': audio = AAC(path)
            elif file_type == '.wma': audio = ASF(path)
            
            audio_for_info = audio
            
            tags['artist'] = safe_get(audio, 'artist', default=tags.get('artist', 'Unbekannt'))
            tags['title'] = safe_get(audio, 'title', default=tags.get('title', name))
            tags['year'] = safe_get(audio, 'date') or safe_get(audio, 'year')
            tags['genre'] = safe_get(audio, 'genre')
            tags['album'] = safe_get(audio, 'album')
            tags['albumartist'] = safe_get(audio, 'albumartist')
            tags['track'] = safe_get(audio, 'tracknumber') or safe_get(audio, 'track')
            tags['disc'] = safe_get(audio, 'discnumber')
            tags['codec'] = file_type[1:].upper()
        
        # Stream info elements
        if audio_for_info and hasattr(audio_for_info, 'info'):
            info = audio_for_info.info
            if hasattr(info, 'bitrate') and info.bitrate:
                tags['bitrate'] = f"{int((info.bitrate + 500) // 1000)} kbps"
            if hasattr(info, 'sample_rate') and info.sample_rate:
                tags['samplerate'] = format_samplerate(info.sample_rate)
            if hasattr(info, 'bits_per_sample') and info.bits_per_sample and info.bits_per_sample > 0:
                tags['bitdepth'] = f"{info.bits_per_sample} Bit"

        # Tag types
        if audio_for_info and hasattr(audio_for_info, 'tags') and audio_for_info.tags is not None:
            tag_name = type(audio_for_info.tags).__name__
            if tag_name == 'ID3' and hasattr(audio_for_info.tags, 'version'):
                tags['tagtype'] = f"ID3v{audio_for_info.tags.version[0]}.{audio_for_info.tags.version[1]}"
            elif tag_name == 'MP4Tags':
                tags['tagtype'] = 'MP4Tags'
            elif tag_name == 'OggVComment':
                tags['tagtype'] = 'Vorbis Comment (Ogg)'
            elif tag_name == 'VCFLACDict':
                tags['tagtype'] = 'Vorbis Comment (FLAC)'
            else:
                tags['tagtype'] = tag_name
            
        # Cover Art
        if file_type == '.mp3' and audio_for_info:
            tags['has_art'] = 'Yes' if any(k.startswith('APIC') for k in audio_for_info.keys()) else 'No'
        elif file_type == '.flac' and audio_for_info:
            tags['has_art'] = 'Yes' if len(audio_for_info.pictures) > 0 else 'No'
        elif file_type in {'.m4a', '.alac', '.m4b'} and audio_for_info:
            tags['has_art'] = 'Yes' if 'covr' in audio_for_info.keys() else 'No'
                
    except Exception:
        pass

    return tags
