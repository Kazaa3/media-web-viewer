"""
Metadata Pipeline Orchestrator.
"""
from pathlib import Path
from typing import Dict, Any
import logging

log = logging.getLogger(__name__)

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
            log.warning(f"MetadataPipeline: File not found {self.filepath}")
            return {}
            
        try:
            return ffprobe_suite(self.filepath)
        except Exception as e:
            log.error(f"MetadataPipeline: Orchestration failed for {self.filepath}: {e}")
            return {}
