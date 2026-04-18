import os
import time
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Tuple, cast

# --- Forensic Handshake Imports ---
from src.core.config_master import (
    GLOBAL_CONFIG, ALL_AUDIO_EXTENSIONS, ALL_VIDEO_EXTENSIONS, 
    PICTURE_EXTENSIONS, DOCUMENT_EXTENSIONS, ARCHIVE_EXTENSIONS,
    log_dropped_reasons
)
from src.core.models import MASTER_CAT_MAP, TECH_MARKERS, get_allowed_internal_cats
from src.core import db

# Project Root Resolution (Consistent with main.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Specialized Lazy Config Proxy (Shim for PARSER_CONFIG)
# In a full-scale refactor, this would be centralized.
def get_parser_config():
    from src.core.main import PARSER_CONFIG
    return PARSER_CONFIG

from src.core.logger import get_logger
log = get_logger("api_library")

def apply_library_filters(all_media: List[Dict],
                          force_raw: bool = False,
                          search: str = "",
                          genre: str = "all",
                          year: str = "all",
                          active_branch: str = None) -> Tuple[List[Dict], Dict[str, Any]]:
    """
    @brief Unified category mapping and filtering (v1.35.99 Logic Audit).
    @return Tuple of (filtered_list, audit_metadata)
    """
    # Avoid circular import from main.py which causes threading deadlocks in Eel (v1.46.038)
    if force_raw and not search and genre == "all" and year == "all":
        log.info("[BD-AUDIT] STAGE 0 (RAW): Bypassing all filters.")
        return all_media, {"status": "raw_bypass", "dropped_total": 0, "stage": 0}

    # Internal fallback to avoid circular lock during concurrent requests
    displayed_cats = ["all", "audio", "video", "pictures", "disk_images", "documents"]
    allowed_internal_cats = get_allowed_internal_cats(displayed_cats)

    branch_registry = GLOBAL_CONFIG.get("branch_architecture_registry", {})
    supported_by_branch = branch_registry.get(active_branch) if active_branch else None

    if supported_by_branch:
        log.info(f"[BRIDGE] Enforcing architectural constraints for branch: {str(active_branch).upper() if active_branch else 'NONE'}")

    log.info(f"[DB-SCAN] Filtering through {len(all_media)} candidates. Mode: {active_branch or 'GLOBAL'}")
    
    filtered = []
    dropped_reasons = GLOBAL_CONFIG["audit_registry"]["dropped_reasons_template"].copy()
    dropped_paths = []

    # Get Hydration Mode once (SSOT)
    h_registry = GLOBAL_CONFIG.get('forensic_hydration_registry', {})
    h_mode = h_registry.get('mode', 'both')

    real_count_potential = 0
    mock_count_potential = 0

    for item in all_media:
        item_is_mock = bool(item.get('is_mock', 0))
        
        # 1. Forensic Hydration Guard (Consolidated v1.46.050)
        if h_mode == 'real' and item_is_mock:
            dropped_reasons["mock_filtered"] = dropped_reasons.get("mock_filtered", 0) + 1
            continue
        if h_mode == 'mock' and not item_is_mock:
            dropped_reasons["real_filtered"] = dropped_reasons.get("real_filtered", 0) + 1
            continue
        
        if not item_is_mock: real_count_potential += 1
        else: mock_count_potential += 1

        if genre == "all" and "all" in displayed_cats:
            filtered.append(item)
            continue

        item_cat = str(item.get('category', 'unknown')).lower()
        path = str(item.get('path', '')).lower()
        ext = os.path.splitext(path)[1] if path else ""

        if item_cat not in allowed_internal_cats or item_cat in ['klassik', 'musik', 'music', 'multimedia']:
            if ext in ALL_AUDIO_EXTENSIONS or item_cat in ['klassik', 'musik', 'music']:
                item_cat = 'audio'
            elif ext in ALL_VIDEO_EXTENSIONS:
                item_cat = 'video'
            elif item_cat == 'multimedia':
                item_cat = 'video'
            item['category'] = item_cat
            
        if not force_raw and supported_by_branch:
            if "all" not in supported_by_branch and item_cat not in supported_by_branch:
                item_stage = item.get('capability_stage') or item_cat
                if item_stage not in supported_by_branch:
                    dropped_reasons["branch_lock"] += 1
                    dropped_paths.append(path)
                    continue

        if search and search.lower() not in str(item.get('name', '')).lower():
            dropped_reasons["search_mismatch"] += 1
            continue

        item_genre = item.get('tags', {}).get('genre', '').lower()
        if genre != "all" and genre.lower() not in item_genre:
            dropped_reasons["genre_mismatch"] += 1
            continue

        item_year = str(item.get('tags', {}).get('year', ''))
        if year != "all" and year != item_year:
            dropped_reasons["year_mismatch"] += 1
            continue

        filtered.append(item)

    audit_meta = {
        "status": "filtered",
        "kept": len(filtered),
        "dropped_total": sum(dropped_reasons.values()),
        "dropped_reasons": dropped_reasons,
        "allowed_cats": allowed_internal_cats,
        "hydration_stats": {
            "mode": h_mode,
            "real_available": real_count_potential,
            "mock_available": mock_count_potential
        }
    }

    log_dropped_reasons(dropped_reasons, f"Library Filter ({active_branch or 'ALL'})", sample_paths=dropped_paths)

    if not filtered and all_media:
        return all_media, {"status": "emergency_raw", "dropped_total": 0, "stage": 0, "audit": audit_meta}

    return filtered, audit_meta

def get_library(force_raw: bool = False, audit_stage: int = 0, active_branch: str = None) -> Dict[str, Any]:
    """Unified library bridge with integrated forensics (v1.35.96)"""
    log.info(f"[BD-AUDIT] Handshake: API-Library get_library triggered.")
    
    # [v1.46.032] SSOT Overrides
    h_registry = GLOBAL_CONFIG.get('forensic_hydration_registry', {})
    if h_registry.get('audit_stage') is not None:
        # Enforce SSOT if explicitly set in config
        config_stage = h_registry.get('audit_stage')
        if config_stage > 0:
            audit_stage = config_stage

    pid = os.getpid()
    db_path = str(Path(db.DB_FILENAME).resolve())

    db_exists = os.path.exists(db_path)
    db_size = os.path.getsize(db_path) if db_exists else -1
    db_health = "unknown"
    
    if db_exists:
        try:
            conn = sqlite3.connect(db_path, timeout=1)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            db_health = cursor.fetchone()[0].lower()
            conn.close()
        except Exception:
            db_health = "error"

    fs_audit = {"exists": db_exists, "size": db_size, "health": db_health, "pid": pid, "path": db_path}
    all_media = []
    count_total = 0

    try:
        all_media = db.get_all_media()
        count_total = len(all_media)
    except Exception as e:
        log.error(f"[BD-AUDIT] DATABASE CRITICAL FAILURE: {e}")
        # [v1.46.058] Still try to get the count even if it fails partially
        count_total = 0
        status = "db_busy"

    for item in all_media:
        path = str(item.get('path', '')).lower()
        ext = os.path.splitext(path)[1]
        cat_legacy = str(item.get('category', '')).lower()
        if ext in ALL_AUDIO_EXTENSIONS: item['category'] = 'audio'
        elif ext in ALL_VIDEO_EXTENSIONS: item['category'] = 'video'

    filtered_media, logic_audit = apply_library_filters(all_media, force_raw=force_raw, active_branch=active_branch)

    # [v1.46.050] Hardened Fallback Logic
    # We no longer filter again here, as apply_library_filters handling it.
    final_media = filtered_media

    # Forensic Check: Mode-Aware Fallback
    h_mode = logic_audit.get("hydration_stats", {}).get("mode", "both")
    
    if len(final_media) == 0 and count_total > 0:
        if h_mode == 'real':
            # DO NOT return mocks if REAL was requested and none found.
            log.warning(f"[BD-AUDIT] REAL mode requested but 0 items found. Blocking mock fallback.")
            status = "empty_real_set"
        else:
            final_media = all_media[:2] # Fallback for BOTH/MOCK
            status = "recovery-emergency"
    else:
        status = "synchronized"

    return {
        "media": final_media,
        "db_count": count_total if count_total > 0 else len(all_media),
        "status": status,
        "audit": {
            "stage": audit_stage,
            "pid": pid,
            "db": fs_audit,
            "logic": logic_audit,
            "final_count": len(final_media)
        }
    }

def get_library_audit_summary() -> Dict[str, Any]:
    """Provides a breakdown of item counts at each stage of hydration."""
    all_media = db.get_all_media()
    total = len(all_media)
    cat_filtered, _ = apply_library_filters(all_media, force_raw=True)
    full_filtered, full_audit = apply_library_filters(all_media, force_raw=False)

    return {
        "stages": {
            "0_db_raw": total,
            "1_ssot_norm": total,
            "2_cat_mapped": len(cat_filtered),
            "3_production": len(full_filtered)
        },
        "dropped_reasons": full_audit.get("dropped_reasons", {}),
        "allowed_cats": full_audit.get("allowed_cats", [])
    }

def force_sync_all():
    """Emergency recovery: bypass all filters."""
    all_media = db.get_all_media()
    return {"media": all_media, "db_count": len(all_media), "status": "raw-recovery"}

def sync_playback_state(payload: Dict[str, Any]) -> bool:
    """Synchronizes technical playback state to the backend."""
    from src.core import config_master
    try:
        config_master.SHARED_PLAYBACK_STATE.update({
            "queue_count": payload.get("queueCount", 0),
            "active_index": payload.get("index", -1),
            "active_path": payload.get("path"),
            "last_update": time.time()
        })
        return True
    except Exception:
        return False

def get_library_filtered(search: str = "", genre: str = "all", year: str = "all",
                         sort_by: str = "name", force_raw: bool = False, active_branch: str = None) -> Dict[str, Any]:
    """Advanced filtering for the media library."""
    all_media = db.get_all_media()
    filtered, logic_audit = apply_library_filters(
        all_media, force_raw=force_raw, search=search, genre=genre, year=year, active_branch=active_branch)

    # Sorting
    if sort_by == "year":
        filtered.sort(key=lambda x: str(x.get('tags', {}).get('year', '9999')), reverse=True)
    elif sort_by == "artist":
        filtered.sort(key=lambda x: str(x.get('tags', {}).get('artist', 'z')).lower())
    else:
        filtered.sort(key=lambda x: str(x.get('name', 'z')).lower())

    return {
        "media": filtered,
        "db_count": len(all_media),
        "status": "ready"
    }
