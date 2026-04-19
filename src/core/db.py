#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Database Module

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import sqlite3
import json
import os
import time
from src.core.logger import get_logger
log = get_logger("db")
log.info(f"[DB-INIT] Initializing DB module. PID: {os.getpid()}")

from pathlib import Path
from typing import Iterable, Dict, Any, Optional

from src.core.config_master import GLOBAL_CONFIG


DB_DIR = Path(GLOBAL_CONFIG["storage_registry"]["data_dir"]).resolve()
DB_FILENAME = str(Path(GLOBAL_CONFIG["storage_registry"]["db_path"]).resolve())

_DB_INITIALIZED = False
_RESETTING = False
MAX_INIT_RETRIES = 3

# Reduce initial logging to avoid I/O saturation
if os.environ.get("MWV_DB_VERBOSE", "0") == "1":
    log.info(f"[DB-PATH] Centralized Absolute Target: {DB_FILENAME} (Exists: {os.path.exists(DB_FILENAME)})")


class DatabaseHandler:
    """Wrapper class for database operations to maintain API consistency."""
    def __init__(self):
        init_db()
        self.db_path = DB_FILENAME

    def get_db_stats(self):
        return get_db_stats()

    def get_all_media(self):
        return get_all_media()

    def get_media_by_name(self, name):
        return get_media_by_name(name)

    def delete_media_by_id(self, item_id):
        return delete_media_by_id(item_id)

    def update_item_metadata(self, item_path, updates):
        # Placeholder for existing function if it exists or needs to be routed
        return True

def get_default_scan_dir() -> Path:
    """
    Return the project default scan directory (Centralized v1.41.00).
    """
    return Path(GLOBAL_CONFIG["storage_registry"]["media_dir"]).resolve()

def get_active_db_path() -> Path:
    """
    Return the active database path used by the application.
    """
    return Path(DB_FILENAME).resolve()

def get_legacy_db_candidates(
    *,
    project_root: Path | None = None,
    home_dir: Path | None = None,
    cwd: Path | None = None,
) -> list[Path]:
    """
    Return known legacy database locations that may contain stale data.
    """
    module_dir = Path(__file__).resolve().parent
    # src/core -> root
    project = (project_root or module_dir.parent.parent).resolve()
    
    # Base candidates from config (Centralized v1.41.00)
    config_candidates = GLOBAL_CONFIG["storage_registry"]["legacy_db_candidates"]
    
    candidates = []
    for c_str in config_candidates:
        if c_str.startswith("~/"):
            candidates.append(Path.home() / c_str[2:])
        elif c_str.startswith("./"):
            candidates.append(project / c_str[2:])
        elif c_str.startswith("../"):
            candidates.append(project.parent / c_str[3:])
        else:
            candidates.append(Path(c_str))

    seen: set[Path] = set()
    unique_candidates: list[Path] = []
    for candidate in candidates:
        candidate_resolved = candidate.resolve()
        if candidate_resolved.exists() and candidate_resolved not in seen:
            unique_candidates.append(candidate_resolved)
            seen.add(candidate_resolved)
            
    return unique_candidates


def list_legacy_databases(candidates: Iterable[Path] | None = None) -> list[Path]:
    """
    Return existing legacy database files excluding the active DB path.
    """
    active_db = get_active_db_path()
    check_candidates = list(candidates) if candidates is not None else get_legacy_db_candidates()

    existing: list[Path] = []
    for candidate in check_candidates:
        resolved = candidate.resolve()
        if resolved == active_db:
            continue
        if resolved.exists() and resolved.is_file():
            existing.append(resolved)
    return existing


def cleanup_legacy_databases(candidates: Iterable[Path] | None = None) -> list[str]:
    """
    Remove legacy database files and return deleted file paths.
    """
    deleted: list[str] = []
    for legacy_db in list_legacy_databases(candidates=candidates):
        try:
            legacy_db.unlink()
            deleted.append(str(legacy_db))
        except Exception:
            log.debug(f"[ROOT-CLEANUP] Could not delete {name}", exc_info=True)
            continue
    return deleted


import threading
_DB_INIT_LOCK = threading.Lock()
_INIT_IN_PROGRESS = False
_ROOT_CLEANED = False

def cleanup_legacy_root_files():
    """
    Identifies and removes 0MB legacy leak files from the project root.
    (v1.46.132 Forensic Cleanup)
    """
    global _ROOT_CLEANED
    if _ROOT_CLEANED:
        return
        
    try:
        from src.core.config_master import PROJECT_ROOT
        legacy_names = ["logging", "media.db", "media_library.db", "media_viewer.db"]
        
        for name in legacy_names:
            target = PROJECT_ROOT / name
            if target.exists() and target.is_file():
                # Only remove if 0MB (leak) or if we are sure it's legacy
                size = target.stat().st_size
                if size == 0:
                    try:
                        target.unlink()
                        log.info(f"[ROOT-CLEANUP] Deleted 0MB legacy file: {name}")
                    except Exception as e:
                        log.debug(f"[ROOT-CLEANUP] Could not delete {name}: {e}")
                else:
                    log.warning(f"[ROOT-CLEANUP] Skipping non-empty legacy candidate: {name} ({size} bytes)")
        
        _ROOT_CLEANED = True
    except Exception as e:
        log.error(f"[ROOT-CLEANUP] Critical error during cleanup: {e}", exc_info=True)



def init_db(depth: int = 0):
    """
    Initializes the database and runs migrations if needed.
    @param depth Recursion depth tracking to prevent infinite stalling (v1.46.046).
    """
    global _DB_INITIALIZED, _INIT_IN_PROGRESS
    
    # 1. Thread & Recursion Safety (v1.46.046)
    if _DB_INITIALIZED:
        return True
    
    if depth > MAX_INIT_RETRIES:
        log.critical(f"[DB-STALL] Max recursion depth ({MAX_INIT_RETRIES}) exceeded. Aborting init.")
        return False

    with _DB_INIT_LOCK:
        if _DB_INITIALIZED:
            return True
            
        _INIT_IN_PROGRESS = True
        try:
            # 2. Path Forensic Check
            db_path_obj = Path(DB_FILENAME)
            exists = db_path_obj.exists()
            size = db_path_obj.stat().st_size if exists else -1
            
            if depth == 0:
                log.info(f"[BD-AUDIT] init_db starting. PID: {os.getpid()} | Path: {DB_FILENAME} | Exists: {exists} | Size: {size} bytes")
                # Surgical Cleanup (Forensic Phase 7)
                cleanup_legacy_root_files()

            # Always ensure the directory exists
            DB_DIR.mkdir(parents=True, exist_ok=True)

            if depth == 0:
                log.info(f"[DB] Checking database integrity at {DB_FILENAME}...")
            
            retry_count = 0
            conn = None
            while retry_count < MAX_INIT_RETRIES:
                try:
                    # [v1.46.061] Centralized Timeout (SSOT)
                    db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 2.0)
                    conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
                    cursor = conn.cursor()
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count >= MAX_INIT_RETRIES:
                        log.error(f"[DB-CRITICAL] Failed to connect to DB after {retry_count} attempts: {e}", exc_info=True)
                        return False
                    log.warning(f"[DB-RETRY] DB connect failed (attempt {retry_count}): {e}")
                    time.sleep(0.2)

            if not conn:
                return False

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    path TEXT,
                    type TEXT,
                    duration TEXT,
                    category TEXT,
                    is_transcoded BOOLEAN,
                    transcoded_format TEXT,
                    tags TEXT,
                    extension TEXT,
                    container TEXT,
                    tag_type TEXT,
                    codec TEXT,
                    has_artwork BOOLEAN DEFAULT 0,
                    art_path TEXT,
                    full_tags TEXT,
                    media_type TEXT,
                    subtype TEXT,
                    file_type TEXT,
                    isbn TEXT,
                    imdb TEXT,
                    tmdb TEXT,
                    discogs TEXT,
                    amazon_cover TEXT,
                    parent_id INTEGER,
                    playback_position REAL DEFAULT 0,
                    last_played TEXT,
                    duration_sec REAL,
                    is_mock BOOLEAN DEFAULT 0,
                    mock_stage INTEGER DEFAULT 0,
                    available BOOLEAN DEFAULT 1,
                    FOREIGN KEY(parent_id) REFERENCES media(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlist_media (
                    playlist_id INTEGER,
                    media_id INTEGER,
                    position INTEGER,
                    FOREIGN KEY(playlist_id) REFERENCES playlists(id),
                    FOREIGN KEY(media_id) REFERENCES media(id)
                )
            """)

            # Migration: Add columns if missing (for existing databases)
            new_columns = [
                ("category", "TEXT"),
                ("extension", "TEXT"),
                ("container", "TEXT"),
                ("tag_type", "TEXT"),
                ("codec", "TEXT"),
                ("art_path", "TEXT"),
                ("full_tags", "TEXT"),
                ("media_type", "TEXT"),
                ("subtype", "TEXT"),
                ("file_type", "TEXT"),
                ("isbn", "TEXT"),
                ("imdb", "TEXT"),
                ("tmdb", "TEXT"),
                ("discogs", "TEXT"),
                ("amazon_cover", "TEXT"),
                ("parent_id", "INTEGER"),
                ("playback_position", "REAL DEFAULT 0"),
                ("last_played", "TEXT"),
                ("duration_sec", "REAL DEFAULT 0"),
                ("is_mock", "BOOLEAN DEFAULT 0"),
                ("mock_stage", "INTEGER DEFAULT 0"),
                ("available", "BOOLEAN DEFAULT 1")
            ]
            
            # Get existing columns
            cursor.execute("PRAGMA table_info(media)")
            existing_cols = {row[1] for row in cursor.fetchall()}
            
            for col_name, col_type in new_columns:
                if col_name not in existing_cols:
                    try:
                        log.warning(f"[DB-MIGRATION] Adding missing column: {col_name} ({col_type})")
                        cursor.execute(f"ALTER TABLE media ADD COLUMN {col_name} {col_type}")
                        conn.commit()
                    except Exception as e:
                        log.error(f"Migration error for column {col_name}: {e}", exc_info=True)

            # Migration: Rename categories to new SSOT standards (v1.35.75)
            try:
                cursor.execute("UPDATE media SET category = 'pictures' WHERE category = 'images'")
                cursor.execute("UPDATE media SET category = 'disk_images' WHERE category = 'iso'")
                cursor.execute("UPDATE media SET category = 'video' WHERE category = 'multimedia'")
                cursor.execute("UPDATE media SET category = 'unknown' WHERE category = 'unbekannt' OR category IS NULL OR category = ''")
                # New v1.35.96: Lowercase all categories to ensure SSOT compatibility
                cursor.execute("UPDATE media SET category = LOWER(category)")
                conn.commit()
                log.info("[DB] [MIGRATION-v1.35.96] Successfully synchronized category casing (LOWER).")
            except Exception as e:
                log.warning(f"[DB] [MIGRATION-v1.35.96] Renaming migration skipped or failed: {e}")

            _DB_INITIALIZED = True
            log.debug("Database initialization/migration complete.")

            conn.commit()
            conn.close()
            log.info("[DB] Database initialization/migration successful.")
            return True
        except Exception as e:
            log.critical(f"[DB-FATAL] Initialization failed: {e}", exc_info=True)
            if 'conn' in locals() and conn:
                conn.close()
            return False
        finally:
            _INIT_IN_PROGRESS = False

    conn.commit()
    conn.close()
    log.info("[DB] Database initialization/migration successful.")


def factory_reset(depth: int = 0):
    """
    Deletes the current database file and re-initializes from scratch.
    @param depth Inherited recursion depth (v1.41.00).
    """
    global _RESETTING, _DB_INITIALIZED
    if _RESETTING:
        log.critical("[DB-STALL] Recursive factory_reset detected. Aborting to prevent infinite loop.")
        return False
    _RESETTING = True
    log.warning(f"[DB] FACTORY RESET TRIGGERED. Deleting {DB_FILENAME} (Depth: {depth})...")
    db_path = Path(DB_FILENAME)
    if db_path.exists():
        try:
            db_path.unlink()
            log.info("[DB] Database file deleted successfully.")
        except Exception as e:
            log.error(f"[DB] Could not delete database file: {e}", exc_info=True)
            # Try to just clear tables if file delete fails
            clear_media()
    _DB_INITIALIZED = False
    try:
        init_db(depth=depth)
    finally:
        _RESETTING = False
    return True


def get_known_media_names():
    """
    @brief Retrieves all media names already present in the database.
    @details Ruft alle bereits in der Datenbank vorhandenen Mediennamen ab.
    @return A set of media names / Ein Set mit Mediennamen.
    """
    init_db()
    db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 10.0)
    conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM media")
    names = {row[0] for row in cursor.fetchall()}
    conn.close()
    return names


def clear_media():
    """
    @brief Deletes all entries from the media table.
    @details Löscht alle Einträge aus der Tabelle 'media'.
    """
    db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 10.0)
    conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
    conn.execute("DELETE FROM media")
    conn.commit()
    conn.close()


def insert_media_batch(items: list[dict]):
    """
    @brief Inserts multiple media items in a single transaction (High Performance).
    @details Refactored v1.46.066: Analysis performed OUTSIDE transaction to prevent DB locks.
    """
    if not items: return
    
    # 1. PRE-ANALYSIS: Perform all slow I/O before locking the database
    analyzed_data = []
    from src.core.ffprobe_analyzer import ffprobe_analyze
    
    for item_dict in items:
        filepath = item_dict.get('path')
        analysis = ffprobe_analyze(filepath)
        
        # Merge analysis into item data
        item_copy = item_dict.copy()
        item_copy['_forensic_analysis'] = analysis
        analyzed_data.append(item_copy)

    # 2. FAST-TX: Open connection only for the actual write
    db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 10.0)
    conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
    cursor = conn.cursor()
    try:
        for item_dict in analyzed_data:
            analysis = item_dict.get('_forensic_analysis', {})
            
            # Extract granular forensic markers
            subtype = analysis.get("media_subtype", "FILE")
            codec = analysis.get("codec", "unknown")
            
            cursor.execute('''
                INSERT OR REPLACE INTO media (
                    name, path, type, duration, category, 
                    is_transcoded, transcoded_format, tags, extension, 
                    container, tag_type, codec, has_artwork, art_path, 
                    full_tags, media_type, subtype, file_type, isbn, 
                    imdb, tmdb, discogs, amazon_cover, parent_id, 
                    is_mock, mock_stage
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item_dict.get('name'), str(item_dict.get('path', '')), item_dict.get('type', 'other'),
                item_dict.get('duration'), item_dict.get('category', 'Unknown'),
                item_dict.get('is_transcoded', 0), item_dict.get('transcoded_format'),
                json.dumps(item_dict.get('tags', {})), item_dict.get('extension'),
                item_dict.get('container'), item_dict.get('tag_type'), codec,
                item_dict.get('has_artwork', 0), item_dict.get('art_path'),
                json.dumps(item_dict.get('full_tags', {})), item_dict.get('media_type'),
                subtype, item_dict.get('file_type'),
                item_dict.get('isbn'), item_dict.get('imdb'), item_dict.get('tmdb'),
                item_dict.get('discogs'), item_dict.get('amazon_cover'), item_dict.get('parent_id'),
                item_dict.get('is_mock', 0), item_dict.get('mock_stage', 0)
            ))
        conn.commit()
        log.info(f"[DB] [BATCH-SUCCESS] Inserted {len(items)} items in one transaction.")
    except Exception as e:
        log.error(f"[DB] [BATCH-ERROR] {e}", exc_info=True)
        conn.rollback()
    finally:
        conn.close()

def insert_media(item_dict):
    """
    @brief Inserts a new media item into the database.
    @details Refactored v1.46.066: Increased timeout.
    """
    db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 10.0)
    conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO media (name, path, type, duration, category, is_transcoded,
                             transcoded_format, tags, extension, container, tag_type, codec, 
                             has_artwork, art_path, full_tags, media_type, subtype, file_type,
                             isbn, imdb, tmdb, discogs, amazon_cover, parent_id, is_mock, mock_stage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_dict['name'],
            item_dict['path'],
            item_dict['type'],
            item_dict['duration'],
            item_dict.get('category', 'Audio'),
            item_dict['is_transcoded'],
            item_dict.get('transcoded_format'),
            json.dumps(item_dict['tags']),
            item_dict.get('extension'),
            item_dict.get('container'),
            item_dict.get('tag_type'),
            item_dict.get('codec'),
            1 if item_dict.get('has_artwork') else 0,
            item_dict.get('art_path'),
            json.dumps(item_dict.get('full_tags', {})),
            item_dict.get('media_type'),
            item_dict.get('subtype'),
            item_dict.get('file_type'),
            item_dict.get('isbn'),
            item_dict.get('imdb'),
            item_dict.get('tmdb'),
            item_dict.get('discogs'),
            item_dict.get('amazon_cover'),
            item_dict.get('parent_id'),
            item_dict.get('is_mock', 0),
            item_dict.get('mock_stage', 0)
        ))
        conn.commit()
        last_id = cursor.lastrowid
        if last_id and last_id % 50 == 0:
            log.info(f"[DB] [INSERT-PROGRESS] Processed {last_id} items...")
        log.debug(f"[DB] [INSERT-SUCCESS] {item_dict['name']} | Type: {item_dict['type']} | ID: {last_id}")
        conn.close()
        return last_id
    except sqlite3.IntegrityError as e:
        log.warning(f"[DB-VERIFY] [INSERT-SKIP] IntegrityError: '{item_dict['name']}' might already exist. ({e})")
        conn.close()
        return None
    except Exception as e:
        log.error(f"[DB-VERIFY] [INSERT-CRITICAL] Failed to index '{item_dict['name']}': {e}", exc_info=True)
        conn.close()
        raise


def get_all_media():
    """Alias for library compatibility (v1.41.00)."""
    return get_all_media_items()

def get_library():
    """Alias for main.py compatibility (v1.41.00)."""
    return get_all_media_items()

def row_to_dict(row):
    """
    @brief Unified helper to convert a database row to a standardized media dictionary.
    """
    try:
        tags = json.loads(row['tags']) if row['tags'] else {}
    except (json.JSONDecodeError, TypeError):
        tags = {}
        
    try:
        full_tags = json.loads(row['full_tags']) if row['full_tags'] else {}
    except (json.JSONDecodeError, TypeError):
        full_tags = {}

    return {
        'id': row['id'],
        'name': row['name'],
        'path': row['path'],
        'type': row['type'],
        'duration': row['duration'],
        'category': row['category'],
        'extension': row['extension'],
        'container': row['container'],
        'tag_type': row['tag_type'],
        'codec': row['codec'],
        'art_path': row['art_path'],
        'has_artwork': bool(row['has_artwork']),
        'is_transcoded': bool(row['is_transcoded']),
        'transcoded_format': row['transcoded_format'],
        'tags': tags,
        'full_tags': full_tags,
        'media_type': row['media_type'] if 'media_type' in row.keys() else 'unknown',
        'subtype': row['subtype'] if 'subtype' in row.keys() else 'unknown',
        'file_type': row['file_type'] if 'file_type' in row.keys() else 'unknown',
        'isbn': row['isbn'] if 'isbn' in row.keys() else None,
        'imdb': row['imdb'] if 'imdb' in row.keys() else None,
        'tmdb': row['tmdb'] if 'tmdb' in row.keys() else None,
        'discogs': row['discogs'] if 'discogs' in row.keys() else None,
        'amazon_cover': row['amazon_cover'] if 'amazon_cover' in row.keys() else None,
        'parent_id': row['parent_id'] if 'parent_id' in row.keys() else None,
        'playback_position': (row['playback_position'] or 0) if 'playback_position' in row.keys() else 0,
        'last_played': row['last_played'] if 'last_played' in row.keys() else None,
        'duration_sec': (row['duration_sec'] or 0) if 'duration_sec' in row.keys() else 0,
        'is_mock': bool(row['is_mock']) if 'is_mock' in row.keys() else False,
        'mock_stage': (row['mock_stage'] or 0) if 'mock_stage' in row.keys() else 0,
        'available': bool(row['available']) if 'available' in row.keys() else True
    }

def get_all_media_items():
    """
    @brief Retrieves all media items from the database.
    @details Ruft alle Medien-Items aus der Datenbank ab.
    @return List of media dictionaries / Liste von Medien-Dictionaries.
    """
    # [DIAGNOSTIC] Excessive Chain Audit (v1.35.96)
    pid = os.getpid()
    log.info(f"[BD-AUDIT] [get_all_media] Starting query. PID: {pid} | Path: {DB_FILENAME}")
    
    init_db()
    try:
        # [v1.46.061] Centralized Fail-fast (SSOT)
        db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 2.0)
        conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM media ORDER BY name")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        log.warning(f"[DB-LOCKED] Database is busy, returning empty set: {e}")
        return []
    log.info(f"[BD-AUDIT] [get_all_media] Finished query. Found {len(rows)} raw rows.")

    media_list = []
    for row in rows:
        media_list.append(row_to_dict(row))
    conn.close()
    return media_list


def get_media_path(name):
    """
    @brief Returns the full file path for a given media name.
    """
    db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 10.0)
    conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM media WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def get_media_by_name(name):
    """
    @brief Retrieves a single media item's full record by its unique name.
    @details Ruft den vollständigen Datensatz eines Mediums anhand seines Namens ab.
    @param name Media name / Datenbank-Name.
    @return Media dictionary or None / Medien-Dictionary oder None.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM media WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row_to_dict(row)
    return None


def get_media_by_id(media_id):
    """
    @brief Retrieves a single media item's full record by its unique ID.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM media WHERE id = ?", (media_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row_to_dict(row)
    return None


def get_media_by_path(path):
    """
    @brief Retrieves a single media item's full record by its filesystem path.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM media WHERE path = ?", (path,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row_to_dict(row)
    return None


def get_media_by_remote_id(field, value):
    """
    @brief Retrieves a media item by a remote ID field (isbn, imdb, tmdb, discogs).
    """
    if field not in ['isbn', 'imdb', 'tmdb', 'discogs']:
        return None
        
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM media WHERE {field} = ?", (value,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row_to_dict(row)
    return None


def check_media_availability():
    """
    @brief Scans all items in the database and updates their 'available' status.
    @return (Total Items, Missing Items)
    """
    total = 0
    missing = 0
    try:
        conn = sqlite3.connect(DB_FILENAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, path FROM media")
        rows = cursor.fetchall()
        total = len(rows)
        
        updates = []
        for row in rows:
            path_str = row['path']
            exists = os.path.exists(path_str)
            # [USER-RETRY] Persistent trace for rename forensics
            if not exists:
                missing += 1
                log.warning(f"[DB-VERIFY] Path Missing/Renamed: {path_str}")
            else:
                log.info(f"[DB-VERIFY] Path OK: {path_str}")
            
            updates.append((1 if exists else 0, row['id']))
            
        cursor.executemany("UPDATE media SET available = ? WHERE id = ?", updates)
        conn.commit()
        conn.close()
    except Exception as e:
        log.error(f"[DB-VERIFY] Error: {e}", exc_info=True)
        
    return total, missing


def update_media_tags(name, tags_dict):
    """
    @brief Updates the tags of a media item in the database.
    @details Aktualisiert die Tags eines Medien-Items in der Datenbank.
    @param name Media record name / Datenbank-Name.
    @param tags_dict New tags dictionary / Neues Dictionary mit Tags.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE media
        SET tags = ?, 
            full_tags = ?,
            isbn = ?,
            imdb = ?,
            tmdb = ?,
            discogs = ?,
            amazon_cover = ?,
            parent_id = ?,
            is_mock = ?,
            mock_stage = ?
        WHERE name = ?
    """, (
        json.dumps(tags_dict), 
        json.dumps(tags_dict.get('full_tags', {})),
        tags_dict.get('isbn'),
        tags_dict.get('imdb'),
        tags_dict.get('tmdb'),
        tags_dict.get('discogs'),
        tags_dict.get('amazon_cover'),
        tags_dict.get('parent_id'),
        tags_dict.get('is_mock', 0),
        tags_dict.get('mock_stage', 0),
        name
    ))
    conn.commit()
    conn.close()


def rename_media(old_name, new_name):
    # ... existing ...
    pass

# --- [v1.54.001] OBJECT-CENTRIC EXTENSIONS ---

def set_item_parent(item_id: int, parent_id: int) -> bool:
    """
    Establishes a parent-child relationship between two media records.
    (Used for grouping files into Film/Album Objects).
    """
    db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 10.0)
    conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE media SET parent_id = ? WHERE id = ?", (parent_id, item_id))
        conn.commit()
        return True
    except Exception as e:
        log.error(f"[DB-HIERARCHY] Failed to set parent {parent_id} for item {item_id}: {e}")
        return False
    finally:
        conn.close()

def insert_media_object(obj_dict: Dict[str, Any]) -> Optional[int]:
    """
    Inserts a virtual 'Object' record (Film/Album container) into the DB.
    """
    # Map the object dict to the media table schema
    media_dict = {
        'name': obj_dict.get('name'),
        'path': obj_dict.get('path'),
        'type': 'object',
        'category': obj_dict.get('category', 'unknown'),
        'subtype': obj_dict.get('subtype', 'OBJECT'),
        'duration': '',
        'is_transcoded': 0,
        'tags': json.dumps(obj_dict.get('metadata', {})),
        'full_tags': json.dumps(obj_dict.get('metadata', {})),
    }
    return insert_media(media_dict)
    """
    @brief Renames a media item in the database.
    @details Benennt ein Medium in der DB um.
    @param old_name Current record name / Aktueller Name.
    @param new_name New record name / Neuer Name.
    @return Success status / Erfolgsstatus.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE media SET name = ? WHERE name = ?", (new_name, old_name))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_media_by_id(item_id):
    """
    @brief Deletes a media item from the database by ID (v1.37.17).
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM media WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return True


def delete_media(name):
    """
    @brief Deletes a media item from the database.
    @details Löscht ein Medium aus der DB.
    @param name Media name / Medienname.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM media WHERE name = ?", (name,))
        conn.commit()
    finally:
        conn.close()


def get_db_stats():
    """
    @brief Returns statistics about the database.
    @details Gibt Statistiken über die Datenbank zurück.
    @return Stats dictionary / Dictionary mit Statistiken.
    """
    init_db()
    try:
        # [v1.46.061] Centralized Fail-fast (SSOT)
        db_timeout = GLOBAL_CONFIG.get("forensic_hydration_registry", {}).get("db_timeout", 2.0)
        conn = sqlite3.connect(DB_FILENAME, timeout=db_timeout)
        cursor = conn.cursor()
    except sqlite3.OperationalError as e:
        log.warning(f"[DB-STATS-LOCKED] Statistics query blocked: {e}")
        return {'total_items': 0, 'mock_items': 0, 'categories': {}}

    cursor.execute("SELECT COUNT(*) FROM media")
    total_items = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM media WHERE is_mock = 1")
    mock_items = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) FROM media GROUP BY category")
    categories = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return {
        'total_items': total_items,
        'mock_items': mock_items,
        'categories': categories
    }


def get_media_count():
    """
    @brief Returns the total number of items in the media table (Fast).
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM media")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def update_playback_position(name, position):
    """
    @brief Updates the persistent playback position for a media item.
    """
    import datetime
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE media 
        SET playback_position = ?, 
            last_played = ?
        WHERE name = ?
    """, (position, datetime.datetime.now().isoformat(), name))
    conn.commit()
    conn.close()


def get_playback_position(name):
    """
    @brief Retrieves the last stored playback position.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT playback_position FROM media WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0


def update_media_duration(name, duration_sec):
    """
    @brief Updates the total duration in seconds for a media item.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE media 
        SET duration_sec = ?
        WHERE name = ?
    """, (duration_sec, name))
    conn.commit()
    conn.close()


def get_media_by_category(category):
    """
    @brief Retrieves all media items belonging to a specific category.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM media WHERE category = ? ORDER BY name", (category,))
    rows = cursor.fetchall()
    
    media_list = []
    for row in rows:
        media_list.append({
            'id': row['id'],
            'name': row['name'],
            'path': row['path'],
            'type': row['type'],
            'duration': row['duration'],
            'category': row['category'],
            'extension': row['extension'],
            'container': row['container'],
            'tag_type': row['tag_type'],
            'codec': row['codec'],
            'art_path': row['art_path'],
            'has_artwork': bool(row['has_artwork']),
            'is_transcoded': bool(row['is_transcoded']),
            'transcoded_format': row['transcoded_format'],
            'tags': json.loads(row['tags']) if row['tags'] else {},
            'full_tags': json.loads(row['full_tags']) if row['full_tags'] else {},
            'playback_position': row['playback_position'] or 0,
            'last_played': row['last_played'],
            'duration_sec': row['duration_sec'] or 0
        })
    conn.close()
    return media_list


def search_media(query):
    """
    @brief Searches for media items by name or tags.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Basic search in name and path
    sql_query = f"%{query}%"
    cursor.execute("SELECT * FROM media WHERE name LIKE ? OR path LIKE ? ORDER BY name", (sql_query, sql_query))
    rows = cursor.fetchall()
    
    media_list = []
    for row in rows:
        media_list.append({
            'id': row['id'],
            'name': row['name'],
            'path': row['path'],
            'type': row['type'],
            'duration': row['duration'],
            'category': row['category'],
            'extension': row['extension'],
            'container': row['container'],
            'tag_type': row['tag_type'],
            'codec': row['codec'],
            'art_path': row['art_path'],
            'has_artwork': bool(row['has_artwork']),
            'is_transcoded': bool(row['is_transcoded']),
            'transcoded_format': row['transcoded_format'],
            'tags': json.loads(row['tags']) if row['tags'] else {},
            'full_tags': json.loads(row['full_tags']) if row['full_tags'] else {},
            'playback_position': row['playback_position'] or 0,
            'last_played': row['last_played'],
            'duration_sec': row['duration_sec'] or 0
        })
    conn.close()
    return media_list


def get_media_by_path(path):
    """
    @brief Retrieves a single media item by its filesystem path.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM media WHERE path = ?", (str(path),))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'id': row['id'],
            'name': row['name'],
            'path': row['path'],
            'type': row['type'],
            'duration': row['duration'],
            'category': row['category'],
            'extension': row['extension'],
            'container': row['container'],
            'tag_type': row['tag_type'],
            'codec': row['codec'],
            'art_path': row['art_path'],
            'has_artwork': bool(row['has_artwork']),
            'is_transcoded': bool(row['is_transcoded']),
            'transcoded_format': row['transcoded_format'],
            'tags': json.loads(row['tags']) if row['tags'] else {},
            'full_tags': json.loads(row['full_tags']) if row['full_tags'] else {},
            'playback_position': row['playback_position'] or 0,
            'last_played': row['last_played'],
            'duration_sec': row['duration_sec'] or 0
        }
    return None


# --- Playlist Management (v1.37.32) ---

def get_all_playlists():
    """
    @brief Retrieves all playlist records.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists ORDER BY name")
    rows = cursor.fetchall()
    playlists = []
    for row in rows:
        playlists.append({
            'id': row['id'],
            'name': row['name']
        })
    conn.close()
    return playlists


def get_playlist_items(playlist_id):
    """
    @brief Retrieves all media items for a specific playlist.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, pm.position 
        FROM media m
        JOIN playlist_media pm ON m.id = pm.media_id
        WHERE pm.playlist_id = ?
        ORDER BY pm.position
    """, (playlist_id,))
    rows = cursor.fetchall()
    
    media_list = []
    for row in rows:
        item = {
            'id': row['id'],
            'name': row['name'],
            'path': row['path'],
            'type': row['type'],
            'category': row['category'],
            'position': row['position']
        }
        try:
            item['tags'] = json.loads(row['tags']) if row['tags'] else {}
        except:
            item['tags'] = {}
        media_list.append(item)
    conn.close()
    return media_list


def get_playlist_orphans(playlist_id):
    """
    @brief Finds media_ids in playlist_media that do not exist in the media table.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pm.media_id, pm.position
        FROM playlist_media pm
        LEFT JOIN media m ON pm.media_id = m.id
        WHERE pm.playlist_id = ? AND m.id IS NULL
    """, (playlist_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"media_id": r[0], "position": r[1]} for r in rows]


def prune_playlist_orphans(playlist_id):
    """
    @brief Removes playlist_media entries for a specific playlist that do not exist in the media table.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM playlist_media 
        WHERE playlist_id = ? AND media_id NOT IN (SELECT id FROM media)
    """, (playlist_id,))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted_count
