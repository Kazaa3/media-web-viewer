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
from pathlib import Path
from typing import Any, Dict, List
from importlib.metadata import distributions

try:
    from src.core import hardware_detector
    _HW_DETECTOR = True
except ImportError:
    _HW_DETECTOR = False

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
    return shutil.which(name) or os.environ.get(f"MWV_PATH_{name.upper().replace('-', '_')}", fallback)

def get_binary_version(name: str) -> str:
    """Safely get the version of a binary."""
    path = discover_binary(name)
    if not path:
        return "Not Found"
    try:
        if name == "vlc":
            cmd = [path, "--version"]
        elif name == "mpv":
            cmd = [path, "--version"]
        else:
            cmd = [path, "-version"] # standard for ffmpeg, mkvmerge
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        combined = (res.stdout or "") + (res.stderr or "")
        
        # Broad patterns for different tools
        patterns = [
            r"version ([0-9\.\-]+)",      # ffmpeg, ffprobe
            r"v([0-9\.\-]+)",             # mkvmerge
            r"VLC version ([0-9\.\-]+)",  # vlc
            r"([0-9]+\.[0-9]+\.[0-9]+)"   # fallback generic semantic version
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

# --- GLOBAL CONFIGURATION DICTIONARY ---
GLOBAL_CONFIG: Dict[str, Any] = {
    # System & Paths
    # System & Ports
    "port": int(os.environ.get("MWV_PORT", 8345)),
    "vlc_port": int(os.environ.get("MWV_VLC_PORT", 8080)),
    "mtx_port": int(os.environ.get("MWV_MTX_PORT", 8888)),
    "debug_mode": get_env_bool("MWV_DEBUG", True),
    "db_filename": os.environ.get("MWV_DB", str(PROJECT_ROOT / "data" / "database.db")),
    "docker_mode": get_env_bool("MWV_DOCKER", False),
    
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
        "mkvinfo": discover_binary("mkvinfo", "mkvinfo"),
        "mkvextract": discover_binary("mkvextract", "mkvextract"),
        "mediamtx": discover_binary("mediamtx", "mediamtx"),
        "swyh-rs-cli": discover_binary("swyh-rs-cli", "swyh-rs-cli"),
        "spotifyd": discover_binary("spotifyd", "spotifyd"),
        "spt": discover_binary("spt", "spt"),
        "pyvidplayer2": discover_binary("pyvidplayer2", "pyvidplayer2"),
        "mpv": discover_binary("mpv", "mpv")
    },
    
    # --- STORAGE REGISTRY (v1.35.68 Centralized) ---
    "storage_registry": {
        "project_root": str(PROJECT_ROOT),
        "data_dir": str(PROJECT_ROOT / "data"),
        "media_dir": str(PROJECT_ROOT / "media"),
        "db_path": os.environ.get("MWV_DB", str(PROJECT_ROOT / "data" / "database.db")),
        "log_dir": str(PROJECT_ROOT / "logs"),
        "cache_dir": str(PROJECT_ROOT / "cache"),
        "legacy_db_candidates": [
            "~/media_library.db",
            "./media_library.db",
            "./dist/media_library.db",
            "../media_library.db"
        ]
    },
    
    # --- CATEGORY & ROUTING REGISTRY (v1.35.68 Centralized) ---
    "category_registry": {
        "master_map": {
            "audio": [
                "audio", "album", "klassik", "hörbuch", "hörspiel", "podcast", 
                "musik", "compilation", "single", "radio", "soundtrack", "playlist", 
                "music", "song"
            ],
            "multimedia": [
                "multimedia", "video", "film", "serie", "tv", "movie", "tv show", 
                "musikvideos", "animes", "cartoons", "video object", "animations", 
                "documentary", "dok", "dokumentation", "concert", "konzerte",
                "iso", "disk-abbild", "pal dvd", "ntsc dvd", "blu-ray", "hd-dvd"
            ],
            "images": ["bilder", "grafik", "bild", "foto", "images", "gallery"],
            "documents": ["dokument", "pdf", "text", "doc", "docx", "txt", "office"],
            "ebooks": ["e-book", "ebook", "epub", "mobi"],
            "abbild": ["abbild", "iso/image", "disk image", "pal dvd", "ntsc dvd", "blu-ray", "disk-abbild", "dvd object"],
            "spiel": ["spiel", "game", "pc spiel", "digitales spiel", "steam"],
            "beigabe": ["beigabe", "supplement", "software", "additional"],
            "transcoded": [],
            "iso": ["abbild", "disk-abbild", "iso"]
        },
        "tech_markers": {
            "transcoded": ["_transcoded", ".mp4_transcoded"],
            "iso": [".iso", ".bin", ".cue", ".nrg"],
            "mock": ["is_mock"],
            "stage": ["stage", "recovery", "is_stage"]
        },
        "branch_map": {
            "audio": ["audio"],
            "multimedia": ["multimedia", "abbild", "video"]
        }
    },
    
    # --- EXTENSION & PARSER REGISTRY (v1.35.68 Centralized) ---
    "extension_registry": {
        "audio": {".mp3", ".flac", ".ogg", ".wav", ".m4a", ".alac", ".opus", ".aac", ".wma", ".m4b", ".aiff", ".ac3", ".mka", ".dts", ".dtshd", ".pcm", ".ra", ".rm"},
        "video": {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv", ".mpg", ".mpeg", ".m4v", ".3gp", ".3g2", ".ogv", ".mts", ".m2ts", ".ts", ".m2t", ".m2v", ".divx", ".xvid", ".vob", ".dat", ".rmvb", ".asf"},
        "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"},
        "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".html", ".htm"},
        "ebooks": {".epub", ".mobi", ".azw", ".fb2"},
        "disk_images": {".iso", ".bin", ".img", ".cue", ".nrg", ".mdf", ".toast", ".ccd", ".daa"},
        "dsd": {".dsf", ".dff", ".dsd"},
        "hd_dvd": {".evo", ".map", ".bup"}
    },
    "playback_registry": {
        "playable_keywords": ["dvd", "blu-ray", "vcd", "laserdisc", "sacd", "dsd", "cd-extra", "dvd-audio", "dvd-vr", "video cd", "super vcd", "high-res", "cd-rom", "dvd daten", "blu-ray daten"],
        "playable_exts": [".mp4", ".mkv", ".avi", ".mp3", ".flac", ".wav", ".m4a", ".dsf", ".dff", ".ts", ".alac", ".aiff", ".mpeg", ".mpg", ".mov", ".webm", ".wmv", ".m4v", ".3gp", ".ogv", ".vob", ".m2ts", ".iso", ".bin", ".img"],
        "native_exts": [".mp4", ".mkv", ".webm", ".ogv", ".mp3", ".wav", ".ogg", ".m4a", ".flac"],
        "native_codecs": ["h264", "avc1", "vp8", "vp9", "av1", "aac", "mp4a", "mp3", "opus", "vorbis", "flac", "pcm"]
    },
    "parser_registry": {
        "default_chain": ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "pycdlib", "isoparser", "ebml", "mkvparse", "enzyme", "pymkv", "tinytag", "eyed3", "music_tag"],
        "categories": {
            "audio": ["mutagen", "tinytag", "eyed3", "music_tag"],
            "multimedia": ["container", "mkvmerge", "mkvinfo", "vlc", "isoparser", "pycdlib", "ebml", "mkvparse", "enzyme", "pymkv"],
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
        "vlc": get_binary_version("vlc"),
        "mpv": get_binary_version("mpv"),
        "mkvmerge": get_binary_version("mkvmerge"),
        "python": sys.version.split()[0]
    },
    
    # --- TRANSCODING & ENGINE SETTINGS (v1.35.68 Centralized) ---
    "transcoding_settings": {
        "ffmpeg_preset": os.environ.get("MWV_FFMPEG_PRESET", "veryfast"),
        "video_bitrate": os.environ.get("MWV_VIDEO_BITRATE", "4000k"),
        "audio_bitrate": os.environ.get("MWV_AUDIO_BITRATE", "192k"),
        "hls_time": int(os.environ.get("MWV_HLS_TIME", 2)),
        "hls_list_size": int(os.environ.get("MWV_HLS_LIST_SIZE", 0)),
        "fmp4_frag_duration": int(os.environ.get("MWV_FMP4_FRAG", 5000)), # ms
        "hwaccel": os.environ.get("MWV_HWACCEL", "auto")
    },
    
    "mediamtx_settings": {
        "host": os.environ.get("MWV_MTX_HOST", "localhost"),
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
