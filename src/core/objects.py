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
class ObjectAsset:
    """
    Represents a single supplementary asset (e.g., Cover, Booklet, Disk Art).
    """
    path: str
    asset_type: str  # front, back, disc, inlay, booklet, poster
    locale: str = "US"  # Country/Locale code
    name: str = ""

@dataclass
class ObjectRelease:
    """
    Represents a specific release version of an object (e.g., Japanese Deluxe Edition).
    """
    name: str
    media_type: str  # DVD, Blu-ray, CD, Digital, Vinyl
    country: str = "US"
    edition: str = "Standard"
    year: str = ""
    items: List[int] = field(default_factory=list) # Member MediaItem IDs
    assets: List[ObjectAsset] = field(default_factory=list)

@dataclass
class MediaStream:
    """
    Represents an internal track within a media container (MKV, MP4, M4B).
    """
    index: int
    stream_type: str  # video, audio, subtitle
    codec: str = ""
    language: str = "und"
    title: str = ""
    is_default: bool = False
    is_forced: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MediaChapter:
    """
    Represents an internal time marker (Chapter) within a container.
    """
    id: int
    start_time: float
    end_time: float
    title: str = ""

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
    items: List[int] = field(default_factory=list)  # ALL IDs of child MediaItems
    sidecars: Dict[str, str] = field(default_factory=dict)  # k: variant, v: path (NFO, CUE, etc.)
    subtype: str = "OBJECT"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # [v1.54.002] High-Density Asset Model
    releases: List[ObjectRelease] = field(default_factory=list)
    global_assets: List[ObjectAsset] = field(default_factory=list)

    # [v1.54.003] Forensic Topology
    streams: List[MediaStream] = field(default_factory=list)
    chapters: List[MediaChapter] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "category": self.category,
            "items": self.items,
            "sidecars": self.sidecars,
            "subtype": self.subtype,
            "metadata": self.metadata,
            "releases": [r.__dict__ for r in self.releases],
            "global_assets": [a.__dict__ for a in self.global_assets],
            "streams": [s.__dict__ for s in self.streams],
            "chapters": [c.__dict__ for c in self.chapters]
        }

@dataclass
class FilmObject(MediaObject):
    """
    Specialized entity for Film collections.
    Supports versioning (Director's Cut, Extended) and release-specific sidecars.
    """
    subtype: str = "FILM_OBJECT"
    versions: Dict[str, int] = field(default_factory=dict)  # k: Cut name, v: item_id
    
    def __post_init__(self):
        self.category = "video"

@dataclass
class AudioRelease(MediaObject):
    """
    Specialized entity for Music collections (Albums, Singles, OST, etc.).
    Supports multiple releases (CD, Digital, SACD), CUE files, and EAC logs.
    """
    subtype: str = "AUDIO_RELEASE_OBJECT"
    is_gapless: bool = False
    has_cue: bool = False
    has_log: bool = False
    
    def __post_init__(self):
        self.category = "audio"

@dataclass
class AudiobookObject(MediaObject):
    """
    Specialized entity for Literary Media (M4B, MP3 Books).
    Supports internal chapters, Nero/Quicktime markers, and narrator metadata.
    """
    subtype: str = "AUDIOBOOK_OBJECT"
    narrator: str = ""
    author: str = ""
    series: str = ""
    volume: Optional[int] = None
    
    def __post_init__(self):
        self.category = "audio"

@dataclass
class SequenceObject(MediaObject):
    """
    Specialized entity for ordered sequences of media items.
    """
    subtype: str = "SEQUENCE_OBJECT"
    ordered_items: List[int] = field(default_factory=list) # Member IDs in sequence
    loop_mode: str = "none" # none, all, single
    
    def __post_init__(self):
        self.category = "audio" # Default to audio, can be mixed

def create_forensic_object(obj_type: str, **kwargs) -> MediaObject:
    """Factory function for creating specialized objects."""
    if obj_type.lower() == "film":
        return FilmObject(**kwargs)
    elif obj_type.lower() == "audio":
        return AudioRelease(**kwargs)
    elif obj_type.lower() == "audiobook":
        return AudiobookObject(**kwargs)
    elif obj_type.lower() == "sequence":
        return SequenceObject(**kwargs)
    return MediaObject(**kwargs)
