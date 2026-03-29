from pathlib import Path
from typing import Any, Optional
import re
import os
import json
import subprocess
import shutil
from src.core import logger

# Get specialized logger for format_utils
log = logger.get_logger("format_utils")

def detect_file_format(path: Optional[Path | str], tags: Optional[dict[str, Any]] = None) -> str:
    """
    @brief Determines the standardized file format for a given media file.
    @details Unterscheidet und standardisiert das Dateiformat je nach Typ (Audio, Video, ISO, etc.).
    @param path Path object to the file.
    @param tags Optional metadata tags for content detection.
    @return Standardized file format string (e.g., 'MP3', 'MKV', 'ISO', 'FLAC', 'PAL DVD').
    """
    try:
        # Normalize path input
        if path is None:
            return 'UNKNOWN'
        
        path_obj = Path(path) if not isinstance(path, Path) else path
        ext = (path_obj.suffix or '').lower()
        path_str = str(path_obj).lower()

        # Global Priorities (PC/Digital Games) - independent of extension
        if 'steamlibrary' in path_str or 'steamapps' in path_str or 'common' in path_str:
            return 'Digitales Spiel (Steam)'
    except Exception:
        return 'UNKNOWN'

    # Helper to format extension string like '.mp3' -> 'MP3'
    def _fmt(ext_raw: str) -> str:
        if not ext_raw:
            return 'UNKNOWN'
        return ext_raw.lstrip('.').upper()

    if ext in AUDIO_EXTENSIONS or ext in VIDEO_EXTENSIONS:
        tags = tags or {}
        # Normalize tag retrieval
        def _tag(key: str) -> str:
            try:
                return str(tags.get(key, '') or '').lower()
            except Exception:
                return ''

        # Specialized Video Detection (HDR, Interlaced, Deep Color)
        if ext in VIDEO_EXTENSIONS:
            hdr = _tag('video_hdr')
            scan = _tag('video_scan_type')
            bits = _tag('video_bit_depth')
            if hdr and hdr != 'none':
                return f'HDR {hdr.upper()} Video'
            if 'interlaced' in scan:
                return 'Interlaced Video'
            if '10 bit' in bits or '12 bit' in bits:
                return f'{bits.title()} Deep Color Video'

        # High-Res Audio detection (FLAC, WAV, AIFF, ALAC)
        if ext in AUDIO_EXTENSIONS:
            bits = _tag('audio_bit_depth')
            sr = _tag('samplerate')
            
            # Helper to check if High-Res
            def _is_high_res(b_str: str, s_str: str) -> bool:
                try:
                    b_match = re.search(r'\d+', b_str)
                    s_match = re.search(r'\d+', s_str)
                    b = int(b_match.group()) if b_match else 0
                    s = int(s_match.group()) if s_match else 0
                    return b > 16 or s > 48000
                except (ValueError, AttributeError):
                    return False

            if _is_high_res(bits, sr):
                sr_fmt = format_samplerate(sr)
                return f'High-Res {_fmt(ext)} ({bits or "24"}-bit/{sr_fmt})'

        return _fmt(ext)

    if ext in DISK_IMAGE_EXTENSIONS:
        # Try to detect content (PAL DVD, Blu-ray, etc.)
        try:
            size_gb = 0.0
            if path_obj.exists():
                try:
                    size_gb = os.path.getsize(str(path_obj)) / (1024**3)
                except (OSError, PermissionError):
                    size_gb = 0.0
        except Exception:
            size_gb = 0.0

        tags = tags or {}
        # Normalize tag retrieval to avoid crashes on weird types
        def _tag(key: str) -> str:
            try:
                return str(tags.get(key, '') or '').lower()
            except Exception:
                return ''

        volume_id = _tag('pycdlib_volume_id')
        standard = _tag('standard')
        container = _tag('container')
        title = _tag('title')
        is_dvd = _tag('pycdlib_is_dvd') == 'true'
        is_dvd_audio = _tag('pycdlib_is_dvd_audio') == 'true'
        is_dvd_vr = _tag('pycdlib_is_dvd_vr') == 'true'
        is_bluray = _tag('pycdlib_is_bluray') == 'true'
        is_hvdvd = _tag('pycdlib_is_hvdvd') == 'true'
        is_vcd = _tag('pycdlib_is_vcd') == 'true'
        is_svcd = _tag('pycdlib_is_svcd') == 'true'
        is_cdi = _tag('pycdlib_is_cdi') == 'true'
        is_photocd = _tag('pycdlib_is_photocd') == 'true'
        is_cd_extra = _tag('pycdlib_is_cd_extra') == 'true'

        # 1. PC / Digital Games (Priority: High)
        if 'win32' in volume_id or 'setup' in title or any(k in volume_id for k in ['spiel', 'game', 'software']):
            return 'PC Spiel (Index)'

        # 2. Specialized Optical Standards (Rainbow & DVD Books)
        if is_dvd_audio:
            return 'DVD-Audio (Abbild)'
        if is_dvd_vr:
            return 'DVD-VR (Video Recording)'
        if is_vcd:
            return 'Video CD (Abbild)'
        if is_svcd:
            return 'Super VCD (Abbild)'
        if is_cdi:
            return 'CD-i (Abbild)'
        if is_photocd:
            return 'Photo CD (Index)'
        if is_cd_extra:
            return 'CD-Extra (Abbild)'

        # 3. Video Priorities
        if 'pal' in volume_id or 'pal' in standard:
            return 'PAL DVD (Abbild)'
        if 'ntsc' in volume_id or 'ntsc' in standard:
            return 'NTSC DVD (Abbild)'
        if is_hvdvd or 'hvdvd_ts' in title or 'hvdvd' in volume_id:
            return 'HD DVD (Abbild)'
        if is_bluray or any(k in volume_id for k in ['blu', 'bd', 'brd']):
            return 'Blu-ray (Abbild)'
        if is_dvd or 'dvd video' in container or 'video_ts' in title:
            return 'DVD (Abbild)'
        if any(k in volume_id for k in ['sacd', 'dsd']):
            return 'SACD (Abbild)'

        # 4. Data / Rom Priorities
        if is_cdi or 'cd-i' in volume_id:
            return 'CD-i (Abbild)'
        if 'cdrom' in volume_id or 'compact disc' in volume_id:
            return 'CD-ROM (Abbild)'
        if 'dvd data' in volume_id:
            return 'DVD Daten (Abbild)'
        if 'bluray data' in volume_id:
            return 'Blu-ray Daten (Abbild)'

        # Specialized Video Detection (HDR, Interlaced, Deep Color) - Also for ISOS if metadata is present
        hdr = _tag('video_hdr')
        scan = _tag('video_scan_type')
        bits = _tag('video_bit_depth')
        if hdr and hdr != 'none':
            return f'HDR {hdr} Video'
        if 'interlaced' in scan:
            return 'Interlaced Video'
        if '10 bit' in bits or '12 bit' in bits:
            return f'{bits} Deep Color Video'

        # 3. Audio Priorities
        if any(k in volume_id for k in ['sacd', 'audio cd', 'cda']):
            return 'Audio-CD (Abbild)'

        # Heuristics based on size if no tags
        if size_gb > 9.0:
            return 'Blu-ray (Abbild)'
        if size_gb > 1.0:
            return 'DVD (Abbild)'
        if size_gb > 0.1:
            return 'CD-ROM (Abbild)'

        # Ensure .iso is standardized as 'Disk-Abbild' if no higher priority metadata is found
        return 'Disk-Abbild'

    # DSD / High-Res Audio detection
    if ext in DSD_EXTENSIONS:
        tags = tags or {}
        samplerate = str(tags.get('samplerate', '')).lower()
        if '2822' in samplerate or '2.8' in samplerate:
            return 'DSD64 (SACD Quality)'
        if '5644' in samplerate or '5.6' in samplerate:
            return 'DSD128'
        if '11289' in samplerate or '11.2' in samplerate:
            return 'DSD256'
        if '22579' in samplerate or '22.5' in samplerate:
            return 'DSD512'
        return 'DSD Audio'

    if ext in EBOOK_EXTENSIONS:
        return _fmt(ext)
    if ext in DOCUMENT_EXTENSIONS:
        return _fmt(ext)
    if ext in IMAGE_EXTENSIONS:
        return _fmt(ext)
    # Fallback: if no extension but path points to directory, try to infer
    try:
        if isinstance(path, Path) and path.is_dir():
            return 'DIRECTORY'
    except Exception:
        pass
    return _fmt(ext)


def is_playable(format_label: str, tags: dict[str, Any]) -> bool:
    """
    @brief Determines if a file should be playable or just indexed.
    @param format_label Result from detect_file_format.
    @param tags Extracted tags.
    """
    label = (format_label or "").lower()
    
    # Clearly non-playable data formats
    if 'pc spiel' in label or 'digitales spiel' in label or '(index)' in label:
        return False
        
    # Movie/Audio images are playable
    playable_keywords = [
        'dvd', 'blu-ray', 'vcd', 'laserdisc', 'sacd', 'dsd', 'cd-extra', 
        'dvd-audio', 'dvd-vr', 'video cd', 'super vcd', 'high-res',
        'cd-rom', 'dvd daten', 'blu-ray daten'
    ]
    if any(k in label for k in playable_keywords):
        return True
        
    # Standard media files are always playable
    full_path = str(tags.get('path', ''))
    ext = Path(full_path).suffix.lower() if full_path else ''
    
    # Check against known playable extensions
    playable_exts = (
        '.mp4', '.mkv', '.avi', '.mp3', '.flac', '.wav', 
        '.m4a', '.dsf', '.dff', '.ts', '.alac', '.aiff',
        '.mpeg', '.mpg', '.mov', '.webm', '.wmv', '.m4v',
        '.3gp', '.ogv', '.vob', '.m2ts', '.iso', '.bin', '.img'
    )
    if ext in playable_exts:
        return True
        
    return False

# Config File Path
CONFIG_FILE = Path.home() / '.config' / 'gui_media_web_viewer' / 'parser_config.json'


def get_default_scan_dir() -> Path:
    """
    Return the project default scan directory (<project_root>/media).
    """
    return (Path(__file__).resolve().parent.parent.parent / "media").resolve()


# Central Parser Configuration
# This avoids circular imports with main.py
PARSER_CONFIG: dict[str, Any] = {
    "start_page": "player",
    "enable_mock_data": False,
    "app_mode": "High-Performance", # Choices: High-Performance, Low-Bandwidth
    "bandwidth_limit": 20, # MB/s
    "playback_mode": "chrome_native", # Default: chrome_native, ffmpeg, cvlc, mkvmerge, direct
    "vlc_embedded": True,
    "parser_mode": "lightweight",  # Choices: lightweight, full, ultimate
    "browse_default_dir": str(Path.home()),
    "library_dir": str(get_default_scan_dir()),
    "additional_library_dirs": [],
    "parser_chain": [
        "filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", 
        "pycdlib", "isoparser", "ebml", "mkvparse", "enzyme", "pymkv", 
        "tinytag", "eyed3", "music_tag"
    ],
    "parser_mode": "lightweight",
    "fast_scan_enabled": True,  # New global fast-scan toggle
    "debug_scan": True,
    "debug_parser": True,
    "debug_flags": {
        "system": False,
        "ui": False,
        "lib": False,
        "browser": False,
        "edit": False,
        "options": False,
        "start": False,
        "parser": False,
        "scan": False,
        "player": False,
        "db": False,
        "tests": False,
        "api": False,
        "web": False,
        "i18n": False,
        "websocket": False,
        "performance": False,
        "metadata": False,
        "transcode": False,
        "file_ops": False,
        "network": False
    },
    "additional_library_dirs": [],
    "language": "en",
    "mutagen_prefer_albumartist": True,
    "mutagen_extract_lyrics": False,
    "pymediainfo_full_scan": False,
    "ffmpeg_deep_analysis": False,
    "ffmpeg_extract_thumbnails": True,
    "enable_isoparser_parser": False, # Disabled by default (slow)
    "enable_pycdlib_parser": False,   # Disabled by default (slow)
    "enable_ebml_parser": False,     # Disabled by default (slow)
    "enable_mkvparse_parser": False,  # Disabled by default (slow)
    "enable_enzyme_parser": False,    # Disabled by default (slow)
    "enable_pymkv_parser": False,     # Disabled by default (slow)
    "indexed_categories": ["audio", "video", "images", "documents", "ebooks", "abbild", "spiel", "beigabe", "supplements", "games"],
    "displayed_categories": ["audio", "video", "images", "documents", "ebooks", "abbild", "spiel", "beigabe", "supplements", "games"],
    "feature_flags": {
        "experimental_transcoding": False,
        "verbose_parsing": False,
        "show_test_tab": True,
        "analyse_mode": False,
        "write_mode": False
    },

    "browser_choice": "auto",  # auto, google-chrome, chromium, chrome, chromium-browser
    "browser_flags": [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-gpu",
        "--window-size=1550,800",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--remote-debugging-port=9222"
    ],
    "env_vars": {
        "EEL_MODE": "production",
        "PYTHONPATH": "."
    },

    "log_level": "INFO",
    "api_timeout": 10,
    "env": "production",
    "parser_settings": {
        "mkvmerge": {
            "cli_flags": "",
            "timeout": 10
        },
        "ffprobe": {
            "cli_flags": "",
            "timeout": 10
        },
        "ffmpeg": {
            "deep_analysis": False,
            "timeout": 30
        },
        "vlc": {
            "timeout": 5
        },
        "mutagen": {
            "prefer_albumartist": True
        },
        "mkvinfo": {
            "timeout": 10
        }
    }
}

# Parser which are known to be slow on certain files (ISO, MKV etc)
SLOW_PARSERS = {"isoparser", "pycdlib", "ebml", "mkvparse", "enzyme", "pymkv"}


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
        (project_root / "docs" / "logbuch").resolve(),
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
                # Migration: Ensure all default keys exist
                for key, value in PARSER_CONFIG.items():
                    if key not in loaded:
                        loaded[key] = value
                    
                    # Ensure nested dicts like feature_flags are merged
                    if isinstance(value, dict) and key in loaded and isinstance(loaded[key], dict):
                        for subkey, subvalue in value.items():
                            if subkey not in loaded[key]:
                                loaded[key][subkey] = subvalue

                    # Ensure lists like categories are expanded with new defaults
                    # (only if they are missing some of the new defaults)
                    if isinstance(value, list) and key in ["indexed_categories", "displayed_categories"] and isinstance(loaded.get(key), list):
                        new_items = [i for i in value if i not in loaded[key]]
                        if new_items:
                            loaded[key].extend(new_items)

                PARSER_CONFIG.update(loaded)
                
                # Migration: Ensure all default parsers are in the chain
                default_chain = ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "pycdlib", "isoparser", "ebml", "mkvparse", "enzyme", "pymkv", "tinytag", "eyed3", "music_tag"]
                current_chain = PARSER_CONFIG.get("parser_chain", [])
                if not current_chain:
                    PARSER_CONFIG["parser_chain"] = default_chain
                else:
                    # Append missing default parsers to the end if they are not present
                    for p in default_chain:
                        if p not in current_chain:
                            current_chain.append(p)
                    PARSER_CONFIG["parser_chain"] = current_chain
                
                # Sync path configuration
                all_paths = []
                lib_dir = PARSER_CONFIG.get("library_dir")
                if lib_dir:
                    all_paths.append(lib_dir)
                all_paths.extend(PARSER_CONFIG.get("additional_library_dirs", []))
                
                # If both are empty, use current scan_dirs (migration)
                if not all_paths:
                    all_paths = PARSER_CONFIG.get("scan_dirs", [])
                
                PARSER_CONFIG["scan_dirs"] = sanitize_scan_dirs(all_paths)
                
                # Update library_dir/additional_library_dirs from sanitized scan_dirs
                if PARSER_CONFIG["scan_dirs"]:
                    PARSER_CONFIG["library_dir"] = PARSER_CONFIG["scan_dirs"][0]
                    PARSER_CONFIG["additional_library_dirs"] = PARSER_CONFIG["scan_dirs"][1:]
                
                # Persistence: Save the migrated config back to disk to ensure 
                # all new defaults (categories, flags) are permanent.
                save_parser_config()
        except Exception as e:
            log.error(f"Error loading config: {e}")
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
        # Sync scan_dirs before saving
        all_paths = []
        if PARSER_CONFIG.get("library_dir"):
            all_paths.append(PARSER_CONFIG.get("library_dir"))
        all_paths.extend(PARSER_CONFIG.get("additional_library_dirs", []))
        PARSER_CONFIG["scan_dirs"] = sanitize_scan_dirs(all_paths)

        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(PARSER_CONFIG, f, indent=4)
    except Exception as e:
        log.error(f"Error saving config: {e}")


def reset_parser_config() -> None:
    """
    @brief Resets the parser configuration to default and deletes the config file.
    """
    if CONFIG_FILE.exists():
        try:
            CONFIG_FILE.unlink()
            log.info(f"Config file {CONFIG_FILE} deleted. Reloading defaults.")
        except Exception as e:
            log.error(f"Error deleting config file: {e}")
    
    # Re-initialize with defaults
    # We can't easily re-run the module-level code, so we just manually reset the dict
    # but for simplicity, we tell the user to restart or we trigger a reload.
    # For now, just deleting it is what "reset" usually means.


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
    '.mp3', '.flac', '.ogg', '.wav', '.m4a', '.alac', '.opus', '.aac', '.wma', '.m4b', '.aiff',
    '.ac3', '.mka', '.dts', '.dtshd', '.mka', '.pcm', '.ra', '.rm'
}
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.mpg',
    '.mpeg', '.m4v', '.3gp', '.3g2', '.ogv', '.mts', '.m2ts', '.ts',
    '.m2t', '.m2v', '.divx', '.xvid', '.vob', '.dat', '.rmvb', '.asf'
}
DOCUMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm'
}
DISK_IMAGE_EXTENSIONS = {
    '.iso', '.bin', '.img', '.cue', '.nrg', '.mdf', '.toast', '.ccd', '.daa'
}
EBOOK_EXTENSIONS = {
    '.epub', '.mobi', '.azw', '.fb2'
}
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'
}
DSD_EXTENSIONS = {
    '.dsf', '.dff', '.dsd'
}
HDDVD_EXTENSIONS = {
    '.evo', '.map', '.bup'
}

ALL_AUDIO_EXTENSIONS = AUDIO_EXTENSIONS | DSD_EXTENSIONS
ALL_MULTIMEDIA_EXTENSIONS = VIDEO_EXTENSIONS | DISK_IMAGE_EXTENSIONS | HDDVD_EXTENSIONS


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


def format_scan_type(scan_type: Any, scan_order: Any = None) -> str:
    """
    @brief Standardizes scan type (Progressive/Interlaced).
    """
    if not scan_type:
        return ""
    st = str(scan_type).capitalize()
    if 'Interlaced' in st:
        if scan_order:
            memo = " (TFF)" if 'Top' in str(scan_order) else " (BFF)"
            return f"Interlaced{memo}"
        return "Interlaced"
    return st


def format_chroma(chroma: Any) -> str:
    """
    @brief Standardizes chroma subsampling.
    """
    if not chroma:
        return ""
    c = str(chroma).replace(':', '')
    if len(c) == 3:
        return f"{c[0]}:{c[1]}:{c[2]}"
    return c


def format_color_info(space: Any, transfer: Any = None, matrix: Any = None, hdr: Any = None) -> dict[str, str]:
    """
    @brief Standardizes color space and HDR info.
    """
    res = {
        "color_space": str(space).upper() if space else "",
        "hdr_format": "None"
    }
    
    # HDR detection logic
    t = str(transfer).lower() if transfer else ""
    if hdr:
        res["hdr_format"] = str(hdr)
    elif 'smpte 2084' in t or 'pq' in t:
        res["hdr_format"] = "HDR10"
    elif 'arib std-b67' in t or 'hlg' in t:
        res["hdr_format"] = "HLG"
        
    if matrix:
        res["matrix"] = str(matrix).upper()
        
    return res


def is_chrome_native(ext: str, codec: str = "") -> bool:
    """
    Returns True if both extension and codec are natively supported by Chrome.
    """
    native_exts = {'.mp4', '.mkv', '.webm', '.ogv', '.mp3', '.wav', '.ogg', '.m4a', '.flac'}
    ext_ok = (ext or "").lower() in native_exts
    
    if not codec:
        return ext_ok
        
    c = codec.lower()
    # Common native codecs
    native_codecs = {
        'h264', 'avc1', 'vp8', 'vp9', 'av1',  # Video
        'aac', 'mp4a', 'mp3', 'opus', 'vorbis', 'flac', 'pcm' # Audio
    }
    
    codec_ok = any(nc in c for nc in native_codecs)
    return ext_ok and codec_ok


def is_direct_play_capable(path: Path | str, client: str = 'browser') -> bool:
    """
    Standardized check if a file can be played directly in the browser (Chrome).
    """
    p = Path(path)
    ext = p.suffix.lower()
    
    # Fast check by extension first
    if ext not in {'.mp4', '.mkv', '.webm', '.mp3', '.ogg', '.wav', '.flac', '.m4a'}:
        return False
        
    # Deep check with ffprobe if needed (optional optimization: cache this)
    try:
        analysis = ffprobe_suite(path)
        v_codec = analysis.get('video_codec', '')
        return is_chrome_native(ext, v_codec)
    except Exception:
        return is_chrome_native(ext)


def ffprobe_suite(path: Path | str) -> dict[str, Any]:
    """
    Runs ffprobe on the given path and returns a structured analysis object.
    """
    ffprobe_path = shutil.which("ffprobe") or "ffprobe"
    
    p = Path(path)
    if p.exists() and p.is_dir():
         try:
             iso_file = next((f for f in os.listdir(p) if f.lower().endswith(('.iso', '.bin', '.img'))), None)
             if iso_file:
                 p = p / iso_file
         except:
             pass

    try:
        # Try normal probe first
        data = None
        result = subprocess.run([ffprobe_path, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(p)], 
                                capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
        elif p.suffix.lower() == ".iso":
            # Fallback for Blu-ray ISOs
            log.info(f"[ffprobe] Normal probe failed for ISO, trying bluray: protocol for {p}")
            result = subprocess.run([ffprobe_path, "-v", "error", "-show_format", "-show_streams", "-of", "json", f"bluray:{p}"], 
                                    capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
        
        if not data:
            log.error(f"ffprobe failed completely for {path}")
            return {}
        
        streams = data.get('streams', [])
        fmt = data.get('format', {})
        
        v_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
        a_streams = [s for s in streams if s.get('codec_type') == 'audio']
        s_streams = [s for s in streams if s.get('codec_type') == 'subtitle']
        
        duration_raw = fmt.get('duration')
        duration = float(duration_raw) / 60.0 if duration_raw else 0.0
        
        size_raw = fmt.get('size')
        size_mb = float(size_raw) / (1024 * 1024) if size_raw else 0.0
        
        return {
            "container": format_container(fmt.get('format_name', ''), Path(path).suffix),
            "duration_min": round(float(duration), 1),
            "duration_sec": float(fmt.get('duration', 0.0)),
            "size_mb": round(float(size_mb), 1),
            "video_codec": str(v_stream.get('codec_name', 'unknown')),
            "width": int(v_stream.get('width', 0)),
            "height": int(v_stream.get('height', 0)),
            "pix_fmt": str(v_stream.get('pix_fmt', '')),
            "audio_codec": str(a_streams[0].get('codec_name', 'none')) if a_streams else 'none',
            "audio_channels": int(a_streams[0].get('channels', 0)) if a_streams else 0,
            "subs": len(s_streams),
            "chapters": len(data.get('chapters', [])),
            "scan_type": str(v_stream.get('field_order', 'progressive')),
            "hdr": 'hdr' in str(v_stream.get('color_transfer', '')).lower() or v_stream.get('color_space') == 'bt2020nc'
        }
    except Exception as e:
        log.error(f"ffprobe failed for {path}: {e}")
        return {}


def ffprobe_quality_score(analysis: dict[str, Any]) -> int:
    """
    Calculates a quality score (0-100) based on tech specs.
    """
    if not analysis:
        return 0
        
    score = 0
    h = analysis.get('height', 0)
    
    # Resolution base
    if h >= 2160: score += 50  # 4K
    elif h >= 1080: score += 40 # FHD
    elif h >= 720: score += 30  # HD
    else: score += 10           # SD
    
    # HDR bonus
    if analysis.get('hdr'):
        score += 20
        
    # Audio bonus
    channels = analysis.get('audio_channels', 0)
    if channels >= 6: score += 15 # 5.1+
    elif channels >= 2: score += 5 # Stereo
    
    # Extras
    if analysis.get('subs', 0) > 0: score += 5
    if analysis.get('chapters', 0) > 0: score += 10
    
    return min(100, score)
