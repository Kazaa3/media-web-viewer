from pathlib import Path
from parsers.format_utils import PARSER_CONFIG, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS
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
        self.category = self.get_category()

    def get_category(self):
        """Detects the category of the media item based on extension and metadata tags."""
        ext = self.type.lower()
        path_str = str(self.path).lower()
        tags = self.tags or {}
        
        # 1. Strict .m4b -> Hörbuch (as requested previously)
        if ext == '.m4b':
            return 'Hörbuch'
            
        # 2. Audio Parser Logic
        if ext in AUDIO_EXTENSIONS:
            artist = (tags.get('artist') or "").lower()
            album = (tags.get('album') or "").lower()

            # - Compilation: if VA / Various Artists (NOT just unknown)
            if any(k in artist for k in ['va', 'various artists', 'various']):
                return 'Compilation'
            
            # - Single: if album tag not filled OR "single" in string (album title)
            if not album or 'single' in album:
                return 'Single'
            
            # - Album: if album tag filled
            if album:
                return 'Album'

            # Fallback detection for Audiobook (Hörbuch) from path/genre
            genre = tags.get('genre', '').lower()
            if any(k in path_str for k in ['hörbuch', 'hörbücher', 'audiobook', 'audiobooks']) or 'audiobook' in genre or 'hörbuch' in genre:
                return 'Hörbuch'
                
            return 'Audio'

        # 3. Non-Audio fallbacks (Videos, E-Books, Docs)
        elif ext in VIDEO_EXTENSIONS:
            if 'serie' in path_str or 'tv' in path_str or 'season' in path_str:
                return 'Serie'
            return 'Film'
        elif ext in EBOOK_EXTENSIONS:
            return 'E-Book'
        elif ext in DOCUMENT_EXTENSIONS:
            return 'Dokument'
        
        return 'Unbekannt'

    def show_info(self):
        print(self.name)
        print(str(self.path))
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
        
        # Filter tags: Only keep what's strictly necessary for the UI/Database to save space
        whitelist = {
            'title', 'artist', 'album', 'year', 'genre', 'track', 'totaltracks',
            'disc', 'codec', 'bitdepth', 'samplerate', 'bitrate', 'size',
            'has_art', 'container', 'tagtype', '_parser_times', 'releasetype', 'compilation'
        }
        filtered_tags = {k: v for k, v in self.tags.items() if k in whitelist}
        
        return {
            'name': self.name,
            'path': str(self.path),
            'duration': duration_str,
            'tags': filtered_tags,
            'type': self.type[1:] if self.type.startswith('.') else self.type,
            'category': self.category,
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format
        }
