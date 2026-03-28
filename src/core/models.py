#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Data Models

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from pathlib import Path
from typing import Optional, Any

try:
    from src.parsers.format_utils import (
        PARSER_CONFIG, SLOW_PARSERS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS,
        DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, IMAGE_EXTENSIONS,
        DISK_IMAGE_EXTENSIONS
    )
    from src.parsers import media_parser
    from src.core import logger
except ImportError:
    # Fallback for environments where src is in PYTHONPATH
    from parsers.format_utils import (
        PARSER_CONFIG, SLOW_PARSERS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS,
        DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, IMAGE_EXTENSIONS,
        DISK_IMAGE_EXTENSIONS
    )
    from parsers import media_parser
    import logger
import re

# Get specialized logger for models
log = logger.get_logger("models")

# In General & Debug:
# Comments are stored as dictionaries and imported as JSON.
# dict (JSON missing like in a few versions before)


class MediaItem:
    """
    @brief Represents a single media file with comprehensive metadata.
    @details Repräsentiert eine einzelne Mediendatei mit umfassenden Metadaten.
    """

    def __init__(self, name, path, is_mock=False):
        """
        @brief Initializes a MediaItem and triggers metadata extraction.
        @details Initialisiert ein MediaItem und startet die Metadaten-Extraktion.
        @param name File basename / Basis-Dateiname.
        @param path Absolute filesystem path / Absoluter Dateipfad.
        """
        self.name = name
        self.path = Path(path)
        self.is_directory = self.path.is_dir()
        if self.is_directory:
            self.type = 'Folder'
        else:
            self.type = self.path.suffix.lower()

        self.is_mock = is_mock
        # Debug mode is handled centrally through logger level
        parser_mode = PARSER_CONFIG.get("parser_mode", "lightweight")
        # extract_metadata historically returned (duration, tags) but some
        # compatibility changes return (tags, parser_times) or a dict of tags.
        _meta = media_parser.extract_metadata(self.path, self.name, mode=parser_mode)
        self.duration = 0
        self.tags = {}
        # Normalize possible return shapes
        if isinstance(_meta, tuple):
            if len(_meta) == 2:
                a, b = _meta
                if isinstance(a, (int, float)):
                    self.duration = int(a)
                    self.tags = b or {}
                elif isinstance(a, dict):
                    # (tags, parser_times)
                    self.tags = a or {}
                    if isinstance(b, dict):
                        self.tags['_parser_times'] = b
                        self.duration = int(b.get('duration', a.get('duration', 0)) or 0)
                    elif isinstance(b, (int, float)):
                        self.duration = int(b)
                    elif isinstance(b, dict):
                        self.duration = int(b.get('duration', 0) or 0)
                else:
                    # Fallback: try interpreting b as tags/duration
                    if isinstance(b, (int, float)):
                        self.duration = int(b)
                    elif isinstance(b, dict):
                        self.tags = b
        elif isinstance(_meta, dict):
            # older parser returns tags dict only
            self.tags = _meta
            self.duration = int(self.tags.get('duration', 0) or 0)
        else:
            # unknown shape — leave defaults
            pass
        self.category = self.get_category()

        # Logical separation: type, format, content
        from parsers.format_utils import detect_file_format
        self.logical_type = self.detect_logical_type()
        self.file_format = detect_file_format(self.path, self.tags)
        self.content_type = self.detect_content_type()
        
        from src.parsers.format_utils import is_playable
        tags_with_path = (self.tags or {}).copy()
        tags_with_path['path'] = str(self.path)
        self.is_playable = is_playable(self.file_format, tags_with_path)

        # Extract artwork if enabled
        self.art_path = self.extract_artwork()
        self.has_artwork = self.art_path is not None
        self.is_missing_cover = not self.has_artwork

        # New separated metadata fields
        # Normalize extension to lowercase without leading dot (tests expect 'mp3', not '.MP3' or 'MP3')
        ext = (self.file_format or '')
        if isinstance(ext, str):
            ext = ext.lstrip('.').lower()
        self.extension = ext

        # --- v2.5: Item/Object Split & Remote IDs ---
        self.media_type = 'container' if self.is_directory else 'file'
        
        # Mapping which media_type tokens are stable (backward compat with old media_type mapping)
        lt = (self.logical_type or '')
        lt_mapping = {
            'video': 'video', 'Video': 'video',
            'Audio': 'audio', 'audio': 'audio', 'Hörbuch': 'audio', 'Album': 'audio', 
            'Klassik': 'audio', 'Podcast': 'audio', 'Soundtrack': 'audio',
            'Compilation': 'audio', 'Single': 'audio', 'Playlist': 'playlist',
            'Bilder': 'image', 'E-Book': 'ebook', 'Dokument': 'document', 'Abbild': 'disk',
            'Ordner': 'folder', 'Serie': 'video', 'Film': 'video', 'Unbekannt': 'unknown'
        }
        self.type_token = lt_mapping.get(lt, str(lt).lower())
        
        # Subtype (for containers) and FileType (for files)
        self.category = self.get_category()
        if self.media_type == 'container':
             self.subtype = self.category.lower().replace(' ', '_')
             self.file_type = None
        else:
             self.subtype = None
             self.file_type = f"{self.type_token.lower()}-file"
             if self.category == 'Hörbuch' and self.extension == 'm4b':
                 self.file_type = 'hoerbuch-m4b'

        # Remote IDs from tags
        self.isbn = self.tags.get('isbn')
        self.imdb = self.tags.get('imdb')
        self.tmdb = self.tags.get('tmdb')
        self.discogs = self.tags.get('discogs')
        self.amazon_cover = self.tags.get('amazon_cover')
        self.parent_id = self.tags.get('parent_id')

        self.container = self.tags.get('container', self.extension)
        self.tag_type = self.tags.get('tagtype', 'plain')
        self.codec = self.tags.get('codec', self.extension)

    def detect_logical_type(self):
        ext = self.type.lower()
        if ext in DISK_IMAGE_EXTENSIONS or ext in ['.bin', '.img']:
            return 'Abbild'
        if self.type == 'Folder':
            # Check if it contains media indicators
            p_str = str(self.path).lower()
            if (self.path / 'VIDEO_TS').exists() or (self.path / 'BDMV').exists():
                return 'Film' # Direct film object if it's a DVD/BD folder
            if any(self.path.glob('*.iso')) or any(self.path.glob('*.bin')):
                return 'Film' # Folder containing disc images is often a Film Object
            return 'Ordner'
        if ext in VIDEO_EXTENSIONS:
            return 'Video'
        if ext in AUDIO_EXTENSIONS:
            return 'Audio'
        if ext in IMAGE_EXTENSIONS:
            return 'Bilder'
        if ext in EBOOK_EXTENSIONS:
            return 'E-Book'
        if ext in DOCUMENT_EXTENSIONS:
            return 'Dokument'
        return 'Unbekannt'

    def detect_content_type(self):
        ext = self.type.lower()
        path_str = str(self.path).lower()
        tags = self.tags or {}
        
        # 1. DVD / Disk Image Objects
        is_disc = ext in ('.iso', '.bin', '.img') or (self.is_directory and (self.path / "VIDEO_TS").exists())
        
        if is_disc:
            vol_id = str(tags.get('pycdlib_volume_id', tags.get('iso_volume_label', ''))).lower()
            if 'pal' in vol_id or 'dvd' in vol_id:
                return 'PAL DVD'
            if 'ntsc' in vol_id:
                return 'NTSC DVD'
            # Check file counts for Data vs Video DVD
            try:
                files_count = int(tags.get('iso_files_count', 0))
                if files_count > 50: return 'Data DVD'
                if files_count > 0: return 'Mixed Media'
            except: pass
            return 'DVD Object'
            
        # 2. Film Object Detection (Folders with metadata or specific structure)
        if self.is_directory:
            # Check for year in folder name or tags
            has_year = 'year' in tags or re.search(r'(19|20)\d{2}', self.path.name)
            if has_year and any(self.path.glob('*.[mmap][kpk4][v4i]')): # simple check for video files
                return 'Film Object'
                
        return self.category

    def get_category(self):
        """
        @brief Detects the category of the media item based on extension and metadata tags.
        @details Erkennt die Kategorie basierend auf Dateiendung und Metadaten-Tags.
        @return Category string (e.g., 'Album', 'Hörbuch', 'Film').
        """
        ext = self.type.lower()
        path_str = str(self.path).lower()
        tags = self.tags or {}
        logical = self.detect_logical_type()

        # 1. Folders / Video / DVD / ISO
        if logical == 'Ordner' or logical == 'Film':
            # Sub-classification for folders
            if any(k in path_str for k in ['serie', 'tv', 'season', 'staffel']) or tags.get('is_series'):
                return 'Serie'
            
            # DVD Folder detection (VIDEO_TS / BDMV)
            if (self.path / 'VIDEO_TS').exists() or (self.path / 'BDMV').exists():
                 return 'Film'
                 
            # Folder with ISOs / Images
            disk_pat = ('*.iso', '*.bin', '*.img')
            if any(any(self.path.glob(p)) for p in disk_pat):
                return 'Film'

            if any(k in path_str for k in ['film', 'movie']):
                return 'Film'
                
            # Detect Year in Folder -> likely a Movie folder
            if re.search(r'[\(\[\s]((?:19|20)\d{2})[\)\]\s]?', self.path.name):
                return 'Film'
                
            return 'Ordner'

        # 2. Audio-based Sub-Categorization
        if logical == 'Audio':
            genre = str(tags.get('genre') or '').lower()
            if any(k in genre for k in ['klassik', 'classical', 'opera']):
                return 'Klassik'
            if any(k in path_str for k in ['podcast']):
                return 'Podcast'
            if 'compilation' in tags:
                 return 'Compilation'
                 
            # Single check: If it's a folder-object and contains < 3 files
            if self.is_directory:
                tracks = [f for f in self.path.glob('*') if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS]
                if 0 < len(tracks) < 3:
                     return 'Single'
            else:
                # If it's a file but name contains 'Single' or similar
                if 'single' in self.path.name.lower():
                     return 'Single'

        # 3. Book detection (ISBN)
        if tags.get('isbn') or logical == 'E-Book':
            return 'Buch'

        if logical == 'Video':
            if any(k in path_str for k in ['serie', 'tv', 'season', 'staffel', 'erie']) or tags.get('is_series'):
                return 'Serie'
            return 'Film'
        
        if logical == 'Abbild':
            # Use content_type from format_utils if available via metadata
            from parsers.format_utils import detect_file_format
            fmt = detect_file_format(self.path, tags)
            if 'DVD' in fmt or 'Blu-ray' in fmt:
                return 'Film'
            if 'SACD' in fmt or 'Audio-CD' in fmt:
                return 'Album'
            
            # Specialized detection for PC Games and Book Discs
            vol_id = str(tags.get('pycdlib_volume_id', tags.get('iso_volume_label', ''))).upper()
            if any(k in vol_id for k in ['DVD', 'PAL', 'NTSC', 'VTS']):
                 return 'Film'
                 
            if any(k in vol_id for k in ['S3GOLD', 'GAME', 'PLAY', 'SPIEL', 'SIMS']):
                return 'Spiel'
            
            if any(k in path_str for k in ['spiel', 'game', 'software']):
                 return 'Spiel'
                 
            if any(k in path_str for k in ['buch', 'book', 'beigabe']):
                return 'Beigabe'
                
            if any(k in path_str for k in ['film', 'movie']) or ext in ('.iso', '.img', '.bin'):
                 return 'Film'
            return 'Abbild'

        if ext in EBOOK_EXTENSIONS:
            return 'E-Book'
        if ext in DOCUMENT_EXTENSIONS:
            return 'Dokument'
        if ext in IMAGE_EXTENSIONS:
            return 'Bilder'
        
        # New: Playlists
        if ext in ('.m3u', '.m3u8', '.pls'):
            return 'Playlist'

        # 2. Audio Parser Logic
        if ext in AUDIO_EXTENSIONS or ext == '.m4b':
            # Priority 1: Hörbuch (m4b extension or keyword in path/genre)
            genre = str(tags.get('genre') or '').lower()
            album = str(tags.get('album') or '').lower()
            artist = str(tags.get('artist') or '').lower()
            path_str = str(self.path).lower()
            if ext == '.m4b' or any(
                k in path_str for k in [
                    'hörbuch',
                    'hörbücher',
                    'audiobook',
                    'audiobooks']) or 'audiobook' in genre or 'hörbuch' in genre:
                return 'Hörbuch'

            if 'podcast' in path_str or 'podcast' in genre:
                return 'Podcast'

            # Priority 2: Music specific tags
            artist = str(tags.get('artist') or "").lower()
            album = str(tags.get('album') or "").lower()

            # Priority 3: Klassik
            if any(k in genre for k in ['klassik', 'classical', 'klaqssik']) or \
               any(k in artist for k in ['beethoven', 'mozart', 'bach', 'chopin', 'klassik', 'classical']) or \
               any(k in path_str for k in ['klassik', 'classical', 'klaqssik']):
                return 'Klassik'

            # Priority 4: Soundtrack
            if any(k in path_str for k in ['ost', 'soundtrack', 'o.s.t']) or \
               any(k in album for k in ['ost', 'soundtrack', 'original motion picture']):
                return 'Soundtrack'

            # Priority 5: Compilations / Albums / Singles
            if any(k in artist for k in ['va', 'various artists', 'various', 'compilation']):
                return 'Compilation'

            if album:
                if 'single' in album:
                    return 'Single'
                return 'Album'

            # Fallback: Folder-based logic for Albums
            if tags.get('album'):
                return 'Album'

            return 'Audio'

        return 'Unbekannt'

    def extract_artwork(self) -> Optional[str]:
        """
        @brief Extracts embedded artwork (cover) from media files.
        @details Extrahiert eingebettete Cover-Bilder.
        @return Path to the extracted image or None.
        """
        from src.parsers.artwork_extractor import extractor
        logical = getattr(self, 'logical_type', 'Unbekannt')
        return extractor.extract(self.path, self.tags, logical)

    def show_info(self):
        """
        @brief Logs the media item information.
        @details Schreibt die Medien-Informationen in das Log.
        """
        info_dict = self.to_dict()
        log.info(f"MediaItem Info: {info_dict['name']} | Path: {info_dict['path']} | Category: {info_dict['category']}")
        log.debug(f"Full Tags for {info_dict['name']}: {info_dict['tags']}")

    def to_dict(self):
        """
        @brief Converts the MediaItem into a dictionary for UI and Database.
        @details Konvertiert das MediaItem in ein Dictionary für UI und Datenbank.
        @return A dictionary containing all serialized metadata / Ein Dictionary mit allen Metadaten.
        """
        hours, remainder = divmod(self.duration, 3600)
        mins, secs = divmod(remainder, 60)

        if hours > 0:
            duration_str = f"{hours}:{mins:02d}:{secs:02d}"
        else:
            duration_str = f"{mins}:{secs:02d}"

        codec = str(self.tags.get('codec') or '').upper()
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
            
        # Is Chrome Native?
        from src.parsers.format_utils import is_chrome_native
        chrome_native = is_chrome_native(self.type, codec)

        # Filter tags: Only keep what's strictly necessary for the UI/Database to save space
        whitelist = {
            'title', 'artist', 'album', 'year', 'genre', 'track', 'totaltracks',
            'disc', 'codec', 'bitdepth', 'samplerate', 'bitrate', 'size',
            'has_art', 'container', 'tagtype', '_parser_times', 'releasetype', 'compilation',
            'resolution', 'width', 'height', 'fps', 'video_codec', 'audio_track_count',
            'subtitle_count', 'subtitle_languages', 'language', 'standard', 'frame_rate',
            'video_scan_type', 'video_chroma', 'video_color_space', 'video_hdr',
            'video_bit_depth', 'video_matrix', 'chapters'
        }
        filtered_tags = {k: v for k, v in self.tags.items() if k in whitelist}

        return {
            'name': self.name,
            'path': str(self.path),
            'duration': duration_str,
            'tags': filtered_tags,
            'type': self.media_type,
            'extension': self.extension,
            'container': self.container,
            'tag_type': self.tag_type,
            'codec': self.codec,
            'category': self.category,
            'logical_type': self.logical_type,
            'file_format': self.file_format,
            'content_type': self.content_type,
            'is_artwork_missing': self.is_missing_cover,
            'is_playable': self.is_playable,
            'is_directory': self.is_directory,
            'art_path': self.art_path,
            'artwork': self.art_path, # Alias for frontend
            'has_artwork': self.has_artwork,
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format,
            'is_chrome_native': chrome_native,
            'year': filtered_tags.get('year', ''),
            'film_title': filtered_tags.get('title', self.name),
            'media_type': self.media_type,
            'subtype': self.subtype,
            'file_type': self.file_type,
            'isbn': self.isbn,
            'imdb': self.imdb,
            'tmdb': self.tmdb,
            'discogs': self.discogs,
            'amazon_cover': self.amazon_cover,
            'parent_id': self.parent_id,
            'is_mock': self.is_mock
        }
