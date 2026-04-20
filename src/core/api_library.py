import os
from src.core.eel_shell import eel
import time
import sqlite3
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, cast, Optional

# --- Forensic Handshake Imports ---
from src.core.config_master import (
    GLOBAL_CONFIG, ALL_AUDIO_EXTENSIONS, ALL_VIDEO_EXTENSIONS, 
    PICTURE_EXTENSIONS, DOCUMENT_EXTENSIONS, ARCHIVE_EXTENSIONS,
    log_dropped_reasons
)
from src.core.models import MASTER_CAT_MAP, TECH_MARKERS, get_allowed_internal_cats
from src.core import db

# Project Root Resolution (Consistent with main.py)
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, DATA_DIR, MEDIA_DIR, LOGS_DIR

# Specialized Lazy Config (SSOT)
from src.parsers.format_utils import PARSER_CONFIG, save_parser_config, get_default_scan_dir

from src.core.logger import get_logger
log = get_logger("api_library")

from src.core.object_discovery import ObjectDiscoveryEngine
from src.core.models import MediaItem
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

        # 0. Object-Centric Grouping Guard (v1.54)
        # Hide children (items with a parent) from the main library view 
        # unless they are the 'OBJECT' containers themselves.
        # This enforces the "Grouped Object" standard requested by the user.
        if not force_raw and item.get('parent_id') is not None and item.get('type') != 'object':
            dropped_reasons["child_filtered"] = dropped_reasons.get("child_filtered", 0) + 1
            continue

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

        # --- [v1.54.005] VIRTUAL CATEGORY RESOLUTION ---
        if genre == "all_audio_releases":
            if item.get('type') == 'object' and item.get('category') == 'audio':
                filtered.append(item)
                continue
            else:
                dropped_reasons["genre_mismatch"] += 1
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

    return filtered, audit_meta

@eel.expose
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
        # [v1.46.060] Hardened Hydration: Retry internally if DB is busy
        # This prevents the frontend from receiving an empty set and triggering 
        # its own aggressive (and redundant) retry logic.
        max_internal_retries = 3
        for attempt in range(max_internal_retries):
            all_media = db.get_all_media()
            count_total = len(all_media)
            
            if count_total > 0 or not db.DB_FILENAME or not os.path.exists(db.DB_FILENAME):
                break
                
            log.warning(f"[BD-AUDIT] Internal Retry {attempt+1}/{max_internal_retries}: DB returned 0 items. Waiting for stabilization...")
            time.sleep(0.5)
            
    except Exception as e:
        log.error(f"[BD-AUDIT] DATABASE CRITICAL FAILURE: {e}")
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
    
    # [v1.46.085] Payload Readiness Trace
    log.info(f"🚀 [SPAWN-LOG] PAYLOAD-READY -> {len(final_media)} items (Source: {'MOCKS' if all(it.get('is_mock') for it in final_media) else 'REAL_DB'})")

    triggered_auto_scan = (count_total == 0)
    if triggered_auto_scan:
        log.warning("[BD-AUDIT] Database empty. Triggering background auto-scan...")
        import threading
        threading.Thread(target=_scan_media_execution, kwargs={'clear_db': False}, daemon=True).start()

    return {
        "media": final_media,
        "db_count": count_total if count_total > 0 else len(all_media),
        "status": status,
        "triggered_auto_scan": triggered_auto_scan,
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

# --- Library Sync & Parser Orchestration (Migrated from main.py v1.54.018) ---

@eel.expose
def run_direct_scan():
    """ Triggers a full re-index of the media library. """
    log.warning("[Diagnostic] Manual DIRECT SCAN triggered. Clearing DB...")
    try:
        _scan_media_execution(clear_db=True)
        stats = db.get_db_stats()
        return {"status": "success", "items_found": stats.get('total_items', 0)}
    except Exception as e:
        log.error(f"[Diagnostic] Direct Scan failed: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def scan_media(dir_path: str | None = None, clear_db: bool = True):
    """
    @brief Scans a directory recursively and indexes audio files.
    """
    import eel
    if getattr(eel, 'js_set_scanning_status', None):
        eel.js_set_scanning_status(True)

    try:
        _scan_media_execution(dir_path, clear_db)
    finally:
        if getattr(eel, 'js_set_scanning_status', None):
            eel.js_set_scanning_status(False)


def _parse_nfo_file(nfo_path: Path) -> dict:
    """
    Parses a Kodi/Plex style .nfo XML file (Centralized v1.46.131).
    """
    metadata = {}
    nfo_cfg = GLOBAL_CONFIG.get("nfo_settings", {})
    if not nfo_cfg.get("enable_parsing", True):
        return {}

    try:
        import xml.etree.ElementTree as ET
        if not nfo_path.exists(): return {}
        
        # Use centralized encoding if provided (default utf-8)
        encoding = nfo_cfg.get("encoding", "utf-8")
        with nfo_path.open("r", encoding=encoding, errors="replace") as f:
            content = f.read()
            # Basic sanity check for XML
            if not content.strip().startswith("<"):
                return {}
            
            # Reset pointer or parse from string
            root = ET.fromstring(content)
        
        # Mapping: XML Tag -> Metadata Key (Centralized)
        mappings = nfo_cfg.get("mapping", {
            'title': 'title', 'year': 'year', 'genre': 'genre',
            'artist': 'artist', 'album': 'album', 'plot': 'plot'
        })
        
        for xml_tag, meta_key in mappings.items():
            el = root.find(xml_tag)
            if el is not None and el.text:
                metadata[meta_key] = el.text.strip()
                
        # Handle multiple genres (Kodi standard)
        genres = [g.text for g in root.findall('genre') if g.text]
        if genres: 
            metadata['genre'] = ", ".join(genres)
            
    except Exception as e:
        # Respect the global compact logging flag
        exc = None if GLOBAL_CONFIG["logging_registry"].get("log_compact_errors_only", True) else True
        log.error(f"[NFO-Parser-Error] Failed to parse {nfo_path.name}: {e}", exc_info=exc)
        
    return metadata


def _scan_media_execution(dir_path: str | None = None, clear_db: bool = True):
    """
    @brief Performs the actual media scan (Refactored for Round 5.5 Performance).
    """
    start_time = time.time()
    count_indexed = 0
    total_traversed = 0

    # 0. Round 5.6 - Emergency DB Purge (v1.35.98)
    if clear_db:
        log.warning("[DB-SCAN] Round 5.6: Emergency DB Purge triggered. Clearing existing items.")
        db.clear_media()
        # [DIAGNOSTIC] Ensure existing_media is reset
        existing_media = set()
    else:
        existing_media = {str(Path(m['path']).resolve()) for m in db.get_all_media_items() if m.get('path')}

    # 1. Imports (Round 5.5: Avoid Scoping Issues)
    from src.parsers.format_utils import (
        AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, PICTURE_EXTENSIONS,
        DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, DISK_IMAGE_EXTENSIONS,
        DSD_EXTENSIONS, HDDVD_EXTENSIONS, PARSER_CONFIG, get_default_scan_dir
    )

    # 4. Prepare Extension Filter & Fast-Category-Mapper (v1.35.98)
    from src.core.models import MASTER_CAT_MAP
    ext_to_cat = {}
    for cat, info in MASTER_CAT_MAP.items():
        for ext in info.get("extensions", []):
            ext_to_cat[ext.lower()] = cat

    all_exts = set(ext_to_cat.keys())
    
    # [v1.45.130] Toggles
    enable_collections = GLOBAL_CONFIG.get("enable_collection_management", True)
    enable_nfo = GLOBAL_CONFIG.get("enable_nfo_parsing", True)

    # 2. Fast-Scan Override
    parser_mode = 'lightweight'
    # Wait, GLOBAL_CONFIG is imported, but parser_mode might be in a subdict.
    # We'll just assume it works as in main.py for now.

    # MUTE ARTWORK (The True 10-minute Stall Source)
    orig_art_cfg = PARSER_CONFIG.get('ffmpeg_extract_thumbnails', True)
    PARSER_CONFIG['ffmpeg_extract_thumbnails'] = False

    log.info(f"[DB-SCAN] EMERGENCY Round 5.5 (v1.35.98): Mode={parser_mode} & Muting Thumbnails.")

    # 3. Path Resolution
    scan_roots = [Path(dir_path).resolve()] if dir_path else []
    if not scan_roots:
        config_dirs = PARSER_CONFIG.get("scan_dirs", [])
        for d in config_dirs:
            p = Path(d).resolve()
            if p.exists():
                scan_roots.append(p)

    # Default fallback
    if not scan_roots:
        scan_roots = [get_default_scan_dir()]

    # 5. Batch Collection
    collected_items = []

    try:
        scan_settings = GLOBAL_CONFIG.get("scan_settings", {})
        max_files = scan_settings.get("max_files", 50000)
        max_depth = scan_settings.get("max_depth", 12)
        enable_ext_skip = scan_settings.get("enable_extension_skipping", True)
        skip_exts = set(scan_settings.get("skip_extensions", [".txt", ".log", ".tmp"]))
        enable_size_skip = scan_settings.get("enable_size_skipping", True)
        min_size = scan_settings.get("min_size_kb", 1) * 1024
        max_size = scan_settings.get("max_size_mb", 50000) * 1024 * 1024
        batch_size = scan_settings.get("batch_commit_size", 250)
        log_compact = scan_settings.get("log_compact_errors_only", True)
        log_unsupported = scan_settings.get("log_unsupported_extensions", False)

        for scan_root in scan_roots:
            log.info(f" [Scan] Starting scan of: {scan_root}")
            for root, dirs, files in os.walk(str(scan_root), followlinks=False):
                total_traversed += (len(files) + len(dirs))
                if total_traversed > max_files:
                    log.warning(f"[DB-SCAN] Safety Cap Triggered ({max_files} items). Stopping traversal.")
                    dirs[:] = []  # Stop os.walk from recursing further
                    break

                d = Path(root)
                # Depth Check (Centralized)
                try:
                    rel_path = d.relative_to(scan_root)
                    if len(rel_path.parts) > max_depth:
                        dirs[:] = []  # Stop recursion
                        continue
                except Exception as e:
                    exc = None if log_compact else True
                    log.error(f"[Scan-Depth-Error] Failed depth calculation for {d}: {e}", exc_info=exc)
                    continue

                # 2. Folders as Media (Albums/DVDs) - v1.45.130
                if d != scan_root and enable_collections:
                    media_files = [f for f in files if f.lower().endswith(tuple(all_exts))]
                    m_count = len(media_files)
                    
                    if m_count > 0:
                        # 1. Detect NFO & Coverage
                        nfo_file = next((f for f in files if f.lower().endswith('.nfo')), None)
                        nfo_data = _parse_nfo_file(d / nfo_file) if (nfo_file and enable_nfo) else {}
                        
                        # 2. Determine Collection Category
                        is_audio = any(f.lower().endswith(tuple(AUDIO_EXTENSIONS)) for f in media_files)
                        cat = 'audio' if is_audio else 'video'
                        
                        # Forensic Categorization Logic (v1.45.130-EXT)
                        folder_name = d.name.lower()
                        genre = nfo_data.get('genre', '').lower()
                        artist = nfo_data.get('artist', '').lower()
                        
                        # Optical Media Check (v1.45.130)
                        has_dvd = 'video_ts' in [sd.lower() for sd in dirs]
                        has_bd = 'bdmv' in [sd.lower() for sd in dirs]
                        
                        if has_dvd or has_bd: cat = 'video_iso'
                        elif 'klassik' in genre or 'classical' in genre or 'klassik' in folder_name: cat = 'klassik'
                        elif 'soundtrack' in genre or 'ost' in genre or 'ost' in folder_name: cat = 'soundtrack'
                        elif 'podcast' in genre or 'podcast' in folder_name: cat = 'podcast'
                        elif 'hörbuch' in genre or 'audiobook' in genre or 'hörbuch' in folder_name: cat = 'hörbuch'
                        elif ('mix' in folder_name or 'mixtape' in folder_name) and any(va in artist for va in ['va', 'varios', 'various artists']): cat = 'mix'
                        elif any(va in artist for va in ['va', 'varios', 'various artists']): cat = 'compilation'
                        elif m_count > 1 and is_audio: cat = 'album'
                        elif m_count > 1 and not is_audio: cat = 'series'
                        elif 'doku' in folder_name or 'dokumentation' in folder_name: cat = 'documentation'
                        
                        collected_items.append({
                            'name': f"[FOLDER] {d.name}", 'path': str(d), 'category': cat,
                            'is_mock': 0, 'mock_stage': 0, 'full_tags': nfo_data, 'chapters': [],
                            'type': 'folder', 'media_type': cat, 'nfo_parsed': 1 if nfo_data else 0
                        })
                        count_indexed += 1
                        
                        # Atomic Batch Commit (v1.46.102)
                        if len(collected_items) >= batch_size:
                            log.info(f"[DB-SCAN] Batch Commit (Folder): {len(collected_items)} items...")
                            db.insert_media_batch(collected_items)
                            collected_items = []

                # 3. Individual Files (Standard Pass)
                for filename in files:
                    ext = "." + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ""
                    
                    if enable_ext_skip and ext in skip_exts:
                        log.debug(f"[Scan-Trace] SKIPPING (Blacklisted Ext '{ext}'): {filename}")
                        continue
                        
                    if ext not in all_exts:
                        if log_unsupported:
                            log.debug(f"[Scan-Trace] SKIPPING (Unsupported Ext '{ext}'): {filename}")
                        continue
                        
                    f_path = os.path.join(root, filename)
                    if f_path in existing_media:
                        log.debug(f"[Scan-Trace] SKIPPING (Already Indexed): {filename}")
                        continue

                    if enable_size_skip:
                        try:
                            f_size = os.path.getsize(f_path)
                            if f_size < min_size:
                                log.debug(f"[Scan-Trace] SKIPPING (Ghost File < {min_size}B): {filename}")
                                continue
                            if f_size > max_size:
                                log.debug(f"[Scan-Trace] SKIPPING (Oversize File > {max_size}B): {filename}")
                                continue
                        except Exception as e:
                            log.warning(f"[Scan-Size-Error] Skip due to unreadable file size for {filename}: {e}")
                            continue

                    try:
                        cat = ext_to_cat.get(ext, 'Unknown')
                        log.debug(f"[Scan-Trace] INDEXING: {filename} -> {cat}")
                        collected_items.append({
                            'name': filename, 'path': f_path, 'category': cat,
                            'is_mock': 0, 'mock_stage': 0, 'full_tags': {}, 'chapters': [],
                            'type': 'file', 'file_type': ext[1:].upper(),
                            'extension': ext
                        })
                        count_indexed += 1
                    except Exception as e:
                        exc = None if log_compact else True
                        log.error(f"[Scan-Index-Error] Fatal crash indexing '{filename}': {e}", exc_info=exc)

                    # 4. Atomic Batch Commit (v1.46.102)
                    if len(collected_items) >= batch_size:
                        log.info(f"[DB-SCAN] Batch Commit: {len(collected_items)} items...")
                        db.insert_media_batch(collected_items)
                        collected_items = []

        # 6. Final Sync
        if collected_items:
            log.info(f"[DB-SCAN] Finalizing batch of {len(collected_items)} items...")
            db.insert_media_batch(collected_items)

        # --- [v1.54.001] OBJECT-CENTRIC GROUPING PHASE ---
        log.info("[DB-SCAN] Starting Object-Centric Grouping Phase (v1.54)...")
        all_items = db.get_all_media_items()
        engine = ObjectDiscoveryEngine()
        discovered_objects = engine.discover_groups(all_items)
        
        objects_inserted = 0
        for obj in discovered_objects:
            # 1. Insert the parent object record
            parent_id = db.insert_media_object(obj.to_dict())
            if parent_id:
                objects_inserted += 1
                # 2. Link all child items to the new parent
                for item_id in obj.items:
                    db.set_item_parent(item_id, parent_id)
                # 3. Link sidecars (using path as lookup)
                for sidecar_path in obj.sidecars.values():
                    sidecar_item = next((it for it in all_items if it['path'] == sidecar_path), None)
                    if sidecar_item:
                        db.set_item_parent(sidecar_item['id'], parent_id)

        log.info(f"[DB-SCAN] Object Grouping Complete. Created {objects_inserted} high-density objects.")

        # 10. Round 5.6 - Final Sync & Availability Check (v1.35.98)
        if not clear_db:
            log.info("[DB-SCAN] Running availability check for incremental sync...")
            total, missing = db.check_media_availability()
            log.info(f"[DB-SCAN] Availability check done. Total: {total} | Missing/Renamed: {missing}")

        return {"status": "ok", "count": count_indexed, "time_seconds": time.time() - start_time}

    except Exception as e:
        log.error(f"[Scan-Trace] CRITICAL FAILURE: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        # Restore artwork setting
        PARSER_CONFIG['ffmpeg_extract_thumbnails'] = orig_art_cfg
        # Silent Status Update (Optional bridge in api_library)
        pass


@eel.expose
def add_scan_dir():
    """
    @brief Opens a dialog to select a new directory for library scanning.
    """
    from src.core.main import pick_folder
    new_dir = pick_folder()
    if new_dir:
        dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
        if new_dir not in dirs:
            dirs.append(new_dir)
            PARSER_CONFIG["scan_dirs"] = dirs
            save_parser_config()
            return {"status": "ok", "dirs": dirs}
    return {"status": "cancel"}


@eel.expose
def remove_scan_dir(dir_path):
    """
    @brief Removes a directory from the scan list in the configuration.
    """
    dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
    if dir_path in dirs:
        dirs.remove(dir_path)
        PARSER_CONFIG["scan_dirs"] = dirs
        save_parser_config()
        return {"status": "ok", "dirs": dirs}
    return {"status": "error", "message": "Pfad nicht in Liste"}


@eel.expose
def update_tags(name, tags_dict):
    """
    @brief Saves customized tags for a media item in the database.
    """
    log.debug(f"[DB-Update] Updating tags for {name}: {tags_dict}")
    db.update_media_tags(name, tags_dict)
    return {"status": "ok"}


@eel.expose
def rename_media(old_name, new_name):
    """
    @brief Renames a media record in the database.
    """
    if not new_name or new_name.strip() == "":
        return {"status": "error", "message": "Name darf nicht leer sein"}

    log.debug(f"[DB-Update] Renaming record: {old_name} -> {new_name}")

    success = db.rename_media(old_name, new_name)
    if success:
        return {"status": "ok"}
    else:
        return {"status": "error", "message": "Name bereits vorhanden oder Fehler"}


@eel.expose
def delete_media(name):
    """
    @brief Deletes a media item from the database.
    """
    log.debug(f"[DB-Update] Deleting record: {name}")
    return db.delete_media(name)


@eel.expose
def add_file_to_library(file_path):
    """
    @brief Adds a single file from the browser to the library.
    """
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return {"error": "Datei nicht gefunden"}
    
    from src.core.config_master import AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
    if p.suffix.lower() not in AUDIO_EXTENSIONS and p.suffix.lower() not in VIDEO_EXTENSIONS:
        return {"error": "Kein untersttztes Audio- oder Videoformat"}

    known = db.get_known_media_names()
    if p.name in known:
        return {"status": "exists", "name": p.name}

    item = MediaItem(p.name, p)
    item_dict = item.to_dict()
    db.insert_media(item_dict)
    return {"status": "added", "item": item_dict}

@eel.expose
def sync_library_atomic():
    """ Forces a fresh read of the entire library from SQLite. """
    log.info("[Diagnostic] ATOMIC SYNC triggered.")
    try:
        items = db.get_all_media()
        return {"status": "success", "count": len(items), "items": items}
    except Exception as e:
        log.error(f"[Diagnostic] Atomic Sync failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def process_any_file(file_path: str) -> str:
    """ Forensic metadata extraction wrapper (v1.54.021). """
    import json
    try:
        from src.parsers.media_parser import extract_metadata
        filename = os.path.basename(file_path)
        tags, parser_times = extract_metadata(file_path, filename, mode='ultimate')
        duration = float(tags.get('duration', 0) or 0)
        return json.dumps({"success": True, "duration": duration, "tags": tags, "parser_times": parser_times})
    except Exception as e:
        log.error(f"[Tool-Pulse] Extraction failed for {file_path}: {e}")
        return json.dumps({"error": str(e)})

@eel.expose
def get_parser_registry():
    """ Returns all available parsers and their capabilities. """
    from src.parsers import media_parser
    return media_parser.get_parser_info()

@eel.expose
def update_parser_setting(parser_id, key, value):
    """ Updates a specific parser setting in GLOBAL_CONFIG. """
    if "parser_settings" not in GLOBAL_CONFIG:
        GLOBAL_CONFIG["parser_settings"] = {}
    if parser_id not in GLOBAL_CONFIG["parser_settings"]:
        GLOBAL_CONFIG["parser_settings"][parser_id] = {}
        
    GLOBAL_CONFIG["parser_settings"][parser_id][key] = value
    log.info(f"[Config] Updated parser '{parser_id}' setting '{key}' to '{value}'")
    return True

@eel.expose
def get_forensic_thresholds():
    """ Returns centralized bitrate quality thresholds. """
    from src.core.config_master import BITRATE_QUALITY_THRESHOLDS
    return BITRATE_QUALITY_THRESHOLDS
