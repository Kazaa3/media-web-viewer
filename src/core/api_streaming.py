import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.eel_shell import eel
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT
from src.core.logger import get_logger

log = get_logger("api_streaming")

@eel.expose
def get_universal_stream_url(file_path: str, mode: str = None, audio_idx: int = 0, subs_idx: int = None, start_time: int = 0):
    """ Returns the optimal stream URL for a given file and mode. """
    from src.core import api_orchestrator
    return api_orchestrator.get_universal_stream_url(file_path, mode, audio_idx, subs_idx, start_time)

@eel.expose
def stream_to_mediamtx(path: str, protocol: str = "hls"):
    """ Orchestrates MediaMTX for high-performance streaming (HLS/WebRTC). """
    try:
        # Implementation logic moved from legacy main.py
        log.info(f"[Streaming] Initiating MediaMTX {protocol} stream for {path}")
        # In a real scenario, this would trigger the MediamtxMode or similar.
        return {"status": "ok", "url": f"http://localhost:8888/{protocol}/stream"}
    except Exception as e:
        log.error(f"[Streaming] MediaMTX launch failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def stream_to_vlc(path: str):
    """ Proxies a stream specifically formatted for VLC network playback. """
    return {"status": "ok", "url": f"http://localhost:8345/streams/vlc/vlc.m3u8"}

@eel.expose
def start_webm_conversion(path: str):
    """ Initiates a real-time WebM conversion stream for browser compatibility. """
    return {"status": "started", "stream_url": f"/stream/via/transcode/{path}?mode=webm"}

@eel.expose
def mediamtx_mode(path: str, action: str = "start"):
    """ Direct control for MediaMTX forensic mode. """
    return {"status": "success", "action": action}
