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
             Since v1.3.7 releases have media_type, subtype (from a user-editable DB
             list), multi-language titles, cover images, multi-disc support, video
             standard/region/container-type columns, a release_identifiers table, and a
             scraper_sources plugin registry.
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

    # v1.3.5 / v1.3.7: Releases table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS releases (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            title             TEXT NOT NULL,
            type              TEXT NOT NULL DEFAULT 'Music',
            media_type        TEXT NOT NULL DEFAULT 'Audio',
            subtype           TEXT,
            year              INTEGER,
            cut               TEXT,
            status            TEXT NOT NULL DEFAULT 'pending',
            scraper_data      TEXT,
            parent_release_id INTEGER,
            video_standard    TEXT,
            region            TEXT,
            container_type    TEXT,
            disc_format       TEXT,
            total_discs       INTEGER,
            created_at        TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY(parent_release_id) REFERENCES releases(id) ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_releases_type       ON releases(type)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_releases_status     ON releases(status)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_releases_year       ON releases(year)
    """)

    # v1.3.5 / v1.3.7: Bridge table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS release_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id  INTEGER NOT NULL,
            media_id    INTEGER NOT NULL,
            position    INTEGER,
            disc_number INTEGER,
            disc_type   TEXT,
            disc_label  TEXT,
            FOREIGN KEY(release_id) REFERENCES releases(id) ON DELETE CASCADE,
            FOREIGN KEY(media_id)  REFERENCES media(id)    ON DELETE CASCADE,
            UNIQUE(media_id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_release_items_release
        ON release_items(release_id, position)
    """)

    # v1.3.7: External identifiers (ISBN-13, UPC, IMDb, MusicBrainz, …)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS release_identifiers (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id INTEGER NOT NULL,
            id_type    TEXT NOT NULL,
            value      TEXT NOT NULL,
            FOREIGN KEY(release_id) REFERENCES releases(id) ON DELETE CASCADE,
            UNIQUE(release_id, id_type, value)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_release_identifiers_type_value
        ON release_identifiers(id_type, value)
    """)

    # v1.3.7: User-manageable list of valid subtypes per media_type.
    # Seeded once with defaults; users/admins can add/remove entries.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS release_subtypes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            media_type TEXT NOT NULL,
            name       TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            UNIQUE(media_type, name)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_release_subtypes_media_type
        ON release_subtypes(media_type, sort_order)
    """)

    # v1.3.7: Multi-language titles (ISO 639-1 language codes + 'original')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS release_titles (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id INTEGER NOT NULL,
            language   TEXT NOT NULL,
            title      TEXT NOT NULL,
            FOREIGN KEY(release_id) REFERENCES releases(id) ON DELETE CASCADE,
            UNIQUE(release_id, language)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_release_titles_release
        ON release_titles(release_id)
    """)

    # v1.3.7: Cover images (front/back/disc/inlay/…) for releases and items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS release_covers (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id INTEGER,
            item_id    INTEGER,
            cover_type TEXT NOT NULL DEFAULT 'front',
            path       TEXT,
            url        TEXT,
            source     TEXT NOT NULL DEFAULT 'local',
            width      INTEGER,
            height     INTEGER,
            FOREIGN KEY(release_id) REFERENCES releases(id) ON DELETE CASCADE,
            FOREIGN KEY(item_id) REFERENCES release_items(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_release_covers_release
        ON release_covers(release_id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_release_covers_item
        ON release_covers(item_id)
    """)

    # v1.3.7: Scraper plugin registry (IMDb, TMDb, MusicBrainz, …)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraper_sources (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL UNIQUE,
            media_type TEXT,
            base_url   TEXT,
            enabled    BOOLEAN NOT NULL DEFAULT 1,
            priority   INTEGER NOT NULL DEFAULT 0,
            config     TEXT
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_scraper_sources_media_type
        ON scraper_sources(media_type, priority)
    """)

    conn.commit()

    # -----------------------------------------------------------------------
    # Migration: Add columns if missing (for existing databases)
    # -----------------------------------------------------------------------
    _migrate_media_columns(cursor, conn)
    _migrate_releases_columns(cursor, conn)
    _migrate_release_items_columns(cursor, conn)

    # Migration: Populate media_tags from existing JSON tags column
    _migrate_tags_to_table(cursor, conn)

    # Migration: Populate media_type from legacy type column
    _migrate_release_media_type(cursor, conn)

    # Seed release_subtypes with built-in defaults (idempotent)
    _seed_release_subtypes(cursor, conn)

    # Seed scraper_sources with well-known defaults (idempotent)
    _seed_scraper_sources(cursor, conn)

    conn.commit()
    conn.close()


def _migrate_media_columns(cursor, conn):
    new_columns = [
        ("category", "TEXT"),
        ("extension", "TEXT"),
        ("container", "TEXT"),
        ("tag_type", "TEXT"),
        ("codec", "TEXT"),
    ]
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE media ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists


def _migrate_releases_columns(cursor, conn):
    new_cols = [
        ("media_type",        "TEXT"),
        ("subtype",           "TEXT"),
        ("parent_release_id", "INTEGER"),
        ("video_standard",    "TEXT"),
        ("region",            "TEXT"),
        ("container_type",    "TEXT"),
        ("disc_format",       "TEXT"),
        ("total_discs",       "INTEGER"),
    ]
    for col_name, col_type in new_cols:
        try:
            cursor.execute(f"ALTER TABLE releases ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists

    # Create indexes now that columns are guaranteed present
    for idx_sql in (
        "CREATE INDEX IF NOT EXISTS idx_releases_media_type ON releases(media_type)",
        "CREATE INDEX IF NOT EXISTS idx_releases_subtype    ON releases(subtype)",
    ):
        try:
            cursor.execute(idx_sql)
        except sqlite3.OperationalError:
            pass
    conn.commit()


def _migrate_release_items_columns(cursor, conn):
    new_cols = [
        ("disc_number", "INTEGER"),
        ("disc_type",   "TEXT"),
        ("disc_label",  "TEXT"),
    ]
    for col_name, col_type in new_cols:
        try:
            cursor.execute(
                f"ALTER TABLE release_items ADD COLUMN {col_name} {col_type}"
            )
            conn.commit()
        except sqlite3.OperationalError:
            pass


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


# Mapping from v1.3.5 legacy `type` values to the v1.3.7 `media_type` column.
_LEGACY_TYPE_TO_MEDIA_TYPE = {
    'Music':    'Audio',
    'Film':     'Video',
    'EBook':    'Document',
    'Document': 'Document',
    'Audio':    'Audio',
    'Video':    'Video',
    'Image':    'Image',
}

# Default subtypes seeded into release_subtypes on first init.
_DEFAULT_SUBTYPES: dict[str, list[tuple[str, int]]] = {
    'Audio': [
        ('Album', 10), ('Compilation', 20), ('Audiobook', 30), ('Classical', 40),
        ('Soundtrack', 50), ('Single', 60), ('EP', 70), ('Live', 80),
    ],
    'Video': [
        ('Film', 10), ('Series', 20), ('Documentary', 30), ('Trailer', 40),
        ('BonusContent', 50), ('Short', 60),
    ],
    'Document': [
        ('EBook', 10), ('Manual', 20), ('Article', 30), ('Comic', 40),
    ],
    'Image': [
        ('Photo', 10), ('Artwork', 20), ('Cover', 30),
    ],
}

# Default scraper sources seeded on first init.
_DEFAULT_SCRAPER_SOURCES: list[dict] = [
    {'name': 'IMDb',         'media_type': 'Video',    'base_url': 'https://www.imdb.com',               'priority': 10},
    {'name': 'TMDb',         'media_type': 'Video',    'base_url': 'https://api.themoviedb.org/3',        'priority': 20},
    {'name': 'MusicBrainz',  'media_type': 'Audio',    'base_url': 'https://musicbrainz.org',             'priority': 10},
    {'name': 'CoverArtArchive', 'media_type': 'Audio', 'base_url': 'https://coverartarchive.org',         'priority': 20},
    {'name': 'OpenLibrary',  'media_type': 'Document', 'base_url': 'https://openlibrary.org',             'priority': 10},
    {'name': 'GoogleBooks',  'media_type': 'Document', 'base_url': 'https://www.googleapis.com/books/v1', 'priority': 20},
]


def _migrate_release_media_type(cursor, conn):
    """
    @brief Populates media_type from the legacy type column for existing releases.
    @details Befüllt media_type aus dem alten type-Feld (v1.3.7-Migration).
    """
    cursor.execute("""
        SELECT id, type FROM releases
        WHERE media_type IS NULL OR media_type = ''
    """)
    rows = cursor.fetchall()
    for release_id, legacy_type in rows:
        media_type = _LEGACY_TYPE_TO_MEDIA_TYPE.get(legacy_type, 'Audio')
        cursor.execute(
            "UPDATE releases SET media_type = ? WHERE id = ?",
            (media_type, release_id),
        )
    conn.commit()


def _seed_release_subtypes(cursor, conn):
    """
    @brief Seeds the release_subtypes table with default values (idempotent).
    @details Befüllt release_subtypes mit Standard-Einträgen (v1.3.7).
    """
    for media_type, entries in _DEFAULT_SUBTYPES.items():
        for name, sort_order in entries:
            try:
                cursor.execute(
                    "INSERT INTO release_subtypes (media_type, name, sort_order) "
                    "VALUES (?, ?, ?)",
                    (media_type, name, sort_order),
                )
            except sqlite3.IntegrityError:
                pass  # Already exists
    conn.commit()


def _seed_scraper_sources(cursor, conn):
    """
    @brief Seeds the scraper_sources table with well-known defaults (idempotent).
    @details Befüllt scraper_sources mit Standard-Scrapern (v1.3.7).
    """
    for src in _DEFAULT_SCRAPER_SOURCES:
        try:
            cursor.execute(
                "INSERT INTO scraper_sources (name, media_type, base_url, priority) "
                "VALUES (?, ?, ?, ?)",
                (src['name'], src['media_type'], src['base_url'], src['priority']),
            )
        except sqlite3.IntegrityError:
            pass  # Already exists
    conn.commit()


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
# Release API (v1.3.5 / v1.3.7)
# ===========================================================================
# A Release groups one or more filesystem items (media rows) into a logical
# unit – e.g. a music album, a film, an audiobook, or an ebook bundle.
#
# media_type:    Audio | Video | Document | Image
# subtype:       defined per media_type in the release_subtypes table
#
# Video-specific:
#   video_standard:  PAL | NTSC | SECAM
#   region:          ISO 3166-1 alpha-2 country code (DE, UK, US, JP, …)
#   container_type:  Blu-ray | PAL DVD | NTSC DVD | VCD | HD DVD | WMV DVD | Digital
#   disc_format:     ISO | BIN | MKV | MP4 | AVI | …
#   total_discs:     integer number of discs in the release
#
# status: pending | scraped | verified | ignored
# ===========================================================================


def insert_release(title, release_type='Music', year=None, cut=None,
                   status='pending', scraper_data=None, *,
                   media_type=None, subtype=None, parent_release_id=None,
                   video_standard=None, region=None, container_type=None,
                   disc_format=None, total_discs=None):
    """
    @brief Inserts a new release record into the database.
    @details Legt einen neuen Release-Datensatz an (v1.3.5/v1.3.7).
    @param title             Release title.
    @param release_type      Legacy type kept for backward compat ('Music', 'Film', …).
    @param year              Release year (integer or None).
    @param cut               Cut/edition string ('Director''s Cut', 'Extended Cut', …).
    @param status            'pending' | 'scraped' | 'verified' | 'ignored'.
    @param scraper_data      Optional dict with scraper-provided metadata.
    @param media_type        'Audio' | 'Video' | 'Document' | 'Image'.  Derived from
                             release_type when omitted.
    @param subtype           Subtype name from release_subtypes (e.g. 'Album', 'Film').
    @param parent_release_id FK to releases.id for bonus-content / child releases.
    @param video_standard    'PAL' | 'NTSC' | 'SECAM' (Video releases).
    @param region            ISO 3166-1 alpha-2 country code, e.g. 'DE', 'US'.
    @param container_type    Physical/logical container: 'Blu-ray', 'PAL DVD', …
    @param disc_format       File format of the disc image: 'ISO', 'BIN', 'MKV', …
    @param total_discs       Number of discs in the release.
    @return Newly created release id.
    """
    if media_type is None:
        media_type = _LEGACY_TYPE_TO_MEDIA_TYPE.get(release_type, 'Audio')
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO releases
            (title, type, media_type, subtype, year, cut, status, scraper_data,
             parent_release_id, video_standard, region, container_type,
             disc_format, total_discs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title, release_type, media_type, subtype, year, cut, status,
        json.dumps(scraper_data) if scraper_data is not None else None,
        parent_release_id, video_standard, region, container_type,
        disc_format, total_discs,
    ))
    conn.commit()
    release_id = cursor.lastrowid
    conn.close()
    return release_id


def get_release(release_id):
    """
    @brief Returns a single release record as a dictionary, including titles and identifiers.
    @details Gibt einen Release-Datensatz inkl. Titeln und Identifikatoren zurück (v1.3.7).
    @param release_id  Primary key of the release.
    @return Release dict or None.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM releases WHERE id = ?", (release_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return None
    result = _release_row_to_dict(row)
    result['identifiers'] = _fetch_identifiers(cursor, release_id)
    result['titles'] = _fetch_titles(cursor, release_id)
    conn.close()
    return result


def get_all_releases(release_type=None, status=None, media_type=None,
                     subtype=None):
    """
    @brief Returns all release records, with optional filters.
    @details Gibt alle Release-Datensätze zurück (v1.3.5/v1.3.7).
    @param release_type  Optional legacy type filter.
    @param status        Optional status filter.
    @param media_type    Optional 'Audio' | 'Video' | 'Document' | 'Image' filter.
    @param subtype       Optional subtype filter.
    @return List of release dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM releases"
    params: list = []
    filters: list[str] = []
    if release_type is not None:
        filters.append("type = ?")
        params.append(release_type)
    if media_type is not None:
        filters.append("media_type = ?")
        params.append(media_type)
    if subtype is not None:
        filters.append("subtype = ?")
        params.append(subtype)
    if status is not None:
        filters.append("status = ?")
        params.append(status)
    if filters:
        sql += " WHERE " + " AND ".join(filters)
    sql += " ORDER BY title"

    cursor.execute(sql, params)
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
    @return True if the record was found and updated.
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
    @brief Deletes a release and all dependent rows (items, identifiers, titles, covers).
    @details Löscht einen Release inkl. aller abhängigen Einträge (v1.3.5/v1.3.7).
    @param release_id  Primary key of the release.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM release_covers      WHERE release_id = ?", (release_id,))
        cursor.execute("DELETE FROM release_identifiers WHERE release_id = ?", (release_id,))
        cursor.execute("DELETE FROM release_titles      WHERE release_id = ?", (release_id,))
        cursor.execute("DELETE FROM release_items       WHERE release_id = ?", (release_id,))
        cursor.execute("DELETE FROM releases            WHERE id = ?",         (release_id,))
        conn.commit()
    finally:
        conn.close()


def assign_item_to_release(release_id, media_name, position=None, *,
                           disc_number=None, disc_type=None, disc_label=None):
    """
    @brief Assigns a media item (file) to a release.
    @details Weist einem Release ein Medien-Item zu (v1.3.5/v1.3.7).
             A media item can belong to exactly one release.
    @param release_id   Release primary key.
    @param media_name   Unique name of the media item (media.name).
    @param position     Track / global position within the release.
    @param disc_number  Disc number for multi-disc releases (1, 2, …).
    @param disc_type    'Film' | 'Bonus' | 'Soundtrack' | 'Extra' | 'Document'.
    @param disc_label   Human-readable disc label, e.g. 'Disc 1 – Extended Cut'.
    @return True if successfully assigned.
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
            INSERT OR REPLACE INTO release_items
                (release_id, media_id, position, disc_number, disc_type, disc_label)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (release_id, media_id, position, disc_number, disc_type, disc_label))
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
    @return True if a row was removed.
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
    @brief Returns all media items belonging to a release, ordered by disc/position.
    @details Gibt alle Medien-Items eines Releases zurück (v1.3.5/v1.3.7).
    @param release_id  Release primary key.
    @return List of dicts with media fields + position + disc metadata.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, m.path, m.type, m.duration, m.category, m.extension,
               m.container, m.tag_type, m.codec, m.is_transcoded,
               m.transcoded_format, m.tags,
               ri.position, ri.disc_number, ri.disc_type, ri.disc_label
        FROM release_items ri
        JOIN media m ON m.id = ri.media_id
        WHERE ri.release_id = ?
        ORDER BY ri.disc_number, ri.position, m.name
    """, (release_id,))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            'name':             row['name'],
            'path':             row['path'],
            'type':             row['type'],
            'duration':         row['duration'],
            'category':         row['category'],
            'extension':        row['extension'],
            'container':        row['container'],
            'tag_type':         row['tag_type'],
            'codec':            row['codec'],
            'is_transcoded':    bool(row['is_transcoded']),
            'transcoded_format': row['transcoded_format'],
            'tags':             json.loads(row['tags']) if row['tags'] else {},
            'position':         row['position'],
            'disc_number':      row['disc_number'],
            'disc_type':        row['disc_type'],
            'disc_label':       row['disc_label'],
        })
    return result


def get_item_release(media_name):
    """
    @brief Returns the release a media item belongs to, or None.
    @details Gibt den Release eines Medien-Items zurück (v1.3.5/v1.3.7).
    @param media_name  Unique name of the media item.
    @return Release dict (including identifiers and titles) or None.
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
    if row is None:
        conn.close()
        return None
    result = _release_row_to_dict(row)
    result['identifiers'] = _fetch_identifiers(cursor, result['id'])
    result['titles']      = _fetch_titles(cursor, result['id'])
    conn.close()
    return result


def search_releases(query, release_type=None, media_type=None, subtype=None):
    """
    @brief Full-text substring search on release titles.
    @details Sucht in Release-Titeln nach einer Zeichenkette (v1.3.5/v1.3.7).
    @param query        Substring to search for.
    @param release_type Optional legacy type filter.
    @param media_type   Optional media_type filter ('Audio', 'Video', …).
    @param subtype      Optional subtype filter.
    @return List of matching release dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM releases WHERE title LIKE ?"
    params: list = [f"%{query}%"]
    if release_type is not None:
        sql += " AND type = ?"
        params.append(release_type)
    if media_type is not None:
        sql += " AND media_type = ?"
        params.append(media_type)
    if subtype is not None:
        sql += " AND subtype = ?"
        params.append(subtype)
    sql += " ORDER BY title"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [_release_row_to_dict(r) for r in rows]


def _fetch_identifiers(cursor, release_id):
    """Returns identifiers for a release as list of {id_type, value} dicts."""
    cursor.execute("""
        SELECT id_type, value FROM release_identifiers
        WHERE release_id = ?
        ORDER BY id_type, value
    """, (release_id,))
    return [{'id_type': r[0], 'value': r[1]} for r in cursor.fetchall()]


def _fetch_titles(cursor, release_id):
    """Returns multi-language titles as {language: title} dict."""
    cursor.execute("""
        SELECT language, title FROM release_titles
        WHERE release_id = ?
        ORDER BY language
    """, (release_id,))
    return {r[0]: r[1] for r in cursor.fetchall()}


def _release_row_to_dict(row):
    """
    @brief Converts a releases table row to a Python dictionary.
    @details Wandelt eine releases-Zeile in ein Dictionary um (v1.3.5/v1.3.7).
    @param row  sqlite3.Row from the releases table.
    @return Release dict with scraper_data deserialized.
    """
    scraper_raw = row['scraper_data']
    try:
        scraper_parsed = json.loads(scraper_raw) if scraper_raw else None
    except (json.JSONDecodeError, TypeError):
        scraper_parsed = scraper_raw

    keys = row.keys()
    return {
        'id':                row['id'],
        'title':             row['title'],
        'type':              row['type'],
        'media_type':        row['media_type']        if 'media_type'        in keys else None,
        'subtype':           row['subtype']           if 'subtype'           in keys else None,
        'year':              row['year'],
        'cut':               row['cut'],
        'status':            row['status'],
        'scraper_data':      scraper_parsed,
        'parent_release_id': row['parent_release_id'] if 'parent_release_id' in keys else None,
        'video_standard':    row['video_standard']    if 'video_standard'    in keys else None,
        'region':            row['region']            if 'region'            in keys else None,
        'container_type':    row['container_type']    if 'container_type'    in keys else None,
        'disc_format':       row['disc_format']       if 'disc_format'       in keys else None,
        'total_discs':       row['total_discs']       if 'total_discs'       in keys else None,
        'created_at':        row['created_at'],
    }


# ===========================================================================
# Release Identifiers API (v1.3.7)
# ===========================================================================
# A release can carry any number of external identifiers:
#   ISBN-13, ISBN-10, ISBN, ISSN, DOI
#   UPC, EAN, Barcode, Catalog
#   IMDb, TMDb, MusicBrainz, ASIN
# ===========================================================================


def add_release_identifier(release_id, id_type, value):
    """
    @brief Adds an external identifier to a release.
    @param release_id  Release primary key.
    @param id_type     Identifier type, e.g. 'ISBN-13', 'UPC', 'IMDb'.
    @param value       Identifier value string.
    @return True if newly inserted, False if it already existed.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO release_identifiers (release_id, id_type, value)
            VALUES (?, ?, ?)
        """, (release_id, id_type, value))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_release_identifiers(release_id):
    """
    @brief Returns all identifiers for a release.
    @param release_id  Release primary key.
    @return List of {'id_type': ..., 'value': ...} dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_type, value FROM release_identifiers
        WHERE release_id = ?
        ORDER BY id_type, value
    """, (release_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{'id_type': r[0], 'value': r[1]} for r in rows]


def remove_release_identifier(release_id, id_type, value):
    """
    @brief Removes a specific identifier from a release.
    @return True if a row was removed.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM release_identifiers
            WHERE release_id = ? AND id_type = ? AND value = ?
        """, (release_id, id_type, value))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_releases_by_identifier(id_type, value):
    """
    @brief Returns all releases that carry a specific identifier.
    @param id_type  Identifier type string.
    @param value    Identifier value to match exactly.
    @return List of release dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.* FROM releases r
        JOIN release_identifiers ri ON ri.release_id = r.id
        WHERE ri.id_type = ? AND ri.value = ?
        ORDER BY r.title
    """, (id_type, value))
    rows = cursor.fetchall()
    conn.close()
    return [_release_row_to_dict(r) for r in rows]


# ===========================================================================
# Release Subtypes API (v1.3.7)
# ===========================================================================
# The release_subtypes table is the authoritative list of valid subtype values
# per media_type.  Users/admins can add custom entries; built-in defaults are
# seeded on init_db().
# ===========================================================================


def get_release_subtypes(media_type=None):
    """
    @brief Returns the list of defined subtypes, optionally filtered by media_type.
    @param media_type  Optional filter ('Audio', 'Video', 'Document', 'Image').
    @return List of {'media_type': ..., 'name': ..., 'sort_order': ...} dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    if media_type is not None:
        cursor.execute("""
            SELECT media_type, name, sort_order FROM release_subtypes
            WHERE media_type = ?
            ORDER BY sort_order, name
        """, (media_type,))
    else:
        cursor.execute("""
            SELECT media_type, name, sort_order FROM release_subtypes
            ORDER BY media_type, sort_order, name
        """)
    rows = cursor.fetchall()
    conn.close()
    return [{'media_type': r[0], 'name': r[1], 'sort_order': r[2]} for r in rows]


def add_release_subtype(media_type, name, sort_order=0):
    """
    @brief Adds a new subtype entry to the release_subtypes table.
    @param media_type   'Audio' | 'Video' | 'Document' | 'Image'.
    @param name         Subtype name (e.g. 'Extended Cut').
    @param sort_order   Display sort order (default 0).
    @return True if newly inserted, False if already existed.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO release_subtypes (media_type, name, sort_order)
            VALUES (?, ?, ?)
        """, (media_type, name, sort_order))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_release_subtype(media_type, name):
    """
    @brief Removes a subtype entry from the release_subtypes table.
    @return True if a row was removed.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM release_subtypes WHERE media_type = ? AND name = ?
        """, (media_type, name))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


# ===========================================================================
# Release Titles API (v1.3.7)
# ===========================================================================
# Film titles exist in multiple languages (German, English, original, …).
# Language codes follow ISO 639-1 ('de', 'en', 'fr', …).
# Use 'original' for the original-language title.
# ===========================================================================


def set_release_title(release_id, language, title):
    """
    @brief Sets (inserts or replaces) a language-specific title for a release.
    @param release_id  Release primary key.
    @param language    ISO 639-1 code (e.g. 'de', 'en') or 'original'.
    @param title       Title string in that language.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO release_titles (release_id, language, title)
            VALUES (?, ?, ?)
        """, (release_id, language, title))
        conn.commit()
    finally:
        conn.close()


def get_release_titles(release_id):
    """
    @brief Returns all language-specific titles for a release.
    @param release_id  Release primary key.
    @return Dict {language: title}, e.g. {'de': 'Der Pate', 'en': 'The Godfather'}.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT language, title FROM release_titles
        WHERE release_id = ?
        ORDER BY language
    """, (release_id,))
    rows = cursor.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}


def remove_release_title(release_id, language):
    """
    @brief Removes the title for a specific language.
    @return True if a row was removed.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM release_titles WHERE release_id = ? AND language = ?
        """, (release_id, language))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


# ===========================================================================
# Release Covers API (v1.3.7)
# ===========================================================================
# Covers / artwork can be attached to a release or to a specific release_item.
# cover_type: front | back | disc | inlay | spine | poster | screenshot | …
# source:     local | scraper | imdb | tmdb | musicbrainz | coverartarchive | …
# ===========================================================================


def add_release_cover(release_id=None, item_id=None, cover_type='front',
                      path=None, url=None, source='local',
                      width=None, height=None):
    """
    @brief Adds a cover image entry for a release or a release item.
    @param release_id  Release primary key (may be None if item_id given).
    @param item_id     release_items primary key (may be None if release_id given).
    @param cover_type  'front' | 'back' | 'disc' | 'inlay' | 'poster' | …
    @param path        Local filesystem path (optional).
    @param url         Remote URL from scraper (optional).
    @param source      Origin: 'local' | 'imdb' | 'tmdb' | 'musicbrainz' | …
    @param width       Image width in pixels (optional).
    @param height      Image height in pixels (optional).
    @return Newly created cover id.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO release_covers
                (release_id, item_id, cover_type, path, url, source, width, height)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (release_id, item_id, cover_type, path, url, source, width, height))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_release_covers(release_id=None, item_id=None):
    """
    @brief Returns all cover entries for a release or item.
    @param release_id  Filter by release (optional).
    @param item_id     Filter by release_item (optional).
    @return List of cover dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if release_id is not None and item_id is not None:
        cursor.execute("""
            SELECT * FROM release_covers
            WHERE release_id = ? AND item_id = ?
            ORDER BY cover_type
        """, (release_id, item_id))
    elif release_id is not None:
        cursor.execute("""
            SELECT * FROM release_covers WHERE release_id = ?
            ORDER BY cover_type
        """, (release_id,))
    elif item_id is not None:
        cursor.execute("""
            SELECT * FROM release_covers WHERE item_id = ?
            ORDER BY cover_type
        """, (item_id,))
    else:
        return []

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def remove_release_cover(cover_id):
    """
    @brief Removes a cover entry by its primary key.
    @return True if a row was removed.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM release_covers WHERE id = ?", (cover_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


# ===========================================================================
# Scraper Sources API (v1.3.7)
# ===========================================================================
# The scraper_sources table is the plugin registry for media scrapers.
# Well-known sources (IMDb, TMDb, MusicBrainz, …) are seeded on init_db().
# ===========================================================================


def get_scraper_sources(media_type=None, enabled_only=False):
    """
    @brief Returns registered scraper sources, ordered by priority.
    @param media_type   Optional filter ('Video', 'Audio', 'Document', or None for all).
    @param enabled_only Return only enabled sources when True.
    @return List of scraper source dicts.
    """
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM scraper_sources"
    params: list = []
    filters: list[str] = []
    if media_type is not None:
        filters.append("(media_type = ? OR media_type IS NULL)")
        params.append(media_type)
    if enabled_only:
        filters.append("enabled = 1")
    if filters:
        sql += " WHERE " + " AND ".join(filters)
    sql += " ORDER BY priority, name"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def register_scraper_source(name, media_type=None, base_url=None,
                             priority=0, config=None):
    """
    @brief Registers a new scraper source / plugin.
    @param name        Unique name, e.g. 'MyIMDbPlugin'.
    @param media_type  'Video' | 'Audio' | 'Document' | 'Image' | None (all).
    @param base_url    Base URL for the API endpoint.
    @param priority    Lower value = higher priority.
    @param config      Optional dict with plugin-specific configuration.
    @return Scraper source id.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO scraper_sources
                (name, media_type, base_url, priority, config)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name, media_type, base_url, priority,
            json.dumps(config) if config is not None else None,
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def set_scraper_source_enabled(name, enabled):
    """
    @brief Enables or disables a scraper source.
    @return True if the row was found and updated.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE scraper_sources SET enabled = ? WHERE name = ?
        """, (1 if enabled else 0, name))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
