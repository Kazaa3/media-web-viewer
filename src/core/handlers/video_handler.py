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
        from src.core.main import remux_to_mp4_cache  # Avoid circular import, should be refactored
        
        analysis = self.extract_metadata()
        d_sec = analysis.get("duration_sec", 0)
        ext = self.filepath.suffix.lower()
        
        # 1. MKV/Direct Play Handling
        if is_direct_play_capable(self.filepath, client):
            return {"mode": "direct", "url": f"/direct/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec}
            
        # 2. ISO / DVD
        if ext == ".iso" or self.filepath.is_dir():
            return {"mode": "vlc", "path": str(self.filepath), "duration_sec": d_sec}
            
        # 3. Complex Codec Transcoding
        if analysis.get("video_codec") in ["mpeg2video", "hevc", "vc1", "wmv3"]:
            return {"mode": "transcode", "url": f"/transcode/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec}
            
        # 4. MKV Remux Check (Heuristic)
        if ext == ".mkv" and analysis.get("video_codec") == "h264":
            remuxed = remux_to_mp4_cache(self.filepath)
            if remuxed:
                rel_cache = Path(remuxed).name
                return {"mode": "direct", "url": f"/cache/{rel_cache}", "duration_sec": d_sec}
            
        # 5. Fallback
        return {"mode": "transcode", "url": f"/transcode/{urllib.parse.quote(str(relpath))}", "duration_sec": d_sec}
