"""
Base Media Handler Interface.
"""
from pathlib import Path
from typing import Dict, Any, Optional
import abc

class MediaHandler(abc.ABC):
    """
    @brief Base interface for all media handlers.
    @details Defines the contract for processing media requests and routing playback.
    """
    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)
    
    @abc.abstractmethod
    def process(self, client: str = 'browser') -> Dict[str, Any]:
        """
        @brief Process the media file and return a routing dictionary.
        @details Returns a dictionary representing the playback instructions (e.g., {"mode": "direct", "url": "/direct/..."}).
        """
        pass
        
    @abc.abstractmethod
    def extract_metadata(self) -> Dict[str, Any]:
        """
        @brief Extract and standardize metadata.
        @details Uses the metadata_pipeline to gather info.
        """
        pass
