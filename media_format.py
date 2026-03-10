"""
MediaFormat - Definition und Standardisierung von Dateiformaten

Dieses Modul stellt die zentrale Klasse und Hilfsfunktionen zur Verfügung, um das Dateiformat für alle Medientypen (Audio, Video, ISO, Dokumente, E-Books) und Spezialfälle wie PAL DVD oder Blu-ray zu definieren und zu standardisieren.
"""

from pathlib import Path
from typing import Any

from parsers.format_utils import (
    AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, EBOOK_EXTENSIONS, DOCUMENT_EXTENSIONS, IMAGE_EXTENSIONS
)

class MediaFormat:
    """
    @brief Repräsentiert das Dateiformat eines Mediums.
    @details Stellt Typ, Format und ggf. Content (z.B. PAL DVD) bereit.
    """
    def __init__(self, path: Path, tags: dict[str, Any] = None):
        self.path = path
        self.tags = tags or {}
        self.extension = path.suffix.lower()
        self.type = self.detect_type()
        self.format = self.detect_format()
        self.content = self.detect_content()

    def detect_type(self) -> str:
        ext = self.extension
        if ext == '.iso':
            return 'ISO/Image'
        if ext in VIDEO_EXTENSIONS:
            return 'Video'
        if ext in AUDIO_EXTENSIONS:
            return 'Audio'
        if ext == '.m4b' or any(k in str(self.path).lower() for k in ['h\u00f6rbuch', 'hörbuch', 'audiobook']):
            return 'Hörbuch'
        if ext in IMAGE_EXTENSIONS:
            return 'Bilder'
        if ext in EBOOK_EXTENSIONS:
            return 'E-Book'
        if ext in DOCUMENT_EXTENSIONS:
            return 'Dokument'
        return 'Unbekannt'

    def detect_format(self) -> str:
        ext = self.extension
        if ext in AUDIO_EXTENSIONS:
            return ext[1:].upper()
        if ext in VIDEO_EXTENSIONS:
            return ext[1:].upper()
        if ext == '.iso':
            return 'ISO'
        if ext in EBOOK_EXTENSIONS:
            return ext[1:].upper()
        if ext in DOCUMENT_EXTENSIONS:
            return ext[1:].upper()
        return ext[1:].upper() if ext else 'UNKNOWN'

    def detect_content(self) -> str:
        ext = self.extension
        volume_id = self.tags.get('pycdlib_volume_id', '').lower() if self.tags else ''
        container = self.tags.get('container', '').lower() if self.tags else ''
        # ISO-basierte Medien
        if ext == '.iso':
            if 'pal' in volume_id:
                return 'PAL DVD'
            if 'ntsc' in volume_id:
                return 'NTSC DVD'
            if 'wmv' in volume_id or 'wmv' in container:
                return 'WMV DVD'
            if 'hd dvd' in volume_id or 'hddvd' in volume_id:
                return 'HD DVD'
            if 'blu' in volume_id or 'bd' in volume_id:
                return 'Blu-ray'
            if 'audio cd' in volume_id or 'cd' in volume_id:
                return 'Audio CD'
            if 'data' in volume_id or 'daten' in volume_id or 'data disc' in volume_id:
                return 'Daten-Disc'
            return 'ISO Image'
        # Audio-CD als Datei (z.B. .cue/.bin/.wav/.flac mit CD-Tags)
        if ext in {'.cue', '.bin', '.wav', '.flac'}:
            if 'audio cd' in volume_id or 'cd' in volume_id:
                return 'Audio CD'
        return ''

    def to_dict(self) -> dict[str, Any]:
        return {
            'type': self.type,
            'format': self.format,
            'content': self.content,
            'extension': self.extension
        }
