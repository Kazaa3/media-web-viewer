#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forensic Object Discovery Engine (v1.54.001)
Identifies and groups media collections (Films, Albums) from raw filesystem items.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from src.core.objects import (
    FilmObject, AudioRelease, AudiobookObject, SequenceObject, create_forensic_object
)
from src.parsers.format_utils import natural_sort_key

log = get_logger("object_discovery")

# --- REGISTRY: VERSION MARKERS (v1.54) ---
# Common nomenclature for Film and Album variations
VERSION_MARKERS = {
    "film": [
        "director's cut", "directors cut", "dc",
        "extended", "extended cut", "extended edition",
        "theatrical", "theatrical cut", "theatrical edition",
        "unrated", "ultimate", "final cut", "workprint",
        "remastered", "anniversary", "collector's edition"
    ],
    "album": [
        "standard", "deluxe", "premium", "limited", "anniversary",
        "remastered", "expanded", "japanese edition", "tour edition"
    ]
}

# --- REGISTRY: RELEVANT SIDECARS ---
SIDECAR_EXTENSIONS = {
    "film": [".nfo", ".txt"],
    "album": [".cue", ".log", ".txt", ".m3u", ".m3u8"],
    "covers": [".jpg", ".jpeg", ".png"]
}

class ObjectDiscoveryEngine:
    """
    Forensic engine to analyze a set of MediaItems and group them into logical Objects.
    """
    def __init__(self):
        self._version_regex = re.compile(r'[\(\[]([^\]\)]+)[\)\]]')

    def discover_groups(self, items: List[Dict[str, Any]]) -> List[Any]:
        """
        Main entry point for grouping.
        Matches files by parent directory and filename heuristics.
        """
        # 1. Group by parent directory
        by_folder: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            folder = str(Path(item['path']).parent)
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(item)
            
        objects = []
        for folder, folder_items in by_folder.items():
            objs = self._analyze_folder_context(folder, folder_items)
            objects.extend(objs)
            
        return objects

    def _analyze_folder_context(self, folder_path: str, items: List[Dict[str, Any]]) -> List[Any]:
        """
        Analyzes a single folder to determine if it's an 'Object' (Album/Film/Audiobook/Playlist).
        """
        folder_name = Path(folder_path).name
        
        # Split items into categories
        videos = [i for i in items if i.get('category') == 'video']
        audios = [i for i in items if i.get('category') == 'audio']
        playlists = [i for i in items if i.get('category') in ['playlists', 'playlist']]
        sidecars = [i for i in items if i.get('category') not in ['video', 'audio', 'playlist', 'playlists']]
        
        discovered = []
        
        # --- A. Film Object Detection ---
        if videos:
            if len(videos) == 1:
                obj = create_forensic_object("film", name=videos[0]['name'], path=folder_path)
                obj.items = [videos[0]['id']]
                self._enrich_film_sidecars(obj, items)
                discovered.append(obj)
            else:
                base_groups = self._group_by_base_name(videos)
                for base_name, group in base_groups.items():
                    obj = create_forensic_object("film", name=base_name, path=folder_path)
                    obj.items = [i['id'] for i in group]
                    for item in group:
                        version = self._extract_version_info(item['name'], "film")
                        if version:
                            obj.versions[version] = item['id']
                    self._enrich_film_sidecars(obj, items)
                    discovered.append(obj)
                    
        # --- B. Audiobook & Audio Discovery ---
        if audios and not videos:
            # 1. Detect M4B (Single-file Audiobook)
            m4b_items = [i for i in audios if str(i['path']).lower().endswith('.m4b')]
            if m4b_items:
                for m4b in m4b_items:
                    obj = create_forensic_object("audiobook", name=m4b['name'], path=m4b['path'])
                    obj.items = [m4b['id']]
                    discovered.append(obj)
                # Remove M4B from generic audio processing
                audios = [i for i in audios if not str(i['path']).lower().endswith('.m4b')]

            if audios:
                # 2. Heuristic: Audiobook Folder vs Audio Collection
                is_likely_audiobook = any(k in folder_name.lower() for k in ["hörbuch", "audiobook", "book", "lesung"])
                is_likely_album = any(i.get('tags', {}).get('album') for i in audios)

                if is_likely_audiobook and not is_likely_album:
                    obj = create_forensic_object("audiobook", name=folder_name, path=folder_path)
                else:
                    album_title = audios[0].get('tags', {}).get('album', folder_name)
                    obj = create_forensic_object("audio", name=album_title, path=folder_path)
                
                obj.items = [i['id'] for i in audios]
                self._enrich_audio_sidecars(obj, items)
                discovered.append(obj)

        # --- C. Sequence Discovery ---
        for pl in playlists:
            obj = create_forensic_object("sequence", name=pl['name'], path=pl['path'])
            obj.items = [pl['id']]
            discovered.append(obj)
            
        return discovered

    def _group_by_base_name(self, items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Groups files that share a common prefix before version markers."""
        groups = {}
        for item in items:
            name = item['name']
            # Heuristic: Remove bracketed info to find base name
            base = self._version_regex.sub('', name).strip()
            # Remove extension for comparison
            base = os.path.splitext(base)[0]
            if base not in groups:
                groups[base] = []
            groups[base].append(item)
        return groups

    def _extract_version_info(self, filename: str, category: str) -> Optional[str]:
        """Extracts version strings (e.g. Director's Cut) from filename."""
        matches = self._version_regex.findall(filename)
        markers = VERSION_MARKERS.get(category, [])
        for m in matches:
            if any(marker in m.lower() for marker in markers):
                return m.strip()
        return None

    def _enrich_film_sidecars(self, obj: FilmObject, all_items: List[Dict[str, Any]]):
        """Identifies NFOs and Covers for Films."""
        for item in all_items:
            ext = str(item.get('extension', '')).lower()
            if ext in SIDECAR_EXTENSIONS["film"]:
                obj.sidecars["nfo"] = item['path']
            elif ext in SIDECAR_EXTENSIONS["covers"]:
                obj.covers.append(item['path'])

    def _enrich_audio_sidecars(self, obj: AudioRelease, all_items: List[Dict[str, Any]]):
        """Identifies CUE, Log, and Playlists for Audio Collections."""
        for item in all_items:
            ext = str(item.get('extension', '')).lower()
            if ext == ".cue":
                obj.has_cue = True
                obj.sidecars["cue"] = item['path']
            elif ext == ".log":
                obj.has_log = True
                obj.sidecars["log"] = item['path']
            elif ext in [".m3u", ".m3u8"]:
                obj.sidecars["playlist"] = item['path']
            elif ext in SIDECAR_EXTENSIONS["covers"]:
                # Use as cover
                if not obj.metadata.get("cover"):
                    obj.metadata["cover"] = item['path']
