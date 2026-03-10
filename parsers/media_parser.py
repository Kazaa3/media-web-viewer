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

    for step_name, step_func in parser_steps:
        needs_more_info = True if mode == 'full' else (
            not tags.get('samplerate')
            or not tags.get('bitrate')
            or not tags.get('bitdepth')
            or not tags.get('codec')
            or tags.get('codec') == file_type[1:].lower()
            or not tags.get('container')
            or not duration
            or (file_type in ['.m4b', '.mkv', '.m4a', '.mp4'] and not tags.get('chapters'))
        )

        t0 = time.time()
        try:
            if step_func:
                # Only run isoparser if enabled and file is .iso
                if step_name == "isoparser" and not isoparser_enabled:
                    parser_times[step_name] = 0.0
                    continue
                tags = cast(dict[str, Any], step_func(
                    path_obj, file_type, tags, mode=mode))
                parser_times[step_name] = time.time() - t0
            elif step_name == "ebml" and ebml_enabled and file_type == ".mkv":
                from ebml.container import File
                ebml_file = File(str(path_obj))
                segment = next(ebml_file.children_named("Segment"), None)
                if segment:
                    tags['ebml_title'] = getattr(segment, 'title', None)
                    tags['ebml_duration'] = getattr(segment, 'duration', None)
                    tags['ebml_tracks'] = [
                        {
                            'type': getattr(track, 'track_type', None),
                            'language': getattr(track, 'language', None),
                            'codec_id': getattr(track, 'codec_id', None)
                        }
                        for track in getattr(segment, 'tracks', [])
                    ]
                    tags['ebml_chapters'] = getattr(segment, 'chapters', None)
                log.debug(f"EBML parser finished for '{filename}'")
                parser_times[step_name] = time.time() - t0
            elif step_name == "mkvparse" and mkvparse_enabled and file_type == ".mkv":
                import mkvparse
                # Beispiel: mkvparse kann Streams und Tracks extrahieren
                try:
                    with open(str(path_obj), 'rb') as f:
                        mkvparse.parse(f, lambda elem, data: log.debug(f"mkvparse: {elem} {data}"))
                except Exception as e:
                    log.error(f"mkvparse error for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
            elif step_name == "enzyme" and enzyme_enabled and file_type in [".mkv", ".mp4"]:
                import enzyme
                try:
                    movie = enzyme.Movie(str(path_obj))
                    tags['enzyme_tracks'] = movie.tracks
                    tags['enzyme_duration'] = movie.duration
                except Exception as e:
                    log.error(f"enzyme error for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
            elif step_name == "pycdlib" and pycdlib_enabled and file_type == ".iso":
                import pycdlib
                try:
                    iso = pycdlib.PyCdlib()
                    iso.open(str(path_obj))
                    tags['pycdlib_volume_id'] = iso.get_volume_id()
                    iso.close()
                except Exception as e:
                    log.error(f"pycdlib error for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
            elif step_name == "pymkv" and pymkv_enabled and file_type == ".mkv":
                import pymkv
                try:
                    mkv = pymkv.MKVFile(str(path_obj))
                    tags['pymkv_tracks'] = mkv.tracks
                except Exception as e:
                    log.error(f"pymkv error for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
            elif step_name == "tinytag" and tinytag_enabled and file_type in [".mp3", ".m4a", ".ogg", ".flac", ".wav", ".wma"]:
                from tinytag import TinyTag
                try:
                    tag = TinyTag.get(str(path_obj))
                    tags['tinytag_title'] = tag.title
                    tags['tinytag_artist'] = tag.artist
                    tags['tinytag_duration'] = tag.duration
                except Exception as e:
                    log.error(f"tinytag error for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
            elif step_name == "eyed3" and eyed3_enabled and file_type == ".mp3":
                import eyed3
                try:
                    audiofile = eyed3.load(str(path_obj))
                    if audiofile and audiofile.tag:
                        tags['eyed3_title'] = audiofile.tag.title
                        tags['eyed3_artist'] = audiofile.tag.artist
                        tags['eyed3_album'] = audiofile.tag.album
                        tags['eyed3_duration'] = audiofile.info.time_secs if audiofile.info else None
                except Exception as e:
                    log.error(f"eyed3 error for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
            elif step_name == "music_tag" and music_tag_enabled and file_type in [".mp3", ".flac", ".m4a", ".ogg", ".wav", ".wma"]:
                try:
                    import music_tag
                    f = music_tag.load_file(str(path_obj))
                    tags['music_tag_title'] = f['title'].value
                    tags['music_tag_artist'] = f['artist'].value
                    tags['music_tag_album'] = f['album'].value
                    tags['music_tag_duration'] = f['duration'].value
                except Exception as e:
                    log.error(f"music_tag error for '{filename}': {e}")
                parser_times[step_name] = time.time() - t0
            else:
                parser_times[step_name] = 0.0
        except Exception as e:
            log.error(f"{step_name} parser error for '{filename}': {e}")
            parser_times[step_name] = time.time() - t0

        # Update duration safely after each potential parser
        if 'duration' in tags and tags['duration'] and not duration:
            try:
                duration = int(tags['duration'])
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
    return duration, tags
