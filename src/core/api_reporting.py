import os
import sys
import psutil
import time
import sqlite3
import logging
import platform
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple, cast
from urllib.parse import unquote

# --- Forensic Handshake Imports ---
from src.core.config_master import (
    GLOBAL_CONFIG, DISK_IMAGE_EXTENSIONS
)
from src.core.models import get_allowed_internal_cats, audit_category_chain
from src.core import db, hardware_detector
from src.core.api_library import apply_library_filters

# Project Root Resolution
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
log = logging.getLogger("api_reporting")

# --- Specialized Reports ---

def get_startup_report():
    """Returns the high-resolution StartupProfiler report (v1.41.00)."""
    from src.core.main import profiler
    if profiler:
        return profiler.get_report()
    return {"status": "error", "message": "Profiler not initialized"}

def get_global_health_audit():
    """Aggregates all 14 diagnostic layers into a Readiness Score."""
    try:
        health_report = {
            "status": "ok",
            "readiness_score": 0,
            "level": "DEGRADED",
            "metrics": {}
        }
        # 1. DB HEALTH
        db_stats = db.get_db_stats()
        health_report["metrics"]["db"] = "SYNC" if db_stats.get("total_items", 0) > 0 else "EMPTY"
        # 2. SYS HEALTH
        mem = psutil.virtual_memory()
        health_report["metrics"]["sys"] = "STABLE" if mem.percent < 85 else "HEAVY_LOAD"
        # 3. VOL HEALTH
        media_dir = GLOBAL_CONFIG["storage_registry"]["media_dir"]
        health_report["metrics"]["vol"] = "MOUNTED" if os.path.exists(media_dir) else "DISCONNECTED"
        # 4. PRC HEALTH
        parent = psutil.Process(os.getpid())
        zombies = [c for c in parent.children(recursive=True) if c.status() == psutil.STATUS_ZOMBIE]
        health_report["metrics"]["prc"] = "CLEAN" if len(zombies) == 0 else "ZOMBIE_DETECTED"
        # 5. DRV HEALTH
        hw_enc = hardware_detector.get_best_hw_encoder()
        health_report["metrics"]["drv"] = "ACCEL_ACTIVE" if "h264_" in hw_enc and "libx264" not in hw_enc else "SOFTWARE_ONLY"
        # Scoring Logic
        score = 0
        for k, v in health_report["metrics"].items():
            if v in ["SYNC", "STABLE", "MOUNTED", "CLEAN", "ACCEL_ACTIVE"]: score += 20
        health_report["readiness_score"] = score
        if score >= 90: health_report["level"] = "BATTLE-READY"
        elif score >= 60: health_report["level"] = "STABILIZED"
        return health_report
    except Exception as e:
        log.error(f"[Forensic-HLT] Health Audit Failed: {e}")
        return {"status": "error", "message": str(e)}

def get_db_stats():
    """Returns statistical information about the database content."""
    stats = db.get_db_stats()
    stats["active_db"] = str(db.get_active_db_path())
    stats["db_exists"] = os.path.exists(db.DB_FILENAME)
    stats["project_root"] = str(PROJECT_ROOT)
    return stats

# --- Forensic Suite ---

def get_storage_forensics():
    """Storage Forensic Audit: Volume Discovery (v1.46.101 Align)."""
    media_path = PROJECT_ROOT / "media"
    if not media_path.exists():
        log.error(f"[Forensic-STR] Media path missing: {media_path}")
        return {"status": "error", "message": f"Media path not found: {media_path}"}
    
    scan_settings = GLOBAL_CONFIG.get("scan_settings", {})
    forensic_settings = GLOBAL_CONFIG.get("forensic_settings", {})
    
    enable_ext_skip = scan_settings.get("enable_extension_skipping", True)
    skip_exts = set(scan_settings.get("skip_extensions", []))
    enable_size_skip = scan_settings.get("enable_size_skipping", True)
    min_size = scan_settings.get("min_size_kb", 1) * 1024
    max_size = scan_settings.get("max_size_mb", 50000) * 1024 * 1024
    max_report_count = forensic_settings.get("max_largest_files_report", 15)

    results = {
        "status": "ok", 
        "total_files": 0, 
        "total_folders": 0, 
        "total_size_bytes": 0, 
        "skipped_files": 0,
        "largest_files": []
    }
    
    all_files = []
    
    for root, dirs, files in os.walk(str(media_path)):
        results["total_folders"] += 1
        for f in files:
            f_path = Path(root) / f
            ext = f_path.suffix.lower()
            
            # --- Robustness Filter (Aligned with Scanner) ---
            if enable_ext_skip and ext in skip_exts:
                results["skipped_files"] += 1
                continue
                
            try:
                f_size = f_path.stat().st_size
                
                if enable_size_skip and (f_size < min_size or f_size > max_size):
                    results["skipped_files"] += 1
                    continue

                results["total_files"] += 1
                results["total_size_bytes"] += f_size
                all_files.append({
                    "name": f, 
                    "size": f_size, 
                    "path": str(f_path.relative_to(PROJECT_ROOT)),
                    "ext": ext
                })
            except Exception as e:
                log.warning(f"[Forensic-STR] Failed to stat {f}: {e}")
                results["skipped_files"] += 1
                
    all_files.sort(key=lambda x: x["size"], reverse=True)
    results["largest_files"] = all_files[:max_report_count]
    return results

def get_process_forensics():
    """Forensic Child Process Audit (v1.37.35)."""
    try:
        parent = psutil.Process(os.getpid())
        children = parent.children(recursive=True)
        proc_list = []
        for p in children:
            try:
                proc_list.append({"pid": p.pid, "name": p.name(), "status": p.status().upper()})
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        return {"status": "ok", "active_workers": len(proc_list), "processes": proc_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_api_forensics(exposed_registry: List[Dict]):
    """Forensic Internal API Registry & Documentation (v1.37.39)."""
    return {"status": "ok", "registry": exposed_registry, "total_endpoints": len(exposed_registry)}

def audit_specific_item(query: str) -> Dict[str, Any]:
    """Deep audit of a specific item's journey from DB to GUI."""
    all_media = db.get_all_media()
    match = next((i for i in all_media if query.lower() in i.get('name','').lower() or query.lower() in i.get('path','').lower()), None)
    if not match: return {"status": "not_found"}
    category_audit = audit_category_chain(match)
    filtered, logic_audit = apply_library_filters([match], force_raw=False)
    passed = len(filtered) > 0
    return {
        "status": "found", "item": match,
        "stages": {
            "db": {"status": "ok"},
            "models": {"status": "ok", "log": category_audit},
            "backend_filter": {"status": "ok" if passed else "dropped"}
        }
    }

# --- Metadata Reports ---

def get_cover_extraction_report():
    """Analyzes artwork efficiency and sources."""
    items = db.get_all_media()
    report = {'total': len(items), 'has_artwork': 0, 'sources': {'cache': 0, 'folder': 0}}
    for item in items:
        art = item.get('art_path') or item.get('artwork')
        if art:
            report['has_artwork'] += 1
            if '.cache' in str(art): report['sources']['cache'] += 1
            else: report['sources']['folder'] += 1
    return report

def get_routing_suite_report():
    """Aggregates routing statistics and quality scores."""
    from src.parsers.format_utils import ffprobe_quality_score, is_direct_play_capable
    items = db.get_all_media()
    total_score, video_count = 0, 0
    modes = {'direct': 0, 'transcode': 0, 'other': 0}
    for item in items:
        if item.get('category') != 'video': continue
        video_count += 1
        tags = item.get('tags', {})
        total_score += ffprobe_quality_score(tags)
        if is_direct_play_capable(item.get('path',''), 'browser'): modes['direct'] += 1
        else: modes['transcode'] += 1
    return {
        "avg_quality": round(total_score/video_count, 1) if video_count > 0 else 0,
        "modes": modes,
        "total": len(items)
    }

def get_security_forensics():
    """Forensic Security & Authority Audit (v1.37.38)."""
    db_path = db.get_active_db_path()
    return {
        "status": "ok",
        "security": {
            "uid": os.getuid() if hasattr(os, "getuid") else 0,
            "db_writable": os.access(db_path, os.W_OK),
            "platform": platform.platform()
        }
    }

def prune_ghost_items(item_ids: List[str]) -> Dict[str, Any]:
    """Safely prunes ghost items from the database."""
    if not item_ids or not isinstance(item_ids, list):
        return {"status": "error", "message": "Invalid ID list provided."}
    pruned_count = 0
    try:
        for itm_id in item_ids:
            if db.delete_media_by_id(itm_id):
                pruned_count += 1
        return {"status": "success", "count": pruned_count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def kill_stalled_ffmpeg_streams() -> Dict[str, Any]:
    """Purges all FFmpeg/mkvmerge processes associated with the project."""
    project_fragment = "gui_media_web_viewer"
    killed_count = 0
    try:
        current_proc = psutil.Process()
        ancestor_pids = {p.pid for p in current_proc.parents()}
        ancestor_pids.add(os.getpid())
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                pid = proc.info['pid']
                if pid in ancestor_pids: continue
                name = (proc.info.get('name') or "").lower()
                cmd_str = " ".join(proc.info.get('cmdline') or []).lower()
                if ("ffmpeg" in name or "mkvmerge" in name) and project_fragment in cmd_str:
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        return {"status": "success", "count": killed_count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_hardware_forensics():
    """Forensic Hardware Acceleration & Driver Audit."""
    hw_info = hardware_detector.get_capabilities()
    return {"status": "ok", "hardware": hw_info}

def check_database_resilience():
    """Performs forensic library resilience audit."""
    results = {"status": "ok", "sqlite_health": "unknown", "fs_parity": {"total_items": 0, "ghost_count": 0, "ghost_items": []}}
    try:
        conn = sqlite3.connect(db.DB_FILENAME)
        results["sqlite_health"] = conn.execute("PRAGMA integrity_check").fetchone()[0]
        conn.close()
        items = db.get_all_media()
        results["fs_parity"]["total_items"] = len(items)
        for item in items:
            if item.get('path') and not os.path.exists(item.get('path')):
                results["fs_parity"]["ghost_items"].append({"id": item.get('id'), "name": item.get('name')})
        results["fs_parity"]["ghost_count"] = len(results["fs_parity"]["ghost_items"])
    except Exception as e:
        results["status"] = "error"
    return results

def get_library_forensics():
    """Unified Forensic Bridge for library statistics."""
    db_items = db.get_library() or []
    cat_stats, ext_stats = {}, {}
    for item in db_items:
        cat = item.get('category', 'unknown').lower()
        ext = os.path.splitext(str(item.get('path', '')))[1].lower() or '.dat'
        cat_stats[cat] = cat_stats.get(cat, 0) + 1
        ext_stats[ext] = ext_stats.get(ext, 0) + 1
    return {"status": "success", "total": len(db_items), "categories": cat_stats, "formats": ext_stats}

def get_playlist_forensics():
    """Playlist Forensic Audit: Integrity & Repair."""
    playlists = db.get_all_playlists()
    results = {"status": "ok", "playlists": []}
    for pl in playlists:
        items = db.get_playlist_items(pl['id'])
        orphans = db.get_playlist_orphans(pl['id'])
        missing = sum(1 for i in items if i.get('path') and not os.path.exists(i['path']))
        results["playlists"].append({
            "id": pl['id'], "name": pl['name'], "item_count": len(items),
            "relational_orphans": len(orphans), "physical_missing": missing
        })
    return results

def prune_playlist_orphans(playlist_id):
    """Surgical Pruning for Playlist Relational Orphans."""
    try:
        count = db.prune_playlist_orphans(playlist_id)
        return {"status": "success", "count": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_state_forensics():
    """Forensic State Persistence Audit."""
    return {"status": "ok", "version": GLOBAL_CONFIG.get("version"), "debug": GLOBAL_CONFIG.get("debug_mode")}

def get_net_ping():
    """Sub-millisecond bridge ping."""
    return {"status": "ok", "timestamp": time.time()}

def terminate_worker_process(pid):
    """Surgical Termination for Background Workers."""
    try:
        proc = psutil.Process(int(pid))
        parent = psutil.Process(os.getpid())
        if int(pid) in [c.pid for c in parent.children(recursive=True)]:
            proc.terminate()
            return {"status": "success"}
        return {"status": "error", "message": "Access Denied"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_environment_forensics():
    """Forensic Software Stack & Environment Audit."""
    return {"status": "ok", "python": sys.version, "platform": platform.platform()}
