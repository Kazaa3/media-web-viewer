"""
Video-specific handler.
"""
from pathlib import Path
from typing import Dict, Any
import urllib.parse
from .media_handler import MediaHandler
from .metadata_pipeline import MetadataPipeline

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
        @brief Route video playback based on codec, container, and client capabilities.
        """
        from src.parsers.format_utils import is_direct_play_capable
        from src.core.remux_utils import remux_to_mp4_cache
        
        analysis = self.extract_metadata()
        d_sec = analysis.get("duration_sec", 0)
        ext = self.filepath.suffix.lower()
        
        # --- Centralized Media Routing (v1.35.68 Sync) ---
        is_direct = is_direct_play_capable(self.filepath, client)
        tags = analysis

        if is_direct:
            mode = 'direct'
        elif ext in ('.iso', '.bin', '.img') or self.filepath.is_dir() or analysis.get('is_disc'):
            mode = 'transcode'
        elif 'mpeg' in str(tags.get('video_codec', '')).lower() or 'vc1' in str(tags.get('video_codec', '')).lower():
            mode = 'transcode'
        elif tags.get('hdr') or analysis.get('hdr_type'):
            mode = 'vlc'
        else:
            mode = 'hls'

        # Response construction
        if mode == 'direct':
            return {"mode": "direct", "url": f"/direct/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec}
        elif mode == 'transcode':
            return {"mode": "transcode", "url": f"/transcode/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec}
        elif mode == 'vlc':
            return {"mode": "vlc", "path": str(self.filepath), "duration_sec": d_sec}
        else:
            return {"mode": "hls", "url": f"/hls/{urllib.parse.quote(str(relpath))}/index.m3u8", "duration_sec": d_sec}
