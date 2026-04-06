#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Category Master (Unified Categorization Chain)
v1.35.68 - Central source of truth for all media categories and mappings.
"""

import os
from typing import List, Dict

from src.core.config_master import GLOBAL_CONFIG

# Master Map (Centralized v1.35.68)
MASTER_CAT_MAP = GLOBAL_CONFIG["category_registry"]["master_map"]

# Technical Markers (Centralized v1.35.68)
TECH_MARKERS = GLOBAL_CONFIG["category_registry"]["tech_markers"]

# Sub-categories for UI branch management (Centralized v1.35.68)
BRANCH_MAP = GLOBAL_CONFIG["category_registry"]["branch_map"]

def audit_category_chain(item: Dict) -> str:
    """
    Automated debugging helper for the category chain.
    Describes why an item is assigned to a specific category.
    """
    raw_cat = str(item.get('category', 'Unbekannt')).lower()
    path = item.get('path', 'unknown')
    
    matched_branch = None
    for branch, internal_cats in MASTER_CAT_MAP.items():
        # Canonical comparison (standardized lowercase IDs)
        if raw_cat in [ic.lower() for ic in internal_cats] or raw_cat == branch.lower():
            matched_branch = branch
            break
            
    if matched_branch:
        return f"[AUDIT] Item '{item.get('name')}' (DB: {raw_cat}) -> CHAIN: Master={matched_branch} -> STATUS: OK"
    else:
        # Fallback: check if raw_cat is a known master branch itself
        if raw_cat in [b.lower() for b in MASTER_CAT_MAP.keys()]:
            return f"[AUDIT] Item '{item.get('name')}' (DB: {raw_cat}) -> CHAIN: Direct Master Match -> STATUS: OK"
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
