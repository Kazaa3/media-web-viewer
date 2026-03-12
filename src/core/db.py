#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Database Module

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

from pathlib import Path
from typing import Iterable

# Use project-local data/ directory if available, otherwise fallback to home
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_DATA_DIR = PROJECT_ROOT / "data"

if LOCAL_DATA_DIR.exists():
    DB_DIR = LOCAL_DATA_DIR
    DB_FILENAME = str(DB_DIR / "database.db")
else:
    DB_DIR = Path.home() / ".media-web-viewer"
    DB_FILENAME = str(DB_DIR / "media_library.db")


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
    project = (project_root or module_dir).resolve()
    home = (home_dir or Path.home()).resolve()
    current = (cwd or Path.cwd()).resolve()

    candidates = [
        home / "media_library.db",
        project / "media_library.db",
        project / "dist" / "media_library.db",
        current / "media_library.db",
        project.parent / "media_library.db",
    ]

    seen: set[Path] = set()
    unique_candidates: list[Path] = []
    for candidate in candidates:
        candidate_resolved = candidate.resolve()
        if candidate_resolved not in seen:
            seen.add(candidate_resolved)
            unique_candidates.append(candidate_resolved)
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
    @brief Initializes the SQLite database and creates necessary tables.
    @details Initialisiert die SQLite-Datenbank und erstellt die notwendigen Tabellen.
    """
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

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
            full_tags TEXT
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
        ("full_tags", "TEXT")
    ]
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE media ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists

    conn.commit()
    conn.close()


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
                             transcoded_format, tags, extension, container, tag_type, codec, has_artwork, full_tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            json.dumps(item_dict.get('full_tags', {}))
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Schon vorhanden
    finally:
        conn.close()


def get_all_media():
    """
    @brief Retrieves all media items from the database.
    @details Ruft alle Medien-Items aus der Datenbank ab.
    @return List of media dictionaries / Liste von Medien-Dictionaries.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM media ORDER BY name")
    rows = cursor.fetchall()

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
            'has_artwork': bool(row['has_artwork']),
            'is_transcoded': bool(row['is_transcoded']),
            'transcoded_format': row['transcoded_format'],
            'tags': json.loads(row['tags']) if row['tags'] else {},
            'full_tags': json.loads(row['full_tags']) if row['full_tags'] else {}
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
        SET tags = ?, full_tags = ?
        WHERE name = ?
    """, (json.dumps(tags_dict), json.dumps(tags_dict.get('full_tags', {})), name))
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

    cursor.execute("SELECT category, COUNT(*) FROM media GROUP BY category")
    categories = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return {
        'total_items': total_items,
        'categories': categories
    }
