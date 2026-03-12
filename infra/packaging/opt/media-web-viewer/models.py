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
from parsers.format_utils import (
    PARSER_CONFIG, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS,
    DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS
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
        self.type = self.path.suffix.lower()

        # Debug mode is handled centrally through logger level
        parser_mode = PARSER_CONFIG.get("parser_mode", "lightweight")
        self.duration, self.tags = media_parser.extract_metadata(
            self.path,
            self.name,
            mode=parser_mode
        )
        self.category = self.get_category()

        # New separated metadata fields
        self.extension = self.type[1:] if self.type.startswith('.') else self.type
        self.media_type = "video" if self.type in VIDEO_EXTENSIONS else "audio"
        self.container = self.tags.get('container', self.extension)
        self.tag_type = self.tags.get('tagtype', 'plain')
        self.codec = self.tags.get('codec', self.extension)

    def get_category(self):
        """
        @brief Detects the category of the media item based on extension and metadata tags.
        @details Erkennt die Kategorie basierend auf Dateiendung und Metadaten-Tags.
        @return Category string (e.g., 'Album', 'Hörbuch', 'Film').
        """
        ext = self.type.lower()
        path_str = str(self.path).lower()
        tags = self.tags or {}

        # 1. Video / E-Book / Document (Non-Audio)
        if ext in VIDEO_EXTENSIONS:
            if any(k in path_str for k in ['serie', 'tv', 'season', 'staffel']):
                return 'Serie'
            return 'Film'
        if ext in EBOOK_EXTENSIONS:
            return 'E-Book'
        if ext in DOCUMENT_EXTENSIONS:
            return 'Dokument'

        # 2. Audio Parser Logic
        if ext in AUDIO_EXTENSIONS or ext == '.m4b':
            # Priority 1: Hörbuch (m4b extension or keyword in path/genre)
            genre = tags.get('genre', '').lower()
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
            'has_art', 'container', 'tagtype', '_parser_times', 'releasetype', 'compilation'
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
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format
        }
