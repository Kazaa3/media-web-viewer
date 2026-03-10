from pathlib import Path
from typing import Any
import re
import os
import json

def detect_file_format(path: Path, tags: dict[str, Any] = None) -> str:
    """
    @brief Determines the standardized file format for a given media file.
    @details Unterscheidet und standardisiert das Dateiformat je nach Typ (Audio, Video, ISO, etc.).
    @param path Path object to the file.
    @param tags Optional metadata tags for content detection.
    @return Standardized file format string (e.g., 'MP3', 'MKV', 'ISO', 'FLAC', 'PAL DVD').
    """
    ext = path.suffix.lower()
    if ext in AUDIO_EXTENSIONS:
        return ext[1:].upper()
    if ext in VIDEO_EXTENSIONS:
        return ext[1:].upper()
    if ext in IMAGE_EXTENSIONS:
        return ext[1:].upper()
    if ext == '.iso':
        # Try to detect content (PAL DVD, Blu-ray, etc.)
        if tags:
            volume_id = tags.get('pycdlib_volume_id', '').lower()
            standard = tags.get('standard', '').lower()
            container = tags.get('container', '').lower()
            title = tags.get('title', '').lower()

            # Video Priorities
            if 'pal' in volume_id or 'pal' in standard:
                return 'PAL DVD (ISO)'
            if 'ntsc' in volume_id or 'ntsc' in standard:
                return 'NTSC DVD (ISO)'
            if 'dvd video' in container or 'video_ts' in title:
                return 'DVD (ISO)'
            if any(k in volume_id for k in ['blu', 'bd', 'brd']):
                return 'Blu-ray (ISO)'
            
            # Audio Priorities
            if any(k in volume_id for k in ['sacd', 'audio cd', 'cda']):
                return 'Audio-CD (Abbild)'
        return 'Abbild'
    if ext in EBOOK_EXTENSIONS:
        return ext[1:].upper()
    if ext in DOCUMENT_EXTENSIONS:
        return ext[1:].upper()
    if ext in IMAGE_EXTENSIONS:
        return ext[1:].upper()
    return ext[1:].upper() if ext else 'UNKNOWN'

# Config File Path
CONFIG_FILE = Path.home() / '.config' / 'gui_media_web_viewer' / 'parser_config.json'


def get_default_scan_dir() -> Path:
    """
    Return the project default scan directory (<project_root>/media).
    """
    return (Path(__file__).resolve().parent.parent / "media").resolve()


# Central Parser Configuration
# This avoids circular imports with main.py
PARSER_CONFIG: dict[str, Any] = {
    "parser_chain": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "isoparser"],
    "parser_mode": "lightweight",
    "debug_scan": True,
    "debug_parser": True,
    "scan_dirs": [str(get_default_scan_dir())],
    "language": "de",
    "mutagen_prefer_albumartist": True,
    "mutagen_extract_lyrics": False,
    "pymediainfo_full_scan": False,
    "ffmpeg_deep_analysis": False,
    "ffmpeg_extract_thumbnails": True,
    "enable_isoparser_parser": True
}


def sanitize_scan_dirs(scan_dirs: Any) -> list[str]:
    """
    Sanitize configured scan directories.

    - keep only existing directories
    - remove duplicates
    - exclude internal project directories like logbuch and dist
    """
    default_scan_dir = get_default_scan_dir()

    if not isinstance(scan_dirs, list):
        scan_dirs = []

    project_root = Path(__file__).resolve().parent.parent
    blocked_dirs = {
        (project_root / "logbuch").resolve(),
        (project_root / "dist").resolve(),
        (project_root / ".git").resolve(),
        (project_root / ".venv").resolve(),
        (project_root / "packaging").resolve(),
    }

    sanitized: list[str] = []
    seen: set[Path] = set()

    for raw_dir in scan_dirs:
        if not isinstance(raw_dir, str) or not raw_dir.strip():
            continue

        candidate = Path(raw_dir).expanduser().resolve()

        if candidate == default_scan_dir:
            candidate.mkdir(parents=True, exist_ok=True)
        if not candidate.exists() or not candidate.is_dir():
            continue
        if candidate in blocked_dirs:
            continue
        if candidate in seen:
            continue

        seen.add(candidate)
        sanitized.append(str(candidate))

    # Ensure default media directory is always available as baseline scan dir
    default_scan_dir.mkdir(parents=True, exist_ok=True)
    if str(default_scan_dir) not in sanitized:
        sanitized.insert(0, str(default_scan_dir))

    return sanitized


def load_parser_config() -> None:
    """
    @brief Loads the parser configuration from the central JSON file.
    @details Lädt die Parser-Konfiguration aus der zentralen JSON-Datei.
    """
    global PARSER_CONFIG
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
                PARSER_CONFIG.update(loaded)
                PARSER_CONFIG["scan_dirs"] = sanitize_scan_dirs(PARSER_CONFIG.get("scan_dirs", []))
        except Exception as e:
            print(f"Error loading config: {e}")
    else:
        # Ensure directory exists but wait to save until needed
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        save_parser_config()


def save_parser_config() -> None:
    """
    @brief Saves the current parser configuration to disk.
    @details Speichert die aktuelle Parser-Konfiguration auf der Festplatte.
    """
    try:
        PARSER_CONFIG["scan_dirs"] = sanitize_scan_dirs(PARSER_CONFIG.get("scan_dirs", []))
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(PARSER_CONFIG, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")


# Load immediately on import
load_parser_config()


def natural_sort_key(text: Any) -> list[tuple[bool, Any]]:
    """
    @brief Generates a key for natural/numeric sorting (e.g., 'Track 2' < 'Track 10').
    @details Erzeugt einen Schlüssel für natürliche/numerische Sortierung.
    @param text input string or number / Eingabe-String oder Zahl.
    @return A list of sortable parts / Eine Liste sortierbarer Teile.
    """
    if text is None:
        return []
    if isinstance(text, (int, float)):
        return [(True, text)]
    s = str(text)
    parts = re.split(r'(\d+)', s)
    # Return a list of tuples to avoid mixed-type comparisons in list elements
    # Format: (is_digit, value)
    return [(True, int(c)) if c.isdigit() else (False, c.lower()) for c in parts if c]


# Extension Categories
AUDIO_EXTENSIONS = {
    '.mp3', '.flac', '.ogg', '.wav', '.m4a', '.alac', '.opus', '.aac', '.wma', '.m4b'
}
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.mpg',
    '.mpeg', '.m4v', '.3gp', '.3g2', '.ogv', '.mts', '.m2ts', '.iso'
}
DOCUMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm'
}
EBOOK_EXTENSIONS = {
    '.epub', '.mobi', '.azw', '.fb2'
}
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'
}


def format_samplerate(hz: Any) -> str:
    """
    @brief Standardizes sample rate display (e.g., 44100 -> 44.1 kHz).
    @details Normalisiert die Anzeige der Samplerate.
    @param hz Sample rate in Hz.
    @return Formatted string (e.g., '44.1 kHz').
    """
    try:
        hz = float(hz)
        khz = hz / 1000
        return f"{int(khz)} kHz" if khz.is_integer() else f"{khz:g} kHz"
    except (ValueError, TypeError):
        return ""


def format_codec(raw_codec: Any, track_info: Any = None) -> str:
    """
    @brief Standardizes codec naming (lowercase, PCM details).
    @details Normalisiert Codec-Namen (Kleinschreibung, PCM-Details).
    @param raw_codec Raw codec string from parser / Roh-Codec-String.
    @param track_info Optional PyMediainfo track object for PCM details / Optionales Track-Objekt für PCM-Details.
    @return Standardized codec string / Normalisierter Codec-String.
    """
    if not raw_codec:
        return ""

    codec = str(raw_codec).lower()

    # Generic mappings for common codecs to match user preference
    codec_map = {
        'mpeg audio': 'mp3',
        'vorbis': 'ogg',
        'opus': 'opus',
        'flac': 'flac',
        'alac': 'alac',
        'aac': 'aac',
        'm4a': 'aac'
    }

    # PCM specific handling
    if codec == 'pcm' and track_info:
        sign = 'S' if getattr(track_info, 'format_settings__sign', '') == 'Signed' else 'U'
        end = 'LE' if getattr(track_info, 'format_settings__endianness', '') == 'Little' else 'BE'
        bps = getattr(track_info, 'bit_depth', '')
        return f"PCM_{sign}{bps}{end}"

    # Special case for PCM if it already looks like PCM_S16LE
    if codec.startswith('pcm_'):
        return str(raw_codec).upper()

    return codec_map.get(codec, codec)


def format_container(raw_container: Any, file_type: str | None = None) -> str:
    """
    @brief Standardizes container naming (e.g., 'matroska' -> 'mkv').
    @details Normalisiert Container-Namen.
    @param raw_container Raw container string / Roh-Container-String.
    @param file_type Optional extension for fallback / Optionale Extension für Fallback.
    @return Standardized container string / Normalisierter Container-String.
    """
    container = str(raw_container).lower().strip() if raw_container else ""

    if not container and file_type:
        container = file_type[1:].lower() if file_type else ""

    # Handle ambiguous FFmpeg container outputs
    if container == 'matroska,webm':
        if file_type == '.webm':
            return 'webm'
        return 'mkv'

    container_map = {
        'matroska': 'mkv',
        'mov,mp4,m4a,3gp,3g2,mj2': 'mp4',
        'mpeg-4': 'mp4',
        'quicktime': 'mp4',
        'asf': 'wma',
        'ogg': 'ogg',
        'flac': 'flac',
        'mp3': 'mp3'
    }

    # Fallback to file_type if we have a generic ID3/WAV container that isn't really a "container"
    if container in ('id3', 'wav') and file_type:
        return file_type[1:].lower() if file_type else ""

    return container_map.get(container, container)


def format_tagtype(raw_tagtype: Any) -> str:
    """
    @brief Standardizes meta tag types into human-readable formats (e.g., 'MP4Tags' -> 'm4tags').
    @details Normalisiert Metadaten-Tag-Typen.
    @param raw_tagtype Raw tag type string / Roh-Tagtyp-String.
    @return Standardized tag type / Normalisierter Tagtyp.
    """
    if not raw_tagtype:
        return "plain"

    tag = str(raw_tagtype).strip()

    # Already formatted versions (e.g. ID3v2.3)
    if tag.startswith("ID3v"):
        return tag

    tag_map = {
        'ID3': 'ID3',
        'MP4Tags': 'm4tags',
        'OggVComment': 'OggVComment',
        'VCFLACDict': 'VCFLACDict',
        'ASF': 'asf',
        'APETag': 'APEv2'
    }

    return tag_map.get(tag, tag)


def format_bitdepth(
    bit_depth: Any,
    codec: Any = None,
    file_type: str | None = None,
    internal_fmt: str | None = None
) -> str:
    """
    @brief Standardizes bit depth display (e.g., '24 Bit (s32)', '16 Bit (lossy)').
    @details Normalisiert die Anzeige der Bit-Tiefe.
    @param bit_depth Raw bit depth / Roh-Bittiefe.
    @param codec Optional codec for context / Optionaler Codec.
    @param file_type Optional extension for lossy detection / Optionale Extension für Lossy-Erkennung.
    @param internal_fmt Optional FFmpeg internal format / Optionales FFmpeg-Internes Format.
    @return Formatted bit depth string / Formatierter Bittiefe-String.
    """
    if not bit_depth:
        # Check for lossy extensions if bitdepth is missing
        lossy_extensions = {'.mp3', '.ogg', '.aac', '.m4a', '.m4b', '.wma', '.opus'}
        if file_type in lossy_extensions:
            return "16 Bit (lossy)"
        return "16 Bit"  # Generic default

    try:
        bd_int = int(bit_depth)

        # Check if it is a PCM codec (either explicitly passed or detected in codec string)
        is_pcm = False
        if codec:
            c_upper = str(codec).upper()
            if 'PCM' in c_upper or c_upper == 'WAV':
                is_pcm = True

        if is_pcm:
            if bd_int == 24:
                return "24 Bit (s32)"
            elif bd_int == 16:
                return "16 Bit (s16)"
            elif bd_int == 32:
                # Could be float or int, usually s32 or flt
                suffix = f"({internal_fmt})" if internal_fmt else "(s32)"
                return f"32 Bit {suffix}"

        # FFmpeg internal format mapping (e.g. s16, s32, fltp)
        if internal_fmt:
            # Check for specific user requested mapping: 24 Bit (s32) if it came from PCM_S24LE
            if internal_fmt in ('s32', 's32p') and bd_int == 24:
                return "24 Bit (s32)"

            fmt_map = {
                'u8': '8 Bit (u8)', 'u8p': '8 Bit (u8p)',
                's16': '16 Bit (s16)', 's16p': '16 Bit (s16p)',
                's24': '24 Bit (s24)', 's24p': '24 Bit (s24p)',
                's32': '32 Bit (s32)', 's32p': '32 Bit (s32p)',
                's64': '64 Bit (s64)', 's64p': '64 Bit (s64p)',
                'flt': '32 Bit (flt)', 'fltp': '32 Bit (fltp)',
                'dbl': '64 Bit (dbl)', 'dblp': '64 Bit (dblp)',
            }
            if internal_fmt in fmt_map:
                label = fmt_map[internal_fmt]
                if internal_fmt in ('flt', 'fltp', 'dbl', 'dblp'):
                    return f"{label} Float ({internal_fmt})"
                return label

        return f"{bd_int} Bit"
    except (ValueError, TypeError):
        return str(bit_depth)
