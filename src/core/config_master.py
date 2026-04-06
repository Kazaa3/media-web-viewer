#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Config Master (Centralized Config & Flag Orchestrator)
v1.35.68 - Unified source of truth for backend and frontend settings.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Any, Dict, List
try:
    from dotenv import load_dotenv
    _DOTENV_LOADED = True
except ImportError:
    _DOTENV_LOADED = False

# --- PROJECT PATH CALCULATION ---
MAIN_FILE = Path(__file__).resolve()
PROJECT_ROOT = MAIN_FILE.parent.parent.parent

# Load local environment overrides if available
if _DOTENV_LOADED:
    load_dotenv(PROJECT_ROOT / ".env")

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
    return shutil.which(name) or os.environ.get(f"MWV_PATH_{name.upper().replace('-', '_')}", fallback)

# --- GLOBAL CONFIGURATION DICTIONARY ---
GLOBAL_CONFIG: Dict[str, Any] = {
    # System & Paths
    # System & Ports
    "port": int(os.environ.get("MWV_PORT", 8345)),
    "vlc_port": int(os.environ.get("MWV_VLC_PORT", 8080)),
    "debug_mode": get_env_bool("MWV_DEBUG", True),
    "db_filename": os.environ.get("MWV_DB", str(PROJECT_ROOT / "data" / "database.db")),
    
    # UI & Performance
    "start_page": os.environ.get("MWV_START_PAGE", "player"),
    "window_width": int(os.environ.get("MWV_WIDTH", 1550)),
    "window_height": int(os.environ.get("MWV_HEIGHT", 800)),
    "boot_watchdog_max_ticks": int(os.environ.get("MWV_WATCHDOG_TICKS", 12)),
    "app_mode": os.environ.get("MWV_APP_MODE", "High-Performance"),
    "bandwidth_mode": os.environ.get("MWV_BANDWIDTH", "high"), # low, high
    "vlc_embedded": get_env_bool("MWV_VLC_EMBEDDED", True),
    "connectionless": get_env_bool("MWV_CONNECTIONLESS", False), 
    
    # Testing & Diagnostics (v1.35.68)
    "test_engine": os.environ.get("MWV_TEST_ENGINE", "chrome-headless"), # playwright, selenium, chrome-headless
    "headless_mode": get_env_bool("MWV_HEADLESS", True),
    
    # Parser & Library
    "auto_scan": get_env_bool("MWV_AUTO_SCAN", True),
    "fast_scan": get_env_bool("MWV_FAST_SCAN", True),
    "parser_mode": os.environ.get("MWV_PARSER_MODE", "lightweight"), # lightweight, full, ultimate
    "displayed_categories": ["audio", "multimedia", "images", "documents", "ebooks", "abbild"],
    
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
    "indexed_categories": ["audio", "video", "images", "documents", "ebooks", "abbild", "spiel", "beigabe", "supplements", "games"],
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
    
    # Active Branch
    "active_branch": os.environ.get("MWV_BRANCH", "audio"), # audio, multimedia
    
    # Tool & Parser Settings (v1.35.68)
    "parser_settings": {
        "mkvmerge": {"cli_flags": "", "timeout": 10},
        "ffprobe": {"cli_flags": "", "timeout": 10},
        "ffmpeg": {"deep_analysis": False, "timeout": 30},
        "vlc": {"timeout": 5},
        "mutagen": {"prefer_albumartist": True},
        "mkvinfo": {"timeout": 10}
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
        "mkvmerge": discover_binary("mkvmerge", "mkvmerge"),
        "mkvinfo": discover_binary("mkvinfo", "mkvinfo")
    },
    
    # --- BROWSER DISCOVERY LADDER ---
    "browsers": [
        "google-chrome-stable", "google-chrome", "chrome",
        "chromium-browser", "chromium", "firefox", "msedge", "brave"
    ]
}

# Parser constants moved to core for centralization
SLOW_PARSERS = {"isoparser", "pycdlib", "ebml", "mkvparse", "enzyme", "pymkv"}

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
