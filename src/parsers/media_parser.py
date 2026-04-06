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
from . import ebml_parser
from . import mkvparse_parser
from . import enzyme_parser
from . import pycdlib_parser
from . import pymkv_parser
from . import tinytag_parser
from . import eyed3_parser
from . import music_tag_parser
import multiprocessing
from src.core.config_master import GLOBAL_CONFIG

# Parser Categories (Centralized v1.35.68)
AUDIO_PARSER_IDS = set(GLOBAL_CONFIG["parser_registry"]["categories"]["audio"])
MULTIMEDIA_PARSER_IDS = set(GLOBAL_CONFIG["parser_registry"]["categories"]["multimedia"])
UNIVERSAL_PARSER_IDS = set(GLOBAL_CONFIG["parser_registry"]["categories"]["universal"])

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

# Magic byte signatures (Centralized v1.35.68)
_sig_map = GLOBAL_CONFIG["parser_registry"]["magic_signatures"]
REQUIRED_MAGIC = {k: bytes.fromhex(v) for k, v in _sig_map.items()}

def get_file_magic(path: Path, length: int = 16, offset: int = 0) -> bytes:
    """
    @brief Reads bytes from a file at a specific offset.
    """
    try:
        with path.open("rb") as f:
            if offset > 0:
                f.seek(offset)
            return f.read(length)
    except Exception:
        return b""

def validate_semantic_consistency(tags: dict[str, Any], filename: str):
    """
    @brief Compares metadata from different sources for sanity.
    """
    # 1. Duration Cross-Check
    durations = []
    for k in tags:
        if 'duration' in k.lower() and tags[k]:
            try:
                durations.append(float(tags[k]))
            except (ValueError, TypeError):
                continue
    
    if len(set(durations)) > 1:
        avg_dur = sum(durations) / len(durations)
        discrepancy = max(durations) - min(durations)
        if discrepancy > 5: # More than 5 seconds difference
            log.warning(f"⚖️ [Semantic-Validation] Duration discrepancy for '{filename}': {min(durations)}s to {max(durations)}s")

def _sandboxed_worker(func, queue, *args, **kwargs):
    """
    Internal worker for multiprocessing.
    """
    try:
        result = func(*args, **kwargs)
        queue.put((True, result))
    except Exception as e:
        queue.put((False, str(e)))

def run_sandboxed(func, timeout, *args, **kwargs):
    """
    @brief Runs a function in a separate process to isolate crashes/hangs.
    """
    result_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=_sandboxed_worker, args=(func, result_queue) + args, kwargs=kwargs)
    p.start()
    
    try:
        success, result = result_queue.get(timeout=timeout)
        p.join(timeout=1.0)
        if success:
            return result
        else:
            raise Exception(f"Sandboxed process error: {result}")
    except (multiprocessing.TimeoutError, queue.Empty):
        p.terminate()
        p.join()
        raise TimeoutError(f"Sandboxed process timed out after {timeout}s")
    except Exception as e:
        p.terminate()
        p.join()
        raise e


# Mapping which parsers are responsible for which file types (Centralized v1.35.68)
PARSER_MAPPING = GLOBAL_CONFIG["parser_registry"]["extension_map"]


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
    @return Tuple (duration, tags) / Tupel (Dauer, Tags).
    """
    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from .format_utils import ALL_AUDIO_EXTENSIONS
    
    if file_type in ALL_AUDIO_EXTENSIONS:
        return extract_metadata_audio(path, filename, mode, **kwargs)
    else:
        return extract_metadata_multimedia(path, filename, mode, **kwargs)

def extract_metadata_audio(path, filename, mode='lightweight', **kwargs):
    """
    @brief Specialized branch for audio-only extraction.
    """
    log.debug(f"🎵 [Audio-Branch] Starting extraction for '{filename}'")
    return _extract_metadata_internal(path, filename, mode, category='audio', **kwargs)

def extract_metadata_multimedia(path, filename, mode='lightweight', **kwargs):
    """
    @brief Specialized branch for multimedia (video/ISO) extraction.
    """
    log.debug(f"🎬 [Multimedia-Branch] Starting extraction for '{filename}'")
    return _extract_metadata_internal(path, filename, mode, category='multimedia', **kwargs)

def _extract_metadata_internal(path, filename, mode='lightweight', category=None, **kwargs):
    """
    @brief Core extraction logic shared by branches.
    """
    logging.info(f"[Parser-Trace] Starte Parsing für '{filename}' (Mode: {mode}, Category: {category})")
    if mode in ('full', 'ultimate'):
        logging.info(f"[Parser-Trace] 🚀 {mode.capitalize()} Mode aktiviert für '{filename}' – sammle ALLE Tags!")

    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from .format_utils import PARSER_CONFIG, format_bitdepth, format_codec, format_container, format_tagtype

    tags: dict[str, Any] = {
        'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
        'codec': '', 'size': '', 'tagtype': '', 'container': '',
        'has_art': 'No', 'title': '', 'artist': '', 'album': '',
        'date': '', 'genre': '', 'track': '', 'totaltracks': '',
        'disc': '', 'totaldiscs': '',
        'name': filename,
        'type': 'directory' if path_obj.is_dir() else 'file' if path_obj.is_file() else 'missing',
    }
    # Initialize full_tags for high-fidelity modes (v1.35.68 Centralized)
    if mode in ('full', 'ultimate') and 'full_tags' not in tags:
        tags['full_tags'] = {}

    duration = 0
    parser_times = {}

    from typing import cast
    parser_chain = cast(list[str], PARSER_CONFIG.get(
        "parser_chain", ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "isoparser"]))
    log.debug(f"DEBUG: PARSER_CONFIG['parser_chain']: {parser_chain}")

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
        ("ebml", ebml_parser.parse),
        ("mkvparse", mkvparse_parser.parse),
        ("enzyme", enzyme_parser.parse),
        ("pycdlib", pycdlib_parser.parse),
        ("pymkv", pymkv_parser.parse),
        ("tinytag", tinytag_parser.parse),
        ("eyed3", eyed3_parser.parse),
        ("music_tag", music_tag_parser.parse),
    ]

    MAX_RETRIES = PARSER_CONFIG.get("parser_max_retries", 2)

    active_steps = []
    for p_id in parser_chain:
        step = next((s for s in parser_steps if s[0] == p_id), None)
        if step:
            active_steps.append(step)

    from .format_utils import PARSER_CONFIG, SLOW_PARSERS

    error_shortcircuit = False
    
    # Branch-based chain filtering:
    # We skip parsers that don't belong to the file's primary category (audio vs multimedia)
    # unless they are universal.
    is_audio = category == 'audio'
    
    for step_name, step_func in active_steps:
        if error_shortcircuit:
            log.debug(f"Shortcircuit: Skipping remaining parsers for '{filename}' due to prior error.")
            break
            
        # Category Isolation
        if is_audio and step_name in MULTIMEDIA_PARSER_IDS:
             log.debug(f"🔇 [Audio-Branch] Skipping multimedia parser '{step_name}' for '{filename}'")
             continue
        
        if not is_audio and step_name in AUDIO_PARSER_IDS:
             log.debug(f"🔇 [Multimedia-Branch] Skipping audio parser '{step_name}' for '{filename}'")
             continue
        is_slow = step_name in SLOW_PARSERS
        fast_scan = PARSER_CONFIG.get("fast_scan_enabled", True)
        if is_slow and mode != 'full' and fast_scan:
            log.debug(f"⏩ [Fast-Scan] Skipping slow parser '{step_name}' for '{filename}'")
            continue
            
        # Magic Byte Verification
        required_magic = REQUIRED_MAGIC.get(step_name)
        if required_magic:
            offset = 32769 if step_name in ["pycdlib", "isoparser"] else 0
            file_magic = get_file_magic(path_obj, len(required_magic), offset=offset)
            if not file_magic.startswith(required_magic):
                log.debug(f"🔍 [Magic-Check] Skipping '{step_name}' for '{filename}': magic {file_magic.hex()} mismatch at {offset}")
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
                
                if step_name in ["pymediainfo", "pycdlib", "isoparser"]:
                    # Optimization: Skip heavy parsers for very large ISO files
                    # They tend to cause extreme memory spikes during full/deep scans
                    if file_type == ".iso" and path_obj.stat().st_size > 500 * 1024 * 1024:
                        logging.info(f"Skipping {step_name} for large ISO: {filename}")
                        parser_times[step_name] = time.time() - t0
                        success = True
                        continue

                if step_func:
                    current_tags = cast(dict[str, Any], step_func(
                        path_obj, file_type, current_tags, filename, 
                        mode=('full' if mode == 'ultimate' else mode),
                        settings=p_settings))
                    current_tags = sanitize_metadata(current_tags)
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "ebml":
                    def parse_ebml_isolated(path_o):
                        from ebml.container import File
                        with path_o.open('rb') as f_ebml:
                            ef = File(f_ebml)
                            seg = next(ef.children_named("Segment"), None)
                            if seg:
                                return {
                                    'ebml_title': getattr(seg, 'title', None),
                                    'ebml_duration': getattr(seg, 'duration', None),
                                    'ebml_tracks': [
                                        {
                                            'type': getattr(tr, 'track_type', None),
                                            'language': getattr(tr, 'language', None),
                                            'codec_id': getattr(tr, 'codec_id', None)
                                        }
                                        for tr in getattr(seg, 'tracks', [])[:50] # Limit tracks
                                    ]
                                }
                        return {}
                    
                    res = run_sandboxed(parse_ebml_isolated, timeout=5.0, path_o=path_obj)
                    current_tags.update(res)
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
                    def parse_enzyme_isolated(path_o):
                        import enzyme
                        with path_o.open('rb') as f_enz:
                            movie = enzyme.MKV(f_enz)
                            return {
                                'enzyme_tracks': (movie.audio_tracks + movie.video_tracks)[:50],
                                'enzyme_duration': movie.info.duration.total_seconds() if movie.info and movie.info.duration else None
                            }
                    
                    res = run_sandboxed(parse_enzyme_isolated, timeout=5.0, path_o=path_obj)
                    current_tags.update(res)
                    current_tags = sanitize_metadata(current_tags)
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "pycdlib":
                    def parse_pycdlib_isolated(path_o):
                        import pycdlib
                        iso = pycdlib.PyCdlib()
                        iso.open(str(path_o))
                        
                        tags = {}
                        def safe_str(val):
                            if val is None: return ""
                            # Some pycdlib versions return specialized objects with a .text attribute (bytes)
                            if hasattr(val, 'text'):
                                val = val.text
                            if hasattr(val, 'decode'):
                                return val.decode('utf-8', 'replace').strip()
                            return str(val).strip()

                        try:
                            pvd = iso.pvd
                        except:
                            pvd = None

                        if pvd:
                            tags['pycdlib_volume_id'] = safe_str(pvd.volume_identifier)
                            tags['pycdlib_publisher'] = safe_str(pvd.publisher_identifier)
                            tags['pycdlib_application'] = safe_str(pvd.application_identifier)
                            tags['pycdlib_preparer'] = safe_str(pvd.preparer_identifier)
                            try:
                                cdate = pvd.volume_creation_date
                                if hasattr(cdate, 'year') and cdate.year > 0:
                                    tags['pycdlib_creation_date'] = f"{cdate.year:04d}-{cdate.month:02d}-{cdate.dayofmonth:02d} {cdate.hour:02d}:{cdate.minute:02d}:{cdate.second:02d}"
                                else:
                                    tags['pycdlib_creation_date'] = safe_str(cdate)
                            except: pass

                        tags['pycdlib_has_joliet'] = iso.has_joliet()
                        tags['pycdlib_has_rock_ridge'] = iso.has_rock_ridge()
                        tags['pycdlib_has_udf'] = iso.has_udf()
                        
                        # Content Detection (Search for DVD/BD markers in root)
                        try:
                            children = list(iso.list_children(iso_path='/'))
                            for c in children:
                                # file_identifier can be an attribute or a method depending on version
                                ident = c.file_identifier() if callable(c.file_identifier) else c.file_identifier
                                ident_str = safe_str(ident).upper()
                                if 'VIDEO_TS' in ident_str:
                                    tags['pycdlib_is_dvd'] = True
                                if 'AUDIO_TS' in ident_str:
                                    tags['pycdlib_is_dvd_audio'] = True
                                if 'DVD_RTAV' in ident_str:
                                    tags['pycdlib_is_dvd_vr'] = True
                                if 'BDMV' in ident_str:
                                    tags['pycdlib_is_bluray'] = True
                                if 'HVDVD_TS' in ident_str:
                                    tags['pycdlib_is_hvdvd'] = True
                                if 'MPEGAV' in ident_str:
                                    tags['pycdlib_is_vcd'] = True
                                if 'SEGMENT' in ident_str or 'SVCD' in ident_str:
                                    tags['pycdlib_is_svcd'] = True
                                if 'CDI' in ident_str:
                                    tags['pycdlib_is_cdi'] = True
                                if 'PHOTO_CD' in ident_str:
                                    tags['pycdlib_is_photocd'] = True
                                if 'CDPLUS' in ident_str:
                                    tags['pycdlib_is_cd_extra'] = True
                        except: pass

                        iso.close()
                        return tags
                    
                    res = run_sandboxed(parse_pycdlib_isolated, timeout=5.0, path_o=path_obj)
                    current_tags.update(res)
                    current_tags = sanitize_metadata(current_tags)
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "pymkv":
                    import pymkv
                    import shutil
                    mkvmerge_bin = GLOBAL_CONFIG["program_paths"].get("mkvmerge", "mkvmerge")
                    if not shutil.which(mkvmerge_bin):
                         raise FileNotFoundError(f"{mkvmerge_bin} binary not found in PATH")
                    mkv = pymkv.MKVFile(str(path_obj), mkvmerge_path=mkvmerge_bin)
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
    
    # Semantic Cross-Validation
    validate_semantic_consistency(tags, filename)
    
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
