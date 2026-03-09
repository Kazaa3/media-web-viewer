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
             Since v1.3.4 a dedicated 'tags' table replaces the JSON blob in media.tags.
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

    # v1.3.4: Dedicated tags table (EAV schema)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_id INTEGER NOT NULL,
            key TEXT NOT NULL,
            value TEXT,
            FOREIGN KEY(media_id) REFERENCES media(id) ON DELETE CASCADE,
            UNIQUE(media_id, key)
        )
    """)

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_tags_media_id ON tags(media_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_tags_key ON tags(key)"
    )

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

    conn.commit()

    # v1.3.4 migration: populate 'tags' table from existing JSON blobs
    _migrate_json_tags_to_table(cursor)
    conn.commit()
    conn.close()


def _migrate_json_tags_to_table(cursor):
    """
    @brief One-time migration: moves tag data from media.tags JSON blob into
           the dedicated tags table.
    @details Einmalige Migration: Überträgt Tag-Daten aus dem JSON-Blob
             media.tags in die dedizierte tags-Tabelle.
    @param cursor Active database cursor / Aktiver Datenbank-Cursor.
    """
    cursor.execute("SELECT id, tags FROM media WHERE tags IS NOT NULL AND tags != ''")
    rows = cursor.fetchall()
    for media_id, tags_json in rows:
        try:
            tags_dict = json.loads(tags_json)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(tags_dict, dict):
            continue
        for key, value in tags_dict.items():
            cursor.execute("""
                INSERT OR IGNORE INTO tags (media_id, key, value)
                VALUES (?, ?, ?)
            """, (media_id, key, _tag_value_to_str(value)))


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


def _tag_value_to_str(value) -> str:
    """
    @brief Serializes a single tag value to a string for database storage.
    @details Serialisiert einen Tag-Wert als String für die Datenbankspeicherung.
             Plain strings are stored as-is; everything else is JSON-encoded.
    @param value Tag value to serialize / Zu serialisierender Tag-Wert.
    @return String representation / String-Darstellung.
    """
    return value if isinstance(value, str) else json.dumps(value)


def _tag_value_from_str(raw_value):
    """
    @brief Deserializes a tag value from its stored string representation.
    @details Deserialisiert einen Tag-Wert aus seiner gespeicherten String-Darstellung.
             JSON-encoded values are decoded; plain strings are returned as-is.
    @param raw_value Stored string value / Gespeicherter String-Wert.
    @return Deserialized value / Deserialisierter Wert.
    """
    try:
        return json.loads(raw_value)
    except (json.JSONDecodeError, TypeError):
        return raw_value


def insert_media(item_dict):
    """
    @brief Inserts a new media item into the database.
    @details Fügt ein neues Medien-Item in die Datenbank ein.
             Since v1.3.4 tags are also written to the dedicated tags table.
    @param item_dict Metadata dictionary / Dictionary mit Metadaten.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        tags_dict = item_dict.get('tags') or {}
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
            json.dumps(tags_dict),
            item_dict.get('extension'),
            item_dict.get('container'),
            item_dict.get('tag_type'),
            item_dict.get('codec')
        ))
        media_id = cursor.lastrowid

        # v1.3.4: Write individual tag rows to the dedicated tags table
        _write_tags_for_media(cursor, media_id, tags_dict)
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Schon vorhanden
    finally:
        conn.close()


def _write_tags_for_media(cursor, media_id, tags_dict):
    """
    @brief Writes all key/value pairs from tags_dict into the tags table for
           the given media_id, replacing any existing rows for that media item.
    @details Schreibt alle Schlüssel-Wert-Paare aus tags_dict in die tags-Tabelle
             für die angegebene media_id und ersetzt vorhandene Einträge.
    @param cursor Active database cursor / Aktiver Datenbank-Cursor.
    @param media_id Primary key of the media row / Primärschlüssel des Media-Eintrags.
    @param tags_dict Dictionary of tag key/value pairs / Tag-Dictionary.
    """
    cursor.execute("DELETE FROM tags WHERE media_id = ?", (media_id,))
    for key, value in tags_dict.items():
        cursor.execute("""
            INSERT INTO tags (media_id, key, value) VALUES (?, ?, ?)
        """, (media_id, key, _tag_value_to_str(value)))


def get_all_media():
    """
    @brief Retrieves all media items from the database.
    @details Ruft alle Medien-Items aus der Datenbank ab.
             Since v1.3.4 tags are read from the dedicated tags table.
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
        tags = _load_tags_for_media(cursor, row['id'])
        # Fall back to legacy JSON blob if the tags table has no entries yet
        if not tags and row['tags']:
            try:
                tags = json.loads(row['tags'])
            except (json.JSONDecodeError, TypeError):
                tags = {}
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
            'tags': tags
        })
    conn.close()
    return media_list


def _load_tags_for_media(cursor, media_id):
    """
    @brief Loads tags for a single media item from the dedicated tags table.
    @details Lädt Tags für ein einzelnes Medien-Item aus der dedizierten tags-Tabelle.
    @param cursor Active database cursor / Aktiver Datenbank-Cursor.
    @param media_id Primary key of the media row / Primärschlüssel des Media-Eintrags.
    @return Dictionary of tag key/value pairs / Tag-Dictionary.
    """
    cursor.execute("SELECT key, value FROM tags WHERE media_id = ?", (media_id,))
    return {key: _tag_value_from_str(value) for key, value in cursor.fetchall()}


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
             Since v1.3.4 tags are stored in the dedicated tags table and the
             legacy JSON blob in media.tags is kept in sync for compatibility.
    @param name Media record name / Datenbank-Name.
    @param tags_dict New tags dictionary / Neues Dictionary mit Tags.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    # Keep JSON blob in sync for backward compatibility
    cursor.execute("""
        UPDATE media
        SET tags = ?
        WHERE name = ?
    """, (json.dumps(tags_dict), name))
    cursor.execute("SELECT id FROM media WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        _write_tags_for_media(cursor, row[0], tags_dict)
    conn.commit()
    conn.close()


def get_media_tags(name):
    """
    @brief Returns the tags dictionary for a single media item.
    @details Gibt das Tags-Dictionary für ein einzelnes Medien-Item zurück.
             Reads from the dedicated tags table (v1.3.4+).
    @param name Media record name / Datenbank-Name.
    @return Dictionary of tag key/value pairs, or empty dict if not found.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, tags FROM media WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return {}
    media_id, legacy_tags_json = row
    tags = _load_tags_for_media(cursor, media_id)
    if not tags and legacy_tags_json:
        try:
            tags = json.loads(legacy_tags_json)
        except (json.JSONDecodeError, TypeError):
            tags = {}
    conn.close()
    return tags


def get_tags_by_key(key):
    """
    @brief Returns all media items that have the given tag key, with their values.
    @details Gibt alle Medien-Items zurück, die den angegebenen Tag-Schlüssel
             besitzen, zusammen mit den zugehörigen Werten.
    @param key Tag key to search for / Zu suchender Tag-Schlüssel.
    @return List of dicts with 'name' and 'value' / Liste von Dicts mit Name und Wert.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, t.value
        FROM tags t
        JOIN media m ON m.id = t.media_id
        WHERE t.key = ?
        ORDER BY m.name
    """, (key,))
    results = []
    for media_name, raw_value in cursor.fetchall():
        results.append({'name': media_name, 'value': _tag_value_from_str(raw_value)})
    conn.close()
    return results


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
