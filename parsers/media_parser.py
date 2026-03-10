import time
from typing import Any
from pathlib import Path
from . import filename_parser
from . import mutagen_parser
from . import pymediainfo_parser
from . import ffprobe_parser
from . import ffmpeg_parser
from . import container_parser
import logger
import logging

# Get specialized logger for parser component
log = logger.get_logger("parser")


def extract_metadata(path, filename, mode='lightweight', file_type=None):
    """
    @brief Orchestrates the metadata extraction process using a sequential parser chain.
    @details Orchestriert den Metadaten-Extraktionsprozess über eine sequentielle Parser-Kette.
    @param path Path to the media file / Pfad zur Mediendatei.
    @param filename Original filename for fallback parsing / Originaldateiname für Fallback-Parsing.
    @param mode Extraction mode ('lightweight' or 'full') / Extraktionsmodus ('lightweight' oder 'full').
    @return Tuple (duration, tags) / Tupel (Dauer, Tags).
    """
    log.debug(f"Starte Parsing für '{filename}' (Mode: {mode})")
    logger.debug("metadata", f"Extraction requested for: {filename} (Mode: {mode})")
    if mode == 'full':
        log.debug(f"🚀 Full Mode aktiviert für '{filename}' – sammle ALLE Tags!")

    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from .format_utils import PARSER_CONFIG, format_bitdepth, format_codec, format_container, format_tagtype

    tags: dict[str, Any] = {
        'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
        'codec': '', 'size': '', 'tagtype': '', 'container': '',
        'has_art': 'No', 'title': '', 'artist': '', 'album': '',
        'date': '', 'genre': '', 'track': '', 'totaltracks': '',
        'disc': '', 'totaldiscs': ''
    }
    if mode == 'full':
        tags['full_tags'] = {}

    duration = 0
    parser_times = {}

    from typing import cast
    # Iterate dynamically through the user-configured parser chain
    parser_chain = cast(list[str], PARSER_CONFIG.get(
        "parser_chain", ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"]))

    # Neue Iteration: Alle verfügbaren Parser als optionale Schritte
    from . import isoparser_parser
    parser_steps = [
        ("filename", filename_parser.parse),
        ("container", container_parser.parse),
        ("mutagen", mutagen_parser.parse),
        ("pymediainfo", pymediainfo_parser.parse),
        ("ffprobe", ffprobe_parser.parse),
        ("ffmpeg", ffmpeg_parser.parse),
        ("isoparser", isoparser_parser.parse),  # new alternative ISO parser
        ("ebml", None),  # handled below
        ("mkvparse", None),  # handled below
        ("enzyme", None),  # handled below
        ("pycdlib", None),  # handled below
        ("pymkv", None),  # handled below
        ("tinytag", None),  # handled below
        ("eyed3", None),  # handled below
        ("music_tag", None),  # handled below
    ]

    ebml_enabled = PARSER_CONFIG.get("enable_ebml_parser", False)
    mkvparse_enabled = PARSER_CONFIG.get("enable_mkvparse_parser", False)
    enzyme_enabled = PARSER_CONFIG.get("enable_enzyme_parser", False)
    pycdlib_enabled = PARSER_CONFIG.get("enable_pycdlib_parser", False)
    pymkv_enabled = PARSER_CONFIG.get("enable_pymkv_parser", False)
    tinytag_enabled = PARSER_CONFIG.get("enable_tinytag_parser", False)
    eyed3_enabled = PARSER_CONFIG.get("enable_eyed3_parser", False)
    music_tag_enabled = PARSER_CONFIG.get("enable_music_tag_parser", False)
    isoparser_enabled = PARSER_CONFIG.get("enable_isoparser_parser", True)  # default enabled

    MAX_RETRIES = PARSER_CONFIG.get("parser_max_retries", 2)

    # Filter and sort parser_steps according to the configured parser_chain
    active_steps = []
    for p_id in parser_chain:
        step = next((s for s in parser_steps if s[0] == p_id), None)
        if step:
            active_steps.append(step)

    for step_name, step_func in active_steps:
        # Skip if we already have enough information (for lightweight mode)
        # or if mode is 'full' we always continue to gather all tags.
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
            # M4B / MKV often need chapters which filename parser can't provide
            needs_chapters = file_type in ['.m4b', '.mkv', '.m4a', '.mp4'] and not tags.get('chapters')
            
            if has_essential and not needs_chapters:
                continue

        # Initialize local variables for the retry loop
        current_tags = tags
        attempt = 0
        success = False
        while attempt <= MAX_RETRIES and not success:
            t0 = time.time()
            try:
                if step_func:
                    # Only run isoparser if enabled and file is .iso
                    if step_name == "isoparser" and not isoparser_enabled:
                        parser_times[step_name] = 0.0
                        success = True
                        continue
                    
                    current_tags = cast(dict[str, Any], step_func(
                        path_obj, file_type, current_tags, filename, mode=mode))
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "ebml" and ebml_enabled and file_type == ".mkv":
                    from ebml.container import File
                    ebml_file = File(str(path_obj))
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
                    log.debug(f"EBML parser finished for '{filename}'")
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "mkvparse" and mkvparse_enabled and file_type == ".mkv":
                    import mkvparse
                    with open(str(path_obj), 'rb') as f:
                        mkvparse.parse(f, lambda elem, data: log.debug(f"mkvparse: {elem} {data}"))
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "enzyme" and enzyme_enabled and file_type in [".mkv", ".mp4"]:
                    import enzyme
                    movie = enzyme.Movie(str(path_obj))
                    current_tags['enzyme_tracks'] = movie.tracks
                    current_tags['enzyme_duration'] = movie.duration
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "pycdlib" and pycdlib_enabled and file_type == ".iso":
                    import pycdlib
                    iso = pycdlib.PyCdlib()
                    iso.open(str(path_obj))
                    current_tags['pycdlib_volume_id'] = iso.get_volume_id()
                    iso.close()
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "pymkv" and pymkv_enabled and file_type == ".mkv":
                    import pymkv
                    mkv = pymkv.MKVFile(str(path_obj))
                    current_tags['pymkv_tracks'] = mkv.tracks
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "tinytag" and tinytag_enabled and file_type in [".mp3", ".m4a", ".ogg", ".flac", ".wav", ".wma"]:
                    from tinytag import TinyTag
                    tag = TinyTag.get(str(path_obj))
                    current_tags['tinytag_title'] = tag.title
                    current_tags['tinytag_artist'] = tag.artist
                    current_tags['tinytag_duration'] = tag.duration
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "eyed3" and eyed3_enabled and file_type == ".mp3":
                    import eyed3
                    audiofile = eyed3.load(str(path_obj))
                    if audiofile and audiofile.tag:
                        current_tags['eyed3_title'] = audiofile.tag.title
                        current_tags['eyed3_artist'] = audiofile.tag.artist
                        current_tags['eyed3_album'] = audiofile.tag.album
                        current_tags['eyed3_duration'] = audiofile.info.time_secs if audiofile.info else None
                    parser_times[step_name] = time.time() - t0
                    success = True
                elif step_name == "music_tag" and music_tag_enabled and file_type in [".mp3", ".flac", ".m4a", ".ogg", ".wav", ".wma"]:
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
            except Exception as e:
                attempt += 1
                if attempt <= MAX_RETRIES:
                    log.warning(f"Parser {step_name} failed (Attempt {attempt}/{MAX_RETRIES+1}) for '{filename}': {e}. Retrying...")
                    time.sleep(0.05 * attempt)
                else:
                    log.error(f"{step_name} parser error after {MAX_RETRIES} retries for '{filename}': {e}")
                    parser_times[step_name] = time.time() - t0
        
        tags = current_tags

        # Update duration safely after each potential parser
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

    tags['_parser_times'] = parser_times
    logger.debug("metadata", f"Metadata extraction complete for {filename}. Parsers: {list(parser_times.keys())}")
    return int(duration), cast(dict[str, Any], tags)
