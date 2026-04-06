#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Category Master (Unified Categorization Chain)
v1.35.68 - Central source of truth for all media categories and mappings.
"""

import os
from typing import List, Dict

# Master Map: "Frontend Category Key" -> ["List of internal DB labels"]
# Unified: Audio and Multimedia (including Video)
MASTER_CAT_MAP: Dict[str, List[str]] = {
    "audio": [
        "audio", "album", "klassik", "hörbuch", "hörspiel", "podcast", 
        "musik", "compilation", "single", "radio", "soundtrack", "playlist", 
        "music", "song"
    ],
    "multimedia": [
        "multimedia", "video", "film", "serie", "tv", "movie", "tv show", 
        "musikvideos", "animes", "cartoons", "video object", "animations", 
        "documentary", "dok", "dokumentation", "concert", "konzerte",
        "iso", "disk-abbild", "pal dvd", "ntsc dvd", "blu-ray", "hd-dvd"
    ],
    "images": [
        "bilder", "grafik", "bild", "foto", "images", "gallery"
    ],
    "documents": [
        "dokument", "pdf", "text", "doc", "docx", "txt", "office"
    ],
    "ebooks": [
        "e-book", "ebook", "epub", "mobi"
    ],
    "abbild": [
        "abbild", "iso/image", "disk image", "pal dvd", "ntsc dvd", 
        "blu-ray", "disk-abbild", "dvd object"
    ],
    "spiel": [
        "spiel", "game", "pc spiel", "digitales spiel", "steam"
    ],
    "beigabe": [
        "beigabe", "supplement", "software", "additional"
    ],
    # Technical / Virtual Categories (v1.35.68)
    "transcoded": [], # Handled by filename marker check below
    "iso": ["abbild", "disk-abbild", "iso"]
}

# Technical Markers for non-category based filtering
TECH_MARKERS = {
    "transcoded": ["_transcoded", ".mp4_transcoded"],
    "iso": [".iso", ".bin", ".cue", ".nrg"],
    "mock": ["is_mock"],
    "stage": ["stage", "recovery", "is_stage"]
}

# Sub-categories for UI branch management
BRANCH_MAP = {
    "audio": ["audio"],
    "multimedia": ["multimedia", "abbild", "video"]
}

def audit_category_chain(item: Dict) -> str:
    """
    Automated debugging helper for the category chain.
    Describes why an item is assigned to a specific category.
    """
    raw_cat = str(item.get('category', 'Unbekannt')).lower()
    path = item.get('path', 'unknown')
    
    matched_branch = None
    for branch, internal_cats in MASTER_CAT_MAP.items():
        if raw_cat in internal_cats:
            matched_branch = branch
            break
            
    if matched_branch:
        return f"[AUDIT] Item '{item.get('name')}' (DB: {raw_cat}) -> CHAIN: Master={matched_branch} -> STATUS: OK"
    else:
        return f"[AUDIT] Item '{item.get('name')}' (DB: {raw_cat}) -> CHAIN: NO MATCH FOUND -> STATUS: DROPPED"

def get_allowed_internal_cats(displayed_cats: List[str]) -> List[str]:
    """
    Returns the flattened list of internal labels for the requested categories.
    """
    allowed = set()
    for dc in displayed_cats:
        labels = MASTER_CAT_MAP.get(dc.lower(), [])
        for label in labels:
            allowed.add(label.lower())
    return list(allowed)
