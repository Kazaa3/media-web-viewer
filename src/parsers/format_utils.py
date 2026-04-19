from pathlib import Path
from typing import Any, Optional
import re
import os
import json
import subprocess
import shutil
import eel
from src.core.logger import get_logger
from src.core.config_master import (
    GLOBAL_CONFIG, MEDIA_DIR,
    AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, PICTURE_EXTENSIONS,
    DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, DISK_IMAGE_EXTENSIONS,
    PLAYLIST_EXTENSIONS, ALL_AUDIO_EXTENSIONS, ALL_VIDEO_EXTENSIONS
)
from src.core.models import (
    PLAYABLE_KEYWORDS, PLAYABLE_EXTENSIONS, 
    DSD_EXTENSIONS, HDDVD_EXTENSIONS, 
    NATIVE_EXTENSIONS, NATIVE_CODECS, LOSSY_EXTENSIONS, SLOW_PARSERS
)

# Specialized logger (v1.46.132 Modernized)
log = get_logger("format_utils")

def detect_file_format(path: Optional[Path | str], tags: Optional[dict[str, Any]] = None) -> str:
    """
    Unified format detection wrapper (v1.35.81 Redirect).
    """
    if path is None:
        return 'UNKNOWN'
    from src.core.models import MediaFormat
    return MediaFormat(Path(path), tags).format

# Configuration Centralization (Phase 9)
reg = GLOBAL_CONFIG.get("parser_registry", {})
CONFIG_FILE = Path(reg.get("legacy_config_path", "~/.config/gui_media_web_viewer/parser_config.json")).expanduser()

def get_default_scan_dir() -> Path:
    """
    Return the project default scan directory (Centralized v1.35.98).
    """
    return Path(GLOBAL_CONFIG.get("scan_media_dir", str(MEDIA_DIR)))

# Use Centralized Config (v1.41.00)
PARSER_CONFIG = GLOBAL_CONFIG

def sanitize_scan_dirs(scan_dirs: Any) -> list[str]:
    """
    Sanitize configured scan directories.
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

    default_scan_dir.mkdir(parents=True, exist_ok=True)
    if str(default_scan_dir) not in sanitized:
        sanitized.insert(0, str(default_scan_dir))

    return sanitized


def load_parser_config() -> None:
    """
    @brief Loads the parser configuration from the central JSON file.
    """
    global PARSER_CONFIG
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
                for key, value in PARSER_CONFIG.items():
                    if key not in loaded:
                        loaded[key] = value
                    
                    if isinstance(value, dict) and key in loaded and isinstance(loaded[key], dict):
                        for subkey, subvalue in value.items():
                            if subkey not in loaded[key]:
                                loaded[key][subkey] = subvalue

                    if isinstance(value, list) and key in ["indexed_categories", "displayed_categories"] and isinstance(loaded.get(key), list):
                        new_items = [i for i in value if i not in loaded[key]]
                        if new_items:
                            loaded[key].extend(new_items)

                PARSER_CONFIG.update(loaded)
                
                default_chain = GLOBAL_CONFIG.get("parser_registry", {}).get("default_chain", [])
                current_chain = PARSER_CONFIG.get("parser_chain", [])
                if not current_chain:
                    PARSER_CONFIG["parser_chain"] = default_chain
                else:
                    for p in default_chain:
                        if p not in current_chain:
                            current_chain.append(p)
                    PARSER_CONFIG["parser_chain"] = current_chain
                
                all_paths = []
                lib_dir = PARSER_CONFIG.get("library_dir")
                if lib_dir:
                    all_paths.append(lib_dir)
                all_paths.extend(PARSER_CONFIG.get("additional_library_dirs", []))
                
                if not all_paths:
                    all_paths = PARSER_CONFIG.get("scan_dirs", [])
                
                PARSER_CONFIG["scan_dirs"] = sanitize_scan_dirs(all_paths)
                
                if PARSER_CONFIG["scan_dirs"]:
                    PARSER_CONFIG["library_dir"] = PARSER_CONFIG["scan_dirs"][0]
                    PARSER_CONFIG["additional_library_dirs"] = PARSER_CONFIG["scan_dirs"][1:]
                
                save_parser_config()
        except (json.JSONDecodeError, Exception) as e:
            log.warning(f"[Config] File at {CONFIG_FILE} is malformed. Restoring SSOT. {e}", exc_info=True)
            if CONFIG_FILE.exists():
                try: CONFIG_FILE.unlink() # Force purge
                except: pass
            
            for key, value in GLOBAL_CONFIG.items():
                PARSER_CONFIG[key] = value
            save_parser_config()
    else:
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        save_parser_config()


class ConfigJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)


def save_parser_config() -> None:
    try:
        all_paths = []
        if PARSER_CONFIG.get("library_dir"):
            all_paths.append(PARSER_CONFIG.get("library_dir"))
        all_paths.extend(PARSER_CONFIG.get("additional_library_dirs", []))
        PARSER_CONFIG["scan_dirs"] = sanitize_scan_dirs(all_paths)

        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(PARSER_CONFIG, f, indent=4, cls=ConfigJSONEncoder)
    except Exception as e:
        log.error(f"[Config] Error saving {CONFIG_FILE}: {e}", exc_info=True)


def reset_parser_config() -> None:
    if CONFIG_FILE.exists():
        try:
            CONFIG_FILE.unlink()
            log.info(f"[Config] Reset successful: {CONFIG_FILE} deleted.")
        except Exception as e:
            log.error(f"[Config] Reset failed: {e}", exc_info=True)


load_parser_config()

def natural_sort_key(text: Any) -> list[tuple[bool, Any]]:
    if text is None:
        return []
    if isinstance(text, (int, float)):
        return [(True, text)]
    s = str(text)
    parts = re.split(r'(\d+)', s)
    return [(True, int(c)) if c.isdigit() else (False, c.lower()) for c in parts if c]


def format_samplerate(hz: Any) -> str:
    try:
        hz = float(hz)
        khz = hz / 1000
        return f"{int(khz)} kHz" if khz.is_integer() else f"{khz:g} kHz"
    except (ValueError, TypeError):
        return ""


def format_codec(raw_codec: Any, track_info: Any = None) -> str:
    if not raw_codec:
        return ""
    codec = str(raw_codec).lower()
    codec_map = GLOBAL_CONFIG.get("parser_registry", {}).get("codec_map", {})
    if codec == 'pcm' and track_info:
        sign = 'S' if getattr(track_info, 'format_settings__sign', '') == 'Signed' else 'U'
        end = 'LE' if getattr(track_info, 'format_settings__endianness', '') == 'Little' else 'BE'
        bps = getattr(track_info, 'bit_depth', '')
        return f"PCM_{sign}{bps}{end}"
    if codec.startswith('pcm_'):
        return str(raw_codec).upper()
    return codec_map.get(codec, codec)


def format_container(raw_container: Any, file_type: str | None = None) -> str:
    container = str(raw_container).lower().strip() if raw_container else ""
    if not container and file_type:
        container = file_type[1:].lower()
    if container == 'matroska,webm':
        if file_type == '.webm': return 'webm'
        return 'mkv'
    container_map = GLOBAL_CONFIG.get("parser_registry", {}).get("container_map", {})
    if container in ('id3', 'wav') and file_type:
        return file_type[1:].lower()
    return container_map.get(container, container)


def format_tagtype(raw_tagtype: Any) -> str:
    if not raw_tagtype: return "plain"
    tag = str(raw_tagtype).strip()
    if tag.startswith("ID3v"): return tag
    tag_map = GLOBAL_CONFIG.get("parser_registry", {}).get("tag_type_map", {})
    return tag_map.get(tag, tag)


def format_bitdepth(bit_depth: Any, codec: Any = None, file_type: str | None = None, internal_fmt: str | None = None) -> str:
    if file_type and str(file_type).lower() in LOSSY_EXTENSIONS: return ""
    if not bit_depth: return ""
    try:
        bd_int = int(bit_depth)
        if internal_fmt:
            if internal_fmt in ('s32', 's32p') and bd_int == 24: return "24 Bit"
            fmt_map = {
                'u8': '8 Bit', 'u8p': '8 Bit', 's16': '16 Bit', 's16p': '16 Bit',
                's24': '24 Bit', 's24p': '24 Bit', 's32': '32 Bit', 's32p': '32 Bit',
                's64': '64 Bit', 's64p': '64 Bit', 'flt': '32 Bit Float', 'fltp': '32 Bit Float',
                'dbl': '64 Bit Float', 'dblp': '64 Bit Float',
            }
            if internal_fmt in fmt_map: return fmt_map[internal_fmt]
        return f"{bd_int} Bit"
    except (ValueError, TypeError): return ""


def get_installed_packages_local() -> dict:
    return GLOBAL_CONFIG.get("installed_packages", {})


def format_scan_type(scan_type: Any, scan_order: Any = None) -> str:
    if not scan_type: return ""
    st = str(scan_type).capitalize()
    if 'Interlaced' in st:
        memo = (" (TFF)" if 'Top' in str(scan_order) else " (BFF)") if scan_order else ""
        return f"Interlaced{memo}"
    return st


def format_chroma(chroma: Any) -> str:
    if not chroma: return ""
    c = str(chroma).replace(':', '')
    return f"{c[0]}:{c[1]}:{c[2]}" if len(c) == 3 else c


def format_color_info(space: Any, transfer: Any = None, matrix: Any = None, hdr: Any = None) -> dict[str, str]:
    res = {"color_space": str(space).upper() if space else "", "hdr_format": "None"}
    t = str(transfer).lower() if transfer else ""
    if hdr: res["hdr_format"] = str(hdr)
    elif 'smpte 2084' in t or 'pq' in t: res["hdr_format"] = "HDR10"
    elif 'arib std-b67' in t or 'hlg' in t: res["hdr_format"] = "HLG"
    if matrix: res["matrix"] = str(matrix).upper()
    return res


def is_chrome_native(ext: str, codec: str = "") -> bool:
    ext_ok = (ext or "").lower() in NATIVE_EXTENSIONS
    if not codec: return ext_ok
    c = codec.lower()
    return ext_ok and any(nc in c for nc in NATIVE_CODECS)


def is_direct_play_capable(path: Path | str, client: str = 'browser') -> bool:
    p = Path(path)
    ext = p.suffix.lower()
    if ext not in {'.mp4', '.mkv', '.webm', '.mp3', '.ogg', '.wav', '.flac', '.m4a'}: return False
    try:
        analysis = ffprobe_suite(path)
        return is_chrome_native(ext, analysis.get('video_codec', ''))
    except Exception: return is_chrome_native(ext)


def ffprobe_suite(path: Path | str) -> dict[str, Any]:
    ffprobe_path = GLOBAL_CONFIG.get("program_paths", {}).get("ffprobe", "ffprobe")
    p = Path(path)
    if p.exists() and p.is_dir():
         try:
             iso_file = next((f for f in os.listdir(p) if f.lower().endswith(('.iso', '.bin', '.img'))), None)
             if iso_file: p = p / iso_file
         except: pass
    try:
        data = None
        result = subprocess.run([ffprobe_path, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(p)], 
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            data = json.loads(result.stdout)
        elif p.suffix.lower() == ".iso":
            log.info(f"[ffprobe] Normal probe failed for ISO, try bluray: {p}")
            result = subprocess.run([ffprobe_path, "-v", "error", "-show_format", "-show_streams", "-of", "json", f"bluray:{p}"], 
                                    capture_output=True, text=True, timeout=15)
            if result.returncode == 0: data = json.loads(result.stdout)
        
        if not data:
            log.error(f"[ffprobe] Process failed completely for {p}")
            return {}
        
        streams = data.get('streams', [])
        fmt = data.get('format', {})
        v_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
        a_streams = [s for s in streams if s.get('codec_type') == 'audio']
        s_streams = [s for s in streams if s.get('codec_type') == 'subtitle']
        
        d_raw = fmt.get('duration')
        d_sec = float(d_raw) if d_raw else 0.0
        size_raw = fmt.get('size')
        size_mb = float(size_raw) / (1024 * 1024) if size_raw else 0.0
        
        return {
            "container": format_container(fmt.get('format_name', ''), p.suffix),
            "duration": d_sec, # Centralized SSOT Field
            "duration_min": round(d_sec / 60.0, 1),
            "size_mb": round(size_mb, 1),
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
        log.error(f"[ffprobe] Failed for {p}: {e}", exc_info=True)
        return {}


def ffprobe_quality_score(analysis: dict[str, Any]) -> int:
    if not analysis: return 0
    score = 0
    h = analysis.get('height', 0)
    weights = GLOBAL_CONFIG.get("diagnostic_registry", {}).get("quality_score_weights", {})
    res_w = weights.get("resolution", {})
    if h >= 2160: score += res_w.get("2160", 40)
    elif h >= 1080: score += res_w.get("1080", 30)
    elif h >= 720: score += res_w.get("720", 20)
    else: score += res_w.get("default", 10)
    if analysis.get('hdr'): score += weights.get("hdr", 10)
    channels = analysis.get('audio_channels', 0)
    if channels >= 6: score += weights.get("audio", {}).get("multichannel", 20)
    elif channels >= 2: score += weights.get("audio", {}).get("stereo", 10)
    if analysis.get('subs', 0) > 0: score += weights.get("extras", {}).get("subs", 5)
    if analysis.get('chapters', 0) > 0: score += weights.get("extras", {}).get("chapters", 5)
    return min(100, score)

