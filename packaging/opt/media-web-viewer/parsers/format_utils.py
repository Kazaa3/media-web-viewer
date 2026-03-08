import re
import os
import json
from pathlib import Path

# Config File Path
CONFIG_FILE = Path.home() / '.config' / 'gui_media_web_viewer' / 'parser_config.json'

# Central Parser Configuration
# This avoids circular imports with main.py
PARSER_CONFIG = {
    "parser_chain": ["filename", "container", "mutagen", "pymediainfo", "ffmpeg"],
    "parser_mode": "lightweight",
    "debug_scan": True,
    "debug_parser": True,
    "scan_dirs": [str(Path(__file__).resolve().parent.parent / "media")],
    "language": "de",
    "mutagen_prefer_albumartist": True,
    "mutagen_extract_lyrics": False,
    "pymediainfo_full_scan": False,
    "ffmpeg_deep_analysis": False,
    "ffmpeg_extract_thumbnails": True
}


def load_parser_config():
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
        except Exception as e:
            print(f"Error loading config: {e}")
    else:
        # Ensure directory exists but wait to save until needed
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        save_parser_config()


def save_parser_config():
    """
    @brief Saves the current parser configuration to disk.
    @details Speichert die aktuelle Parser-Konfiguration auf der Festplatte.
    """
    try:
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(PARSER_CONFIG, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")


# Load immediately on import
load_parser_config()


def natural_sort_key(text):
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
    '.mp4',
    '.avi',
    '.mov',
    '.mkv',
    '.webm',
    '.flv',
    '.wmv',
    '.mpg',
    '.mpeg',
    '.m4v',
    '.3gp',
    '.3g2',
    '.ogv',
    '.mts',
    '.m2ts'}
DOCUMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm'
}
EBOOK_EXTENSIONS = {
    '.epub', '.mobi', '.azw', '.fb2'
}


def format_samplerate(hz):
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


def format_codec(raw_codec, track_info=None):
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
        return raw_codec.upper()

    return codec_map.get(codec, codec)


def format_container(raw_container, file_type=None):
    """
    @brief Standardizes container naming (e.g., 'matroska' -> 'mkv').
    @details Normalisiert Container-Namen.
    @param raw_container Raw container string / Roh-Container-String.
    @param file_type Optional extension for fallback / Optionale Extension für Fallback.
    @return Standardized container string / Normalisierter Container-String.
    """
    container = str(raw_container).lower().strip() if raw_container else ""

    if not container and file_type:
        container = file_type[1:].lower()

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
        return file_type[1:].lower()

    return container_map.get(container, container)


def format_tagtype(raw_tagtype):
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
        'OggVComment': 'vorbis comment',
        'VCFLACDict': 'vorbis comment',
        'ASF': 'asf',
        'ASFTags': 'asf',
        'APETag': 'APEv2'
    }

    return tag_map.get(tag, tag)


def format_bitdepth(bit_depth, codec=None, file_type=None, internal_fmt=None):
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
