#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forensic Object Models (v1.54.001)
Higher-level orchestration layer for grouping media files into unified entities.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path

@dataclass
class MediaObject:
    """
    Base class for virtual grouping entities (Forensic SSOT).
    Represents a collection of files (versions, sidecars) that form a single logical asset.
    """
    id: Optional[int] = None
    name: str = ""
    path: str = ""  # The anchor path (usually the folder containing the assets)
    category: str = "unknown"
    items: List[int] = field(default_factory=list)  # IDs of child MediaItems
    sidecars: Dict[str, str] = field(default_factory=dict)  # k: variant, v: path (NFO, CUE, etc.)
    subtype: str = "OBJECT"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "category": self.category,
            "items": self.items,
            "sidecars": self.sidecars,
            "subtype": self.subtype,
            "metadata": self.metadata
        }

@dataclass
class FilmObject(MediaObject):
    """
    Specialized entity for Film collections.
    Supports versioning (Director's Cut, Extended) and release-specific sidecars.
    """
    subtype: str = "FILM_OBJECT"
    versions: Dict[str, int] = field(default_factory=dict)  # k: Cut name, v: item_id
    covers: List[str] = field(default_factory=list) # List of image paths (US, DE, etc.)
    
    def __post_init__(self):
        self.category = "video"

@dataclass
class AlbumObject(MediaObject):
    """
    Specialized entity for Music collections.
    Supports multiple releases (CD, Digital, SACD), CUE files, and EAC logs.
    """
    subtype: str = "ALBUM_OBJECT"
    releases: List[Dict[str, Any]] = field(default_factory=list)
    is_gapless: bool = False
    has_cue: bool = False
    has_log: bool = False
    
    def __post_init__(self):
        self.category = "audio"

def create_forensic_object(obj_type: str, **kwargs) -> MediaObject:
    """Factory function for creating specialized objects."""
    if obj_type.lower() == "film":
        return FilmObject(**kwargs)
    elif obj_type.lower() == "album":
        return AlbumObject(**kwargs)
    return MediaObject(**kwargs)
