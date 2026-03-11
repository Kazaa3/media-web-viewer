#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Data Models

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
from parsers.format_utils import (
    PARSER_CONFIG, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS,
    DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, IMAGE_EXTENSIONS,
    DISK_IMAGE_EXTENSIONS
)
from parsers import media_parser
import logger

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

    def __init__(self, name, path):
        """
        @brief Initializes a MediaItem and triggers metadata extraction.
        @details Initialisiert ein MediaItem und startet die Metadaten-Extraktion.
        @param name File basename / Basis-Dateiname.
        @param path Absolute filesystem path / Absoluter Dateipfad.
        """
        self.name = name
        self.path = Path(path)
        if self.path.is_dir():
            self.type = 'Folder'
        else:
            self.type = self.path.suffix.lower()

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
                    # try to extract duration from parser_times or b
                    if isinstance(b, (int, float)):
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

        # Normalize media_type to a stable, lowercase token for tests and UI
        lt = (self.logical_type or '')
        mapping = {
            'video': 'video', 'Video': 'video',
            'Audio': 'audio', 'audio': 'audio', 'Hörbuch': 'audio', 'Album': 'audio', 'Klassik': 'audio',
            'Bilder': 'image', 'E-Book': 'ebook', 'Dokument': 'document', 'Abbild': 'disk',
            'Ordner': 'folder', 'Serie': 'video', 'Film': 'video', 'Unbekannt': 'unknown'
        }
        self.media_type = mapping.get(lt, str(lt).lower())
        self.container = self.tags.get('container', self.extension)
        self.tag_type = self.tags.get('tagtype', 'plain')
        self.codec = self.tags.get('codec', self.extension)

    def detect_logical_type(self):
        ext = self.type.lower()
        if ext in DISK_IMAGE_EXTENSIONS:
            return 'Abbild'
        if self.type == 'Folder':
            # Check if it contains media indicators
            if (self.path / 'VIDEO_TS').exists() or (self.path / 'BDMV').exists():
                return 'Ordner' # Categorized as folder, but content will be 'Film'
            if any(self.path.glob('*.iso')):
                return 'Ordner'
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
        tags = self.tags or {}
        # ISO / Disk Image: try to detect PAL DVD
        if ext in DISK_IMAGE_EXTENSIONS:
            volume_id = tags.get('pycdlib_volume_id', '').lower()
            if 'pal' in volume_id or 'dvd' in volume_id:
                return 'PAL DVD'
            return 'Disk Image'
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
        if logical == 'Ordner':
            # Sub-classification for folders
            if any(k in path_str for k in ['serie', 'tv', 'season', 'staffel']):
                return 'Serie'
            if (self.path / 'VIDEO_TS').exists() or (self.path / 'BDMV').exists() or any(self.path.glob('*.iso')):
                return 'Film'
            return 'Ordner'

        if logical == 'Video':
            if any(k in path_str for k in ['serie', 'tv', 'season', 'staffel']):
                return 'Serie'
            return 'Film'
        
        if logical == 'Abbild':
            # Use content_type from format_utils if available via metadata
            from parsers.format_utils import detect_file_format
            fmt = detect_file_format(self.path, tags)
            if 'DVD' in fmt or 'Blu-ray' in fmt:
                return fmt
            if 'SACD' in fmt or 'Audio-CD' in fmt:
                return 'Album'
            
            # Specialized detection for PC Games and Book Discs
            vol_id = tags.get('pycdlib_volume_id', '').upper()
            if any(k in vol_id for k in ['S3GOLD', 'GAME', 'PLAY', 'SPIEL', 'SIMS']):
                return 'Spiel'
            
            path_lower = str(self.path).lower()
            if any(k in path_lower for k in ['spiel', 'game', 'software']):
                 return 'Spiel'
                 
            if any(k in path_lower for k in ['buch', 'book', 'beigabe']):
                return 'Beigabe'
                
            return 'Abbild'

        if ext in EBOOK_EXTENSIONS:
            return 'E-Book'
        if ext in DOCUMENT_EXTENSIONS:
            return 'Dokument'
        if ext in IMAGE_EXTENSIONS:
            return 'Bilder'

        # 2. Audio Parser Logic
        if ext in AUDIO_EXTENSIONS or ext == '.m4b':
            # Priority 1: Hörbuch (m4b extension or keyword in path/genre)
            genre = (tags.get('genre') or '').lower()
            album = (tags.get('album') or '').lower()
            artist = (tags.get('artist') or '').lower()
            if ext == '.m4b' or any(
                k in path_str for k in [
                    'hörbuch',
                    'hörbücher',
                    'audiobook',
                    'audiobooks']) or 'audiobook' in genre or 'hörbuch' in genre:
                return 'Hörbuch'

            # Priority 2: Music specific tags
            artist = (tags.get('artist') or "").lower()
            album = (tags.get('album') or "").lower()

            # Priority 3: Klassik
            if any(k in genre for k in ['klassik', 'classical']) or \
               any(k in artist for k in ['beethoven', 'mozart', 'bach', 'chopin', 'klassik', 'classical']) or \
               any(k in path_str for k in ['klassik', 'classical']):
                return 'Klassik'

            # Priority 4: Compilations / Albums / Singles
            if any(k in artist for k in ['va', 'various artists', 'various', 'compilation']):
                return 'Compilation'

            if album:
                if 'single' in album:
                    return 'Single'
                return 'Album'

            return 'Audio'

        return 'Unbekannt'

    def extract_artwork(self) -> Optional[str]:
        """
        @brief Extracts embedded artwork (cover) from media files.
        @details Extrahiert eingebettete Cover-Bilder.
        @return Path to the extracted image or None.
        """
        from parsers.artwork_extractor import extractor
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
            'has_art', 'container', 'tagtype', '_parser_times', 'releasetype', 'compilation',
            'resolution', 'width', 'height', 'fps', 'video_codec', 'audio_track_count',
            'subtitle_count', 'subtitle_languages', 'language'
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
            'art_path': self.art_path,
            'has_artwork': self.has_artwork,
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format
        }
