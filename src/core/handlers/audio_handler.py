"""
Audio-specific handler.
"""
from pathlib import Path
from typing import Dict, Any
import urllib.parse
from .media_handler import MediaHandler
from .metadata_pipeline import MetadataPipeline

class AudioHandler(MediaHandler):
    """
    @brief Specialized handler for audio formats.
    """
    def __init__(self, filepath: str | Path):
        super().__init__(filepath)
        self.pipeline = MetadataPipeline(self.filepath)

    def extract_metadata(self) -> Dict[str, Any]:
        return self.pipeline.execute()

    def process(self, client: str = 'browser', relpath: str = "") -> Dict[str, Any]:
        """
        @brief Process audio file.
        @details Usually routes to direct play because most audio is browser-compatible.
        """
        analysis = self.extract_metadata()
        d_sec = analysis.get("duration_sec", 0)
        
        # Audio is almost always direct streamed.
        # Fallback to transcode (e.g. for DSD or unsupported FLAC in some browsers) could be added here.
        url = f"/direct/{urllib.parse.quote(str(relpath))}"
        
        # A full routing might need the relative path from the media root
        # This will be passed from the orchestrator
        return {
            "mode": "direct",
            "url": url,
            "duration_sec": d_sec,
            "analysis": analysis
        }
