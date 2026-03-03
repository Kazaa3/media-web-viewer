import time
from pathlib import Path
from . import filename_parser
from . import mutagen_parser
from . import pymediainfo_parser
from . import ffmpeg_parser

def extract_metadata(path, filename, debug=False):
    """
    Zentraler Parser, der Redundanzen vermeidet und FFmpeg-Subprozesse
    für die Indexierung überflüssig macht.
    """
    if debug:
        print(f"[Debug-Parser] Starte Parsing für: {filename}")
        
    path_obj = Path(path)
    file_type = path_obj.suffix.lower()
    from .format_utils import PARSER_CONFIG, format_bitdepth
    
    tags = {}
    duration = 0
    
    # Iterate dynamically through the user-configured parser chain
    parser_chain = PARSER_CONFIG.get("parser_chain", ["filename", "mutagen", "pymediainfo", "ffmpeg", "container"])
    
    for parser_name in parser_chain:
        # Check if we still need critical information, otherwise skip heavy parsers
        needs_more_info = (
            not tags.get('samplerate') or 
            not tags.get('bitrate') or 
            not tags.get('bitdepth') or
            not tags.get('codec') or
            not duration
        )
        
        if parser_name == "filename":
            tags = filename_parser.parse(path_obj, filename, tags=tags)
            
        elif parser_name == "mutagen":
            tags = mutagen_parser.parse(path_obj, file_type, tags, filename)
            
        elif parser_name == "pymediainfo" and needs_more_info:
            tags = pymediainfo_parser.parse(path_obj, file_type, tags)
            
        elif parser_name == "ffmpeg" and needs_more_info:
            tags = ffmpeg_parser.parse(path_obj, file_type, tags)
            
        elif parser_name == "container" and needs_more_info:
            # Fallback block mostly handled inside ffmpeg, but isolated here for config flexibility
            if not tags.get('container'):
                 tags['container'] = file_type[1:].lower()
                 if not tags.get('codec'):
                     tags['codec'] = file_type[1:].lower()

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
            
    return duration, tags
