import time
import copy
import subprocess
from typing import Any
from pathlib import Path
from . import filename_parser
from . import mutagen_parser
from . import pymediainfo_parser
from . import ffprobe_parser
from . import ffmpeg_parser
from . import container_parser
from . import mkvinfo_parser
from . import mkvmerge_parser
from . import vlc_parser
from . import isoparser_parser
import logger
import logging

# Get specialized logger for parser component
log = logger.get_logger("parser")

MAX_TAG_LEN = 4096  # Max length for any single string tag
MAX_CHAPTERS = 500  # Max number of chapters to keep

def sanitize_metadata(tags: dict[str, Any]) -> dict[str, Any]:
    """
    @brief Sanitizes metadata to prevent memory bloat or UI lag.
    """
    for key, value in tags.items():
        if isinstance(value, str) and len(value) > MAX_TAG_LEN:
            log.warning(f"Truncating long tag '{key}' ({len(value)} chars)")
            tags[key] = value[:MAX_TAG_LEN] + "..."
    
    if "chapters" in tags and isinstance(tags["chapters"], list):
        if len(tags["chapters"]) > MAX_CHAPTERS:
            log.warning(f"Truncating excessive chapters ({len(tags['chapters'])} -> {MAX_CHAPTERS})")
            tags["chapters"] = tags["chapters"][:MAX_CHAPTERS]
            
    return tags


# Mapping which parsers are responsible for which file types (extensions including dot)
# If a file type is not in this mapping, all parsers in the chain will be attempted (legacy behavior).
# If a file type IS in this mapping, only the listed parsers will be executed.
PARSER_MAPPING = {
    # --- AUDIO ---
    ".mp3":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "eyed3", "music_tag"],
    ".flac": ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
    ".m4a":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
    ".m4b":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
    ".ogg":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
    ".wav":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
    ".wma":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
    
    # --- VIDEO ---
    ".mkv":  ["filename", "container", "mkvmerge", "mkvinfo", "vlc", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "ebml", "mkvparse", "enzyme", "pymkv"],
    ".mp4":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "enzyme"],
    ".m4v":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
    ".avi":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
    ".mov":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
    ".webm": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
    ".wmv":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
    ".mpg":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
    ".mpeg": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
    
    ".iso":    ["filename", "pycdlib", "isoparser", "pymediainfo", "ffprobe", "ffmpeg"],
    ".bin":    ["filename", "pycdlib", "isoparser", "pymediainfo", "ffprobe", "ffmpeg"],
    ".img":    ["filename", "pycdlib", "isoparser", "pymediainfo", "ffprobe", "ffmpeg"],
    ".jpg":    ["filename", "pymediainfo", "ffprobe", "ffmpeg"],
    ".jpeg":   ["filename", "pymediainfo", "ffprobe", "ffmpeg"],
    ".png":    ["filename", "pymediainfo", "ffprobe", "ffmpeg"],
    ".webp":   ["filename", "pymediainfo", "ffprobe", "ffmpeg"],
    
    # --- DOCUMENTS & EBOOKS ---
    ".pdf":    ["filename", "pymediainfo", "ffprobe"],
    ".epub":   ["filename", "pymediainfo", "ffprobe"],
}


def get_parser_info() -> dict[str, Any]:
    """
    @brief Aggregates info about all available parsers, their capabilities and settings schemas.
    """
    parsers = {
        "mutagen": mutagen_parser,
        "pymediainfo": pymediainfo_parser,
        "ffprobe": ffprobe_parser,
        "ffmpeg": ffmpeg_parser,
        "mkvmerge": mkvmerge_parser,
        "mkvinfo": mkvinfo_parser,
        "vlc": vlc_parser,
        "filename": filename_parser,
        "container": container_parser,
        "isoparser": isoparser_parser
    }
    
    info = {}
    for p_id, p_mod in parsers.items():
        p_info = {}
        if hasattr(p_mod, 'get_capabilities'):
            p_info['capabilities'] = p_mod.get_capabilities()
        if hasattr(p_mod, 'get_settings_schema'):
            p_info['settings_schema'] = p_mod.get_settings_schema()
        
        if p_info:
            info[p_id] = p_info
            
    return info


def extract_metadata(path, filename, mode='lightweight', file_type=None, **kwargs):
    """
    @brief Orchestrates the metadata extraction process using a sequential parser chain.
    @details Orchestriert den Metadaten-Extraktionsprozess über eine sequentielle Parser-Kette.
    @param path Path to the media file / Pfad zur Mediendatei.
    @param filename Original filename for fallback parsing / Originaldateiname für Fallback-Parsing.
    @param mode Extraction mode ('lightweight', 'full', or 'ultimate') / Extraktionsmodus ('lightweight', 'full' oder 'ultimate').
    @return Tuple (duration, tags) / Tupel (Dauer, Tags).
    """
    logging.info(f"[Parser-Trace] Starte Parsing für '{filename}' (Mode: {mode})")
    if mode in ('full', 'ultimate'):
        logging.info(f"[Parser-Trace] 🚀 {mode.capitalize()} Mode aktiviert für '{filename}' – sammle ALLE Tags!")

    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from .format_utils import PARSER_CONFIG, format_bitdepth, format_codec, format_container, format_tagtype

    # Early exit: skip parser chain if not a regular file
    if not path_obj.is_file():
        log.warning(f"Early exit: '{filename}' is not a file (type: {'directory' if path_obj.is_dir() else 'unknown'})")
        tags = {
            'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
            'codec': '', 'size': '', 'tagtype': '', 'container': '',
            'has_art': 'No', 'title': '', 'artist': '', 'album': '',
            'date': '', 'genre': '', 'track': '', 'totaltracks': '',
            'disc': '', 'totaldiscs': '',
            'error': 'Not a file',
            'name': filename,
            'type': 'directory' if path_obj.is_dir() else 'unknown',
        }
        return tags, {}

    tags: dict[str, Any] = {
        'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
        'codec': '', 'size': '', 'tagtype': '', 'container': '',
        'has_art': 'No', 'title': '', 'artist': '', 'album': '',
        'date': '', 'genre': '', 'track': '', 'totaltracks': '',
        'disc': '', 'totaldiscs': ''
    }
    if mode in ('full', 'ultimate'):
        tags['full_tags'] = {}

    duration = 0
    parser_times = {}

    from typing import cast
    parser_chain = cast(list[str], PARSER_CONFIG.get(
        "parser_chain", ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "isoparser"]))
    log.debug(f"DEBUG: PARSER_CONFIG['parser_chain']: {parser_chain}")

    from . import isoparser_parser
    parser_steps = [
        ("filename", filename_parser.parse),
        ("container", container_parser.parse),
        ("mutagen", mutagen_parser.parse),
        ("pymediainfo", pymediainfo_parser.parse),
        ("ffprobe", ffprobe_parser.parse),
        ("mkvmerge", mkvmerge_parser.parse),
        ("mkvinfo", mkvinfo_parser.parse),
        ("vlc", vlc_parser.parse),
        ("ffmpeg", ffmpeg_parser.parse),
        ("isoparser", isoparser_parser.parse),
        ("ebml", None),
        ("mkvparse", None),
        ("enzyme", None),
        ("pycdlib", None),
        ("pymkv", None),
        ("tinytag", None),
        ("eyed3", None),
        ("music_tag", None),
    ]

    MAX_RETRIES = PARSER_CONFIG.get("parser_max_retries", 2)

    active_steps = []
    for p_id in parser_chain:
        step = next((s for s in parser_steps if s[0] == p_id), None)
        if step:
            active_steps.append(step)

    from .format_utils import PARSER_CONFIG, SLOW_PARSERS

    error_shortcircuit = False
    for step_name, step_func in active_steps:
        if error_shortcircuit:
            log.debug(f"Shortcircuit: Skipping remaining parsers for '{filename}' due to prior error.")
            break
        if file_type in PARSER_MAPPING and step_name not in PARSER_MAPPING[file_type]:
            continue
        is_slow = step_name in SLOW_PARSERS
        fast_scan = PARSER_CONFIG.get("fast_scan_enabled", True)
        if is_slow and mode != 'full' and fast_scan:
            log.debug(f"⏩ [Fast-Scan] Skipping slow parser '{step_name}' for '{filename}'")
            continue
        if mode != 'full':
            has_essential = (
                tags.get('samplerate')
                and tags.get('bitrate')
                and tags.get('bitdepth')
                and tags.get('codec')
                and tags.get('codec') != file_type[1:].lower()
                and tags.get('container')
                and duration
            )
            needs_chapters = file_type in ['.m4b', '.mkv', '.m4a', '.mp4'] and not tags.get('chapters')
            if has_essential and not needs_chapters:
                continue
        current_tags = tags
        attempt = 0
        success = False
        while attempt <= MAX_RETRIES and not success:
            t0 = time.time()
            tags_backup = copy.deepcopy(current_tags)
            try:
                # In ultimate mode, we want a copy of the tags before this parser
                tags_before = current_tags.copy() if mode == 'ultimate' else None
                
                
                # Get parser specific settings from PARSER_CONFIG
                p_settings = PARSER_CONFIG.get('parser_settings', {}).get(step_name, {})
                
                if step_func:
                    current_tags = cast(dict[str, Any], step_func(
                        path_obj, file_type, current_tags, filename, 
                        mode=('full' if mode == 'ultimate' else mode),
                        settings=p_settings))
                    current_tags = sanitize_metadata(current_tags)
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "ebml":
                    from ebml.container import File
                    with path_obj.open('rb') as f:
                        ebml_file = File(f)
                        segment = next(ebml_file.children_named("Segment"), None)
                        if segment:
                            current_tags['ebml_title'] = getattr(segment, 'title', None)
                            current_tags['ebml_duration'] = getattr(segment, 'duration', None)
                            current_tags['ebml_tracks'] = [
                                {
                                    'type': getattr(track, 'track_type', None),
                                    'language': getattr(track, 'language', None),
                                    'codec_id': getattr(track, 'codec_id', None)
                                }
                                for track in getattr(segment, 'tracks', [])
                            ]
                            current_tags['ebml_chapters'] = getattr(segment, 'chapters', None)
                    current_tags = sanitize_metadata(current_tags)
                    log.debug(f"EBML parser finished for '{filename}'")
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "mkvparse":
                    import mkvparse
                    with open(str(path_obj), 'rb') as f:
                        mkvparse.parse(f, lambda elem, data: log.debug(f"mkvparse: {elem} {data}"))
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "enzyme":
                    import enzyme
                    with path_obj.open('rb') as f:
                        movie = enzyme.MKV(f)
                        current_tags['enzyme_tracks'] = movie.audio_tracks + movie.video_tracks
                        current_tags['enzyme_duration'] = movie.info.duration.total_seconds() if movie.info and movie.info.duration else None
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "pycdlib":
                    import pycdlib
                    iso = pycdlib.PyCdlib()
                    iso.open(str(path_obj))
                    pvd = iso.get_pvd()
                    current_tags['pycdlib_volume_id'] = pvd.volume_identifier.decode('utf-8', 'replace').strip() if pvd else "Unknown"
                    iso.close()
                    current_tags = sanitize_metadata(current_tags)
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "pymkv":
                    import pymkv
                    import shutil
                    if not shutil.which("mkvmerge"):
                         raise FileNotFoundError("mkvmerge binary not found in PATH")
                    mkv = pymkv.MKVFile(str(path_obj))
                    current_tags['pymkv_tracks'] = mkv.tracks
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "tinytag":
                    from tinytag import TinyTag
                    tag = TinyTag.get(str(path_obj))
                    current_tags['tinytag_title'] = tag.title
                    current_tags['tinytag_artist'] = tag.artist
                    current_tags['tinytag_duration'] = tag.duration
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "eyed3":
                    import eyed3
                    audiofile = eyed3.load(str(path_obj))
                    if audiofile and audiofile.tag:
                        current_tags['eyed3_title'] = audiofile.tag.title
                        current_tags['eyed3_artist'] = audiofile.tag.artist
                        current_tags['eyed3_album'] = audiofile.tag.album
                        current_tags['eyed3_duration'] = audiofile.info.time_secs if audiofile.info else None
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "music_tag":
                    import music_tag
                    f = music_tag.load_file(str(path_obj))
                    current_tags['music_tag_title'] = f['title'].value
                    current_tags['music_tag_artist'] = f['artist'].value
                    current_tags['music_tag_album'] = f['album'].value
                    current_tags['music_tag_duration'] = f['duration'].value
                    parser_times[step_name] = time.time() - t0
                    success = True
                else:
                    parser_times[step_name] = 0.0
                    success = True
            except (subprocess.TimeoutExpired, TimeoutError) as e:
                attempt += 1
                current_tags = tags_backup # Restore state
                log.error(f"⏱️ Parser {step_name} timed out for '{filename}' (Attempt {attempt}/{MAX_RETRIES+1}): {e}")
                if attempt > MAX_RETRIES:
                    parser_times[step_name] = time.time() - t0
            except (ImportError, ModuleNotFoundError) as e:
                # Missing dependencies shouldn't be retried
                current_tags = tags_backup # Restore state
                log.error(f"📦 Parser {step_name} failed due to missing dependency for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
                success = True # Skip this parser
            except Exception as e:
                attempt += 1
                current_tags = tags_backup # Restore state
                # Error shortcircuit: skip remaining parsers for typical file errors
                error_str = str(e).lower()
                if any(msg in error_str for msg in ["is a directory", "not a file", "no tag reader found", "mutagen type <class 'nonetype'> not implemented", "failed to read entire volume descriptor", "can't sync to mpeg frame"]):
                    log.error(f"Shortcircuit: {step_name} parser error for '{filename}': {e}")
                    parser_times[step_name] = time.time() - t0
                    error_shortcircuit = True
                    break
                if attempt <= MAX_RETRIES:
                    log.warning(f"⚠️ Parser {step_name} failed (Attempt {attempt}/{MAX_RETRIES+1}) for '{filename}': {e}. Retrying...")
                    time.sleep(0.05 * attempt)
                else:
                    log.error(f"❌ {step_name} parser error after {MAX_RETRIES} retries for '{filename}': {e}")
                    parser_times[step_name] = time.time() - t0
        tags = current_tags
        if 'duration' in tags and tags['duration'] and not duration:
            try:
                duration = int(float(tags['duration']))
            except (ValueError, TypeError):
                duration = 0

    # Final Fallback for Lossy / Missing Bitdepth
    # The user specifically requested formats like MP3 to default to "16 Bit (lossy)"
    # We now use centralized formatting logic.
    if not tags.get('bitdepth'):
        tags['bitdepth'] = format_bitdepth(None, codec=tags.get('codec'), file_type=file_type)

    # Enforce standard formatting for consistency across all parsers
    if tags.get('codec'):
        tags['codec'] = format_codec(tags['codec'])
    if tags.get('container'):
        tags['container'] = format_container(tags['container'], file_type)
    tags['tagtype'] = format_tagtype(tags.get('tagtype'))
    
    # Final sanitization pass
    tags = sanitize_metadata(tags)

    # Final Chapter Sort (Natural & Chronological)
    if tags.get('chapters') and isinstance(tags['chapters'], list):
        from .format_utils import natural_sort_key
        # Detect chapter variants
        nero_variant = any('chapter' in c and 'start_time' in c for c in tags['chapters'])
        apple_variant = any('title' in c and 'start' in c for c in tags['chapters'])
        both_variants = nero_variant and apple_variant
        variant_str = (
            'Beide Varianten (Nero & Apple)' if both_variants else
            'Nero-Variante' if nero_variant else
            'Apple-Variante' if apple_variant else
            'Unbekannte Variante'
        )
        log.info(f"Chapter variant detected: {variant_str} for '{filename}'")
        # Priority: 1. Natural Title, 2. Start Time
        tags['chapters'] = sorted(tags['chapters'], key=lambda x: (
            natural_sort_key(x.get('title', '')), x.get('start', 0.0)))
        if log.isEnabledFor(logging.DEBUG):
            first_chaps = [c.get('title') for c in tags['chapters'][:5]]
            log.debug(f"Sorted {len(tags['chapters'])} chapters. First 5: {first_chaps}")

    total_time = sum(parser_times.values())
    timing_report = ", ".join([f"{p}: {t:.3f}s" for p, t in parser_times.items() if t > 0.001])
    logging.info(f"[Parser-Trace] Metadata extraction complete for {filename} in {total_time:.3f}s.")
    if timing_report:
        logging.info(f"[Parser-Trace] ⏱️ Detailed Timings: {timing_report}")
    # Backwards-compat: return (tags, parser_times) as older tests expect tags first
    return cast(dict[str, Any], tags), parser_times
