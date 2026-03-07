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
import os
import json

from pathlib import Path

# Use a user-writable path for the database
DB_DIR = Path.home() / ".media-web-viewer"
DB_FILENAME = str(DB_DIR / "media_library.db")

def init_db():
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
            tags TEXT
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

    # Migration: Add category column if missing (for existing databases)
    try:
        cursor.execute("ALTER TABLE media ADD COLUMN category TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass # Already exists

    conn.commit()
    conn.close()

def get_known_media_names():
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM media")
    names = {row[0] for row in cursor.fetchall()}
    conn.close()
    return names

def clear_media():
    conn = sqlite3.connect(DB_FILENAME)
    conn.execute("DELETE FROM media")
    conn.commit()
    conn.close()

def insert_media(item_dict):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO media (name, path, type, duration, category, is_transcoded, transcoded_format, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_dict['name'],
            item_dict['path'],
            item_dict['type'],
            item_dict['duration'],
            item_dict.get('category', 'Audio'),
            item_dict['is_transcoded'],
            item_dict.get('transcoded_format'),
            json.dumps(item_dict['tags'])
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Schon vorhanden
    finally:
        conn.close()

def get_all_media():
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
            'is_transcoded': bool(row['is_transcoded']),
            'transcoded_format': row['transcoded_format'],
            'tags': json.loads(row['tags']) if row['tags'] else {}
        })
    conn.close()
    return media_list

def get_media_path(name):
    """Gibt den vollen Dateipfad für einen Mediennamen zurück."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM media WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
def update_media_tags(name, tags_dict):
    """Aktualisiert die Tags eines Medien-Items in der Datenbank."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE media 
        SET tags = ? 
        WHERE name = ?
    """, (json.dumps(tags_dict), name))
    conn.commit()
    conn.close()

def rename_media(old_name, new_name):
    """Benennt ein Medium in der DB um (nur das Feld 'name')."""
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
    """Löscht ein Medium aus der DB."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM media WHERE name = ?", (name,))
        conn.commit()
    finally:
        conn.close()

def get_db_stats():
    """Gibt Statistiken über die Datenbank zurück."""
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
