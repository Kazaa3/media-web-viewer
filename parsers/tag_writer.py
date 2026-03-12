import os
import subprocess
from pathlib import Path
from typing import Any
import logger

log = logger.get_logger("tag_writer")

def write_tags(path: str | Path, tags: dict[str, Any]) -> bool:
    """
    @brief Writes tags back to the media file.
    @details Schreibt Tags zurück in die Mediendatei.
    @param path Absolute path to the file / Absoluter Pfad zur Datei.
    @param tags Dictionary of tags to write / Dictionary mit zu schreibenden Tags.
    @return True if successful, False otherwise / True bei Erfolg, sonst False.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        log.error(f"File not found: {path}")
        return False

    ext = path_obj.suffix.lower()
    
    try:
        if ext == '.mp3':
            return _write_mp3_tags(path_obj, tags)
        elif ext == '.flac':
            return _write_flac_tags(path_obj, tags)
        elif ext in ('.m4a', '.m4b', '.mp4'):
            return _write_mp4_tags(path_obj, tags)
        elif ext == '.mkv':
            return _write_mkv_tags(path_obj, tags)
        else:
            log.warning(f"Unsupported file type for tag writing: {ext}")
            return False
    except Exception as e:
        log.error(f"Failed to write tags to '{path}': {e}")
        return False

def _write_mp3_tags(path: Path, tags: dict[str, Any]) -> bool:
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, TRCK, TPOS
    try:
        audio = ID3(str(path))
    except Exception:
        audio = ID3()
    
    mapping = {
        'title': TIT2,
        'artist': TPE1,
        'album': TALB,
        'date': TDRC,
        'year': TDRC,
        'genre': TCON,
        'track': TRCK,
        'disc': TPOS
    }

    for key, frame_class in mapping.items():
        val = tags.get(key)
        if val:
            audio.add(frame_class(encoding=3, text=[str(val)]))
    
    audio.save()
    return True

def _write_flac_tags(path: Path, tags: dict[str, Any]) -> bool:
    from mutagen.flac import FLAC
    audio = FLAC(str(path))
    
    mapping = {
        'title': 'TITLE',
        'artist': 'ARTIST',
        'album': 'ALBUM',
        'date': 'DATE',
        'year': 'DATE',
        'genre': 'GENRE',
        'track': 'TRACKNUMBER',
        'disc': 'DISCNUMBER'
    }

    for key, flac_key in mapping.items():
        val = tags.get(key)
        if val:
            audio[flac_key] = str(val)
    
    audio.save()
    return True

def _write_mp4_tags(path: Path, tags: dict[str, Any]) -> bool:
    from mutagen.mp4 import MP4
    audio = MP4(str(path))
    
    # MP4 uses non-standard atoms
    mapping = {
        'title': '\xa9nam',
        'artist': '\xa9ART',
        'album': '\xa9alb',
        'date': '\xa9day',
        'year': '\xa9day',
        'genre': '\xa9gen',
        'albumartist': 'aART'
    }

    for key, mp4_key in mapping.items():
        val = tags.get(key)
        if val:
            audio[mp4_key] = [str(val)]
    
    # Track and Disc are tuples (current, total)
    if tags.get('track'):
        try:
            tr = int(tags['track'])
            tot = int(tags.get('totaltracks', 0))
            audio['trkn'] = [(tr, tot)]
        except ValueError:
            pass

    if tags.get('disc'):
        try:
            ds = int(tags['disc'])
            tot = int(tags.get('totaldiscs', 0))
            audio['disk'] = [(ds, tot)]
        except ValueError:
            pass

    audio.save()
    return True

def _write_mkv_tags(path: Path, tags: dict[str, Any]) -> bool:
    """
    Uses mkvpropedit to write header tags to MKV files.
    """
    args = ['mkvpropedit', str(path)]
    
    # MKV properties mapping
    # Note: mkvpropedit uses --set title="..." etc.
    if tags.get('title'):
        args.extend(['--set', f'title={tags["title"]}'])
    
    # For more complex tags, we might need an XML file, 
    # but for basic properties --set title is enough.
    # To set general tags (Artist, etc.), we'd usually use --tags
    
    if len(args) <= 2:
        return True # Nothing to change
        
    try:
        subprocess.run(args, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"mkvpropedit failed: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        log.error("mkvpropedit not found. Please install MKVToolNix.")
        return False
