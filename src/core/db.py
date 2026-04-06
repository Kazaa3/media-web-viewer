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
from src.core.logger import get_logger
log = get_logger("db")
log.info(f"[DB-INIT] Initializing DB module. PID: {os.getpid()}")

from pathlib import Path
from typing import Iterable

from src.core.config_master import GLOBAL_CONFIG

DB_DIR = Path(GLOBAL_CONFIG["storage_registry"]["data_dir"]).resolve()
DB_FILENAME = str(Path(GLOBAL_CONFIG["storage_registry"]["db_path"]).resolve())

log.info(f"[DB-PATH] Centralized Absolute Target: {DB_FILENAME} (Exists: {os.path.exists(DB_FILENAME)})")

_DB_INITIALIZED = False


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

    def update_item_metadata(self, item_path, updates):
        # Placeholder for existing function if it exists or needs to be routed
        return True

def get_default_scan_dir() -> Path:
    """
    Return the project default scan directory (Centralized v1.35.68).
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
    
    # Base candidates from config (Centralized v1.35.68)
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
            continue
    return deleted


def init_db():
    """
    Initializes the database and runs migrations if needed.
    """
    # Always ensure the directory exists, even if _DB_INITIALIZED is true,
    # to handle cases where the directory was deleted (e.g., Factory Reset)
    # while the process is running.
    DB_DIR.mkdir(parents=True, exist_ok=True)

    global _DB_INITIALIZED
    if _DB_INITIALIZED and Path(DB_FILENAME).exists():
        return

    log.info(f"[DB] Checking database integrity at {DB_FILENAME}...")
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
    except Exception as e:
        log.error(f"[DB-CRITICAL] Failed to connect to DB: {e}. Attempting reset...")
        return factory_reset()

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
        ("playback_position", "REAL"),
        ("last_played", "TEXT"),
        ("duration_sec", "REAL"),
        ("is_mock", "BOOLEAN DEFAULT 0"),
        ("mock_stage", "INTEGER DEFAULT 0")
    ]
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE media ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists
        except Exception as e:
            log.error(f"Migration error for column {col_name}: {e}")

    # Migration: Rename categories to new SSOT standards (v1.35.75)
    try:
        cursor.execute("UPDATE media SET category = 'pictures' WHERE category = 'images'")
        cursor.execute("UPDATE media SET category = 'disk_images' WHERE category = 'iso'")
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


def factory_reset():
    """
    Deletes the current database file and re-initializes from scratch.
    """
    log.warning(f"[DB] FACTORY RESET TRIGGERED. Deleting {DB_FILENAME}...")
    db_path = Path(DB_FILENAME)
    if db_path.exists():
        try:
            db_path.unlink()
            log.info("[DB] Database file deleted successfully.")
        except Exception as e:
            log.error(f"[DB] Could not delete database file: {e}")
            # Try to just clear tables if file delete fails
            clear_media()
    
    global _DB_INITIALIZED
    _DB_INITIALIZED = False
    init_db()
    return True


def get_known_media_names():
    """
    @brief Retrieves all media names already present in the database.
    @details Ruft alle bereits in der Datenbank vorhandenen Mediennamen ab.
    @return A set of media names / Ein Set mit Mediennamen.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
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
    conn = sqlite3.connect(DB_FILENAME)
    conn.execute("DELETE FROM media")
    conn.commit()
    conn.close()


def insert_media(item_dict):
    """
    @brief Inserts a new media item into the database.
    @details Fügt ein neues Medien-Item in die Datenbank ein.
    @param item_dict Metadata dictionary / Dictionary mit Metadaten.
    """
    conn = sqlite3.connect(DB_FILENAME)
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
        log.info(f"[DB] [INSERT-SUCCESS] {item_dict['name']} | Type: {item_dict['type']} | ID: {last_id}")
        conn.close()
        return last_id
    except sqlite3.IntegrityError as e:
        log.warning(f"[DB] [INSERT-SKIP] IntegrityError: {item_dict['name']} might already exist. ({e})")
        conn.close()
        return None
    except Exception as e:
        log.error(f"[DB] [INSERT-ERROR] {item_dict['name']}: {e}")
        conn.close()
        raise


def get_all_media():
    """
    @brief Retrieves all media items from the database.
    @details Ruft alle Medien-Items aus der Datenbank ab.
    @return List of media dictionaries / Liste von Medien-Dictionaries.
    """
    print(f"STDOUT: [DB] [get_all_media] Querying table... PID: {os.getpid()}", flush=True)
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    log.info("[DB] [get_all_media] Querying table...")
    cursor.execute("SELECT * FROM media ORDER BY name")
    rows = cursor.fetchall()
    log.info(f"[DB] [get_all_media] Found {len(rows)} raw rows.")

    media_list = []
    for row in rows:
        media_list.append({
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
            'media_type': row['media_type'],
            'subtype': row['subtype'],
            'file_type': row['file_type'],
            'isbn': row['isbn'],
            'imdb': row['imdb'],
            'tmdb': row['tmdb'],
            'discogs': row['discogs'],
            'amazon_cover': row['amazon_cover'],
            'parent_id': row['parent_id'],
            'playback_position': row['playback_position'] or 0,
            'last_played': row['last_played'],
            'duration_sec': row['duration_sec'] or 0,
            'is_mock': bool(row['is_mock']) if 'is_mock' in row.keys() else False,
            'mock_stage': row['mock_stage'] if 'mock_stage' in row.keys() else 0
        })
    conn.close()
    return media_list


def get_media_path(name):
    """
    @brief Returns the full file path for a given media name.
    @details Gibt den vollen Dateipfad für einen Mediennamen zurück.
    @param name Media record name / Datenbank-Name.
    @return Full filesystem path or None / Voller Pfad oder None.
    """
    conn = sqlite3.connect(DB_FILENAME)
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
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

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
