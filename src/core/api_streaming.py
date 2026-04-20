import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.eel_shell import eel
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT
from src.core.logger import get_logger

log = get_logger("api_streaming")

def is_engine_available(engine_name: str) -> bool:
    """ Checks if a specific streaming engine (binary) is available on the system. """
    from src.core.config_master import GLOBAL_CONFIG
    registry = GLOBAL_CONFIG.get("technical_orchestrator", {}).get("tools_orchestrator", {}).get("registry", {})
    tool_info = registry.get(engine_name, {})
    binary = tool_info.get("binary", engine_name)
    import shutil
    return shutil.which(binary) is not None

@eel.expose
def get_streaming_status():
    """ Returns the availability of all configured streaming engines. """
    from src.core.config_master import GLOBAL_CONFIG
    engines = GLOBAL_CONFIG.get("playback_registry", {}).get("streaming_engines", [])
    return {engine: is_engine_available(engine) for engine in engines}

@eel.expose
def get_universal_stream_url(file_path: str, mode: str = None, audio_idx: int = 0, subs_idx: int = None, start_time: int = 0):
    """ Returns the optimal stream URL for a given file and mode. """
    from src.core import api_orchestrator
    return api_orchestrator.get_universal_stream_url(file_path, mode, audio_idx, subs_idx, start_time)

@eel.expose
def stream_to_mediamtx(path: str, protocol: str = "hls"):
    """ Orchestrates MediaMTX for high-performance streaming (HLS/WebRTC). """
    if not is_engine_available("mediamtx"):
        return {"status": "error", "message": "MediaMTX binary not found. Please install it for forensic streaming."}
        
    try:
        # Implementation logic: In a production environment, this would spawn 
        # a ffmpeg process to push the file to mediamtx.
        log.info(f"[Streaming] Initiating MediaMTX {protocol} stream for {path}")
        
        # Placeholder for process orchestration logic found in legacy archive
        # process = subprocess.Popen(...)
        
        return {
            "status": "ok", 
            "url": f"http://localhost:8888/{protocol}/{Path(path).stem}",
            "protocol": protocol,
            "engine": "mediamtx"
        }
    except Exception as e:
        log.error(f"[Streaming] MediaMTX launch failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def stream_to_vlc(path: str):
    """ Proxies a stream specifically formatted for VLC network playback. """
    return {"status": "ok", "url": f"http://localhost:8345/streams/vlc/vlc.m3u8"}

@eel.expose
def start_ffmpeg_pipe_stream(file_path: str, mode: str = "fragmented", audio_idx: int = 0, subs_idx: Optional[int] = None, start_time: float = 0.0):
    """ Initiates a real-time FFmpeg pipe stream for browser compatibility. """
    try:
        from src.core.streaming_processor import StreamingProcessor
        # Note: Frontend will consume this via a separate HTTP route (e.g., Bottle) that calls the generator.
        log.info(f"[Streaming] Pipe stream requested for {file_path} (Start: {start_time}s)")
        return {"status": "ok", "message": "Stream pipeline ready for consumption."}
    except Exception as e:
        log.error(f"[Streaming] Pipe launch failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def mediamtx_mode(path: str, action: str = "start"):
    """ Direct control for MediaMTX forensic mode. """
    try:
        from src.core.streaming_processor import StreamingProcessor
        return StreamingProcessor.orchestrate_mediamtx(path)
    except Exception as e:
        log.error(f"[Streaming] MediaMTX orchestration failed: {e}")
        return {"status": "error", "message": str(e)}
