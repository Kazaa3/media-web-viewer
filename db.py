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
             Since v1.3.5 a releases table groups media items into logical releases
             (albums, films, audiobooks, etc.) with minimal status fields and a
             JSON scraper_data column for scraper-enriched metadata.
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

    # v1.3.5: Releases table – groups items into logical releases.
    # Stores only minimal status information; all scraper-enriched metadata
    # goes into the JSON scraper_data column.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS releases (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            type        TEXT NOT NULL DEFAULT 'Music',
            year        INTEGER,
            cut         TEXT,
            status      TEXT NOT NULL DEFAULT 'pending',
            scraper_data TEXT,
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # Indexes for large-scale queries (100k+ films, 500k+ music files)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_releases_type
        ON releases(type)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_releases_status
        ON releases(status)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_releases_year
        ON releases(year)
    """)

    # v1.3.5: Bridge table – links media items (files) to their parent release.
    # A media item can belong to exactly one release.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS release_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id  INTEGER NOT NULL,
            media_id    INTEGER NOT NULL,
            position    INTEGER,
            FOREIGN KEY(release_id) REFERENCES releases(id) ON DELETE CASCADE,
            FOREIGN KEY(media_id)  REFERENCES media(id)    ON DELETE CASCADE,
            UNIQUE(media_id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_release_items_release
        ON release_items(release_id, position)
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


# ===========================================================================
# Release API (v1.3.5)
# ===========================================================================
# A Release groups one or more filesystem items (media rows) into a logical
# unit – e.g. a music album, a film, an audiobook.  The table stores only
# minimal status fields; all scraper-enriched data lives in scraper_data
# (a Python dict serialised to JSON via json.dumps).
#
# Valid values for `type`:   Music | Film | EBook | Document
# Valid values for `status`: pending | scraped | verified | ignored
# ===========================================================================


def insert_release(title, release_type='Music', year=None, cut=None,
                   status='pending', scraper_data=None):
    """
    @brief Inserts a new release record into the database.
    @details Legt einen neuen Release-Datensatz in der Datenbank an (v1.3.5).
    @param title   Release title (album name, film title, …).
    @param release_type  Media type: 'Music', 'Film', 'EBook', 'Document'.
    @param year    Release year (integer or None).
    @param cut     Cut/edition string for films ('Theatrical Cut', …) or None.
    @param status  Scraper status: 'pending' | 'scraped' | 'verified' | 'ignored'.
    @param scraper_data  Optional dict with scraper-provided metadata.
    @return Newly created release id / Neue Release-ID.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO releases (title, type, year, cut, status, scraper_data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        release_type,
        year,
        cut,
        status,
        json.dumps(scraper_data) if scraper_data is not None else None,
    ))
    conn.commit()
    release_id = cursor.lastrowid
    conn.close()
    return release_id


def get_release(release_id):
    """
    @brief Returns a single release record as a dictionary.
    @details Gibt einen Release-Datensatz als Dictionary zurück (v1.3.5).
    @param release_id  Primary key of the release.
    @return Release dict or None / Release-Dict oder None.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM releases WHERE id = ?", (release_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return _release_row_to_dict(row)


def get_all_releases(release_type=None, status=None):
    """
    @brief Returns all release records, with optional filters.
    @details Gibt alle Release-Datensätze zurück (v1.3.5).
    @param release_type  Optional type filter ('Music', 'Film', …).
    @param status        Optional status filter ('pending', 'scraped', …).
    @return List of release dicts / Liste von Release-Dictionaries.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM releases"
    params = []
    filters = []
    if release_type is not None:
        filters.append("type = ?")
        params.append(release_type)
    if status is not None:
        filters.append("status = ?")
        params.append(status)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += " ORDER BY title"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [_release_row_to_dict(r) for r in rows]


def update_release_scraper_data(release_id, scraper_data, status='scraped'):
    """
    @brief Stores scraper-provided metadata for a release.
    @details Speichert Scraper-Metadaten für einen Release (v1.3.5).
    @param release_id   Primary key of the release.
    @param scraper_data Python dict with scraper-provided metadata.
    @param status       New status value (default: 'scraped').
    @return True if the record was found and updated / True wenn aktualisiert.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE releases SET scraper_data = ?, status = ?
        WHERE id = ?
    """, (json.dumps(scraper_data), status, release_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def update_release_status(release_id, status):
    """
    @brief Updates the status field of a release.
    @details Aktualisiert den Status eines Releases (v1.3.5).
    @param release_id  Primary key of the release.
    @param status      New status string.
    @return True if the record was found and updated.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE releases SET status = ? WHERE id = ?", (status, release_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_release(release_id):
    """
    @brief Deletes a release and its release_items bridge rows.
    @details Löscht einen Release inkl. release_items-Einträge (v1.3.5).
    @param release_id  Primary key of the release.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM release_items WHERE release_id = ?", (release_id,))
        cursor.execute("DELETE FROM releases WHERE id = ?", (release_id,))
        conn.commit()
    finally:
        conn.close()


def assign_item_to_release(release_id, media_name, position=None):
    """
    @brief Assigns a media item (file) to a release.
    @details Weist einem Release ein Medien-Item zu (v1.3.5).
             A media item can belong to exactly one release.
    @param release_id   Release primary key.
    @param media_name   Unique name of the media item (media.name).
    @param position     Track / disc position within the release (optional).
    @return True if successfully assigned / True wenn erfolgreich zugewiesen.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM media WHERE name = ?", (media_name,))
        row = cursor.fetchone()
        if row is None:
            return False
        media_id = row[0]
        cursor.execute("""
            INSERT OR REPLACE INTO release_items (release_id, media_id, position)
            VALUES (?, ?, ?)
        """, (release_id, media_id, position))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_item_from_release(media_name):
    """
    @brief Removes a media item from its current release.
    @details Entfernt ein Medien-Item aus seinem Release (v1.3.5).
    @param media_name  Unique name of the media item.
    @return True if a row was removed / True wenn eine Zeile entfernt wurde.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM release_items
            WHERE media_id = (SELECT id FROM media WHERE name = ?)
        """, (media_name,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_release_items(release_id):
    """
    @brief Returns all media items belonging to a release, ordered by position.
    @details Gibt alle Medien-Items eines Releases zurück (v1.3.5).
    @param release_id  Release primary key.
    @return List of dicts with media fields + position.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, m.path, m.type, m.duration, m.category, m.extension,
               m.container, m.tag_type, m.codec, m.is_transcoded,
               m.transcoded_format, m.tags, ri.position
        FROM release_items ri
        JOIN media m ON m.id = ri.media_id
        WHERE ri.release_id = ?
        ORDER BY ri.position, m.name
    """, (release_id,))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
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
            'tags': json.loads(row['tags']) if row['tags'] else {},
            'position': row['position'],
        })
    return result


def get_item_release(media_name):
    """
    @brief Returns the release a media item belongs to, or None.
    @details Gibt den Release eines Medien-Items zurück (v1.3.5).
    @param media_name  Unique name of the media item.
    @return Release dict or None.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*
        FROM releases r
        JOIN release_items ri ON ri.release_id = r.id
        JOIN media m          ON m.id = ri.media_id
        WHERE m.name = ?
    """, (media_name,))
    row = cursor.fetchone()
    conn.close()
    return _release_row_to_dict(row) if row else None


def search_releases(query, release_type=None):
    """
    @brief Full-text substring search on release titles.
    @details Sucht in Release-Titeln nach einer Zeichenkette (v1.3.5).
    @param query        Substring to search for.
    @param release_type Optional type filter.
    @return List of matching release dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if release_type is not None:
        cursor.execute("""
            SELECT * FROM releases
            WHERE title LIKE ? AND type = ?
            ORDER BY title
        """, (f"%{query}%", release_type))
    else:
        cursor.execute("""
            SELECT * FROM releases
            WHERE title LIKE ?
            ORDER BY title
        """, (f"%{query}%",))

    rows = cursor.fetchall()
    conn.close()
    return [_release_row_to_dict(r) for r in rows]


def _release_row_to_dict(row):
    """
    @brief Converts a releases table row to a Python dictionary.
    @details Wandelt eine releases-Zeile in ein Dictionary um.
    @param row  sqlite3.Row from the releases table.
    @return Release dict with scraper_data deserialized.
    """
    scraper_raw = row['scraper_data']
    try:
        scraper_parsed = json.loads(scraper_raw) if scraper_raw else None
    except (json.JSONDecodeError, TypeError):
        scraper_parsed = scraper_raw
    return {
        'id': row['id'],
        'title': row['title'],
        'type': row['type'],
        'year': row['year'],
        'cut': row['cut'],
        'status': row['status'],
        'scraper_data': scraper_parsed,
        'created_at': row['created_at'],
    }
