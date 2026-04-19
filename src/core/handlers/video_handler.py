"""
Video-specific handler.
"""
from pathlib import Path
from typing import Dict, Any
import urllib.parse
from .media_handler import MediaHandler
from .metadata_pipeline import MetadataPipeline

from src.core.logger import get_logger

log = get_logger("video_handler")

class VideoHandler(MediaHandler):
    """
    @brief Specialized handler for video formats.
    """
    def __init__(self, filepath: str | Path):
        super().__init__(filepath)
        self.pipeline = MetadataPipeline(self.filepath)


    def extract_metadata(self) -> Dict[str, Any]:
        return self.pipeline.execute()

    def process(self, client: str = 'browser', relpath: str = "") -> Dict[str, Any]:
        """
        @brief Route video playback using the centralized smart_route engine.
        """
        from src.core.mode_router import smart_route
        import urllib.parse
        
        # 1. Delegate decision to unified orchestrator (v1.46.046)
        route = smart_route(str(self.filepath))
        mode = route.get("mode", "direct_play")
        analysis = route.get("info", {})
        subtype = analysis.get("media_subtype", "FILE")
        d_sec = analysis.get("duration", 0)
        
        log.info(f"[PLAY-PULSE] VideoHandler delegate: Mode={mode} | Subtype={subtype} | Path={self.filepath.name}")


        # 2. Bridge back to Handshake URL structure
        if mode == 'direct_play':
            # Use the new explicit direct stream route (v1.46.042)
            return {"mode": "direct", "url": f"/stream/via/direct/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec, "analysis": analysis}
        elif mode == 'mpv_wasm':
             return {"mode": "mpv_wasm", "url": f"/stream/via/direct/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec, "analysis": analysis}
        elif mode == 'vlc_bridge':
            return {"mode": "vlc", "path": str(self.filepath), "duration_sec": d_sec, "analysis": analysis}
        elif mode == 'mpv_native':
            return {"mode": "mpv", "path": str(self.filepath), "duration_sec": d_sec, "analysis": analysis}
        elif mode == 'mse':
             return {"mode": "mse", "url": f"/stream/via/mse/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec, "analysis": analysis}
        else:
            # Fallback for HLS/DASH/fMP4
            return {"mode": "hls", "url": f"/hls/{urllib.parse.quote(str(relpath))}/index.m3u8", "duration_sec": d_sec, "analysis": analysis}
