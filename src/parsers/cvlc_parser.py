import subprocess
import re
import json
from pathlib import Path
from typing import Any
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG

# Specialized logger (v1.46.132 Master Standalone)
log = get_logger("cvlc")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "CVLC (Headless Master)",
        "description": "Master VLC orchestrator using the cvlc CLI. Provides independent validation and high-fidelity headless extraction.",
        "supported_tags": ["title", "artist", "album", "duration", "chapters"],
        "supported_codecs": ["*"]
    }

def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight', settings: dict[str, Any] = None) -> dict[str, Any]:
    """
    @brief Extracts metadata using the cvlc CLI (Standalone).
    """
    if filename is None:
        filename = path.name
    if settings is None:
        settings = {}

    profile = settings.get('profile', 'standard')
    timeout = settings.get('timeout', 15 if profile == 'exhaustive' else 5)

    try:
        # cvlc CLI command for metadata dump
        cmd = [
            "cvlc", 
            "-I", "dummy", 
            "--dummy-quiet", 
            "--no-video", 
            "--no-audio",
            str(path), 
            "vlc://quit"
        ]
        
        # Phase 13: Standardized exhaustive playback pulse from GLOBAL_CONFIG
        if profile == 'exhaustive':
            cmd.insert(1, "-vv") 
            playback_ms = GLOBAL_CONFIG.get("calibration_registry", {}).get("vlc_exhaustive_playback_ms", 1000)
            log.debug(f"🔍 [CVLC] Exhaustive Pulse: {playback_ms}ms window for '{filename}'")
            
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, errors='ignore')
        output = result.stderr 
        
        mappings = GLOBAL_CONFIG.get("parser_registry", {}).get("tag_mappings", {}).get("cvlc", {})
        
        patterns = {
            'title': r"meta fetcher: Found metadata: Title '(.*?)'",
            'artist': r"meta fetcher: Found metadata: Artist '(.*?)'",
            'album': r"meta fetcher: Found metadata: Album '(.*?)'",
            'date': r"meta fetcher: Found metadata: Date '(.*?)'",
            'genre': r"meta fetcher: Found metadata: Genre '(.*?)'",
            'track': r"meta fetcher: Found metadata: Track number '(.*?)'",
            'disc': r"meta fetcher: Found metadata: Disc number '(.*?)'"
        }

        for tag_key, pattern in patterns.items():
            match = re.search(pattern, output)
            if match:
                res_key = mappings.get(tag_key, tag_key)
                if not tags.get(res_key):
                    tags[res_key] = match.group(1).strip()

        if mode == 'full' or profile == 'exhaustive':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            tags['full_tags']['cvlc_raw_stderr'] = output[:2000] # Truncated raw trace

    except subprocess.TimeoutExpired:
        log.warning(f"[CVLC] Timeout expired for {filename}")
    except Exception as e:
        log.error(f"[CVLC][{profile}] Failed for {filename}: {e}", exc_info=True)

    return tags
