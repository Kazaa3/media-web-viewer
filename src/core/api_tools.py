import os
import re
import subprocess
import shutil
import psutil
from typing import Dict, Any, Optional

from src.core.config_master import (
    GLOBAL_CONFIG, PROGRAM_REGISTRY, 
    get_binary_version as _get_version_config
)
from src.core.logger import get_logger

log = get_logger("api_tools")

def get_tool_health_report() -> Dict[str, Any]:
    """
    Forensic Toolchain Diagnostics (v1.46.132).
    Checks availability and versions for all registered programs.
    """
    report = {}
    for name, path in PROGRAM_REGISTRY.items():
        if not path or not os.path.exists(path):
            state = "MISSING"
            version = "N/A"
        else:
            state = "OK"
            version = _get_version_config(path)
            
        report[name] = {
            "state": state,
            "path": path,
            "version": version
        }
    return report

def kill_stalled_forensic_processes(targets: Optional[list] = None):
    """
    Forcefully cleans up stalled FFmpeg, MKVMerge, or VLC processes.
    (Migrated from api_reporting v1.46.132)
    """
    if targets is None:
        targets = ['ffmpeg', 'ffprobe', 'mkvmerge', 'vlc', 'cvlc', 'ffplay']
        
    log.info(f"[Cleanup] Targeted forensic audit: killing stalled processes {targets}")
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = (proc.info['name'] or "").lower()
            cmdline = " ".join(proc.info['cmdline'] or []).lower()
            
            if any(t in name for t in targets) or any(t in cmdline for t in targets):
                if proc.info['pid'] != os.getpid():
                    proc.kill()
                    count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    log.info(f"[Cleanup] Terminated {count} forensic artifacts.")
    return count

def kill_stalled_ffmpeg_streams():
    """Specific hook for high-priority FFmpeg cleanup (v1.46.135)."""
    return kill_stalled_forensic_processes(['ffmpeg', 'ffprobe', 'ffplay'])

def super_kill():
    """Nuclear cleanup: Terminates ALL forensic tools and known browsers."""
    targets = ['ffmpeg', 'ffprobe', 'mkvmerge', 'vlc', 'cvlc', 'ffplay', 'chrome', 'chromium', 'firefox']
    return kill_stalled_forensic_processes(targets)

def check_binary_available(name: str) -> bool:
    """Verifies if a specific tool is operational in the registry."""
    path = PROGRAM_REGISTRY.get(name)
    return path is not None and os.path.exists(path)

def get_detailed_tool_stats(name: str) -> Dict[str, Any]:
    """Returns granular metadata for a specific forensic binary."""
    path = PROGRAM_REGISTRY.get(name)
    if not path:
        return {"error": "Tool not registered"}
        
    stats = {
        "name": name,
        "path": path,
        "exists": os.path.exists(path),
        "size": os.path.getsize(path) if os.path.exists(path) else 0,
        "version": _get_version_config(path)
    }
    return stats
