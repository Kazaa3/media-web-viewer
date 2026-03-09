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
import sys

from pathlib import Path
from typing import Iterable

# Use a user-writable path for the database
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
             Since v1.3.4 a dedicated media_tags table stores individual tag key-value
             pairs for efficient querying and filtering.
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
            codec TEXT
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

    # v1.3.4: Dedicated tag storage table for individual key-value querying
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_id INTEGER NOT NULL,
            key TEXT NOT NULL,
            value TEXT,
            FOREIGN KEY(media_id) REFERENCES media(id) ON DELETE CASCADE,
            UNIQUE(media_id, key)
        )
    """)

    # Index for fast tag key/value lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_media_tags_key_value
        ON media_tags(key, value)
    """)

    conn.commit()

    # Migration: Add columns if missing (for existing databases)
    new_columns = [
        ("category", "TEXT"),
        ("extension", "TEXT"),
        ("container", "TEXT"),
        ("tag_type", "TEXT"),
        ("codec", "TEXT")
    ]
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE media ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists

    # Migration: Populate media_tags from existing JSON tags column
    _migrate_tags_to_table(cursor, conn)

    conn.commit()
    conn.close()


def _migrate_tags_to_table(cursor, conn):
    """
    @brief Migrates existing JSON tags to the media_tags table.
    @details Wandelt vorhandene JSON-Tags in die media_tags-Tabelle um (v1.3.4-Migration).
    @param cursor Active database cursor.
    @param conn Active database connection.
    """
    cursor.execute("""
        SELECT m.id, m.tags
        FROM media m
        WHERE m.tags IS NOT NULL AND m.tags != ''
          AND NOT EXISTS (
              SELECT 1 FROM media_tags mt WHERE mt.media_id = m.id
          )
    """)
    rows = cursor.fetchall()
    for media_id, tags_json in rows:
        try:
            tags_dict = json.loads(tags_json)
            if isinstance(tags_dict, dict):
                _insert_tags_to_table(cursor, conn, media_id, tags_dict)
        except (json.JSONDecodeError, TypeError) as exc:
            print(
                f"[db] Warning: skipping tag migration for media_id={media_id} "
                f"(malformed JSON): {exc}",
                file=sys.stderr,
            )


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


def _insert_tags_to_table(cursor, conn, media_id, tags_dict):
    """
    @brief Inserts individual tag key-value pairs into the media_tags table.
    @details Schreibt einzelne Tag-Schlüssel/Wert-Paare in die media_tags-Tabelle.
    @param cursor Active database cursor.
    @param conn Active database connection.
    @param media_id Foreign key referencing media.id.
    @param tags_dict Dictionary of tag key-value pairs.
    """
    for key, value in tags_dict.items():
        if value is None:
            continue
        str_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        cursor.execute("""
            INSERT OR REPLACE INTO media_tags (media_id, key, value)
            VALUES (?, ?, ?)
        """, (media_id, key, str_value))
    conn.commit()


def insert_media(item_dict):
    """
    @brief Inserts a new media item into the database.
    @details Fügt ein neues Medien-Item in die Datenbank ein.
             Since v1.3.4 tag key-value pairs are also written to media_tags.
    @param item_dict Metadata dictionary / Dictionary mit Metadaten.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO media (name, path, type, duration, category, is_transcoded,
                             transcoded_format, tags, extension, container, tag_type, codec)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            item_dict.get('codec')
        ))
        conn.commit()
        media_id = cursor.lastrowid
        tags_dict = item_dict.get('tags') or {}
        if isinstance(tags_dict, dict):
            _insert_tags_to_table(cursor, conn, media_id, tags_dict)
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
            'is_transcoded': bool(row['is_transcoded']),
            'transcoded_format': row['transcoded_format'],
            'tags': json.loads(row['tags']) if row['tags'] else {}
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
             Since v1.3.4 the media_tags table is also updated.
    @param name Media record name / Datenbank-Name.
    @param tags_dict New tags dictionary / Neues Dictionary mit Tags.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE media
        SET tags = ?
        WHERE name = ?
    """, (json.dumps(tags_dict), name))
    conn.commit()

    # Sync media_tags table
    cursor.execute("SELECT id FROM media WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row and isinstance(tags_dict, dict):
        media_id = row[0]
        cursor.execute("DELETE FROM media_tags WHERE media_id = ?", (media_id,))
        conn.commit()
        _insert_tags_to_table(cursor, conn, media_id, tags_dict)
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
             Since v1.3.4 the related media_tags rows are removed as well.
    @param name Media name / Medienname.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM media WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            media_id = row[0]
            cursor.execute("DELETE FROM media_tags WHERE media_id = ?", (media_id,))
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

    cursor.execute("SELECT COUNT(*) FROM media_tags")
    total_tag_entries = cursor.fetchone()[0]

    conn.close()
    return {
        'total_items': total_items,
        'categories': categories,
        'total_tag_entries': total_tag_entries
    }


def search_media_by_tag(key, value):
    """
    @brief Searches for media items that have a specific tag key-value pair.
    @details Sucht Medien-Items anhand eines Tag-Schlüssel/Wert-Paares (v1.3.4).
    @param key Tag key to search for (e.g. 'artist', 'genre').
    @param value Tag value to match (case-insensitive substring match).
    @return List of media name strings / Liste von Mediennamen.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name
        FROM media m
        JOIN media_tags mt ON mt.media_id = m.id
        WHERE mt.key = ? AND mt.value LIKE ?
        ORDER BY m.name
    """, (key, f"%{value}%"))
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names


def get_all_tag_keys():
    """
    @brief Returns all distinct tag keys stored in the database.
    @details Gibt alle eindeutigen Tag-Schlüssel zurück (v1.3.4).
    @return Sorted list of tag key strings / Sortierte Liste von Tag-Schlüsseln.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT key FROM media_tags ORDER BY key")
    keys = [row[0] for row in cursor.fetchall()]
    conn.close()
    return keys


def get_tag_values(key):
    """
    @brief Returns all distinct values stored for a given tag key.
    @details Gibt alle eindeutigen Werte für einen Tag-Schlüssel zurück (v1.3.4).
    @param key Tag key (e.g. 'genre', 'artist').
    @return Sorted list of value strings / Sortierte Liste von Werten.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT value FROM media_tags
        WHERE key = ? AND value IS NOT NULL
        ORDER BY value
    """, (key,))
    values = [row[0] for row in cursor.fetchall()]
    conn.close()
    return values


def get_tag_value(name, key):
    """
    @brief Returns the value of a specific tag for a given media item.
    @details Gibt den Wert eines bestimmten Tags für ein Medium zurück (v1.3.4).
    @param name Media record name / Datenbank-Name.
    @param key Tag key (e.g. 'title', 'artist').
    @return Tag value string or None / Tag-Wert oder None.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mt.value FROM media_tags mt
        JOIN media m ON m.id = mt.media_id
        WHERE m.name = ? AND mt.key = ?
    """, (name, key))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
