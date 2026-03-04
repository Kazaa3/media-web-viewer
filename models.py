from pathlib import Path
from parsers.format_utils import PARSER_CONFIG
from parsers import media_parser

class MediaItem:
    def __init__(self, name, path, debug_flags=None, logger=None):
        self.name = name
        self.path = Path(path)
        self.type = self.path.suffix.lower()
        
        # Default fallbacks if not provided
        self.debug_flags = debug_flags or {"parser": False}
        self.logger = logger or print
        
        parser_mode = PARSER_CONFIG.get("parser_mode", "lightweight")
        self.duration, self.tags = media_parser.extract_metadata(
            self.path, 
            self.name, 
            debug=self.debug_flags.get("parser", False), 
            mode=parser_mode, 
            logger=self.logger
        )

    def show_info(self):
        print(self.name)
        print(self.path)
        print(self.type)
        print(self.duration)
        print(self.tags)
        print("\n")

    def to_dict(self):
        hours, remainder = divmod(self.duration, 3600)
        mins, secs = divmod(remainder, 60)
        
        if hours > 0:
            duration_str = f"{hours}:{mins:02d}:{secs:02d}"
        else:
            duration_str = f"{mins}:{secs:02d}"
            
        codec = self.tags.get('codec', '').upper()
        # Lossless ALAC → transcode to FLAC
        is_alac = self.type == '.alac' or (self.type in {'.m4a', '.m4b'} and 'ALAC' in codec)
        # Lossy WMA → transcode to OGG (Opus)
        is_wma = self.type == '.wma'
        
        is_transcoded = is_alac or is_wma
        if is_alac:
            transcoded_format = 'FLAC'
        elif is_wma:
            transcoded_format = 'OGG'
        else:
            transcoded_format = None
        
        return {
            'name': self.name,
            'path': str(self.path),
            'duration': duration_str,
            'tags': self.tags,
            'type': self.type[1:] if self.type.startswith('.') else self.type,
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format
        }
