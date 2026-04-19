from typing import Any
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
from mutagen.oggopus import OggOpus
from mutagen.wave import WAVE
from mutagen.aac import AAC
from mutagen.asf import ASF
from src.core.config_master import GLOBAL_CONFIG
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_mutagen")

def safe_get(audio: Any, key: str, default: Any = '') -> Any:
    """
    @brief Safely retrieves a tag value from various Mutagen objects.
    @details Handles the differences between ID3 (text[0]), Vorbis (list[0]), and MP4 (list[0]).
    """
    try:
        val = audio.get(key)
        if val is None:
            return default
            
        # ID3 frames (e.g., TPE1)
        if hasattr(val, 'text') and isinstance(val.text, list) and len(val.text) > 0:
            return str(val.text[0])
            
        # Standard lists (Vorbis, MP4, etc.)
        if isinstance(val, list) and len(val) > 0:
            return str(val[0])
            
        return str(val)
    except Exception as e:
        log.debug(f"[Mutagen-SafeGet] Failed for key {key}: {e}")
        return default

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "Mutagen",
        "description": "High-performance audio metadata parser (ID3, FLAC, Vorbis, MP4).",
        "supported_tags": [
            "title", "artist", "album", "year", "genre", "track", "totaltracks", 
            "disc", "totaldiscs", "albumartist", "composer", "lyrics", "chapters"
        ],
        "supported_codecs": [
            "mp3", "flac", "ogg", "opus", "m4a", "alac", "wav", "aac", "wma"
        ]
    }

def get_settings_schema() -> dict[str, Any]:
    return {
        "prefer_albumartist": {
            "type": "boolean",
            "default": True,
            "description": "Prefer TPE2 (Album Artist) over TPE1 (Artist) for the main artist field."
        },
        "extract_lyrics": {
            "type": "boolean",
            "default": False,
            "description": "Extract synchronized and unsynchronized lyrics."
        }
    }

def parse(path, file_type, tags, filename=None, mode='lightweight', settings=None):
    """
    @brief Extracts tags using Mutagen (ID3, FLAC, Vorbis, MP4).
    """
    if filename is None:
        filename = Path(path).name
    if settings is None:
        settings = {}

    audio_for_info: Any = None
    flags = GLOBAL_CONFIG.get("parser_registry", {}).get("feature_flags", {})

    try:
        if file_type == '.flac':
            audio_flac = FLAC(path)
            audio_for_info = audio_flac

            if settings.get('prefer_albumartist', True):
                tags['artist'] = safe_get(audio_flac, 'ALBUMARTIST') or safe_get(
                    audio_flac, 'ARTIST', default=tags.get('artist', 'Unbekannt'))
            else:
                tags['artist'] = safe_get(audio_flac, 'ARTIST', default=tags.get('artist', 'Unbekannt'))

            tags['title'] = safe_get(audio_flac, 'TITLE', default=tags.get('title', filename))
            tags['year'] = safe_get(audio_flac, 'DATE')
            tags['genre'] = safe_get(audio_flac, 'GENRE')
            tags['track'] = safe_get(audio_flac, 'TRACKNUMBER')
            tags['totaltracks'] = safe_get(audio_flac, 'TRACKTOTAL') or safe_get(audio_flac, 'TOTALTRACKS')
            tags['album'] = safe_get(audio_flac, 'ALBUM')
            tags['albumartist'] = safe_get(audio_flac, 'ALBUMARTIST')
            tags['disc'] = safe_get(audio_flac, 'DISCNUMBER')
            tags['codec'] = 'flac'
            if hasattr(audio_flac.info, 'bits_per_sample') and audio_flac.info.bits_per_sample:
                tags['bitdepth'] = f"{audio_flac.info.bits_per_sample} Bit"

            # Chapters for FLAC/Vorbis (Phase 9 Flag)
            if flags.get("extract_chapters", True) and not tags.get('chapters'):
                chapters_flac: list[dict[str, Any]] = []
                from .format_utils import natural_sort_key
                chapter_keys = [k for k in audio_flac.keys() if k.startswith(
                    'CHAPTER') and not k.endswith('NAME') and not k.endswith('URL')]
                for k in sorted(chapter_keys, key=natural_sort_key):
                    idx_flac = k.replace('CHAPTER', '')
                    start_val = audio_flac.get(k)
                    title_val = audio_flac.get(f"CHAPTER{idx_flac}NAME")

                    start_t_flac = 0.0
                    if start_val and isinstance(start_val, list):
                        parts = start_val[0].split(':')
                        if len(parts) == 3:
                            start_t_flac = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
                        elif len(parts) == 2:
                            start_t_flac = float(parts[0]) * 60 + float(parts[1])

                    chapters_flac.append({
                        'start': start_t_flac,
                        'title': title_val[0] if title_val else f"Kapitel {len(chapters_flac) + 1}",
                        'end': 0.0
                    })
                if chapters_flac:
                    tags['chapters'] = sorted(chapters_flac, key=lambda x: (x['start'], natural_sort_key(x['title'])))

        elif file_type == '.mp3':
            audio_mp3 = MP3(path)
            audio_for_info = audio_mp3
            art = audio_mp3.get('TPE1')
            tit = audio_mp3.get('TIT2')
            yr = audio_mp3.get('TDRC') or audio_mp3.get('TYER')
            gn = audio_mp3.get('TCON')
            tr = audio_mp3.get('TRCK')
            alb = audio_mp3.get('TALB')
            aart = audio_mp3.get('TPE2')
            dsc = audio_mp3.get('TPOS')

            if settings.get('prefer_albumartist', True) and aart:
                tags['artist'] = str(aart.text[0]) if hasattr(aart, 'text') else str(aart[0])
            elif art:
                tags['artist'] = str(art.text[0]) if hasattr(art, 'text') else str(art[0])
            else:
                tags['artist'] = tags.get('artist', 'Unbekannt')

            if tit:
                tags['title'] = str(tit.text[0]) if hasattr(tit, 'text') else str(tit[0])
            if yr:
                tags['year'] = str(yr.text[0]) if hasattr(yr, 'text') else str(yr)
            if gn:
                tags['genre'] = str(gn.text[0]) if hasattr(gn, 'text') else str(gn)
            if alb:
                tags['album'] = str(alb.text[0]) if hasattr(alb, 'text') else str(alb[0])
            if aart:
                tags['albumartist'] = str(aart.text[0]) if hasattr(aart, 'text') else str(aart[0])
            if dsc:
                tags['disc'] = str(dsc.text[0]).split('/')[0] if hasattr(dsc, 'text') else str(dsc)

            tr_val = str(tr.text[0]) if tr and hasattr(tr, 'text') else (str(tr) if tr else '')
            if '/' in tr_val:
                tags['track'] = tr_val.split('/')[0]
                tags['totaltracks'] = tr_val.split('/')[1]
            elif tr_val:
                tags['track'] = tr_val

            tags['codec'] = 'mp3'

            # Chapters for MP3 (Phase 9 Flag)
            if flags.get("extract_chapters", True) and not tags.get('chapters'):
                chapters_mp3: list[dict[str, Any]] = []
                if hasattr(audio_mp3, 'tags') and audio_mp3.tags is not None:
                    for key_mp3, frame in audio_mp3.tags.items():
                        if key_mp3.startswith('CHAP'):
                            start_time = frame.start_time / 1000.0 if hasattr(frame, 'start_time') else 0.0
                            end_time = frame.end_time / 1000.0 if hasattr(frame, 'end_time') else 0.0
                            title_mp3 = f"Kapitel {len(chapters_mp3) + 1}"
                            if hasattr(frame, 'sub_frames') and 'TIT2' in frame.sub_frames:
                                title_mp3 = str(frame.sub_frames['TIT2'].text[0])

                            chapters_mp3.append({
                                'start': start_time,
                                'end': end_time,
                                'title': title_mp3
                            })
                if chapters_mp3:
                    from .format_utils import natural_sort_key
                    tags['chapters'] = sorted(chapters_mp3, key=lambda x: (x['start'], natural_sort_key(x['title'])))

        elif file_type in {'.m4a', '.alac', '.m4b', '.mp4'}:
            audio_mp4 = MP4(path)
            audio_for_info = audio_mp4

            if settings.get('prefer_albumartist', True):
                tags['artist'] = safe_get(audio_mp4, 'aART') or safe_get(
                    audio_mp4, '\xa9ART', default=tags.get('artist', 'Unbekannt'))
            else:
                tags['artist'] = safe_get(audio_mp4, '\xa9ART', default=tags.get('artist', 'Unbekannt'))

            tags['title'] = safe_get(audio_mp4, '\xa9nam', default=tags.get('title', filename))
            tags['year'] = safe_get(audio_mp4, '\xa9day')
            tags['genre'] = safe_get(audio_mp4, '\xa9gen')
            tags['album'] = safe_get(audio_mp4, '\xa9alb')
            tags['albumartist'] = safe_get(audio_mp4, 'aART')

            trkn = audio_mp4.get('trkn')
            if trkn and len(trkn) > 0 and isinstance(trkn[0], tuple):
                if len(trkn[0]) > 0 and int(trkn[0][0]) > 0:
                    tags['track'] = str(trkn[0][0])
                if len(trkn[0]) > 1 and int(trkn[0][1]) > 0:
                    tags['totaltracks'] = str(trkn[0][1])
            elif trkn and len(trkn) > 0:
                tags['track'] = str(trkn[0])

            disk = audio_mp4.get('disk')
            if disk and len(disk) > 0 and isinstance(disk[0], tuple):
                if len(disk[0]) > 0 and int(disk[0][0]) > 0:
                    tags['disc'] = str(disk[0][0])
            elif disk and len(disk) > 0:
                tags['disc'] = str(disk[0])

            raw_codec = getattr(audio_mp4.info, 'codec', None)
            tags['codec'] = str(raw_codec).lower() if raw_codec else file_type[1:].lower()

            # Chapters for MP4 (Phase 9 Flag)
            if flags.get("extract_chapters", True) and not tags.get('chapters'):
                chapters_mp4: list[dict[str, Any]] = []
                if hasattr(audio_mp4, 'chapters') and audio_mp4.chapters:
                    for i_mp4, chap_mp4 in enumerate(audio_mp4.chapters):
                        chapters_mp4.append({
                            'start': chap_mp4.start,
                            'title': chap_mp4.title if chap_mp4.title else f"Kapitel {i_mp4 + 1}",
                            'end': chap_mp4.end if hasattr(chap_mp4, 'end') else 0.0
                        })
                if chapters_mp4:
                    from .format_utils import natural_sort_key
                    tags['chapters'] = sorted(chapters_mp4, key=lambda x: (x['start'], natural_sort_key(x['title'])))

        elif file_type in {'.ogg', '.opus', '.wav', '.aac', '.wma'}:
            audio_misc: Any = None
            if file_type == '.ogg':
                audio_misc = OggVorbis(path)
            elif file_type == '.opus':
                audio_misc = OggOpus(path)
            elif file_type == '.wav':
                audio_misc = WAVE(path)
            elif file_type == '.aac':
                audio_misc = AAC(path)
            elif file_type == '.wma':
                audio_misc = ASF(path)

            audio_for_info = audio_misc

            if audio_misc:
                tags['artist'] = safe_get(audio_misc, 'artist', default=tags.get('artist', 'Unbekannt'))
                tags['title'] = safe_get(audio_misc, 'title', default=tags.get('title', filename))
                tags['year'] = safe_get(audio_misc, 'date') or safe_get(audio_misc, 'year')
                tags['genre'] = safe_get(audio_misc, 'genre')
                tags['album'] = safe_get(audio_misc, 'album')
                tags['albumartist'] = safe_get(audio_misc, 'albumartist')
                tags['track'] = safe_get(audio_misc, 'tracknumber') or safe_get(audio_misc, 'track')
                tags['disc'] = safe_get(audio_misc, 'discnumber')

        # Stream info elements
        if audio_for_info and hasattr(audio_for_info, 'info'):
            info = audio_for_info.info
            if hasattr(info, 'bitrate') and info.bitrate:
                tags['bitrate'] = f"{int((info.bitrate + 500) // 1000)} kbps"

            if not tags.get('codec'):
                from .format_utils import format_codec
                tags['codec'] = format_codec(tags.get('file_type') or file_type[1:])

            if not tags.get('samplerate') and hasattr(info, 'sample_rate'):
                from .format_utils import format_samplerate
                tags['samplerate'] = format_samplerate(info.sample_rate)

            if not tags.get('bitdepth') and hasattr(info, 'bits_per_sample'):
                from .format_utils import format_bitdepth
                tags['bitdepth'] = format_bitdepth(info.bits_per_sample, codec=tags.get('codec'), file_type=file_type)

        # Tag types
        if audio_for_info and hasattr(audio_for_info, 'tags') and audio_for_info.tags is not None:
            if mode == 'full':
                for k_full, v_full in audio_for_info.tags.items():
                    tags['full_tags'][f"mutagen_{k_full}"] = str(v_full)

            tag_name = type(audio_for_info.tags).__name__
            if tag_name == 'ID3' and hasattr(audio_for_info.tags, 'version'):
                tags['tagtype'] = f"ID3v{audio_for_info.tags.version[0]}.{audio_for_info.tags.version[1]}"
            elif tag_name == 'MP4Tags':
                tags['tagtype'] = 'MP4Tags'
            elif tag_name == 'OggVComment':
                tags['tagtype'] = 'OggVComment'
            elif tag_name == 'VCFLACDict':
                tags['tagtype'] = 'VCFLACDict'
            elif tag_name == 'ASFTags':
                tags['tagtype'] = 'ASFTags'
            else:
                tags['tagtype'] = tag_name

        # Cover Art
        if audio_for_info:
            if file_type == '.mp3':
                tags['has_art'] = 'Yes' if any(k_art.startswith('APIC') for k_art in audio_for_info.keys()) else 'No'
            elif file_type == '.flac':
                tags['has_art'] = 'Yes' if len(audio_for_info.pictures) > 0 else 'No'
            elif file_type in {'.m4a', '.alac', '.m4b'}:
                tags['has_art'] = 'Yes' if 'covr' in audio_for_info.keys() else 'No'

    except Exception as e:
        log.error(f"[Mutagen-Parser] Failed for {filename}: {e}", exc_info=True)

    return tags

