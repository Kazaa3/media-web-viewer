#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='requests')
dict - Config Master (Centralized Config & Flag Orchestrator)
v1.41.103-SSOT - Unified source of truth for tiered versioning.
"""

# --- v1.46.001 Registry (Tri-Digit Forensic Evolution) ---
APP_VERSION_CORE = "v1.46.017"
APP_VERSION_FRONTEND = "v1.46.017-MASTER-FINAL"
APP_VERSION_BACKEND = "v1.46.017-SUBTYPE-ALIGN"
# Created with MWV v1.46.017-MASTER
APP_VERSION_FULL = f"{APP_VERSION_CORE}-EVO-STABLE"

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

# DISK IMAGE CAPABILITIES (Others)
DISK_IMAGE_EXTENSIONS = {'.iso', '.bin', '.img', '.cue', '.nrg', '.mdf', '.toast', '.ccd', '.daa', '.evo', '.map', '.bup'}

# ADDITIONAL CAPABILITIES (v1.35.98 Centralized)
PICTURE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'
}
ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'
}
DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm'}
EBOOK_EXTENSIONS = {'.epub', '.mobi', '.azw', '.fb2'}

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

# --- VERSION DISCOVERY OPTIMIZATION (v1.41.00) ---
_VERSION_CACHE = {}

def get_binary_version(path: str, flag: str = "-version") -> str:
    """
    Attempts to extract the version string from an external binary.
    Uses a cache to speed up repeated lookups.
    """
    if not path or path == "Unknown": return "N/A"
    
    cache_key = f"{path}_{flag}"
    if cache_key in _VERSION_CACHE:
        return _VERSION_CACHE[cache_key]

    # If we are in synchronous mode (startup), we might want to return 'Discovering...'
    # For now, we allow the first call to be potentially blocking, 
    # but the goal is to background them.
    try:
        if " " in path:
            cmd = path.split() + [flag]
        else:
            cmd = [path, flag]
            
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=1)
        combined = (res.stdout or "") + (res.stderr or "")
        
        patterns = [
            r"version ([0-9\.\-]+)",
            r"v([0-9\.\-]+)",
            r"VLC version ([0-9\.\-]+)",
            r"mpv ([0-9\.\-]+)",
            r"MediaInfo Command line, ([0-9\.\-]+)",
            r"isoinfo ([0-9\.\-]+)",
            r"([0-9]+\.[0-9]+\.[0-9]+)"
        ]
        
        version = "Unknown"
        for p in patterns:
            match = re.search(p, combined)
            if match:
                version = match.group(1)
                break
        
        if version == "Unknown" and combined.strip():
            lines = [l.strip() for l in combined.split("\n") if l.strip()]
            if lines:
                version = lines[0][:37] + "..." if len(lines[0]) > 40 else lines[0]
        
        _VERSION_CACHE[cache_key] = version
        return version
            
    except Exception:
        return "Unknown"

def background_version_discovery(config_dict: dict):
    """
    Worker thread that populates the version information, hardware info, and packages in the background.
    """
    import threading
    def worker():
        try:
            from core.startup_monitor import profiler
            if profiler: profiler.start_phase("Background-Discovery")
        except: profiler = None
        
        # 1. Hardware Info (Previously synchronous bottleneck)
        try:
            # Atomic Bridge v1.41.111: Lazy local import to break cyclic dependency
            from core import hardware_detector
            config_dict["hardware_info"] = hardware_detector.get_hardware_info()
        except ImportError:
            config_dict["hardware_info"] = {"type": "Unknown", "encoders": []}
        except Exception as e:
            print(f"STDOUT: [Background-Discovery] Hardware detection failed: {e}")

        # 2. Package Info (Previously synchronous bottleneck)
        try:
            config_dict["installed_packages"] = get_pip_packages()
        except Exception as e:
            print(f"STDOUT: [Background-Discovery] Package discovery failed: {e}")

        # 3. Binary Versions
        targets = [
            ("ffmpeg", "ffmpeg", "-version"),
            ("ffprobe", "ffprobe", "-version"),
            ("ffplay", "ffplay", "-version"),
            ("vlc", "vlc", "--version"),
            ("mpv", "mpv", "--version"),
            ("mkvmerge", "mkvmerge", "-version"),
            ("m3u8", "m3u8-tester", "--version"),
            ("mediainfo", "mediainfo", "--Version"),
            ("isoinfo", "isoinfo", "--version"),
            ("swyh-rs-cli", "swyh-rs-cli", "--version"),
            ("mediamtx", "mediamtx", "--version"),
            ("spotifyd", "spotifyd", "--version"),
            ("spt", "spt", "--version"),
            ("pyvidplayer2", "pyvidplayer2", "--version"),
            ("doxygen", "doxygen", "--version"),
            ("graphviz", "dot", "-V")
        ]
        
        av = config_dict.get("app_versions", {})
        for key, binary, flag in targets:
            av[key] = get_binary_version(binary, flag)
            
        try:
            if profiler: profiler.end_phase("Background-Discovery")
        except: pass

    threading.Thread(target=worker, daemon=True).start()

# --- VERSION & METADATA CALCULATION (v1.41.00) ---
VERSION_FILE = PROJECT_ROOT / "VERSION"
if VERSION_FILE.exists():
    VERSION = VERSION_FILE.read_text().strip()
else:
    VERSION = "v1.41.00-dev"

# --- NETWORK & HOST CALCULATION ---
APP_PORT = int(os.environ.get("MWV_PORT", 8345))
APP_HOST = os.environ.get("MWV_HOST", "localhost")
BIND_ADDR = os.environ.get("MWV_BIND", "127.0.0.1")

# --- DATABASE PATH RESOLUTION (v1.35.96 Dual-Path logic) ---
DEFAULT_DB_USER = Path.home() / ".media-web-viewer" / "database.db"
DEFAULT_DB_PROJ = PROJECT_ROOT / "data" / "database.db"

if os.environ.get("MWV_DB"):
    SELECTED_DB_PATH = str(Path(os.environ["MWV_DB"]))
elif DEFAULT_DB_USER.exists():
    SELECTED_DB_PATH = str(DEFAULT_DB_USER)
else:
    SELECTED_DB_PATH = str(DEFAULT_DB_PROJ)

# Final Path Enforcement (v1.41.00 Strings for JSON parity)
SELECTED_DB_PATH = str(SELECTED_DB_PATH)

# --- GLOBAL CONFIGURATION DICTIONARY ---
from datetime import datetime
GLOBAL_CONFIG: Dict[str, Any] = {
    "version": VERSION,
    "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "branch_id": os.environ.get("MWV_BRANCH", "multimedia"),
    "orchestrator_version": "v1.46.017-MASTER",
    "build_id": "STABLE-FORENSIC-2026-04-12",
    "build_link_template": "./dist/MediaWebViewer-{{BUILD_ID}}-{{VERSION}}.exe",
    "release_channel": "development",
    
    # --- NETWORK REGISTRY (v1.41.00 Centralized) ---
    "network_settings": {
        "host": APP_HOST,
        "port": APP_PORT,
        "bind_address": BIND_ADDR,
        "api_root": f"http://{BIND_ADDR}:{APP_PORT}"
    },

    # --- VISUALIZER ORCHESTRATION (v1.46.10) ---
    "visualizer_orchestration": {
        "animation_enabled": True,      # Global Toggle
        "default_style": "bars",        # "bars", "circle", "wave"
        "accent_color": "#007aff",      # Reference Blue (Legacy Accent)
        "use_ui_accent": True           # If True, overrides accent_color with UI theme color
    },
    
    # --- EVOLUTION & SAFETY REGISTRY (v1.45 Reconstruction) ---
    "ui_evolution_mode": "stable",   # [v1.45] OPTIONS: "stable", "rebuild", "bridge", "test_ref"
    "unicode_safety_mode": False,   # If True, strips/tags emojis
    "unicode_safety_map": {
        "☢️": "[NUCLEAR]", "✅": "[SUCCESS]", "❌": "[ERROR]", 
        "⚠️": "[WARNING]", "🚀": "[STARTUP]", "⚡": "[ACTIVE]"
    },

    # System & Ports
    "port": APP_PORT,
    "vlc_port": int(os.environ.get("MWV_VLC_PORT", 8080)),
    "mtx_port": int(os.environ.get("MWV_MTX_PORT", 8888)),
    "debug_mode": get_env_bool("MWV_DEBUG", True),
    "db_filename": str(SELECTED_DB_PATH),
    "docker_mode": get_env_bool("MWV_DOCKER", False),
    "hardware_info": {"type": "Awaiting discovery...", "encoders": []},
    "installed_packages": {},
    "enable_collection_management": True, # GLOBAL: Automatische Ordner-Gruppierung. Filmname (Jahr),  Albumartist - Name (Jahr) und Serien werden automatisch erkannt.
    "enable_nfo_parsing": True,          # GLOBAL: XML-Extraktion aus .nfo Dateien.
    
    # --- LOGGING REGISTRY (v1.41.168 Forensic Evolution) ---
    "logging_registry": {
        "log_root": str(PROJECT_ROOT / "logs"),
        "enable_main_log": True,        # Global app.log
        "enable_debug_log": True,       # Detailed debug.log
        "enable_session_log": True,     # Persistent session-specific log
        "enable_symlink": True,         # logs/current -> session_folder
        "use_session_subfolders": True, # logs/<session_id>/...
        "enable_ui_console": True,      # Real-time UI log buffer
        "session_id_format": "{timestamp}_{pid}", # e.g. 1775416263_1001527 for sorting
        
        "main_log": str(PROJECT_ROOT / "logs" / "media_viewer.log"),
        "session_log_name": "session.log", # Named app.log inside subfolder
        
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
        # --- LEVEL 1: MASTER MENU (Top Header) ---
        "master_header_visible": True,       # GLOBAL: Obere Haupt-Navigationsleiste (Kategorien).
        "header_height": 48,                 # GLOBAL: Höhe des Haupt-Headers (px).
        "header_right_visible": True,        # GLOBAL: Sichtbarkeit der System-Tools oben rechts.
        "header_left_width": "30%",          # GLOBAL: Breite des linken Header-Bereichs (Kategorien).
        "header_right_width": "30%",         # GLOBAL: Breite des rechten Header-Bereichs (Tools).
        "header_center_visible": True,       # GLOBAL: Sichtbarkeit des zentralen Titels.
        
        # --- [v1.46.02] FORENSIC GLOBAL SIDEBAR (3-Column Architecture) ---
        "forensic_sidebar_enabled": True,    # GLOBAL: Ob die linke Forensik-Leiste existiert.
        "forensic_sidebar_visible": True,    # DEFAULT: Ob die Leiste beim Start offen ist.
        "forensic_sidebar_width": 280,       # GLOBAL: Breite in Pixeln.
        "forensic_sidebar_behavior": "persistent", # OPTIONS: "persistent", "contextual", "hidden"
        
        # [v1.45.150] ACTIVATE FORENSIC WORKSTATION for modern categories (v1.45.300 Realignment)
        # if (['audio', 'multimedia', 'extended'].includes(category)) {
        #     if (window.MWV_Workstation) window.MWV_Workstation.activate();
        # }
        
        "navigation_orchestrator": {
            "aliases": {
                "player": "media", "bibliothek": "library", "database": "database", "explorer": "library",
                "tools": "tools", "debug": "debug", "diagnostics": "status", "optionen": "system",
                "report": "reporting", "reporting_dashboard": "reporting", "file": "file", "edit": "edit",
                "parser": "parser", "logbuch": "logbuch", "video": "video", "tests": "tests", "status": "status",
                "audio": "media", "audio_native": "media", "audio_transcode": "media", "album": "media",
                "single": "media", "hörbuch": "media", "sampler": "media", "soundtrack": "media",
                "video_iso": "media", "bilder": "media", "epub": "media"
            },
            "level_1": [
                {"id": "audio",      "label": "AUDIO",      "icon": "play",   "action": "audio"},
                {"id": "multimedia", "label": "MULTIMEDIA", "icon": "grid",   "action": "multimedia"},
                {"id": "extended",   "label": "EXTENDED",   "icon": "folder", "action": "extended"},
                {"id": "tools", "label": "TOOLS", "icon": "tool", "action": "tools"},
                {"id": "status", "label": "STATUS", "icon": "sparkles", "action": "status", "color": "#00ffcc"}
            ],
            "level_2": {
                "audio": [
                    {"id": "warteschlange", "label": "Queue", "action": "switchPlayerView('warteschlange')"},
                    {"id": "playlist", "label": "Playlist", "action": "switchPlayerView('playlist')"},
                    {"id": "lyrics", "label": "Lyrics", "action": "switchPlayerView('lyrics')"}
                ],
                "multimedia": [
                    {"id": "coverflow", "label": "Gallery", "action": "let librarySubTab = localStorage.getItem('mwv_multimedia_sub_tab') || 'coverflow'; switchLibrarySubTab(librarySubTab);"},
                    {"id": "table", "label": "Technical List", "action": "switchLibrarySubTab('table')"}
                ],
                "status": [
                    {"id": "health", "label": "Health", "action": "switchDiagnosticsTab('health')"},
                    {"id": "recovery", "label": "Recovery", "action": "switchDiagnosticsTab('recovery')"}
                ],
                "tools": [
                    {"id": "dashboard", "label": "Dashboard", "action": "switchToolsTab('dashboard')"},
                    {"id": "parser", "label": "Parser", "action": "switchToolsTab('parser')"}
                ]
            },
            "level_4": {
                "films":      {"fragment": "fragments/film_view.html",      "init": "initFilmsView"},
                "series":     {"fragment": "fragments/serie_view.html",     "init": "initSeriesView"},
                "albums":     {"fragment": "fragments/album_view.html",     "init": "initAlbumsView"},
                "audiobooks": {"fragment": "fragments/audiobook_view.html", "init": "initAudiobooksView"},
                "cinema":     {"fragment": "fragments/video_view.html",     "init": "initCinemaView"}
            },
            "fragment_hydration": {
                "modals": {"id": "diagnostics-overlay-container", "path": "fragments/diagnostics_sidebar.html"},
                "modals-res": {"id": "modals-placeholder", "path": "fragments/modals_container.html"},
                "player-tabs": {"id": "player-sub-nav-shell", "path": "app.html (inline)"},
                "player-engine": {"id": "player-main-viewport", "path": "fragments/player_queue.html"},
                "player-sidebar": {"id": "player-detailed-sidebar", "path": "app.html (inline)"},
                "player-view-lyrics": {"id": "player-view-lyrics", "path": "fragments/player_queue.html"},
                "library": {"id": "library-main-viewport", "path": "fragments/library_explorer.html"},
                "database": {"id": "database-panel-container", "path": "fragments/database_panel.html"},
                "editor": {"id": "metadata-writer-crud-panel", "path": "fragments/metadata_editor.html"},
                "icons": {"id": "svg-icons-placeholder", "path": "fragments/icons.html"},
                "menus": {"id": "context-menu-placeholder", "path": "fragments/context_menu.html"}
            },
            "diagnostic_sidebar_orchestrator": [
                {"id": "health", "label": "HLT", "title": "Global Health Readiness"},
                {"id": "log", "label": "LOG", "title": "Main System Log"},
                {"id": "item-track", "label": "TRK", "title": "Media Item Tracker"},
                {"id": "sentinel", "label": "SNT", "title": "UI Sentinel Monitor", "color": "#00ffcc"},
                {"id": "debug-db", "label": "DB", "title": "Database Debugger"},
                {"id": "logs", "label": "LOG", "title": "Detailed Trace Logs"},
                {"id": "video-health", "label": "VID", "title": "Video Pipeline Status"},
                {"id": "recovery", "label": "REC", "title": "Forensic Recovery Hub"},
                {"id": "env", "label": "ENV", "title": "Software Stack Audit"},
                {"id": "storage", "label": "STR", "title": "Storage & VFS Check"},
                {"id": "performance", "label": "PER", "title": "Performance Analytics"},
                {"id": "playlist", "label": "PLY", "title": "Playlist Engine Health"},
                {"id": "state", "label": "STA", "title": "Application State Dump"},
                {"id": "network", "label": "NET", "title": "Network & Eel Handshake"},
                {"id": "process", "label": "PRC", "title": "Background Worker Audit"},
                {"id": "driver", "label": "DRV", "title": "Hardware Driver Status"},
                {"id": "security", "label": "SEC", "title": "Permissions & Security"},
                {"id": "api", "label": "API", "title": "Backend API Observer"},
                {"id": "config", "label": "CFG", "title": "Registry Live Toggles", "color": "#ff3366"},
                {"id": "boot", "label": "BOOT", "title": "System Startup Timeline", "color": "#00ffcc"},
                {"id": "hydration-audit", "label": "HYD", "title": "DOM Hydration Integrity", "color": "#ff9500"}
            ]
        },

        # --- [v1.46.017] TECHNICAL & DIAGNOSTIC ORCHESTRATOR ---
        "technical_orchestrator": {
            "intervals": {
                "log_polling_ms": 1000,
                "hydration_audit_ms": 2000,
                "heartbeat_pulse_ms": 5000,
                "sentinel_audit_ms": 1000,
                "recovery_pulse_ms": 1000,
                "dom_hud_update_ms": 2000,
                "ui_broadcast_cooldown_ms": 20,
                "video_stats_update_ms": 1000
            },
            "logging": {
                "max_buffer_size": 10000,
                "unicode_safety_mode": True,
                "enable_ui_console": True
            },
            "hydration": {
                "mock_count": 12,
                "auto_hydrate_enabled": True
            },
            "watchdog": {
                "tick_ms": 500,
                "max_ticks": 12,
                "stall_threshold_s": 2.0
            }
        },

        # --- [v1.46.017] LEVEL 4: SUB-NAV ORCHESTRATOR (Nuclear SSOT) ---
        "sub_nav_orchestrator": {
            "aliases": {
                "player": "media", "bibliothek": "library", "database": "database", "explorer": "library",
                "tools": "tools", "debug": "debug", "diagnostics": "status", "optionen": "system",
                "report": "reporting", "reporting_dashboard": "reporting", "file": "file", "edit": "edit",
                "parser": "parser", "logbuch": "logbuch", "video": "video", "tests": "tests", "status": "status",
                "audio": "media", "audio_native": "media", "audio_transcode": "media", "album": "media",
                "single": "media", "hörbuch": "media", "sampler": "media", "soundtrack": "media",
                "video_iso": "media", "bilder": "media", "epub": "media"
            },
            "registry": {
                "media": [
                    {"id": "warteschlange", "label": "Queue", "action": "switchPlayerView('warteschlange')"},
                    {"id": "playlist", "label": "Playlist Manager", "action": "switchPlayerView('playlist')"},
                    {"id": "visualizer", "label": "Visualizer", "action": "switchPlayerView('visualizer')"},
                    {"id": "lyrics", "label": "Lyrics", "action": "switchPlayerView('lyrics')"},
                    {"id": "video-cinema", "label": "Video Cinema", "action": "switchMediaSubView('video')"}
                ],
                "library": [
                    {"id": "lib-visual", "label": "Visual Explorer", "action": "switchLibrarySubView('visual')"},
                    {"id": "lib-browse", "label": "FileSystem Browse", "action": "switchLibrarySubView('browse')"},
                    {"id": "lib-inventory", "label": "Database Inventory", "action": "switchLibrarySubView('inventory')"},
                    {"id": "lib-cinema", "label": "Cinema View", "action": "switchLibrarySubTab('cinema')"},
                    {"id": "lib-films", "label": "Filme / Movie", "action": "switchLibrarySubTab('films')"},
                    {"id": "lib-series", "label": "Serien / TV", "action": "switchLibrarySubTab('series')"}
                ],
                "database": [
                    {"id": "db-explorer", "label": "DB Explorer", "action": "switchLibrarySubView('inventory')"},
                    {"id": "db-integrity", "label": "Integrity Check", "action": "runNuclearDiagnostics()"},
                    {"id": "db-sync", "label": "Atomic Sync", "action": "triggerDeepSync()"},
                    {"id": "db-recovery", "label": "Recovery Hub", "action": "switchDiagnosticsSubView('recovery')"}
                ],
                "status": [
                    {"id": "status-health", "label": "Core Health", "action": "switchDiagnosticsSubView('health')"},
                    {"id": "status-logs", "label": "Live Logs", "action": "switchDiagnosticsSubView('logs')"},
                    {"id": "status-net", "label": "Network/Eel", "action": "switchDiagnosticsSubView('network')"},
                    {"id": "status-latency", "label": "Logic Latency", "action": "switchDiagnosticsSubView('latency')"}
                ],
                "file": [
                    {"id": "file-local", "label": "Lokale Medien", "action": "switchFileSubView('local')"},
                    {"id": "file-network", "label": "Netzwerk / SMB", "action": "switchFileSubView('network')"},
                    {"id": "file-mounted", "label": "Eingehängte Drv", "action": "switchFileSubView('mounted')"}
                ],
                "edit": [
                    {"id": "edit-basic", "label": "Basic Metadata", "action": "switchEditSubView('basic')"},
                    {"id": "edit-tech", "label": "Technical Specs", "action": "switchEditSubView('technical')"},
                    {"id": "edit-ffprobe", "label": "FFprobe Dump", "action": "switchEditSubView('ffprobe')"},
                    {"id": "edit-album", "label": "Artwork Editor", "action": "switchEditSubView('artwork')"}
                ],
                "system": [
                    {"id": "sys-general", "label": "Allgemein", "action": "switchOptionsView('general')"},
                    {"id": "sys-parser", "label": "Parser Chain", "action": "switchOptionsView('parser')"},
                    {"id": "sys-trans", "label": "Transcoding", "action": "switchOptionsView('transcoding')"},
                    {"id": "sys-env", "label": "Environments", "action": "switchOptionsView('environment')"},
                    {"id": "sys-helpers", "label": "Helper Scripts", "action": "switchOptionsView('helpers')"}
                ],
                "parser": [
                    {"id": "px-chain", "label": "Main Chain", "action": "switchParserView('main')"},
                    {"id": "px-extraction", "label": "Extraction Log", "action": "switchParserView('extraction')"},
                    {"id": "px-bench", "label": "Benchmarking", "action": "switchParserView('benchmark')"}
                ],
                "debug": [
                    {"id": "dbg-sentinel", "label": "UI Sentinel", "action": "switchDiagnosticsSubView('sentinel')"},
                    {"id": "dbg-audit", "label": "Forensic Audit", "action": "switchDiagnosticsSubView('audit')"},
                    {"id": "dbg-state", "label": "AppState Dump", "action": "switchDiagnosticsSubView('state')"}
                ],
                "tests": [
                    {"id": "test-suite", "label": "Active Suite", "action": "switchTestView('suite')"},
                    {"id": "test-scripts", "label": "Test Scripts", "action": "switchTestView('scripts')"},
                    {"id": "test-regress", "label": "Regression", "action": "switchTestView('regression')"}
                ],
                "tools": [
                    {"id": "tool-set", "label": "System Toolset", "action": "switchToolsSubView('main')"},
                    {"id": "tool-workers", "label": "Active Workers", "action": "switchToolsSubView('workers')"},
                    {"id": "tool-pipelines", "label": "AV Pipelines", "action": "switchToolsSubView('pipelines')"}
                ],
                "reporting": [
                    {"id": "rep-overview", "label": "Overview", "action": "switchReportingView('dashboard')"},
                    {"id": "rep-perf", "label": "Performance", "action": "switchReportingView('performance')"},
                    {"id": "rep-errors", "label": "Error Analytics", "action": "switchReportingView('errors')"}
                ],
                "logbuch": [
                    {"id": "log-project", "label": "Projekt Log", "action": "switchLogbookSubView('project')"},
                    {"id": "log-audit", "label": "Audit History", "action": "switchLogbookSubView('audit')"},
                    {"id": "log-feature", "label": "Feature Status", "action": "toggleFeatureStatus()"}
                ],
                "video": [
                    {"id": "vid-cinema", "label": "Cinema Cinema", "action": "switchMediaSubView('video')"},
                    {"id": "vid-accel", "label": "HW Acceleration", "action": "switchMediaSubView('visualizer')"},
                    {"id": "vid-stream", "label": "Stream Relay", "action": "switchOptionsView('transcoding')"}
                ],
                "unsort": [
                    {"id": "unsort-probe", "label": "Deep Probe Hub", "action": "runHydrationAuditProbe()"},
                    {"id": "unsort-sync", "label": "Force Database Sync", "action": "if(window.triggerMasterSync) window.triggerMasterSync()"},
                    {"id": "unsort-ui", "label": "UI Refresh", "action": "refreshViewportLayout()"},
                    {"id": "unsort-log", "label": "System Log", "action": "switchMainCategory('logbuch')"},
                    {"id": "unsort-audit", "label": "System Audit", "action": "openDiagnosticsTab('status')"}
                ]
            }
        },

        # --- [v1.45.300] LIBRARY SIDEBAR ORCHESTRATOR ---
        "library_sidebar_orchestrator": {
            "visible": True,
            "width": 280,
            "sections": [
                {
                    "id": "overview",
                    "label": "Übersicht",
                    "i18n": "sb_overview",
                    "items": [
                        {"id": "overview",   "label": "Alle Medien", "icon": "grid",   "action": "switchLibrarySubTab('coverflow')"},
                        {"id": "cinema",     "label": "Cinema",      "icon": "video",  "action": "switchLibrarySubTab('cinema')"},
                        {"id": "films",      "label": "Filme / Movie", "icon": "film", "action": "switchLibrarySubTab('films')"},
                        {"id": "series",     "label": "Serien",      "icon": "tv",     "action": "switchLibrarySubTab('series')"},
                        {"id": "albums",     "label": "Alben",       "icon": "disc",   "action": "switchLibrarySubTab('albums')"},
                        {"id": "audiobooks", "label": "Hörbuch",     "icon": "book",   "action": "switchLibrarySubTab('audiobooks')"},
                        {"id": "pictures",   "label": "Bilder",      "icon": "image",  "action": "switchLibrarySubTab('pictures')"},
                        {"id": "documents",  "label": "Dokumente",   "icon": "file",   "action": "switchLibrarySubTab('documents')"}
                    ]
                },
                {
                    "id": "views",
                    "label": "Ansichten",
                    "i18n": "sb_views",
                    "items": [
                        {"id": "coverflow", "label": "Coverflow", "icon": "layout",   "action": "switchLibrarySubTab('coverflow')"},
                        {"id": "grid",      "label": "Grid",      "icon": "grid",     "action": "switchLibrarySubTab('grid')"},
                        {"id": "details",   "label": "Details",   "icon": "list",     "action": "switchLibrarySubTab('details')"},
                        {"id": "streaming", "label": "Streaming", "icon": "play",     "action": "switchLibrarySubTab('streaming')"}
                    ]
                }
            ]
        },

        # --- [v1.45.117] GLOBAL ARCHITECTURE REGISTRIES ---
        "library_category_map": [
            {"id": "all",             "label": "ALLE MEDIEN"},
            {"id": "audio",           "label": "audio"},
            {"id": "audio_native",    "label": "audio_native"},
            {"id": "audio_transcode", "label": "audio_transcode"},
            {"id": "album",           "label": "album"},
            {"id": "single",          "label": "single"},
            {"id": "hörbuch",         "label": "hörbuch"},
            {"id": "sampler",         "label": "sampler"},
            {"id": "compilation",     "label": "compilation"},
            {"id": "podcast",         "label": "podcast"},
            {"id": "soundtrack",      "label": "soundtrack"},
            {"id": "klassik",         "label": "klassik"},
            {"id": "video",           "label": "video"},
            {"id": "video_iso",       "label": "iso-image"},
            {"id": "series",          "label": "serie"},
            {"id": "documentation",   "label": "dokumentation"},
            {"id": "bilder",          "label": "bilder"},
            {"id": "pictures",        "label": "bilder"},
            {"id": "epub",            "label": "epub"},
            {"id": "ebooks",          "label": "ebooks"},
            {"id": "docs",            "label": "dokumente"},
            {"id": "documents",       "label": "dokumente"},
            {"id": "archives",        "label": "archiv"},
            {"id": "disk_images",     "label": "disk_images"},
            {"id": "spiel",           "label": "spiel / games"},
            {"id": "games",           "label": "spiel / games"},
            {"id": "beigabe",         "label": "beigabe"},
            {"id": "supplements",     "label": "supplements"},
            {"id": "nfo",             "label": "nfo"},
            {"id": "unknown",         "label": "unbekannt"},
            {"id": "unbekannt",       "label": "unbekannt"}
        ],

        "branch_architecture_registry": {
            "audio":      ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "compilation", "podcast", "soundtrack", "klassik"],
            "multimedia": ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "compilation", "podcast", "soundtrack", "klassik", "video", "video_iso", "series", "documentation", "bilder", "epub", "pictures", "ebooks", "spiel", "beigabe"],
            "extended":   ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "compilation", "podcast", "soundtrack", "klassik", "video", "video_iso", "series", "documentation", "bilder", "epub", "docs", "archives", "nfo", "unknown", "pictures", "ebooks", "documents", "disk_images", "spiel", "games", "beigabe", "supplements", "unbekannt"],
            
            # Legacy/View Aliases (Redirecting frontend view IDs to branch identity)
            "media":      ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "soundtrack", "klassik", "video", "video_iso", "series", "documentation", "bilder", "epub", "docs", "archives", "unknown", "spiel"], 
            "library":    ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "soundtrack", "klassik", "video", "video_iso", "series", "documentation", "bilder", "epub", "docs", "archives", "unknown", "spiel"],
            "database":   ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "soundtrack", "klassik", "video", "video_iso", "series", "documentation", "bilder", "epub", "docs", "archives", "unknown", "spiel"],
            "player":     ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "soundtrack", "klassik", "video", "video_iso", "series", "documentation", "bilder", "epub", "docs", "archives", "unknown", "spiel"],
            "explorer":   ["all", "audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "soundtrack", "klassik", "video", "video_iso", "series", "documentation", "bilder", "epub", "docs", "archives", "unknown", "spiel"]
        },

        # --- [v1.46.00] BRANCH IDENTITY & BUILD REGISTRY ---
        "branch_identity_registry": {
            "audio":      {"label": "BUILD: AUDIO ONLY", "build_id": "MWV-A", "color": "#007aff"},
            "multimedia": {"label": "BUILD: MULTIMEDIA", "build_id": "MWV-M", "color": "#00ffcc"},
            "extended":   {"label": "BUILD: EXTENDED",   "build_id": "MWV-E", "color": "#ff9500"}
        },


        # --- LEVEL 2: CONTEXTUAL PILLS (Sub-Nav) ---
        "sub_nav_visible": True,             # GLOBAL: Kontext-Pill-Leiste (Queue, Lyrics).
        "sub_nav_height": 35,                # GLOBAL: Höhe der Sub-Nav-Leiste (px).
        "sub_nav_offset_left": "0px",        # GLOBAL: Horizontaler Versatz der Sub-Nav Buttons (px/%).
        "sub_nav_width": "100%",             # GLOBAL: Breite der Sub-Nav Leiste.

        # --- LEVEL 3: MODULE TABS (Sub-Menu) ---
        "sub_menu_visible": True,            # GLOBAL: Sichtbarkeit Level 3 (Module Tabs).
        "sub_menu_height": 32,               # GLOBAL: Höhe Level 3 (px).
        "sub_menu_width": "100%",            # GLOBAL: Breite Level 3 (%/px).
        "sub_menu_offset_left": "0px",       # GLOBAL: Horizontaler Versatz Level 3.

        # --- GLOBAL UI ELEMENTS & GEOMETRY ---
        "sidebar_allowed": True,             # GLOBAL: Erlaubt die Sidebar-Nutzung generell.
        "sidebar_visible": False,            # GLOBAL: Sidebar Start-Zustand (True=Offen).
        "sidebar_width": 250,                # GLOBAL: Breite der Sidebar (px).
        "footer_visible": True,              # GLOBAL: Schwebende Media-Steuerung unten.
        "footer_height": 48,                 # GLOBAL: Höhe des Footers (px).
        "diagnostics_hud_visible": True,     # GLOBAL: Technisches HUD-Overlay.

        # --- [v1.46.01] SYSTEM HEADER ORCHESTRATOR ---
        "header_orchestrator": {
            "show_logo": True,
            "logo_text": "dict",
            "left_cluster": [
                {"id": "power",   "visible": True, "title": "Exit Application", "icon": "power",   "action": "exitApplication()"},
                {"id": "restart", "visible": True, "title": "Restart System",   "icon": "refresh", "action": "location.reload()"}
            ],
            "mid_tabs": [
                {"id": "media",      "label": "Player",       "visible": True, "action": "switchMainCategory('media', this)"},
                {"id": "library",    "label": "Bibliothek",   "visible": True, "action": "switchMainCategory('library', this)"},
                {"id": "database",   "label": "Database",     "visible": True, "action": "switchMainCategory('database', this)"},
                {"id": "file",       "label": "Browser",      "visible": True, "action": "switchMainCategory('file', this)"},
                {"id": "edit",       "label": "Edit",         "visible": True, "action": "switchMainCategory('edit', this)"},
                {"id": "system",     "label": "Optionen",     "visible": True, "action": "switchMainCategory('system', this)"},
                {"id": "parser",     "label": "Parser",       "visible": True, "action": "switchMainCategory('parser', this)"},
                {"id": "debug",      "label": "Debug & DB",   "visible": True, "action": "switchMainCategory('debug', this)"},
                {"id": "tests",      "label": "Tests",        "visible": True, "action": "switchMainCategory('tests', this)"},
                {"id": "tools",      "label": "Tools",        "visible": True, "action": "switchMainCategory('tools', this)"},
                {"id": "reporting",  "label": "Report",       "visible": True, "action": "switchMainCategory('reporting', this)"},
                {"id": "logbuch",    "label": "Logbuch",      "visible": True, "action": "switchMainCategory('logbuch', this)"},
                {"id": "video",      "label": "Video",        "visible": True, "action": "switchMainCategory('video', this)"}
            ],
            "right_cluster": [
                {"id": "status",       "visible": True,  "title": "Toggle Technical HUD",     "icon": "pulse",   "action": "toggleTechnicalHUD()",        "color": "#007aff"},
                {"id": "sync",         "visible": True,  "title": "Toggle Sync Anchor",      "icon": "shield",  "action": "toggleSyncAnchor()",         "color": "#2ecc71"},
                {"id": "theme",        "visible": True,  "title": "Switch System Theme",     "icon": "sun",     "action": "toggleTheme()",              "color": "#ff9500"},
                {"id": "footer_hud",   "visible": True,  "title": "Toggle Swiss HUD LED",    "icon": "grid",    "action": "toggleFooterHUD()",          "color": "#9b59b6"},
                {"id": "db_status",    "visible": True,  "title": "Toggle DB Health",        "icon": "db",      "action": "toggleFooterDBStatus()",     "color": "#f1c40f"},
                {"id": "diag",         "visible": True,  "title": "Toggle Diagnostics",      "icon": "diag",    "action": "toggleDiagnosticsSidebar()",  "color": "#ff3366"},
                {"id": "auditor",      "visible": True,  "title": "Toggle DOM Auditor",      "icon": "check",   "action": "toggleDomAuditor()",         "color": "#00ffcc"},
                {"id": "lib_sidebar",  "visible": True,  "title": "Toggle Library Sidebar",  "icon": "layout",  "action": "toggleLibrarySidebar()",     "color": "#007aff"},
                {"id": "sidebar",      "visible": True,  "title": "Toggle Main Sidebar",     "icon": "menu",    "action": "toggleSidebar()",            "color": "#e5e5e7"},
                {"id": "zen",          "visible": True,  "title": "Toggle Zen Mode",         "icon": "zen",     "action": "toggleZenMode()",            "color": "#2ecc71"},
                {"id": "reset_db",     "visible": True,  "title": "Reset System Database",   "icon": "trash",   "action": "resetDatabase()",            "color": "#ff3300"}
            ]
        },

        # --- [v1.46.03] SYSTEM STEERING: HEADER & THEME (NEW) ---
        "header_layout": {
            "btn_size": 26,              # Pixel size (Default: 26)
            "btn_gap": 6,               # Spacing between buttons (Default: 6)
            "btn_border_radius": "50%", # Shape (50% = Circle, 6px = Rounded Square)
            "hover_scale": "1.1",       # Animation scale factor
            "show_tooltips": True       # Enable hover comments
        },
        "themes": {
            "active": "forensic_dark",   # Default theme ID
            "available": ["forensic_dark", "cyber_grid", "matrix_core", "light_pro"]
        },

        # --- [v1.46.01] TECHNICAL OVERLAY STEERING ---
        "technical_overlay": {
            "stable_mode_visible": True,
            "stable_mode_position": {
                "top": 110,
                "right": 280
            },
            "forensic_anchors_visible": True,
            "deck_tag_visible": True,
            "deck_tag_position": {
                "top": 5,
                "left": 5
            },
            "queue_tag_visible": True,
            "queue_tag_position": {
                "top": 5,
                "right": 5
            }
        },
        "enable_context_menu": True,         # GLOBAL: Rechtsklick-Menü für Items.
        "enable_diagnostics_hud": True,      # GLOBAL: Sichtbarkeit des technischen HUDs im Header.
        "enable_dom_auditor": True,          # GLOBAL: Echtzeit-Integritätsprüfung (7-Point Audit).
        "enable_technical_hud": True,        # GLOBAL: Floating PID/BOOT/UP Pills im Header.
        "enable_sync_anchor": True,          # GLOBAL: [DB|GUI] Sync-Metriken im Footer.
        "enable_footer_hud_cluster": True,   # GLOBAL: Swiss FE/BE/DB LED Cluster im Footer.
        "enable_zen_mode": True,             # GLOBAL: Zen Mode (Header/Footer hide) Toggle.
        "enable_footer_db_status": True,     # GLOBAL: DB Status & Hydration Cluster im Footer.
        "enable_header_power_button": True,  # GLOBAL: [v1.41.163] Power/Exit Button oben links.
        "enable_rescue_failover": True,     # GLOBAL: [v1.41.163] Auto-Rescue UI bei Fragment-Fehlern.

        # --- GRANULAR FOOTER SUB-SETTINGS (v1.41.158 Extension) ---
        "footer_settings": {
            "show_version_info": True,       # Toggle: v1.41.x String
            "show_sync_status": True,        # Toggle: "Synchronized" Text
            "show_hydration_labels": True,   # Toggle: M/R/B buttons
            "show_danger_zone": True         # Toggle: RESET button
        },
        
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
        
        # --- [v1.46.005] CONSOLIDATED FLAG REGISTRY (F2C) ---
        "ui_flag_registry": {
            "technical": {
                "enable_technical_hud": "Technical HUD (PID/BOOT)",
                "enable_diagnostics_hud": "Diagnostics HUD (Header)",
                "enable_dom_auditor": "DOM Auditor (7-Point-Pulse)",
                "enable_sync_anchor": "Sync Anchor [DB|GUI]",
                "enable_footer_hud_cluster": "Swiss HUD LED Cluster"
            },
            "workstation": {
                "enable_zen_mode": "Zen Mode (Clean Layout)",
                "enable_footer_db_status": "Footer DB Status",
                "enable_header_power_button": "Header Power Button",
                "enable_rescue_failover": "Auto-Rescue UI"
            },
            "fragments": {
                "ui_fragments.player": "Audio Player Sidebar",
                "ui_fragments.library": "Media Library Sidebar",
                "ui_fragments.video": "Video Cinema Sidebar",
                "ui_fragments.edit": "Metadata Editor Sidebar",
                "ui_fragments.debug": "Technical Debug Sidebar",
                "ui_fragments.logbuch": "Logbook / Journal Sidebar"
            },
            "overlays": {
                "technical_overlay.stable_mode_visible": "Stable Mode Active Badge",
                "technical_overlay.forensic_anchors_visible": "Forensic AI Anchors",
                "technical_overlay.deck_tag_visible": "Deck-Lift [27] Tag",
                "technical_overlay.queue_tag_visible": "Queue-Lift [27] Tag"
            },
            "engines": {
                "audio_engine_enabled": "Audio Engine (Core)",
                "video_engine_enabled": "Video Engine (Core)",
                "queue_panel_enabled": "Media Queue Panel",
                "lyrics_panel_enabled": "Lyrics/Metadata Panel"
            }
        },

        # --- BEHAVIOR & THEME ---
        "theme": "dark",
        "animations_enabled": True,
        "ui_registry": {
            "evolution_mode": "stable", # "stable", "rebuild", "bridge", "test_ref" (v1.45)
            "sidebar_default_open": False,
            "glassmorphism_enabled": True,
            "animation_performance_tier": "high",
            "theme_default": "dark-forensic"
        },
        
        # --- UNICODE & EMOJI REGISTRY (v1.42 Safety Strategy) ---
        "unicode_registry": {
            "safety_mode": False,       # If True, replaces emojis with ASCII tags
            "safety_map": {
                "☢️": "[NUCLEAR]",
                "✅": "[SUCCESS]",
                "❌": "[ERROR]",
                "⚠️": "[WARNING]",
                "🚀": "[STARTUP]",
                "💾": "[SAVE]",
                "🔍": "[PROBE]",
                "🔄": "[SYNC]",
                "⚡": "[ACTIVE]"
            }
        },
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
                { "id": "warteschlange", "label": "Queue",         "action": "switchPlayerView('warteschlange')" },
                { "id": "playlist",      "label": "Mediengalerie", "action": "switchPlayerView('playlist')" },
                { "id": "visualizer",    "label": "Visualizer",    "action": "switchPlayerView('visualizer')" },
                { "id": "lyrics",        "label": "Lyrics",        "action": "switchPlayerView('lyrics')" },
                { "id": "videocinema",   "label": "Video Cinema",  "action": "switchMainCategory('video')" }
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

    # --- DEBUGGING REGISTRY (v1.41.00 Centralized) ---
    
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
    
    # --- UI & UX SETTINGS (v1.41.00 Centralized) ---
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
    
    # Diagnostic Toggles (v1.41.00 Centered)
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
    
    # Tool & Parser Settings (v1.41.00)
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
    
    # Wait & Sleep Intervals (Centralized v1.41.00)
    "sleep_times": {
        "ui_settle": float(os.environ.get("MWV_SLEEP_UI_SETTLE", 2.0)),
        "boot_probe_wait": float(os.environ.get("MWV_SLEEP_BOOT_PROBE", 5.0)),
        "keepalive": float(os.environ.get("MWV_SLEEP_KEEPALIVE", 1.0)),
        "watchdog_tick": float(os.environ.get("MWV_SLEEP_WATCHDOG", 0.5)),
        "retry_delay": float(os.environ.get("MWV_SLEEP_RETRY", 0.5)),
        "poll_fast": float(os.environ.get("MWV_SLEEP_POLL_FAST", 0.1))
    },
    
    # --- EXTERNAL BINARY DISCOVERY (Centralized v1.41.00) ---
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
    
    # --- STORAGE REGISTRY (v1.41.00 Centralized) ---
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
    
    # --- PARSER & UI REGISTRY (v1.41.00 Centralized) ---
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
    
    # --- SCRIPT & UTILITY REGISTRY (v1.41.00 Centralized) ---
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

    # --- DIAGNOSTIC & METRIC REGISTRY (v1.41.00 Centralized) ---
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
    
    # --- PLAYBACK & ENGINE SETISTRY (v1.41.00 Centralized) ---
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
    # --- VERSION & METADATA CALCULATION (v1.41.00 - Deferred) ---
    "app_versions": {
        "ffmpeg": "Discovering...",
        "ffprobe": "Discovering...",
        "ffplay": "Discovering...",
        "vlc": "Discovering...",
        "mpv": "Discovering...",
        "mkvmerge": "Discovering...",
        "m3u8": "Discovering...",
        "mediainfo": "Discovering...",
        "isoinfo": "Discovering...",
        "swyh-rs-cli": "Discovering...",
        "mediamtx": "Discovering...",
        "spotifyd": "Discovering...",
        "spt": "Discovering...",
        "pyvidplayer2": "Discovering...",
        "python": sys.version.split()[0],
        "pip": "Discovering...",
        "conda": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
        "conda_version": "N/A",
        "docker_version": "N/A",
        # PIP Packages Version Registry (Deferred)
        "eel": "N/A",
        "bottle": "N/A",
        "mutagen": "N/A",
        "psutil": "N/A",
        "gevent": "N/A",
        "pytest": "N/A",
        # Toolchain Versions
        "doxygen": "Discovering...",
        "graphviz": "Discovering...",
        "chrome": "Discovering..."
    },
    
    # --- TRANSCODING TOOLCHAIN (v1.41.00 Centralized) ---
    "transcoding_toolchain": {
        "ffmpeg": get_binary_version("ffmpeg"),
        "ffprobe": get_binary_version("ffprobe"),
        "handbrake": get_binary_version("HandBrakeCLI", "--version"),
        "vlc": get_binary_version("vlc", "--version").split()[0] if "VLC" in get_binary_version("vlc", "--version") else "N/A"
    },
    
    # --- PARSING TOOLCHAIN (v1.41.00 Centralized) ---
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
    
    # --- TRANSCODING & ENGINE SETTINGS (v1.41.00 Centralized) ---
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
    
    # --- THIRD-PARTY INTEGRATIONS (v1.41.00 Centralized) ---
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
    
    # --- BROWSER DISCOVERY LADDER (Centralized v1.41.00) ---
    "browsers": [
        "google-chrome-stable", "google-chrome", "chrome",
        "google-chrome-unstable", "google-chrome-beta",
        "chromium-browser", "chromium",
        "firefox", "firefox-developer-edition", "firefox-esr",
        "msedge", "msedge-dev", "msedge-beta",
        "brave-browser", "brave", "opera", "vivaldi"
    ],
    
    # --- HEADLESS & DIALECT REGISTRY (v1.41.00 Centralized) ---
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
        "environment": {
            "env_type": "unknown",
            "env_name": "unknown",
            "env_path": "unknown",
            "python_version": "unknown",
            "python_executable": "unknown",
            "platform": "unknown",
            "venv_active": False,
            "cwd": "unknown",
            "os": "unknown",
            "pid": 0,
            "browser_pid": 0,
            "testbed_pid": 0,
            "selenium_pid": 0,
            "log_level": "INFO",
            "release": "unknown",
            "machine": "unknown",
            "debug_flags": {},
            "version": "unknown"
        },
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

    # --- [v1.46.018] LEGACY NAVIGATION REGISTRY (For Rebuild Context) Level 4 Legacy unused ---
    "legacy_navigation": {
        "sub_nav_registry": {
            "media": [
                { "id": "warteschlange", "label": "Queue", "action": "switchPlayerView('warteschlange')" },
                { "id": "playlist", "label": "Playlist Manager", "action": "switchPlayerView('playlist')" },
                { "id": "visualizer", "label": "Visualizer", "action": "switchPlayerView('visualizer')" },
                { "id": "lyrics", "label": "Lyrics", "action": "switchPlayerView('lyrics')" },
                { "id": "albums", "label": "Alben-Galerie", "action": "switchMediaSubView('albums')" },
                { "id": "audiobooks", "label": "Hörbuch-Sektor", "action": "switchMediaSubView('audiobooks')" },
                { "id": "playlist-mgr", "label": "Playlist-Profi", "action": "switchMediaSubView('playlist-mgr')" }
            ],
            "library": [
                { "id": "lib-visual", "label": "Visual Explorer", "action": "switchLibrarySubView('visual')" },
                { "id": "lib-browse", "label": "FileSystem Browse", "action": "switchLibrarySubView('browse')" },
                { "id": "lib-films", "label": "Kinofilme", "action": "switchLibrarySubTab('films')" },
                { "id": "lib-series", "label": "Serien-Katalog", "action": "switchLibrarySubTab('series')" }
            ],
            "database": [
                { "id": "db-explorer", "label": "DB Explorer", "action": "switchLibrarySubView('inventory')" },
                { "id": "db-integrity", "label": "Integrity Check", "action": "runNuclearDiagnostics()" },
                { "id": "db-sync", "label": "Atomic Sync", "action": "triggerDeepSync()" },
                { "id": "db-recovery", "label": "Recovery Hub", "action": "switchDiagnosticsSubView('recovery')" }
            ],
            "status": [
                { "id": "status-health", "label": "Core Health", "action": "switchDiagnosticsSubView('health')" },
                { "id": "status-logs", "label": "Live Logs", "action": "switchDiagnosticsSubView('logs')" },
                { "id": "status-net", "label": "Network/Eel", "action": "switchDiagnosticsSubView('network')" },
                { "id": "status-latency", "label": "Logic Latency", "action": "switchDiagnosticsSubView('latency')" }
            ],
            "file": [
                { "id": "file-local", "label": "Lokale Medien", "action": "switchFileSubView('local')" },
                { "id": "file-network", "label": "Netzwerk / SMB", "action": "switchFileSubView('network')" },
                { "id": "file-mounted", "label": "Eingehängte Drv", "action": "switchFileSubView('mounted')" }
            ],
            "edit": [
                { "id": "edit-basic", "label": "Basic Metadata", "action": "switchEditSubView('basic')" },
                { "id": "edit-tech", "label": "Technical Specs", "action": "switchEditSubView('technical')" },
                { "id": "edit-ffprobe", "label": "FFprobe Dump", "action": "switchEditSubView('ffprobe')" },
                { "id": "edit-album", "label": "Artwork Editor", "action": "switchEditSubView('artwork')" }
            ],
            "system": [
                { "id": "sys-general", "label": "Allgemein", "action": "switchOptionsView('general')" },
                { "id": "sys-parser", "label": "Parser Chain", "action": "switchOptionsView('parser')" },
                { "id": "sys-trans", "label": "Transcoding", "action": "switchOptionsView('transcoding')" },
                { "id": "sys-env", "label": "Environments", "action": "switchOptionsView('environment')" },
                { "id": "sys-helpers", "label": "Helper Scripts", "action": "switchOptionsView('helpers')" }
            ],
            "parser": [
                { "id": "px-chain", "label": "Main Chain", "action": "switchParserView('main')" },
                { "id": "px-extraction", "label": "Extraction Log", "action": "switchParserView('extraction')" },
                { "id": "px-bench", "label": "Benchmarking", "action": "switchParserView('benchmark')" }
            ],
            "debug": [
                { "id": "dbg-sentinel", "label": "UI Sentinel", "action": "switchDiagnosticsSubView('sentinel')" },
                { "id": "dbg-rescue", "label": "Rettungs-Konsole", "action": "switchDiagnosticsSubView('rescue')" },
                { "id": "dbg-dom", "label": "DOM Auditor", "action": "switchDiagnosticsSubView('dom-audit')" },
                { "id": "dbg-state", "label": "AppState Dump", "action": "switchDiagnosticsSubView('state')" }
            ],
            "tests": [
                { "id": "test-suite", "label": "Active Suite", "action": "switchTestView('suite')" },
                { "id": "test-scripts", "label": "Test Scripts", "action": "switchTestView('scripts')" },
                { "id": "test-regress", "label": "Regression", "action": "switchTestView('regression')" }
            ],
            "tools": [
                { "id": "tool-set", "label": "System Toolset", "action": "switchToolsSubView('main')" },
                { "id": "tool-workers", "label": "Active Workers", "action": "switchToolsSubView('workers')" },
                { "id": "tool-pipelines", "label": "AV Pipelines", "action": "switchToolsSubView('pipelines')" }
            ],
            "reporting": [
                { "id": "rep-overview", "label": "Overview", "action": "switchReportingView('dashboard')" },
                { "id": "rep-health", "label": "System-Monitor", "action": "switchReportingView('health')" },
                { "id": "rep-perf", "label": "Performance", "action": "switchReportingView('performance')" },
                { "id": "rep-errors", "label": "Error Analytics", "action": "switchReportingView('errors')" }
            ],
            "logbuch": [
                { "id": "log-project", "label": "Projekt Log", "action": "switchLogbookSubView('project')" },
                { "id": "log-audit", "label": "Audit History", "action": "switchLogbookSubView('audit')" },
                { "id": "log-feature", "label": "Feature Status", "action": "toggleFeatureStatus()" }
            ],
            "video": [
                { "id": "vid-cinema", "label": "Cinema Cinema", "action": "switchMediaSubView('video')" },
                { "id": "vid-accel", "label": "HW Acceleration", "action": "switchMediaSubView('visualizer')" },
                { "id": "vid-player", "label": "Forensic-Player", "action": "switchMediaSubView('vid-player')" },
                { "id": "vid-engine", "label": "Video-Engine", "action": "switchMediaSubView('vid-engine')" }
            ],
            "unsort": [
                { "id": "unsort-probe", "label": "Deep Probe Hub", "action": "runHydrationAuditProbe()" },
                { "id": "unsort-sync", "label": "Force Database Sync", "action": "if(window.triggerMasterSync) window.triggerMasterSync()" },
                { "id": "unsort-ui", "label": "UI Refresh", "action": "refreshViewportLayout()" }
            ]
        },
        "sub_nav_aliases": {
            "player": "media",
            "bibliothek": "library",
            "database": "database",
            "explorer": "library",
            "tools": "tools",
            "debug": "debug",
            "diagnostics": "status",
            "optionen": "system",
            "report": "reporting",
            "reporting_dashboard": "reporting",
            "file": "file",
            "edit": "edit",
            "parser": "parser",
            "logbuch": "logbuch",
            "video": "video",
            "tests": "tests",
            "status": "status",
            "audio": "media",
            "audio_native": "media",
            "audio_transcode": "media",
            "album": "media",
            "single": "media",
            "hörbuch": "media",
            "sampler": "media",
            "soundtrack": "media",
            "video_iso": "media",
            "bilder": "media",
            "epub": "media"
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
# --- AUTO-TRIGGER BACKGROUND DISCOVERY ---
background_version_discovery(GLOBAL_CONFIG)
