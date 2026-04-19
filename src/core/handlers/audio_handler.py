from pathlib import Path
from typing import Dict, Any
import urllib.parse
from .media_handler import MediaHandler
from .metadata_pipeline import MetadataPipeline
from src.core.logger import get_logger

log = get_logger("audio_handler")

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
        """
        analysis = self.extract_metadata()
        d_sec = analysis.get("duration", 0) # Fixed to SSOT 'duration' (Phase 9)
        
        log.info(f"[PLAY-PULSE] AudioHandler: {self.filepath.name} | Duration: {d_sec}s")
        
        # Audio is almost always direct streamed.
        url = f"/stream/via/direct/{urllib.parse.quote(str(relpath))}"
        
        return {
            "mode": "direct",
            "url": url,
            "duration_sec": d_sec,
            "analysis": analysis
        }

