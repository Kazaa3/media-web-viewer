#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Config Master (Centralized Config & Flag Orchestrator)
v1.35.68 - Unified source of truth for backend and frontend settings.
"""

import os
import sys
import shutil
import re
import subprocess
import eel
from pathlib import Path
from typing import Any, Dict, List
from importlib.metadata import distributions

try:
    from src.core import hardware_detector
    _HW_DETECTOR = True
except ImportError:
    _HW_DETECTOR = False

# --- SSOT: TECHNICAL MEDIA CAPABILITY GROUPS (v1.38.01) ---
# These constants define the technical handling requirements (Native vs. Transcode).
# Use uppercase as per architectural standard.
# More in: models.py

# AUDIO CAPABILITIES
AUDIO_NATIVE = {".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac"}
AUDIO_TRANSCODE = {".wav", ".alac", ".wma", ".aiff", ".dsf", ".dff", ".dsd", ".ac3", ".dts"}
ALL_AUDIO_EXTENSIONS = AUDIO_NATIVE | AUDIO_TRANSCODE
AUDIO_EXTENSIONS = ALL_AUDIO_EXTENSIONS

# VIDEO CAPABILITIES (Pipeline Categorization)
VIDEO_NATIVE = {".mp4", ".webm", ".ogv"}
VIDEO_HD_TRANSCODE = {".mkv", ".mov", ".ts", ".m2ts"}
VIDEO_PAL_TRANSCODE = {".vob", ".mpg", ".mpeg", ".m2v"}
VIDEO_NTSC_TRANSCODE = {".asf", ".wmv", ".3gp", ".3g2"}

# DISK IMAGE CAPABILITIES (ISO/Archives)
DVD_ISO_TRANSCODE = {".iso", ".img", ".nrg", ".bin", ".cue"}
BD_ISO_TRANSCODE = {".iso", ".udf"} # Distinguishing BD usually requires probe, but we group here

ALL_VIDEO_EXTENSIONS = VIDEO_NATIVE | VIDEO_HD_TRANSCODE | VIDEO_PAL_TRANSCODE | VIDEO_NTSC_TRANSCODE | DVD_ISO_TRANSCODE | BD_ISO_TRANSCODE
VIDEO_EXTENSIONS = ALL_VIDEO_EXTENSIONS

# ADDITIONAL CAPABILITIES (v1.35.98 Centralized)
PICTURE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'
}
ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'
}
DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm'}
EBOOK_EXTENSIONS = {'.epub', '.mobi', '.azw', '.fb2'}
DISK_IMAGE_EXTENSIONS = {'.iso', '.bin', '.img', '.cue', '.nrg', '.mdf', '.toast', '.ccd', '.daa', '.evo', '.map', '.bup'}
PLAYLIST_EXTENSIONS = {'.m3u', '.m3u8'}


# --- ARCHIVE CAPABILITIES (v1.38.02) ---
# These constants define the technical handling requirements for archive files.
# Use uppercase as per architectural standard.
ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"}

try:
    from dotenv import load_dotenv
    _DOTENV_LOADED = True
except ImportError:
    _DOTENV_LOADED = False

# --- PROJECT PATH CALCULATION ---
MAIN_FILE = Path(__file__).resolve()
PROJECT_ROOT = MAIN_FILE.parent.parent.parent
APP_DATA_DIR = str(PROJECT_ROOT) # Standardizing on Project Root as primary data hub

# Ensure project root and scripts are in sys.path (Centralized v1.35.98)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Path Discovery
SCAN_MEDIA_DIR = str(PROJECT_ROOT / "media")
BROWSER_DEFAULT_DIR = str(Path.home())

# Load local environment overrides if available
if _DOTENV_LOADED:
    load_dotenv(PROJECT_ROOT / ".env")

def get_pip_packages():
    """Discover installed python packages."""
    return {d.metadata["Name"]: d.version for d in distributions()}

def get_env_bool(name: str, default: bool) -> bool:
    """Helper to read boolean environment variables."""
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")

def get_env_list(name: str, default: list) -> list:
    """Helper to read list environment variables (comma separated)."""
    val = os.environ.get(name)
    if val is None:
        return default
    return [item.strip() for item in val.split(",")]

def discover_binary(name: str, fallback: str = "") -> str:
    """Safely discover a binary path on the current system."""
    if name == "vlc":
        return shutil.which("vlc") or shutil.which("cvlc") or "/usr/bin/vlc"
    if name == "cvlc":
        return shutil.which("cvlc") or "/usr/bin/cvlc"
    return shutil.which(name) or os.environ.get(f"MWV_PATH_{name.upper().replace('-', '_')}", fallback)

def get_binary_version(path: str, flag: str = "-version") -> str:
    """
    Attempts to extract the version string from an external binary.
    """
    if not path or path == "Unknown": return "N/A"
    try:
        if " " in path:
            # Handle paths with spaces or arguments
            cmd = path.split() + [flag]
        else:
            cmd = [path, flag] # use provided flag
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        combined = (res.stdout or "") + (res.stderr or "")
        
        # Broad patterns for different tools
        patterns = [
            r"version ([0-9\.\-]+)",           # ffmpeg, ffprobe, ffplay, pip
            r"v([0-9\.\-]+)",                  # mkvmerge
            r"VLC version ([0-9\.\-]+)",       # vlc
            r"mpv ([0-9\.\-]+)",               # mpv
            r"MediaInfo Command line, ([0-9\.\-]+)", # mediainfo
            r"isoinfo ([0-9\.\-]+)",            # isoinfo
            r"([0-9]+\.[0-9]+\.[0-9]+)"        # fallback generic semantic version
        ]
        
        for p in patterns:
            match = re.search(p, combined)
            if match: return match.group(1)
            
        # Last resort: take the first non-empty line
        lines = [l.strip() for l in combined.split("\n") if l.strip()]
        if lines:
            # Clean up long lines
            first = lines[0]
            if len(first) > 40: first = first[:37] + "..."
            return first
            
    except Exception:
        pass
    return "Unknown"

# --- VERSION & METADATA CALCULATION (v1.35.68) ---
VERSION_FILE = PROJECT_ROOT / "VERSION"
if VERSION_FILE.exists():
    VERSION = VERSION_FILE.read_text().strip()
else:
    VERSION = "v1.35.68-dev"

# --- NETWORK & HOST CALCULATION ---
APP_PORT = int(os.environ.get("MWV_PORT", 8345))
APP_HOST = os.environ.get("MWV_HOST", "localhost")
BIND_ADDR = os.environ.get("MWV_BIND", "127.0.0.1")

# --- DATABASE PATH RESOLUTION (v1.35.96 Dual-Path logic) ---
DEFAULT_DB_USER = Path.home() / ".media-web-viewer" / "database.db"
DEFAULT_DB_PROJ = PROJECT_ROOT / "data" / "database.db"

if os.environ.get("MWV_DB"):
    SELECTED_DB_PATH = Path(os.environ["MWV_DB"])
elif DEFAULT_DB_USER.exists():
    SELECTED_DB_PATH = DEFAULT_DB_USER
else:
    SELECTED_DB_PATH = DEFAULT_DB_PROJ

# --- GLOBAL CONFIGURATION DICTIONARY ---
from datetime import datetime
GLOBAL_CONFIG: Dict[str, Any] = {
    "version": VERSION,
    "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    
    # --- NETWORK REGISTRY (v1.35.68 Centralized) ---
    "network_settings": {
        "host": APP_HOST,
        "port": APP_PORT,
        "bind_address": BIND_ADDR,
        "api_root": f"http://{BIND_ADDR}:{APP_PORT}"
    },

    # System & Ports
    "port": APP_PORT,
    "vlc_port": int(os.environ.get("MWV_VLC_PORT", 8080)),
    "mtx_port": int(os.environ.get("MWV_MTX_PORT", 8888)),
    "debug_mode": get_env_bool("MWV_DEBUG", True),
    "db_filename": str(SELECTED_DB_PATH),
    "docker_mode": get_env_bool("MWV_DOCKER", False),
    
    # --- LOGGING REGISTRY (v1.35.68 Centralized) ---
    "logging_registry": {
        "log_root": str(PROJECT_ROOT / "logs"),
        "main_log": str(PROJECT_ROOT / "logs" / "media_viewer.log"),
        "session_log": str(PROJECT_ROOT / "logs" / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        "log_level": os.environ.get("MWV_LOG_LEVEL", "INFO"),
        "max_size_mb": int(os.environ.get("MWV_LOG_MAX_SIZE", 10)),
        "backup_count": int(os.environ.get("MWV_LOG_BACKUPS", 3)),
        "debug_force": os.environ.get("MWV_DEBUG_FORCE") == "1",
        "log_datefmt": "%H:%M:%S",
        "debug_max_size_mb": 10,
        "debug_backup_count": 1,
        "watchdog_threshold": 2.0,
        "watchdog_timeout": 60, # Startup watchdog timeout (s)
        "venv_mapping": {
            ".venv_run": "core",
            ".venv_core": "core",
            ".venv_dev": "dev",
            ".venv": "full",
            ".venv_test": "test",
            ".venv_selenium": "selenium",
            ".venv_build": "build"
        },
        "max_buffer_size": 10000        # For UI Log Buffer
    },
    
    # --- UI & NAVIGATION REGISTRY (v1.37.52 Centralized) ---
    "ui_settings": {
        # --- GLOBAL MASTER TOGGLES (Autoritativ) ---
        "master_header_visible": True,       # GLOBAL: Obere Haupt-Navigationsleiste (Kategorien).
        "sub_nav_visible": True,             # GLOBAL: Kontext-Pill-Leiste (Queue, Lyrics).
        "module_tabs_visible": True,         # GLOBAL: Interne Modul-Tabs (Detail-Ansichten).
        "footer_visible": True,              # GLOBAL: Schwebende Media-Steuerung unten.
        "sidebar_allowed": True,             # GLOBAL: Erlaubt die Sidebar-Nutzung generell.
        "sidebar_visible": False,            # GLOBAL: Sidebar Start-Zustand (True=Offen).
        "diagnostics_hud_visible": True,     # GLOBAL: Technisches HUD-Overlay.
        
        # --- FUNKTIONALE MODULE (Engine Toggles) ---
        "audio_engine_enabled": True,       # GLOBAL: Audio-Wiedergabe & Player-Engine.
        "video_engine_enabled": True,       # GLOBAL: Video-Wiedergabe & Cinema-Engine.
        "queue_panel_enabled": True,        # GLOBAL: Media-Queue (Abspielliste).
        "lyrics_panel_enabled": True,       # GLOBAL: Metadaten/Lyrics-Panel.
        "mini_player_allowed": True,        # GLOBAL: Floating Mini-Player.
        "global_search_allowed": True,      # GLOBAL: Suchfunktion im Header.

        # --- BEHAVIOR & THEME ---
        "theme": "dark",                     # Farbschema der Anwendung (Standard: Dark/Glass).
        "animations_enabled": True,          # Steuert flüssige UI-Übergänge und Micro-Animations.
        "sub_nav_persistence": True,         # Behält Sub-Menü Zustände beim Kategorie-Wechsel bei.
        "hydration_mode": "B",               # M=Mock, R=Real, B=Both (Handshake-Modus).
        "professional_layout_lock": True,    # [GUI] Erzwingt Layout-Regeln für Profi-Workspaces.
        "kill_on_startup": True,             # Killt Stale-Prozesse beim Booten.
        "pip_installer_timeout": 300,        # [AUTO] Installations-Timeout in Sekunden.

        # --- UI VISIBILITY MATRIX (v1.37.52 Contextual Logic) ---
        # Verfeinert die Sichtbarkeit pro Kategorie (falls Global-Toggle auf True ist).
        "ui_visibility_matrix": {
            "media":      { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": False },
            "library":    { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": True,  "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "database":   { "master_header": True, "contextual_pill_nav": False, "module_tab_nav": False, "footer_visible": False, "sidebar_allowed": False, "diagnostics_hud_allowed": True, "sidebar_visible": False },
            "file":       { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "edit":       { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "system":     { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "parser":     { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "debug":      { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "tests":      { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "tools":      { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "reporting":  { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "logbuch":    { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "video":      { "master_header": True, "contextual_pill_nav": False, "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True }
        }
    },
    
    # --- DEBUGGING REGISTRY (v1.35.68 Centralized) ---
    
    # --- STREAMING & PIPELINE REGISTRY (v1.35.94 Unified) ---
    "atom_detection": {
        "atoms": ["ftyp", "moov", "moof", "mdat"],
        "header_limit": 4096
    },
    
    "large_file_settings": {
        "threshold_gb": 4.0,           # 4GB Safety Cap (FAT32/Stream limit)
        "warn_only": True,              # Only log warning, don't block
        "enforce_crf_limit": 28,        # Force CRF 28+ for large files to save CPU
        "prefer_copy_if_possible": True # Remux instead of transcode for large MP4/MKV
    },
    
    "transcoding_profiles": {
        # VLC HLS Pipeline Profiles (Content-Aware)
        "vlc_hls_profile_pal": {
            "vcodec": "h264", "v_bitrate": 2000, "acodec": "aac", "a_bitrate": 128,
            "channels": 2, "samplerate": 44100, "seglen": 5, "numseg": 10
        },
        "vlc_hls_profile_hd": {
            "vcodec": "h264", "v_bitrate": 4500, "acodec": "aac", "a_bitrate": 192,
            "channels": 2, "samplerate": 48000, "seglen": 5, "numseg": 10
        },
        "hls_fmp4": {
            "vcodec": "libx264", "preset": "ultrafast", "crf": "28",
            "hls_time": 4, "hls_list_size": 3, "format": "hls"
        },
        # FFmpeg Transcoding Targets (Codec-Specific)
        "transcode_audio_aac": {
            "codec": "aac", "bitrate": "192k", "format": "mp4", 
            "movflags": "frag_keyframe+empty_moov+default_base_moof"
        },
        "transcode_audio_opus": {
            "codec": "libopus", "bitrate": "128k", "format": "webm", "movflags": ""
        },
        "transcode_audio_flac": {
            "codec": "flac", "bitrate": "0", "format": "flac", "movflags": ""
        },
        "transcode_audio_wma": {
            "codec": "libopus", "bitrate": "128k", "format": "webm", "movflags": ""
        },
        "video_transcode": {
            "preset": "veryfast", "crf": "23", "a_codec": "aac", "a_bitrate": "128k",
            "format": "mp4", "movflags": "frag_keyframe+empty_moov+default_base_moof"
        },
        "lossless_remux": {
            "flags": ["-c", "copy", "-f", "mp4", "-movflags", "frag_keyframe+empty_moov+default_base_moof"]
        }
    },
    
    # --- PERFORMANCE & STREAMING (v1.35.94 Centralized) ---
    "perf_settings": {
        "chunk_size": 512 * 1024,        # Standard I/O chunk size
        "buffer_size": 1024 * 1024 * 2,  # 2MB playback buffer
        "streaming_buffer_size": 1024 * 1024, # 1MB FFmpeg/mkvmerge pipe buffer
        "mkvmerge_bufsize": 1024 * 1024,
        "transcoder_log_size": 1000,     # Max lines in task buffer
        "max_concurrent_scans": 4,
        "ffmpeg_threads": 0,              # 0 = auto
        "task_timeout": 900               # Default timeout for long-running tasks (seconds)
    },
    
    # --- UI & UX SETTINGS (v1.35.68 Centralized) ---
    "start_page": os.environ.get("MWV_START_PAGE", "player"),
    "window_width": int(os.environ.get("MWV_WIDTH", 1550)),
    "window_height": int(os.environ.get("MWV_HEIGHT", 800)),
    "boot_watchdog_max_ticks": int(os.environ.get("MWV_WATCHDOG_TICKS", 12)),
    "app_mode": os.environ.get("MWV_APP_MODE", "High-Performance"),
    "bandwidth_mode": os.environ.get("MWV_BANDWIDTH", "high"), # low, high
    "vlc_embedded": get_env_bool("MWV_VLC_EMBEDDED", True),
    "connectionless": get_env_bool("MWV_CONNECTIONLESS", False), 

    "test_engine": os.environ.get("MWV_TEST_ENGINE", "chrome-headless"), # playwright, selenium, chrome-headless
    "headless_mode": get_env_bool("MWV_HEADLESS", True),
    "test_settings": {
        "pytest_cmd": ["pytest", "-q"],
        "python_exe": sys.executable,
        "known_venvs": [".venv_testbed", ".venv_dev", "venv"]
    },
    
    # Parser & Library
    "auto_scan": get_env_bool("MWV_AUTO_SCAN", True),
    "fast_scan": get_env_bool("MWV_FAST_SCAN", True),
    "parser_mode": os.environ.get("MWV_PARSER_MODE", "lightweight"), # lightweight, full, ultimate
    "displayed_categories": ["all", "audio", "video", "pictures", "documents", "ebooks", "disk_images", "spiel", "beigabe", "supplements", "games", "unbekannt"],
    "active_branch": os.environ.get("MWV_BRANCH", "video"), # audio, video
    
    "scan_media_dir": SCAN_MEDIA_DIR,
    "browser_default_dir": BROWSER_DEFAULT_DIR,
    
    "scan_settings": {
        "max_depth": 12,
        "max_files": 50000,
        "exclude_patterns": ["node_modules", ".git", "__pycache__", ".venv"]
    },
    
    # Diagnostic Toggles (v1.35.68 Centered)
    "diag_mode": get_env_bool("MWV_DIAG_MODE", False),
    "raw_mode": get_env_bool("MWV_RAW_MODE", False),
    "bypass_db": get_env_bool("MWV_BYPASS_DB", False),
    "hide_real_db": get_env_bool("MWV_HIDE_DB", False),
    "mock_data_enabled": get_env_bool("MWV_MOCK_ENABLED", False),
    
    # Debugging
    "debug_scan": get_env_bool("MWV_DEBUG_SCAN", True),
    "debug_parser": get_env_bool("MWV_DEBUG_PARSER", False),
    "log_level": os.environ.get("MWV_LOG_LEVEL", "INFO"),
    
    # Legacy Parser Settings (Transferred from format_utils.py)
    "indexed_categories": ["audio", "video", "pictures", "documents", "ebooks", "disk_images", "spiel", "beigabe", "supplements", "games", "unbekannt"],
    "parser_chain": [
        "filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", 
        "pycdlib", "isoparser", "ebml", "mkvparse", "enzyme", "pymkv", 
        "tinytag", "eyed3", "music_tag"
    ],
    "mutagen_prefer_albumartist": True,
    "ffmpeg_deep_analysis": False,
    "browser_flags": [
        "--no-sandbox", 
        "--disable-gpu", 
        f"--window-size={int(os.environ.get('MWV_WIDTH', 1550))},{int(os.environ.get('MWV_HEIGHT', 800))}"
    ],
    
    # Storage & Paths
    "library_dir": os.environ.get("MWV_LIB_DIR", str(PROJECT_ROOT / "media")),
    "additional_scan_dirs": get_env_list("MWV_EXTRA_DIRS", []),
    
    # UI Defaults
    "start_tab": os.environ.get("MWV_START_TAB", "player"), 
    "theme": os.environ.get("MWV_THEME", "dark"),
    
    "active_branch": os.environ.get("MWV_BRANCH", "multimedia"), # audio, multimedia
    
    # Tool & Parser Settings (v1.35.68)
    "parser_settings": {
        "mkvmerge": {"cli_flags": "", "timeout": 10},
        "ffprobe": {"cli_flags": "", "timeout": 10},
        "ffmpeg": {"deep_analysis": False, "timeout": 30},
        "handbrake": {"cli_flags": "--preset 'Fast 1080p30'", "timeout": 3600},
        "vlc": {"timeout": 5},
        "mutagen": {"prefer_albumartist": True},
        "mkvinfo": {"timeout": 10}
    },

    # --- PLAYER & ROUTING SETTINGS (v1.35.94 SSOT) ---
    "player_settings": {
        "force_native_audio": True,
        "media_prefixes": ["/media/", "media/"],
        "video_extensions": list(ALL_VIDEO_EXTENSIONS),
        "disk_image_extensions": [".iso", ".bin", ".img"],
        "audio_extensions": list(ALL_AUDIO_EXTENSIONS),
        "hardware_encoders_priority": ["nvenc", "vaapi", "qsv"]
    },
    
    # Wait & Sleep Intervals (Centralized v1.35.68)
    "sleep_times": {
        "ui_settle": float(os.environ.get("MWV_SLEEP_UI_SETTLE", 2.0)),
        "boot_probe_wait": float(os.environ.get("MWV_SLEEP_BOOT_PROBE", 5.0)),
        "keepalive": float(os.environ.get("MWV_SLEEP_KEEPALIVE", 1.0)),
        "watchdog_tick": float(os.environ.get("MWV_SLEEP_WATCHDOG", 0.5)),
        "retry_delay": float(os.environ.get("MWV_SLEEP_RETRY", 0.5)),
        "poll_fast": float(os.environ.get("MWV_SLEEP_POLL_FAST", 0.1))
    },
    
    # --- EXTERNAL BINARY DISCOVERY (Centralized v1.35.68) ---
    "program_paths": {
        "vlc": discover_binary("vlc", "vlc"),
        "cvlc": discover_binary("cvlc", "cvlc"),
        "ffmpeg": discover_binary("ffmpeg", "ffmpeg"),
        "ffprobe": discover_binary("ffprobe", "ffprobe"),
        "ffplay": discover_binary("ffplay", "ffplay"),
        "handbrake": discover_binary("HandBrakeCLI", "HandBrakeCLI"),
        "mkvmerge": discover_binary("mkvmerge", "mkvmerge"),
        "mkvinfo": discover_binary("mkvinfo", "mkvinfo"),
        "mkvextract": discover_binary("mkvextract", "mkvextract"),
        "mkvpropedit": discover_binary("mkvpropedit", "mkvpropedit"),
        "mediamtx": discover_binary("mediamtx", "mediamtx"),
        "swyh-rs-cli": discover_binary("swyh-rs-cli", "swyh-rs-cli"),
        "spotifyd": discover_binary("spotifyd", "spotifyd"), # Spotify Connect daemon
        "spt": discover_binary("spt", "spt"),           # Spotify TUI for remote control
        "pyvidplayer2": discover_binary("pyvidplayer2", "pyvidplayer2"),
        "mpv": discover_binary("mpv", "mpv"),
        "m3u8": discover_binary("m3u8", "m3u8-tester"),
        "isoinfo": discover_binary("isoinfo", "isoinfo"), # ISO 9660 tool
        "mediainfo": discover_binary("mediainfo", "mediainfo"), # MediaInfo CLI backend
        "docker": discover_binary("docker", "docker"), # Docker CLI
        "doxygen": discover_binary("doxygen", "doxygen"), # documentation
        "graphviz": discover_binary("dot", "dot"), # graphviz
        "chrome": discover_binary("google-chrome", "google-chrome") # playwright/eel backend
    },
    
    # --- STORAGE REGISTRY (v1.35.68 Centralized) ---
    "storage_registry": {
        "project_root": str(PROJECT_ROOT),
        "data_dir": str(PROJECT_ROOT / "data"),
        "media_dir": str(PROJECT_ROOT / "media"),
        "db_path": str(SELECTED_DB_PATH),
        "db_dir": str(PROJECT_ROOT / ".media-web-viewer"), # Potential shadow location
        "logbuch_dir": PROJECT_ROOT / "logbuch",            # Logbuch (.md) root subfolder
        "app_logs_dir": PROJECT_ROOT / "logs",              # System logs root subfolder
        "benchmarks_dir": PROJECT_ROOT / "data" / "benchmarks",
        "playback_benchmark_path": PROJECT_ROOT / "data" / "benchmarks" / "playback.json",
        "system_benchmark_path": PROJECT_ROOT / "data" / "benchmarks" / "system.json",
        "test_results_path": PROJECT_ROOT / "data" / "test_results.json",
        "mkv_cache_dir": PROJECT_ROOT / "cache" / "extracted",
        "media_cache_dir": PROJECT_ROOT / "cache" / "media",
        "config_dir": str(Path.home() / ".config" / "gui_media_web_viewer"),
        "pyproject_file": str(PROJECT_ROOT / "pyproject.toml"),
        "version_file": str(PROJECT_ROOT / "VERSION"),
        "benchmarks_file": str(PROJECT_ROOT / "benchmarks.json"),
        "environment_file": str(PROJECT_ROOT / "infra" / "environment.yml"),
        "version_sync_file": str(PROJECT_ROOT / "infra" / "VERSION_SYNC.json"),
        "probe_log": str(PROJECT_ROOT / "probe_results.log"),
        "audit_log": str(PROJECT_ROOT / "audit_debug.log"),
        "web_config": str(PROJECT_ROOT / "web" / "config.json"),
        "web_config_dev": str(PROJECT_ROOT / "web" / "config.develop.json"),
        "web_config_main": str(PROJECT_ROOT / "web" / "config.main.json"),
        "i18n_file": str(PROJECT_ROOT / "web" / "i18n.json"),
        "test_dir": str(PROJECT_ROOT / "tests"),
        "test_data_dir": str(PROJECT_ROOT / "tests" / "data"),
        "test_engines_dir": str(PROJECT_ROOT / "tests" / "engines"),
        "test_legacy_dir": str(PROJECT_ROOT / "tests" / "legacy"),
        "test_reports_dir": str(PROJECT_ROOT / "tests" / "artifacts"),
        "reference_media": {
            "video": str(PROJECT_ROOT / "tests" / "data" / "reference" / "video.mp4"),
            "audio": str(PROJECT_ROOT / "tests" / "data" / "reference" / "audio.mp3"),
            "iso": str(PROJECT_ROOT / "tests" / "data" / "iso" / "test_disc.iso"),
            "mkv": str(PROJECT_ROOT / "tests" / "data" / "reference" / "test.mkv")
        }
    },
    
    # --- PARSER & UI REGISTRY (v1.35.68 Centralized) ---
    "parser_registry": {
        "start_page": os.environ.get("MWV_START_PAGE", "player"),
        "app_mode": os.environ.get("MWV_APP_MODE", "High-Performance"),
        "playback_mode": os.environ.get("MWV_PLAYBACK_MODE", "hls"),
        "library_dir": str(PROJECT_ROOT / "media"),
        "displayed_categories": ["all", "audio", "video", "pictures", "documents", "ebooks", "disk_images", "spiel", "beigabe", "supplements", "games", "multimedia", "unbekannt"],
        "debug_scan": get_env_bool("MWV_DEBUG_SCAN", False),
        "parser_settings": {
            "use_fast_isoparser": True,
            "extract_tags": True,
            "artwork_extraction": True
        }
    },
    
    # --- SCRIPT & UTILITY REGISTRY (v1.35.68 Centralized) ---
    "script_registry": {
        "control": {
            "super_kill": str(PROJECT_ROOT / "scripts" / "super_kill.py"),
            "reboot": str(PROJECT_ROOT / "scripts" / "reboot_mwv.sh"),
            "status_bar": str(PROJECT_ROOT / "scripts" / "status_bar_utils.py")
        },
        "build": {
            "update_version": str(PROJECT_ROOT / "scripts" / "update_version.py"),
            "cleanup": str(PROJECT_ROOT / "scripts" / "cleanup_mwv.sh"),
            "build_deb": str(PROJECT_ROOT / "scripts" / "fast_build_deb.sh")
        },
        "audit": {
            "dom_audit": str(PROJECT_ROOT / "scripts" / "headless_dom_audit.sh"),
            "playback_verify": str(PROJECT_ROOT / "scripts" / "verify_playback.py"),
            "backend_check": str(PROJECT_ROOT / "scripts" / "check_backend_data.py")
        },
        "data": {
            "seed_data": str(PROJECT_ROOT / "scripts" / "seed_test_data.py"),
            "mock_dvd": str(PROJECT_ROOT / "scripts" / "create_mock_dvd.py")
        }
    },
    "legacy_db_candidates": [
        "~/media_library.db",
        "./media_library.db",
        "./dist/media_library.db",
        "../media_library.db"
    ],

    # --- DIAGNOSTIC & METRIC REGISTRY (v1.35.68 Centralized) ---
    "diagnostic_registry": {
        "benchmarks_enabled": get_env_bool("MWV_BENCHMARKS", True),
        "log_level_registry": {
            "TRACE": 5,
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50
        },
        "quality_score_weights": {
            "resolution": {
                "2160": 50,
                "1080": 40,
                "720": 30,
                "default": 10
            },
            "hdr": 20,
            "audio": {
                "multichannel": 15,
                "stereo": 5
            },
            "extras": {
                "subs": 5,
                "chapters": 10
            }
        }
    },
    
    # --- PLAYBACK & ENGINE SETISTRY (v1.35.68 Centralized) ---
    "playback_registry": {
        "modes": ["direct", "transcode", "hls", "vlc", "mpv", "shuttle", "spotify", "hls_mp4frag"],
        "default_video_mode": "hls",
        "default_audio_mode": "direct",
        "hls_segment_type": "fmp4", # mpegts, fmp4
        "force_native_on": [".mp3", ".mp4", ".m4a", ".wav"],
        "streaming_engines": ["ffmpeg", "vlc", "mediamtx", "swyh-rs", "pyvidplayer2"],
        "hls_mp4frag_enabled": True
        # playability and native registries moved to src/core/models.py (v1.35.77)
    },
    "parser_registry": {
        "default_chain": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "pycdlib", "isoparser", "ebml", "mkvparse", "enzyme", "pymkv", "tinytag", "eyed3", "music_tag"],
        "categories": {
            "audio": ["mutagen", "tinytag", "eyed3", "music_tag"],
            "audio": ["audio"],
            "video": ["container", "mkvmerge", "mkvinfo", "vlc", "isoparser", "pycdlib", "ebml", "mkvparse", "enzyme", "pymkv"],
            "universal": ["filename", "pymediainfo", "ffprobe", "ffmpeg"]
        },
        "magic_signatures": {
            "mkvmerge": "1a45dfa3", "mkvinfo": "1a45dfa3", "mkvparse": "1a45dfa3", "enzyme": "1a45dfa3", "pymkv": "1a45dfa3", "ebml": "1a45dfa3",
            "pycdlib": "4344303031", "isoparser": "4344303031", # CD001
            "dsd": "44534420", "dsf": "44534420", "dff": "46524d38" # DSD, FRM8
        },
        "extension_map": {
            ".mp3":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "eyed3", "music_tag"],
            ".flac": ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
            ".m4a":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
            ".m4b":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
            ".ogg":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
            ".wav":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
            ".wma":  ["filename", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "tinytag", "music_tag"],
            ".mkv":  ["filename", "container", "mkvmerge", "mkvinfo", "vlc", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "ebml", "mkvparse", "enzyme", "pymkv"],
            ".mp4":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "enzyme"],
            ".m4v":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            ".avi":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            ".mov":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            ".webm": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            ".wmv":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            ".mpg":  ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            ".mpeg": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            ".iso":  ["filename", "pycdlib", "isoparser", "pymediainfo", "ffprobe", "ffmpeg"],
            ".bin":  ["filename", "pycdlib", "isoparser", "pymediainfo", "ffprobe", "ffmpeg"],
            ".img":  ["filename", "pycdlib", "isoparser", "pymediainfo", "ffprobe", "ffmpeg"],
            ".pdf":  ["filename", "pymediainfo", "ffprobe"],
            ".epub": ["filename", "pymediainfo", "ffprobe"]
        },
        "codec_map": {
            'mpeg audio': 'mp3',
            'vorbis': 'ogg',
            'opus': 'opus',
            'flac': 'flac',
            'alac': 'alac',
            'aac': 'aac',
            'm4a': 'aac'
        },
        "container_map": {
            'matroska': 'mkv',
            'mov,mp4,m4a,3gp,3g2,mj2': 'mp4',
            'mpeg-4': 'mp4',
            'quicktime': 'mp4',
            'asf': 'wma',
            'ogg': 'ogg',
            'flac': 'flac',
            'mp3': 'mp3'
        },
        "tag_type_map": {
            'ID3': 'ID3',
            'MP4Tags': 'm4tags',
            'OggVComment': 'OggVComment',
            'VCFLACDict': 'VCFLACDict',
            'ASF': 'asf',
            'APETag': 'APEv2'
        }
    },
    "streaming_capabilities": [
        {
            "engine": "Chrome Native",
            "modes": ["Integrated", "Direct"],
            "formats": ["MP4", "WebM", "OGG"],
            "codecs": ["H.264", "VP8", "VP9", "AV1"],
            "features": ["HW Accel", "Low Latency", "Browser Native"],
            "notes": "Best for web-compatible MP4 files. Zero transcoding required."
        },
        {
            "engine": "MediaMTX (mmts)",
            "modes": ["HLS", "WebRTC", "RTSP"],
            "formats": ["MP4", "MKV (via FFmpeg)"],
            "codecs": ["H.264", "AAC"],
            "features": ["Multi-device", "Zero client install", "HTTP Streaming"],
            "notes": "Ideal for streaming to multiple devices over network via FFmpeg remux."
        },
        {
            "engine": "VLC (Universal)",
            "modes": ["External", "VLC.js"],
            "formats": ["ISO", "BIN", "IMG", "MKV", "AVI", "DVD", "VIDEO_TS"],
            "codecs": ["All (H.265, AC3, DTS, etc.)"],
            "features": ["DVD Menus", "Subtitles", "Post-processing"],
            "notes": "Universal player for all file types including disc images and legacy formats."
        },
        {
            "engine": "mkvmerge",
            "modes": ["Remux", "Batch"],
            "formats": ["MKV (Output)", "All (Input)"],
            "codecs": ["Container Shift"],
            "features": ["Sub-track preservation", "Fast remux", "ISO to MKV"],
            "notes": "Used for converting incompatible containers into streamable MKV/MP4."
        },
        {
            "engine": "ffplay",
            "modes": ["CLI Preview"],
            "formats": ["All"],
            "codecs": ["All (FFmpeg-based)"],
            "features": ["Low latency", "Raw decoding", "Debug view"],
            "notes": "Technical fallback for quick local playback verification."
        },
        {
            "engine": "swyh-rs (suw)",
            "modes": ["Audio HTTP", "DLNA"],
            "formats": ["WAV", "FLAC", "LPCM"],
            "codecs": ["Lossless PCM"],
            "features": ["System Audio Capture", "Network Audio"],
            "notes": "Specialized for lossless audio streaming to network devices (Stream What You Hear)."
        },
        {
            "engine": "PyPlayer (Integrated)",
            "modes": ["Direct Python"],
            "formats": ["All (FFmpeg compatible)"],
            "codecs": ["All"],
            "features": ["Zero external dependencies", "Native control"],
            "notes": "Built-in Python-based media engine for fallback and simple playback."
        }
    ],
    
    # --- HARDWARE & APP DISCOVERY (v1.35.68 Centralized) ---
    "hardware_info": _HW_DETECTOR and hardware_detector.get_hardware_info() or {},
    "installed_packages": get_pip_packages(),
    "app_versions": {
        "ffmpeg": get_binary_version("ffmpeg"),
        "ffprobe": get_binary_version("ffprobe"),
        "ffplay": get_binary_version("ffplay"),
        "vlc": get_binary_version("vlc", "--version"),
        "mpv": get_binary_version("mpv", "--version"),
        "mkvmerge": get_binary_version("mkvmerge"),
        "m3u8": get_binary_version("m3u8-tester", "--version"),
        "mediainfo": get_binary_version("mediainfo", "--Version"),
        "isoinfo": get_binary_version("isoinfo", "--version"),
        "swyh-rs-cli": get_binary_version("swyh-rs-cli", "--version"),
        "mediamtx": get_binary_version("mediamtx", "--version"),
        "spotifyd": get_binary_version("spotifyd", "--version"),
        "spt": get_binary_version("spt", "--version"),
        "pyvidplayer2": get_binary_version("pyvidplayer2", "--version"),
        "python": sys.version.split()[0],
        "pip": get_binary_version("pip", "--version").split()[1] if " " in get_binary_version("pip", "--version") else "Unknown",
        "conda": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
        "conda_version": get_binary_version("conda", "--version").split()[-1] if "conda" in get_binary_version("conda", "--version").lower() else "N/A",
        "docker_version": get_binary_version("docker", "--version").split()[-1] if "docker" in get_binary_version("docker", "--version").lower() else "N/A",
        # PIP Packages Version Registry
        "eel": get_binary_version("pip", "show eel").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show eel") else "N/A",
        "bottle": get_binary_version("pip", "show bottle").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show bottle") else "N/A",
        "mutagen": get_binary_version("pip", "show mutagen").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show mutagen") else "N/A",
        "psutil": get_binary_version("pip", "show psutil").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show psutil") else "N/A",
        "gevent": get_binary_version("pip", "show gevent").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show gevent") else "N/A",
        "pytest": get_binary_version("pip", "show pytest").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show pytest") else "N/A",
        # Toolchain Versions
        "doxygen": get_binary_version("doxygen", "--version"),
        "graphviz": get_binary_version("dot", "-V").split()[-1] if "version" in get_binary_version("dot", "-V").lower() else "N/A",
        "chrome": get_binary_version("google-chrome", "--version").split()[-1] if "Google Chrome" in get_binary_version("google-chrome", "--version") else "N/A"
    },
    
    # --- TRANSCODING TOOLCHAIN (v1.35.68 Centralized) ---
    "transcoding_toolchain": {
        "ffmpeg": get_binary_version("ffmpeg"),
        "ffprobe": get_binary_version("ffprobe"),
        "handbrake": get_binary_version("HandBrakeCLI", "--version"),
        "vlc": get_binary_version("vlc", "--version").split()[0] if "VLC" in get_binary_version("vlc", "--version") else "N/A"
    },
    
    # --- PARSING TOOLCHAIN (v1.35.68 Centralized) ---
    "parsing_toolchain": {
        "isoparser": get_binary_version("pip", "show isoparser").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show isoparser") else "N/A",
        "pycdlib": get_binary_version("pip", "show pycdlib").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show pycdlib") else "N/A",
        "ebml": get_binary_version("pip", "show ebml").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show ebml") else "N/A",
        "mkvparse": get_binary_version("pip", "show mkvparse").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show mkvparse") else "N/A",
        "enzyme": get_binary_version("pip", "show enzyme").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show enzyme") else "N/A",
        "pymkv": get_binary_version("pip", "show pymkv").split("Version: ")[1].split("\n")[0] if "Version: " in get_binary_version("pip", "show pymkv") else "N/A",
        "vlc": get_binary_version("vlc", "--version").split()[0] if "VLC" in get_binary_version("vlc", "--version") else "N/A",
        "cvlc": get_binary_version("cvlc", "--version").split()[0] if "VLC" in get_binary_version("cvlc", "--version") else "N/A"
    },
    
    # --- TRANSCODING & ENGINE SETTINGS (v1.35.68 Centralized) ---
    "transcoding_settings": {
        "ffmpeg_preset": os.environ.get("MWV_FFMPEG_PRESET", "veryfast"),
        "video_bitrate": os.environ.get("MWV_VIDEO_BITRATE", "4000k"),
        "audio_bitrate": os.environ.get("MWV_AUDIO_BITRATE", "192k"),
        "hls_time": int(os.environ.get("MWV_HLS_TIME", 2)),
        "hls_list_size": int(os.environ.get("MWV_HLS_LIST_SIZE", 0)),
        "fmp4_frag_duration": int(os.environ.get("MWV_FMP4_FRAG", 5000)), # ms
        "hwaccel": os.environ.get("MWV_HWACCEL", "auto"),
        
        "webm_settings": {
            "v_codec": "libvpx-vp9",
            "v_codec_hw": "vp9_nvenc",
            "crf": "30",
            "bitrate_v": "0",
            "a_codec": "libopus",
            "bitrate_a": "128k",
            "deadline": "realtime",
            "row_mt": "1"
        },
        
        "handbrake_settings": {
            "preset": "fast",
            "a_encoder": "copy",
            "subtitle_scan": True,
            "native_lang": "ger",
            "native_dub": True,
            "markers": True,
            "encoder_map": {
                "nvenc": "nvenc_h264",
                "qsv": "qsv_h264",
                "vaapi": "vaapi_h264",
                "fallback": "x264"
            }
        }
    },
    
    "mediamtx_settings": {
        "host": APP_HOST,
        "hls_port": int(os.environ.get("MWV_MTX_HLS_PORT", 8888)),
        "webrtc_port": int(os.environ.get("MWV_MTX_WEBRTC_PORT", 8889)),
        "rtsp_port": int(os.environ.get("MWV_MTX_RTSP_PORT", 8554))
    },
    
    # --- THIRD-PARTY INTEGRATIONS (v1.35.68 Centralized) ---
    "spotify_settings": {
        "client_id": os.environ.get("SPOTIPY_CLIENT_ID", ""),
        "client_secret": os.environ.get("SPOTIPY_CLIENT_SECRET", ""),
        "redirect_uri": os.environ.get("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback"),
        "device_name": os.environ.get("MWV_SPOTIFY_DEVICE", "MediaWebViewer")
    },
    
    "casting_settings": {
        "discovery_timeout": int(os.environ.get("MWV_CAST_TIMEOUT", 10)),
        "swyh_rs_format": os.environ.get("MWV_SWYH_FORMAT", "flac"),
        "chromecast_name": os.environ.get("MWV_CAST_NAME", "")
    },
    
    # --- BROWSER DISCOVERY LADDER (Centralized v1.35.68) ---
    "browsers": [
        "google-chrome-stable", "google-chrome", "chrome",
        "google-chrome-unstable", "google-chrome-beta",
        "chromium-browser", "chromium",
        "firefox", "firefox-developer-edition", "firefox-esr",
        "msedge", "msedge-dev", "msedge-beta",
        "brave-browser", "brave", "opera", "vivaldi"
    ],
    
    # --- HEADLESS & DIALECT REGISTRY (v1.35.68 Centralized) ---
    "headless_registry": {
        "chrome_flags": ["--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
        "firefox_flags": ["-headless"],
        "app_mode_flags": ["--app={url}", "--window-size={width},{height}", "--no-first-run", "--no-default-browser-check"],
        "window_size": os.environ.get("MWV_WINDOW_SIZE", "1280,720"),
        "user_agent": "MediaWebViewer/1.35 (Headless; Linux)",
        "playwright_path": os.environ.get("PLAYWRIGHT_BROWSERS_PATH", str(PROJECT_ROOT / "bin" / "browsers")),
        "is_headless": get_env_bool("MWV_HEADLESS", True),
        "app_url": f"http://{APP_HOST}:{APP_PORT}"
    },
    
    "headless_tools": {
        "playwright": get_binary_version("playwright", "--version") if "playwright" in get_binary_version("pip", "list") else "N/A",
        "puppeteer": "Available" if "puppeteer" in get_binary_version("npm", "list -g") else "N/A",
        "selenium": "Available" if "selenium" in get_binary_version("pip", "list") else "N/A"
    },
    
    # --- TEMPLATE REGISTRY (v1.35.96 Style Sheets) ---
    "templates": {
        "logbook_entry": {
            "name": "",
            "filename": "",
            "title": "",
            "title_de": "",
            "title_en": "",
            "category": "docs",
            "summary": "",
            "summary_de": "",
            "summary_en": "",
            "status": "docs",
            "source": "root",
            "modified_ts": 0.0,
            "modified_iso": ""
        },
        "test_result": {
            "timestamp": 0.0,
            "duration": 0.0,
            "passes": 0,
            "fails": 0,
            "summary": "",
            "files": []
        },
        "test_file": {
            # Placeholder for future test file style sheet. in code but not centralized. look at legacy tests.
        }
    },

    # End of Registry
}


# SLOW_PARSERS and registries moved to src/core/models.py for Ultimate SSOT (v1.35.76)

def set_config_value(key: str, value: Any):
    """Sets a configuration value dynamically at runtime."""
    if key in GLOBAL_CONFIG:
        # Cast value for boolean types if coming from UI
        if isinstance(GLOBAL_CONFIG[key], bool) and not isinstance(value, bool):
            value = str(value).lower() in ("true", "1", "yes", "on")
        GLOBAL_CONFIG[key] = value
        return True
    return False

def get_config_summary():
    """Returns a summary of the current configuration for display."""
    return GLOBAL_CONFIG
