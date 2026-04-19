from pathlib import Path
from typing import Dict, Any
from src.core.logger import get_logger

log = get_logger("metadata_pipeline")

class MetadataPipeline:
    """
    @brief Orchestrates different parsers to build a unified metadata object.
    @details Calls ffprobe_suite, mutagen, or other parsers in sequence.
    """
    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)
        
    def execute(self) -> Dict[str, Any]:
        """
        @brief Runs the metadata extraction pipeline.
        @details Currently heavily relies on ffprobe_suite from format_utils.
        """
        from src.parsers.format_utils import ffprobe_suite
        
        if not self.filepath.exists():
            log.warning(f"[Pipeline] File not found: {self.filepath}")
            return {}
            
        try:
            return ffprobe_suite(self.filepath)
        except Exception as e:
            log.error(f"[Pipeline] Orchestration failed for {self.filepath}: {e}", exc_info=True)
            return {}

