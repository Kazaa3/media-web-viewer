from pathlib import Path
from typing import Any, Optional
import re
import os
import json
import subprocess
import shutil
import eel
from src.core import logger
from src.core.config_master import GLOBAL_CONFIG
from src.core.models import (
    PLAYABLE_KEYWORDS, PLAYABLE_EXTENSIONS, 
    AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, PICTURE_EXTENSIONS,
    DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, DISK_IMAGE_EXTENSIONS,
    DSD_EXTENSIONS, HDDVD_EXTENSIONS, PLAYLIST_EXTENSIONS,
    ALL_AUDIO_EXTENSIONS, ALL_VIDEO_EXTENSIONS,
    NATIVE_EXTENSIONS, NATIVE_CODECS, LOSSY_EXTENSIONS, SLOW_PARSERS
)

# Get specialized logger for format_utils
log = logger.get_logger("format_utils")

def detect_file_format(path: Optional[Path | str], tags: Optional[dict[str, Any]] = None) -> str:
    """
    Unified format detection wrapper (v1.35.81 Redirect).
    """
    if path is None:
        return 'UNKNOWN'
    from src.core.models import MediaFormat
    return MediaFormat(Path(path), tags).format





# Config File Path
CONFIG_FILE = Path.home() / '.config' / 'gui_media_web_viewer' / 'parser_config.json'


def get_default_scan_dir() -> Path:
    """
    Return the project default scan directory (Centralized v1.35.98).
    """
    return Path(GLOBAL_CONFIG.get("scan_media_dir", str(Path(__file__).resolve().parent.parent.parent / "media")))


# Use Centralized Config (v1.35.68)
PARSER_CONFIG = GLOBAL_CONFIG

# SLOW_PARSERS now imported from config_master (Centralized Config v1.35.68)


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
                default_chain = GLOBAL_CONFIG["parser_registry"]["default_chain"]
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
        except (json.JSONDecodeError, Exception) as e:
            log.warning(f"Configuration file at {CONFIG_FILE} is malformed or missing. Restoring SSOT defaults. Error: {e}")
            # Restore from SSOT defaults without clearing the shared reference
            for key, value in GLOBAL_CONFIG.items():
                PARSER_CONFIG[key] = value
            save_parser_config()
    else:
        # Ensure directory exists but wait to save until needed
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        save_parser_config()


class ConfigJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for Pathlib.Path objects (v1.35.68)"""
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)


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
            json.dump(PARSER_CONFIG, f, indent=4, cls=ConfigJSONEncoder)
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


# Extension Categories (Centralized v1.35.68)



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

    # Generic mappings for common codecs (Centralized v1.35.68)
    codec_map = GLOBAL_CONFIG["parser_registry"]["codec_map"]

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

    # Generic mappings for containers (Centralized v1.35.68)
    container_map = GLOBAL_CONFIG["parser_registry"]["container_map"]

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

    # Generic mappings for tag types (Centralized v1.35.68)
    tag_map = GLOBAL_CONFIG["parser_registry"]["tag_type_map"]
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
    # 1. Immediate exclusion for lossy formats (MP3, OGG, etc. have no PCM bit-depth)
    if file_type and str(file_type).lower() in LOSSY_EXTENSIONS:
        return ""

    # 2. Check for missing bit-depth
    if not bit_depth:
        return ""

    try:
        bd_int = int(bit_depth)

        # 3. Use internal FFmpeg format mapping (Authorized SSOT)
        if internal_fmt:
            # Multi-layer precision: 24-bit PCM inside s32/s32p
            if internal_fmt in ('s32', 's32p') and bd_int == 24:
                return "24 Bit"

            fmt_map = {
                'u8': '8 Bit', 'u8p': '8 Bit',
                's16': '16 Bit', 's16p': '16 Bit',
                's24': '24 Bit', 's24p': '24 Bit',
                's32': '32 Bit', 's32p': '32 Bit',
                's64': '64 Bit', 's64p': '64 Bit',
                'flt': '32 Bit Float', 'fltp': '32 Bit Float',
                'dbl': '64 Bit Float', 'dblp': '64 Bit Float',
            }
            if internal_fmt in fmt_map:
                return fmt_map[internal_fmt]

        # 4. Fallback for pure lossless bit depth (FLAC, ALAC, WAV)
        return f"{bd_int} Bit"
    except (ValueError, TypeError):
        return ""



def get_installed_packages_local() -> dict:
    """
    Internal helper for discovered PIP package registry.
    """
    from src.core.config_master import GLOBAL_CONFIG
    return GLOBAL_CONFIG.get("installed_packages", {})


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
    ext_ok = (ext or "").lower() in NATIVE_EXTENSIONS
    
    if not codec:
        return ext_ok
        
    c = codec.lower()
    codec_ok = any(nc in c for nc in NATIVE_CODECS)
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
    # Global/Centralized Binary Orchestration (v1.35.68)
    from src.core.config_master import GLOBAL_CONFIG
    ffprobe_path = GLOBAL_CONFIG["program_paths"].get("ffprobe", "ffprobe")
    
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
    
    # Resolution base (Centralized v1.35.68)
    weights = GLOBAL_CONFIG["diagnostic_registry"]["quality_score_weights"]
    res_w = weights["resolution"]
    
    if h >= 2160: score += res_w["2160"]
    elif h >= 1080: score += res_w["1080"]
    elif h >= 720: score += res_w["720"]
    else: score += res_w["default"]
    
    # HDR bonus
    if analysis.get('hdr'):
        score += weights["hdr"]
        
    # Audio bonus
    channels = analysis.get('audio_channels', 0)
    if channels >= 6: score += weights["audio"]["multichannel"]
    elif channels >= 2: score += weights["audio"]["stereo"]
    
    # Extras
    if analysis.get('subs', 0) > 0: score += weights["extras"]["subs"]
    if analysis.get('chapters', 0) > 0: score += weights["extras"]["chapters"]
    
    return min(100, score)
