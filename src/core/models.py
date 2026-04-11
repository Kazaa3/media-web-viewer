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
from typing import Optional, Any, Dict
from src.parsers import media_parser
from src.core import logger
from src.core.config_master import (
    GLOBAL_CONFIG, AUDIO_NATIVE, AUDIO_TRANSCODE, ALL_AUDIO_EXTENSIONS,
    VIDEO_NATIVE, VIDEO_HD_TRANSCODE, VIDEO_PAL_TRANSCODE, VIDEO_NTSC_TRANSCODE,
    ALL_VIDEO_EXTENSIONS, PICTURE_EXTENSIONS, DOCUMENT_EXTENSIONS,
    EBOOK_EXTENSIONS, DISK_IMAGE_EXTENSIONS, PLAYLIST_EXTENSIONS,
    ARCHIVE_EXTENSIONS
)

# These registries are the absolute source of truth for all media categorization.
# We enforce lowercase English keys internally (audio, multimedia, etc.).

EXTENSION_REGISTRY = {
    "audio": ALL_AUDIO_EXTENSIONS,
    "video": ALL_VIDEO_EXTENSIONS,
    "pictures": PICTURE_EXTENSIONS,
    "documents": DOCUMENT_EXTENSIONS | {".nfo"},
    "ebooks": EBOOK_EXTENSIONS,
    "disk_images": DISK_IMAGE_EXTENSIONS,
    "playlists": PLAYLIST_EXTENSIONS,
    "archives": ARCHIVE_EXTENSIONS,
    "nfo": {".nfo"}
}

MASTER_CAT_MAP = {
    "audio": {
        "internal": "audio",
        "aliases": ["audio", "musik", "music", "song", "radio"],
        "extensions": ALL_AUDIO_EXTENSIONS,
        "native": AUDIO_NATIVE,
        "transcode": AUDIO_TRANSCODE
    },
    "audio_native": {
        "internal": "audio_native",
        "aliases": ["audio native", "audio-native"],
        "extensions": AUDIO_NATIVE,
        "native": AUDIO_NATIVE
    },
    "audio_transcode": {
        "internal": "audio_transcode",
        "aliases": ["audio transcode", "audio-transcode", "alac", "wma"],
        "extensions": AUDIO_TRANSCODE,
        "transcode": AUDIO_TRANSCODE
    },
    "album": {
        "internal": "audio",
        "aliases": ["album", "lp", "cd"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "single": {
        "internal": "audio",
        "aliases": ["single", "ep", "maxi"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "hörbuch": {
        "internal": "audio",
        "aliases": ["hörbuch", "hörspiel", "audiobook"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "sampler": {
        "internal": "audio",
        "aliases": ["sampler", "mix", "compilation"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "compilation": {
        "internal": "audio",
        "aliases": ["compilation", "various artists", "va"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "podcast": {
        "internal": "audio",
        "aliases": ["podcast", "cast", "show"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "mix": {
        "internal": "audio",
        "aliases": ["mix", "mixtape", "set", "dj-set"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "soundtrack": {
        "internal": "audio",
        "aliases": ["soundtrack", "ost", "score"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "klassik": {
        "internal": "audio",
        "aliases": ["klassik", "classical", "opera"],
        "extensions": ALL_AUDIO_EXTENSIONS
    },
    "video": {
        "internal": "video",
        "aliases": ["multimedia", "video", "film", "movie", "tv"],
        "extensions": ALL_VIDEO_EXTENSIONS,
        "native": VIDEO_NATIVE,
        "transcode_hd": VIDEO_HD_TRANSCODE,
        "transcode_pal": VIDEO_PAL_TRANSCODE,
        "transcode_ntsc": VIDEO_NTSC_TRANSCODE
    },
    "video_iso": {
        "internal": "video_iso",
        "aliases": ["video iso", "video-iso", "iso-image", "dvd iso", "optical folder"],
        "extensions": DISK_IMAGE_EXTENSIONS,
        "transcode": DISK_IMAGE_EXTENSIONS
    },
    "series": {
        "internal": "video",
        "aliases": ["series", "serie", "tv-show", "staffel"],
        "extensions": ALL_VIDEO_EXTENSIONS
    },
    "documentation": {
        "internal": "video",
        "aliases": ["documentation", "dokumentation", "doku", "report"],
        "extensions": ALL_VIDEO_EXTENSIONS
    },
    "pictures": {
        "internal": "pictures",
        "aliases": ["bilder", "grafik", "foto", "images", "pictures"],
        "extensions": PICTURE_EXTENSIONS
    },
    "bilder": {  # Alias for global category map parity
        "internal": "pictures",
        "aliases": ["bilder"],
        "extensions": PICTURE_EXTENSIONS
    },
    "ebooks": {
        "internal": "ebooks",
        "aliases": ["e-book", "ebook", "epub", "mobi"],
        "extensions": EBOOK_EXTENSIONS
    },
    "epub": {  # Alias for global category map parity
        "internal": "ebooks",
        "aliases": ["epub"],
        "extensions": EBOOK_EXTENSIONS
    },
    "docs": {
        "internal": "documents",
        "aliases": ["dokumente", "docs", "pdf", "text"],
        "extensions": DOCUMENT_EXTENSIONS
    },
    "archives": {
        "internal": "archives",
        "aliases": ["archiv", "archives", "zip", "rar"],
        "extensions": ARCHIVE_EXTENSIONS
    },
    "nfo": {
        "internal": "nfo",
        "aliases": ["nfo", "info", "metadata"],
        "extensions": {".nfo"}
    }
}

# Calculated Logic Extensions (REDUNDANCY CLEANUP v1.37.07)
# (Constants now imported from config_master.py)

# --- Legacy Compatibility Aliases (v1.37.08) ---
# Restored for backward compatibility with main.py and format_utils.py
DSD_EXTENSIONS = AUDIO_TRANSCODE & {".dsf", ".dff", ".dsd"}
HDDVD_EXTENSIONS = {".evo", ".map", ".bup"}  # Subset of disk_images
# ALL_AUDIO_EXTENSIONS and ALL_VIDEO_EXTENSIONS are already defined above.

TECH_MARKERS = {
    "transcoded": ["_transcoded", ".mp4_transcoded"],
    "iso": [".iso", ".bin", ".cue", ".nrg"],
    "mock": ["is_mock"],
    "stage": ["stage", "recovery", "is_stage"]
}

# --- [v1.45.141] ARCHITECTURE BRIDGE ---
# Hardcoded BRANCH_MAP removed.
# Logistics now driven by 'branch_architecture_registry' in CONFIG_MASTER.

SLOW_PARSERS = {"isoparser", "pycdlib", "ebml", "mkvparse", "enzyme", "pymkv", "pymediainfo", "ffprobe", "ffmpeg"}

# --- ULTIMATE AUDITING LOGIC (v1.35.76) ---


def audit_category_chain(item: Dict) -> str:
    """Automated debugging helper for the category chain assignment (v1.37.07 SSOT)."""
    raw_cat = str(item.get('category', 'Unbekannt')).lower()
    name = item.get('name', 'unknown')

    matched_internal = None
    for internal_key, config in MASTER_CAT_MAP.items():
        if raw_cat == internal_key or raw_cat in config["aliases"]:
            matched_internal = internal_key
            break

    if matched_internal:
        return f"[AUDIT] Item '{name}' ({raw_cat}) -> CHAIN: Internal={matched_internal} -> OK"
    return f"[AUDIT] Item '{name}' ({raw_cat}) -> CHAIN: NO MATCH -> DROPPED"


# --- [v1.45.200] BRANCH IDENTITY & BUILD BRIDGE ---
# This map provides the architectural link between branch IDs and human labels.
# Restored as per user requirement to bridge fixed branches to build process.
BRANCH_MAP = {
    "audio": "BUILD: AUDIO ONLY",  # Legacy
    "multimedia": "BUILD: MULTIMEDIA",  # Current
    "extended": "BUILD: EXTENDED"  # Future
}


def get_branch_label(branch_id: str) -> str:
    """Resolves the professional display name for a branch."""
    reg = GLOBAL_CONFIG.get('branch_identity_registry', {})
    if branch_id in reg:
        return reg[branch_id].get('label', BRANCH_MAP.get(branch_id, branch_id.upper()))
    return BRANCH_MAP.get(branch_id, branch_id.upper())


def get_branch_build_id(branch_id: str) -> str:
    """Resolves the Build ID (e.g. MWV-A) for a branch."""
    reg = GLOBAL_CONFIG.get('branch_identity_registry', {})
    if branch_id in reg:
        return reg[branch_id].get('build_id', 'MWV-GENERIC')
    return "MWV-GENERIC"


def get_build_link(branch_id: str) -> str:
    """Generates the absolute build artifact link for a branch (v1.45.200)."""
    from src.core.config_master import APP_VERSION_CORE
    build_id = get_branch_build_id(branch_id)
    template = GLOBAL_CONFIG.get('build_configuration', {}).get('build_link_template', "")
    if template:
        return template.replace("{{BUILD_ID}}", build_id).replace("{{VERSION}}", APP_VERSION_CORE)
    return f"./dist/MediaWebViewer-{build_id}.exe"

# --- CATEGORY RECONCILIATION ---


def get_allowed_internal_cats(displayed_cats: list[str]) -> list[str]:
    """
    @brief Returns the flattened list of internal labels for the requested categories (v1.37.07 SSOT).
    Supports German aliases and cross-mappings.
    """
    allowed = set()
    # Explicit User-to-Internal Alias Table
    category_alias_table = {
        "musik": "audio", "music": "audio", "audio": "audio", "album": "audio",
        "single": "audio", "hörbuch": "audio", "sampler": "audio", "soundtrack": "audio",
        "video": "video", "film": "video", "movies": "video", "multimedia": "video",
        "video_iso": "video_iso", "iso-image": "video_iso",
        "bilder": "pictures", "fotos": "pictures", "pictures": "pictures", "bilder": "bilder",
        "dokumente": "documents", "docs": "documents", "documents": "documents", "dokumente": "docs",
        "disk_images": "disk_images", "isos": "disk_images",
        "ebooks": "ebooks", "bücher": "ebooks", "epub": "epub",
        "unknown": "unknown", "unbekannt": "unknown"
    }

    for dc in displayed_cats:
        raw_dc = dc.lower()

        # 0. Handle 'all' expansion (v1.41.00 Master Reset)
        if raw_dc == 'all':
            for key in MASTER_CAT_MAP:
                allowed.add(key)
                for alias in MASTER_CAT_MAP[key].get("aliases", []):
                    allowed.add(alias.lower())
            continue

        # 1. Resolve to canonical internal ID
        canonical = category_alias_table.get(raw_dc, raw_dc)

        # 2. Add the canonical ID itself
        allowed.add(canonical)

        # 3. Add all associated sub-labels (aliases) from the MASTER_CAT_MAP
        config = MASTER_CAT_MAP.get(canonical)
        if config:
            for alias in config["aliases"]:
                allowed.add(alias.lower())

    return list(allowed)

# --- PLAYBACK & COMPATIBILITY REGISTRY (v1.35.77 Consolidated) ---


PLAYABLE_KEYWORDS = [
    "dvd", "blu-ray", "vcd", "laserdisc", "sacd", "dsd", "cd-extra",
    "dvd-audio", "dvd-vr", "video cd", "super vcd", "high-res", "cd-rom",
    "dvd daten", "blu-ray daten"
]

PLAYABLE_EXTENSIONS = [
    ".mp4", ".mkv", ".avi", ".mp3", ".flac", ".wav", ".m4a", ".dsf", ".dff",
    ".ts", ".alac", ".aiff", ".mpeg", ".mpg", ".mov", ".webm", ".wmv",
    ".m4v", ".3gp", ".ogv", ".vob", ".m2ts", ".iso", ".bin", ".img"
]

NATIVE_EXTENSIONS = [".mp4", ".mkv", ".webm", ".ogv", ".mp3", ".wav", ".ogg", ".m4a", ".flac"]

NATIVE_CODECS = [
    "h264", "avc1", "vp8", "vp9", "av1", "aac", "mp4a", "mp3",
    "opus", "vorbis", "flac", "pcm"
]

LOSSY_EXTENSIONS = {'.mp3', '.ogg', '.aac', '.m4a', '.m4b', '.wma', '.opus'}

# Get specialized logger for models
log = logger.get_logger("models")


class MediaFormat:
    """
    @brief Unified engine for media format and type detection (v1.35.73 SSOT).
    @details Standardized logic driven by config_master registries.
    """

    def __init__(self, path: Path, tags: dict[str, Any] = None):
        self.path = path
        self.tags = tags or {}
        self.extension = path.suffix.lower()
        self.registry = EXTENSION_REGISTRY

        # Primary Identity
        self.type = self.detect_type()
        self.format = self.detect_format()
        self.content = self.detect_content()
        self.capability_stage = self.detect_capability_stage()

    def detect_capability_stage(self) -> str:
        """
        Determines the granular capability stage for architectural filtering (v1.45.130).
        """
        ext = self.extension
        if ext in AUDIO_NATIVE:
            return "audio_native"
        if ext in AUDIO_TRANSCODE:
            return "audio_transcode"
        if ext in VIDEO_NATIVE:
            return "video_native"
        if ext in VIDEO_HD_TRANSCODE:
            return "video_hd"
        if ext in VIDEO_PAL_TRANSCODE:
            return "video_pal"
        if ext in DISK_IMAGE_EXTENSIONS:
            return "video_iso"
        if ext in PICTURE_EXTENSIONS:
            return "bilder"
        if ext in EBOOK_EXTENSIONS:
            return "epub"
        return "unknown"

    def detect_type(self) -> str:
        ext = self.extension
        if ext in self.registry.get("disk_images", {}):
            return 'disk_images'
        if ext in self.registry.get("video", {}):
            return 'video'
        if ext in self.registry.get("audio", {}):
            # Special case: Audiobook detection
            if ext == '.m4b' or any(k in str(self.path).lower() for k in ['h\u00f6rbuch', 'hörbuch', 'audiobook']):
                return 'audiobook'
            # Special case: Sampler / Compilation detection
            if str(self.tags.get('compilation')).lower() in ('1', 'true', 'yes'):
                return 'sampler'
            return 'audio'
        if ext in self.registry.get("pictures", {}):
            return 'pictures'
        if ext in self.registry.get("ebooks", {}):
            return 'ebooks'
        if ext in self.registry.get("documents", {}):
            return 'documents'
        return 'unknown'

    def detect_format(self) -> str:
        """
        Calculates the specific media format (v1.35.81 Standardized).
        For disk images, it identifies the specialized optical standard.
        """
        ext = self.extension
        if not ext:
            return 'UNKNOWN'

        # Special Handling for Disk Images
        if self.type == 'disk_images':
            tags = self.tags
            def _tag(k): return str(tags.get(k, '') or '').lower()

            # 1. PC / Digital Games
            volume_id = _tag('pycdlib_volume_id')
            title = _tag('title')
            if 'win32' in volume_id or 'setup' in title or any(k in volume_id for k in ['spiel', 'game', 'software']):
                return 'PC Spiel'

            # 2. Specialized Optical Standards
            if _tag('pycdlib_is_dvd_audio') == 'true':
                return 'DVD Audio'
            if _tag('pycdlib_is_vcd') == 'true':
                return 'Video CD'
            if _tag('pycdlib_is_svcd') == 'true':
                return 'Super VCD'
            if _tag('pycdlib_is_cdi') == 'true':
                return 'CD-i'
            if _tag('pycdlib_is_cd_extra') == 'true':
                return 'CD-Extra'
            if _tag('pycdlib_is_hvdvd') == 'true' or 'hvdvd' in volume_id:
                return 'HD DVD'

            # 3. Standard Video Disks
            if _tag('pycdlib_is_bluray') == 'true' or any(k in volume_id for k in ['blu', 'bd', 'brd']):
                return 'Blu-ray'
            if _tag('pycdlib_is_dvd') == 'true' or 'dvd video' in _tag('container') or 'video_ts' in title:
                return 'DVD Video'

            # 4. Audio Specialized
            if any(k in volume_id for k in ['sacd', 'dsd']):
                return 'SACD'

            return 'ISO Image'

        # 5. Specialized Content-aware Labels (v1.35.81)
        # High-Res / HDR logic moved here from format_utils
        tags = self.tags
        def _tag(k): return str(tags.get(k, '') or '').lower()

        fmt_name = ext.upper().lstrip('.') or 'UNKNOWN'

        if self.type == 'audio':
            bits = _tag('audio_bit_depth')
            sr = _tag('audio_sample_rate')
            try:
                b = int(bits) if bits.isdigit() else 16
                import re
                s_match = re.search(r'\d+', sr)
                s = int(s_match.group()) if s_match else 44100
                if b > 16 or s > 48000:
                    from src.parsers.format_utils import format_samplerate
                    return f'High-Res {fmt_name} ({b}-bit/{format_samplerate(s)})'
            except (ValueError, AttributeError, ImportError):
                pass

        if self.type == 'video':
            hdr = _tag('video_hdr')
            scan = _tag('video_scan_type')
            bits = _tag('video_bit_depth')
            if hdr and hdr != 'none':
                return f'HDR {hdr.upper()} Video'
            if 'interlaced' in scan:
                return 'Interlaced Video'
            if '10 bit' in bits or '12 bit' in bits:
                return f'{bits} Deep Color'

        return fmt_name

    @property
    def is_playable(self) -> bool:
        """
        Determines if the format is considered playable (v1.35.82 SSOT).
        Excludes software, indexes, and unknown data formats.
        """
        # Exclusion priorities
        fmt_lower = self.format.lower()
        if any(k in fmt_lower for k in ['pc spiel', 'digitales spiel', '(index)']):
            return False

        # Extension-based whitelist from SSOT
        return self.extension in PLAYABLE_EXTENSIONS

    def detect_content(self) -> str:
        """
        Extracts secondary content markers (v1.35.81 Standardized).
        """
        ext = self.extension
        tags = self.tags
        def _tag(k): return str(tags.get(k, '') or '').lower()

        # Disk Specific Content
        if self.type == 'disk_images':
            standard = _tag('standard')
            volume_id = _tag('pycdlib_volume_id')
            if 'pal' in volume_id or 'pal' in standard:
                return 'Standard: PAL'
            if 'ntsc' in volume_id or 'ntsc' in standard:
                return 'Standard: NTSC'
            if _tag('pycdlib_is_dvd_vr') == 'true':
                return 'VR Mode'
            return ''

        return ''

    def to_dict(self) -> dict[str, Any]:
        return {
            'type': self.type,
            'format': self.format,
            'content': self.content,
            'extension': self.extension
        }


class MediaItem:
    """
    @brief Represents a single media file with comprehensive metadata (v1.35.73 Unified).
    @details Uses the MediaFormat SSOT engine for categorization.
    """

    def __init__(self, name, path, is_mock=False):
        self.name = name
        self.path = Path(path)
        self.is_directory = self.path.is_dir()
        self.is_mock = is_mock

        # 1. Metadata Extraction
        parser_mode = GLOBAL_CONFIG.get("parser_mode", "lightweight")
        _meta = media_parser.extract_metadata(self.path, self.name, mode=parser_mode)

        self.duration = 0
        self.tags = {}
        self._normalize_metadata(_meta)

        # 2. SSOT Categorization (Quadrant Consolidation)
        self.format_info = MediaFormat(self.path, self.tags)
        self.category = self.format_info.type  # Canonical lowercase ID
        self.file_format = self.format_info.format
        self.content_type = self.format_info.content
        self.extension = self.format_info.extension.lstrip('.').lower()
        self.capability_stage = self.format_info.capability_stage

        # 3. Features & Playability
        self.is_playable = self.format_info.is_playable

        # Artwork
        self.art_path = self.extract_artwork()
        self.has_artwork = self.art_path is not None
        self.is_missing_cover = not self.has_artwork

        # Type Tokens (UI Compatibility)
        self.media_type = 'container' if self.is_directory else 'file'
        self.type_token = self.category

        # Mapping extra fields for database parity
        self._set_db_parity_fields()

    def _normalize_metadata(self, _meta):
        if isinstance(_meta, tuple):
            if len(_meta) == 2:
                a, b = _meta
                if isinstance(a, (int, float)):
                    self.duration = int(a)
                    self.tags = b or {}
                elif isinstance(a, dict):
                    self.tags = a or {}
                    if isinstance(b, dict):
                        self.tags['_parser_times'] = b
                        self.duration = int(b.get('duration', a.get('duration', 0)) or 0)
                    elif isinstance(b, (int, float)):
                        self.duration = int(b)
        elif isinstance(_meta, dict):
            self.tags = _meta
            self.duration = int(self.tags.get('duration', 0) or 0)

        # Base fallbacks
        if not self.tags:
            self.tags = {}
        if not self.tags.get('title'):
            self.tags['title'] = self.path.stem if not self.is_directory else self.path.name

    def _set_db_parity_fields(self):
        self.isbn = self.tags.get('isbn')
        self.imdb = self.tags.get('imdb')
        self.tmdb = self.tags.get('tmdb')
        self.discogs = self.tags.get('discogs')
        self.amazon_cover = self.tags.get('amazon_cover')
        self.parent_id = self.tags.get('parent_id')
        self.container = self.tags.get('container', self.extension)
        self.tag_type = self.tags.get('tagtype', 'plain')
        self.codec = self.tags.get('codec', self.extension)

        if self.media_type == 'container':
            self.subtype = self.category.replace(' ', '_')
            self.file_type = None
        else:
            self.subtype = None
            self.file_type = f"{self.category.lower()}-file"

    def extract_artwork(self) -> Optional[str]:
        from src.parsers.artwork_extractor import extractor
        return extractor.extract(self.path, self.tags, self.category)

    def show_info(self):
        info_dict = self.to_dict()
        log.info(f"MediaItem SSOT: {info_dict['name']} | Cat: {info_dict['category']}")
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
        suffix = self.path.suffix.lower()
        # Lossless ALAC → transcode to FLAC (v1.35.98)
        is_alac = suffix == '.alac' or (suffix in {'.m4a', '.m4b'} and 'ALAC' in codec)
        # Lossy WMA → transcode to OGG (Opus)
        is_wma = suffix == '.wma'

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
            'capability_stage': self.capability_stage,
            'file_format': self.file_format,
            'content_type': self.content_type,
            'is_artwork_missing': self.is_missing_cover,
            'is_playable': self.is_playable,
            'is_directory': self.is_directory,
            'art_path': self.art_path,
            'artwork': self.art_path or '/cover/undefined',  # Fallback for UI
            'has_artwork': self.has_artwork,
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format,
            'is_chrome_native': chrome_native,
            'year': filtered_tags.get('year', ''),
            'title': filtered_tags.get('title', self.name),  # Flatten for easier JS access
            'artist': filtered_tags.get('artist', 'Unknown Artist'),  # Flatten for JS
            'album': filtered_tags.get('album', 'No Album'),  # Flatten for JS
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
