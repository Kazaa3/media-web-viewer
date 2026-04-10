#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Config Master (Centralized Config & Flag Orchestrator)
v1.41.127-RECOVERY-HARD - Authoritative structural recovery of tiered headers.
"""

# --- v1.41.109/110 Registry (Atomic & Legacy Hybrid) ---
APP_VERSION_CORE = "v1.41.109"
APP_VERSION_FRONTEND = "v1.41.109-ATOMIC-BRIDGE"
APP_VERSION_BACKEND = "v1.41.109-STABLE"
APP_VERSION_FULL = f"{APP_VERSION_CORE}-LEGACY-EVOLVED"

# Legacy Aliases (Fix for Bootstrap ImportErrors)
APP_VERSION = APP_VERSION_FULL
BACKEND_VERSION = APP_VERSION_BACKEND
FRONTEND_VERSION = APP_VERSION_FRONTEND

import os
import sys
import shutil
import re
import subprocess
import eel
from pathlib import Path
from typing import Any, Dict, List
from importlib.metadata import distributions


# --- SSOT: TECHNICAL MEDIA CAPABILITY GROUPS (v1.38.01) ---
AUDIO_NATIVE = {".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac"}
AUDIO_TRANSCODE = {".wav", ".alac", ".wma", ".aiff", ".dsf", ".dff", ".dsd", ".ac3", ".dts"}
ALL_AUDIO_EXTENSIONS = AUDIO_NATIVE | AUDIO_TRANSCODE
AUDIO_EXTENSIONS = ALL_AUDIO_EXTENSIONS

VIDEO_NATIVE = {".mp4", ".webm", ".ogv"}
VIDEO_HD_TRANSCODE = {".mkv", ".mov", ".ts", ".m2ts"}
VIDEO_PAL_TRANSCODE = {".vob", ".mpg", ".mpeg", ".m2v"}
VIDEO_NTSC_TRANSCODE = {".asf", ".wmv", ".3gp", ".3g2"}

DVD_ISO_TRANSCODE = {".iso", ".img", ".nrg", ".bin", ".cue"}
BD_ISO_TRANSCODE = {".iso", ".udf"}

ALL_VIDEO_EXTENSIONS = VIDEO_NATIVE | VIDEO_HD_TRANSCODE | VIDEO_PAL_TRANSCODE | VIDEO_NTSC_TRANSCODE | DVD_ISO_TRANSCODE | BD_ISO_TRANSCODE
VIDEO_EXTENSIONS = ALL_VIDEO_EXTENSIONS

DISK_IMAGE_EXTENSIONS = {'.iso', '.bin', '.img', '.cue', '.nrg', '.mdf', '.toast', '.ccd', '.daa', '.evo', '.map', '.bup'}

PICTURE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'}
ARCHIVE_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'}
DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm'}
EBOOK_EXTENSIONS = {'.epub', '.mobi', '.azw', '.fb2'}
PLAYLIST_EXTENSIONS = {'.m3u', '.m3u8'}

try:
    from dotenv import load_dotenv
    _DOTENV_LOADED = True
except ImportError:
    _DOTENV_LOADED = False

# --- PROJECT PATH CALCULATION ---
MAIN_FILE = Path(__file__).resolve()
PROJECT_ROOT = MAIN_FILE.parent.parent.parent
APP_DATA_DIR = str(PROJECT_ROOT)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

SCAN_MEDIA_DIR = str(PROJECT_ROOT / "media")
BROWSER_DEFAULT_DIR = str(Path.home())

if _DOTENV_LOADED:
    load_dotenv(PROJECT_ROOT / ".env")

def get_pip_packages():
    return {d.metadata["Name"]: d.version for d in distributions()}

def get_env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None: return default
    return val.lower() in ("true", "1", "yes", "on")

def get_env_list(name: str, default: list) -> list:
    val = os.environ.get(name)
    if val is None: return default
    return [item.strip() for item in val.split(",")]

def discover_binary(name: str, fallback: str = "") -> str:
    if name == "vlc": return shutil.which("vlc") or shutil.which("cvlc") or "/usr/bin/vlc"
    if name == "cvlc": return shutil.which("cvlc") or "/usr/bin/cvlc"
    return shutil.which(name) or os.environ.get(f"MWV_PATH_{name.upper().replace('-', '_')}", fallback)

_VERSION_CACHE = {}

def get_binary_version(path: str, flag: str = "-version") -> str:
    if not path or path == "Unknown": return "N/A"
    cache_key = f"{path}_{flag}"
    if cache_key in _VERSION_CACHE: return _VERSION_CACHE[cache_key]
    try:
        cmd = path.split() + [flag] if " " in path else [path, flag]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=1)
        combined = (res.stdout or "") + (res.stderr or "")
        patterns = [r"version ([0-9\.\-]+)", r"v([0-9\.\-]+)", r"VLC version ([0-9\.\-]+)", r"mpv ([0-9\.\-]+)", r"([0-9]+\.[0-9]+\.[0-9]+)"]
        version = "Unknown"
        for p in patterns:
            match = re.search(p, combined)
            if match:
                version = match.group(1)
                break
        _VERSION_CACHE[cache_key] = version
        return version
    except Exception: return "Unknown"

def background_version_discovery(config_dict: dict):
    import threading
    def worker():
        try:
            from core import hardware_detector
            config_dict["hardware_info"] = hardware_detector.get_hardware_info()
        except: config_dict["hardware_info"] = {"type": "Unknown", "encoders": []}
        try: config_dict["installed_packages"] = get_pip_packages()
        except: pass
        targets = [("ffmpeg", "ffmpeg", "-version"), ("vlc", "vlc", "--version"), ("mpv", "mpv", "--version")]
        av = config_dict.get("app_versions", {})
        for key, binary, flag in targets: av[key] = get_binary_version(binary, flag)
    threading.Thread(target=worker, daemon=True).start()

VERSION_FILE = PROJECT_ROOT / "VERSION"
VERSION = VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else "v1.41.00-dev"

APP_PORT = int(os.environ.get("MWV_PORT", 8345))
APP_HOST = os.environ.get("MWV_HOST", "localhost")
BIND_ADDR = os.environ.get("MWV_BIND", "127.0.0.1")

DEFAULT_DB_USER = Path.home() / ".media-web-viewer" / "database.db"
DEFAULT_DB_PROJ = PROJECT_ROOT / "data" / "database.db"
SELECTED_DB_PATH = str(os.environ.get("MWV_DB", DEFAULT_DB_USER if DEFAULT_DB_USER.exists() else DEFAULT_DB_PROJ))

from datetime import datetime
GLOBAL_CONFIG: Dict[str, Any] = {
    "version": VERSION,
    "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "network_settings": {
        "host": APP_HOST, "port": APP_PORT, "bind_address": BIND_ADDR,
        "api_root": f"http://{BIND_ADDR}:{APP_PORT}"
    },
    "port": APP_PORT,
    "vlc_port": int(os.environ.get("MWV_VLC_PORT", 8080)),
    "debug_mode": get_env_bool("MWV_DEBUG", True),
    "db_filename": str(SELECTED_DB_PATH),
    "logging_registry": {
        "log_root": str(PROJECT_ROOT / "logs"),
        "main_log": str(PROJECT_ROOT / "logs" / "media_viewer.log"),
        "log_level": os.environ.get("MWV_LOG_LEVEL", "INFO")
    },
    
    # --- UI & NAVIGATION REGISTRY (v1.41.127 Recovery) ---
    "ui_settings": {
        # --- LEVEL 1: MASTER MENU (Top Header) ---
        "master_header_visible": True,       # GLOBAL: Obere Haupt-Navigationsleiste (Kategorien).
        "header_height": 48,                 # GLOBAL: Höhe des Haupt-Headers (px).
        "header_right_visible": True,        # GLOBAL: Sichtbarkeit der System-Tools oben rechts.
        "header_left_width": "30%",          # GLOBAL: Breite des linken Header-Bereichs (Kategorien).
        "header_right_width": "30%",         # GLOBAL: Breite des rechten Header-Bereichs (Tools).
        "header_center_visible": True,       # GLOBAL: Sichtbarkeit des zentralen Titels.
        
        # --- LEVEL 2: SUB-MENU (Module Tabs) ---
        "sub_menu_visible": True,            # GLOBAL: Sichtbarkeit Level 2 (ehemals module_tabs).
        "sub_menu_height": 32,               # GLOBAL: Höhe Level 2 (px).
        "sub_menu_width": "100%",            # GLOBAL: Breite Level 2 (%/px).
        "sub_menu_offset_left": "0px",       # GLOBAL: Horizontaler Versatz Level 2.

        # --- LEVEL 3: TERTIARY HEADER (Sub-Nav) ---
        "sub_nav_visible": True,             # GLOBAL: Kontext-Pill-Leiste (Queue, Lyrics).
        "sub_nav_height": 35,                # GLOBAL: Höhe der Sub-Nav-Leiste (px).
        "sub_nav_offset_left": "0px",        # GLOBAL: Horizontaler Versatz der Sub-Nav Buttons (px/%).
        "sub_nav_width": "100%",             # GLOBAL: Breite der Sub-Nav Leiste.

        # --- GLOBAL UI ELEMENTS & GEOMETRY ---
        "sidebar_allowed": True,             # GLOBAL: Erlaubt die Sidebar-Nutzung generell.
        "sidebar_visible": False,            # GLOBAL: Sidebar Start-Zustand (True=Offen).
        "sidebar_width": 250,                # GLOBAL: Breite der Sidebar (px).
        "footer_visible": True,              # GLOBAL: Schwebende Media-Steuerung unten.
        "footer_height": 48,                 # GLOBAL: Höhe des Footers (px).
        "diagnostics_hud_visible": True,     # GLOBAL: Technisches HUD-Overlay.
        
        # --- GRANULAR UI FRAGMENT FLAGS ---
        "ui_fragments": {
            "player": True, "library": True, "video": True, "browser": True, "edit": True, 
            "options": True, "parser": True, "debug": True, "tests": True, "tools": True, 
            "reporting": True, "logbuch": True
        },
        
        # --- FUNKTIONALE MODULE (Engine Toggles) ---
        "audio_engine_enabled": True,       # GLOBAL: Audio-Wiedergabe & Player-Engine.
        "video_engine_enabled": True,       # GLOBAL: Video-Wiedergabe & Cinema-Engine.
        "queue_panel_enabled": True,        # GLOBAL: Media-Queue (Abspielliste).
        "lyrics_panel_enabled": True,       # GLOBAL: Metadaten/Lyrics-Panel.
        "mini_player_allowed": True, 
        "global_search_allowed": True,

        # --- BEHAVIOR & THEME ---
        "theme": "dark",
        "animations_enabled": True,
        "sub_nav_persistence": True,
        "force_sub_nav_visible": True,
        "hydration_mode": "B",
        "professional_layout_lock": True,
        "kill_on_startup": False,
        "pip_installer_timeout": 300,

        # --- UI VISIBILITY MATRIX ---
        "ui_visibility_matrix": {
            "media":      { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": True,  "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": False },
            "library":    { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": True,  "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": False },
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
            "video":      { "master_header": True, "contextual_pill_nav": False, "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": True },
            "status":     { "master_header": True, "contextual_pill_nav": True,  "module_tab_nav": False, "footer_visible": True,  "sidebar_allowed": True,  "diagnostics_hud_allowed": True, "sidebar_visible": False }
        },

        # --- SUB-NAVIGATION REGISTRY ---
        "sub_nav_registry": {
            "media": [
                { "id": "warteschlange", "label": "Queue",      "action": "switchPlayerView('warteschlange')" },
                { "id": "playlist",      "label": "Playlist",   "action": "switchPlayerView('playlist')" },
                { "id": "visualizer",    "label": "Visualizer", "action": "switchPlayerView('visualizer')" },
                { "id": "lyrics",       "label": "Lyrics",      "action": "switchPlayerView('lyrics')" }
            ],
            "library": [
                { "id": "lib-cinema", "label": "Cinema",    "action": "switchLibrarySubTab('cinema')" },
                { "id": "lib-films",  "label": "Filme",     "action": "switchLibrarySubTab('films')" }
            ],
            "status": [
                { "id": "logs",     "label": "Live Logs",    "action": "switchDiagnosticsView('logs')" },
                { "id": "health",   "label": "Core Health",  "action": "switchDiagnosticsView('health')" }
            ],
            "system": [
                { "id": "general",      "label": "Allgemein",    "action": "switchOptionsView('general')" },
                { "id": "appearance",   "label": "Darstellung",  "action": "switchOptionsView('appearance')" }
            ]
        }
    },
    
    "atom_detection": {"atoms": ["ftyp", "moov", "moof", "mdat"], "header_limit": 4096},
    "large_file_settings": {"threshold_gb": 4.0, "warn_only": True},
    "transcoding_profiles": {
        "hls_fmp4": {"vcodec": "libx264", "preset": "ultrafast", "crf": "28", "hls_time": 4, "format": "hls"}
    },
    "perf_settings": {"chunk_size": 524288, "buffer_size": 2097152},
    "program_paths": {
        "vlc": discover_binary("vlc"), "ffmpeg": discover_binary("ffmpeg"), "ffprobe": discover_binary("ffprobe")
    },
    "storage_registry": {
        "project_root": str(PROJECT_ROOT), "data_dir": str(PROJECT_ROOT / "data"), "media_dir": str(PROJECT_ROOT / "media")
    },
    "app_versions": {
        "ffmpeg": "N/A", "ffprobe": "N/A", "vlc": "N/A", "python": sys.version.split()[0]
    }
}

def set_config_value(key: str, value: Any):
    if key in GLOBAL_CONFIG:
        if isinstance(GLOBAL_CONFIG[key], bool) and not isinstance(value, bool):
            value = str(value).lower() in ("true", "1", "yes", "on")
        GLOBAL_CONFIG[key] = value
        return True
    return False

def get_config_summary():
    return GLOBAL_CONFIG

background_version_discovery(GLOBAL_CONFIG)
