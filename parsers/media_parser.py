import time
from pathlib import Path
from . import filename_parser
from . import mutagen_parser
from . import pymediainfo_parser
from . import ffmpeg_parser
from . import container_parser

def extract_metadata(path, filename, debug=False, mode='lightweight', logger=print):
    """
    @brief Orchestrates the metadata extraction process using a sequential parser chain.
    @details Orchestriert den Metadaten-Extraktionsprozess über eine sequentielle Parser-Kette.
    @param path Path to the media file / Pfad zur Mediendatei.
    @param filename Original filename for fallback parsing / Originaldateiname für Fallback-Parsing.
    @param debug Enable verbose logging / Aktiviere ausführliches Logging.
    @param mode Extraction mode ('lightweight' or 'full') / Extraktionsmodus ('lightweight' oder 'full').
    @param logger Logger function / Logging-Funktion.
    @return Tuple (duration, tags) / Tupel (Dauer, Tags).
    """
    if debug:
        logger(f"[Debug-Parser] Starte Parsing für '{filename}' (Mode: {mode})")
    if debug and mode == 'full':
        logger(f"[Debug-Parser] 🚀 Full Mode aktiviert für '{filename}' – sammle ALLE Tags!")
        
    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from .format_utils import PARSER_CONFIG, format_bitdepth, format_codec, format_container, format_tagtype
    
    tags = {}
    if mode == 'full':
        tags['full_tags'] = {}
        
    duration = 0
    parser_times = {}
    
    # Iterate dynamically through the user-configured parser chain
    parser_chain = PARSER_CONFIG.get("parser_chain", ["filename", "container", "mutagen", "pymediainfo", "ffmpeg"])
    
    for parser_name in parser_chain:
        # If in lightweight mode, check if we still need critical information, otherwise skip heavy parsers.
        # In full mode, we want ALL information from EVERY parser, so needs_more_info is always True.
        needs_more_info = True if mode == 'full' else (
            not tags.get('samplerate') or 
            not tags.get('bitrate') or 
            not tags.get('bitdepth') or
            not tags.get('codec') or
            tags.get('codec') == file_type[1:].lower() or
            not tags.get('container') or
            not duration or
            (file_type in ['.m4b', '.mkv', '.m4a', '.mp4'] and not tags.get('chapters'))
        )
        
        if parser_name == "filename":
            t0 = time.time()
            tags = filename_parser.parse(path_obj, filename, tags=tags, mode=mode)
            parser_times["filename"] = time.time() - t0
            
        elif parser_name == "container":
            if needs_more_info:
                t0 = time.time()
                tags = container_parser.parse(path_obj, file_type, tags, mode=mode)
                
                # Fallback block mostly handled inside ffmpeg, but isolated here for config flexibility
                if not tags.get('container'):
                     tags['container'] = file_type[1:].lower()
                     if not tags.get('codec'):
                         tags['codec'] = file_type[1:].lower()
                parser_times["container"] = time.time() - t0
            else:
                parser_times["container"] = 0.0
                
        elif parser_name == "mutagen":
            t0 = time.time()
            tags = mutagen_parser.parse(path_obj, file_type, tags, filename, mode=mode)
            parser_times["mutagen"] = time.time() - t0
            
        elif parser_name == "pymediainfo":
            if needs_more_info:
                t0 = time.time()
                tags = pymediainfo_parser.parse(path_obj, file_type, tags, mode=mode)
                parser_times["pymediainfo"] = time.time() - t0
            else:
                parser_times["pymediainfo"] = 0.0
            
        elif parser_name == "ffmpeg":
            if needs_more_info:
                t0 = time.time()
                tags = ffmpeg_parser.parse(path_obj, file_type, tags, mode=mode)
                parser_times["ffmpeg"] = time.time() - t0
            else:
                parser_times["ffmpeg"] = 0.0

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
        # Priority: 1. Natural Title, 2. Start Time
        tags['chapters'] = sorted(tags['chapters'], key=lambda x: (natural_sort_key(x.get('title', '')), x.get('start', 0.0)))
        if logger and debug:
            first_chaps = [c.get('title') for c in tags['chapters'][:5]]
            logger(f"[Parser] Sorted {len(tags['chapters'])} chapters. First 5: {first_chaps}")

    tags['_parser_times'] = parser_times
            
    return duration, tags
