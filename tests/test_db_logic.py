# Kategorie: Database Test
# Eingabewerte: Media-Dictionaries, Dateipfade
# Ausgabewerte: Datenbank-Einträge
# Testdateien: Temporäre SQLite DB
# Kommentar: Prüft CRUD Operationen auf der Media-Datenbank.

import db
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def temp_db(tmp_path):
    # Use a temporary database file for testing
    original_db = db.DB_FILENAME
    test_db = str(tmp_path / "test_media_library.db")
    db.DB_FILENAME = test_db
    db.init_db()
    yield
    db.DB_FILENAME = original_db


def test_insert_and_get_media(temp_db):
    item = {
        'name': 'test_song.mp3',
        'path': '/path/to/test_song.mp3',
        'type': 'mp3',
        'duration': '3:45',
        'is_transcoded': False,
        'tags': {'title': 'Test Song', 'artist': 'Test Artist'}
    }
    db.insert_media(item)

    all_media = db.get_all_media()
    assert len(all_media) == 1
    assert all_media[0]['name'] == 'test_song.mp3'
    assert all_media[0]['tags']['title'] == 'Test Song'


def test_clear_media(temp_db):
    item = {
        'name': 'test_song.mp3',
        'path': '/path/to/test_song.mp3',
        'type': 'mp3',
        'duration': '3:45',
        'is_transcoded': False,
        'tags': {'title': 'Test Song'}
    }
    db.insert_media(item)
    db.clear_media()
    assert len(db.get_all_media()) == 0


def test_update_tags(temp_db):
    item = {
        'name': 'test_song.mp3',
        'path': '/path/to/test_song.mp3',
        'type': 'mp3',
        'duration': '3:45',
        'is_transcoded': False,
        'tags': {'title': 'Old Title'}
    }
    db.insert_media(item)

    new_tags = {'title': 'New Title'}
    db.update_media_tags('test_song.mp3', new_tags)

    all_media = db.get_all_media()
    assert all_media[0]['tags']['title'] == 'New Title'


# --- v1.3.4 dedicated tags table tests ---

def test_tags_stored_in_dedicated_table(temp_db):
    """Tags are written to the dedicated 'tags' table on insert."""
    import sqlite3 as _sqlite3
    item = {
        'name': 'song_with_tags.mp3',
        'path': '/path/song_with_tags.mp3',
        'type': 'mp3',
        'duration': '4:00',
        'is_transcoded': False,
        'tags': {'title': 'My Song', 'artist': 'Some Artist', 'year': '2024'}
    }
    db.insert_media(item)

    conn = _sqlite3.connect(db.DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT key, value FROM tags t JOIN media m ON m.id = t.media_id WHERE m.name = ?",
        ('song_with_tags.mp3',)
    )
    rows = {k: v for k, v in cursor.fetchall()}
    conn.close()

    assert rows.get('title') == 'My Song'
    assert rows.get('artist') == 'Some Artist'
    assert rows.get('year') == '2024'


def test_get_media_tags(temp_db):
    """get_media_tags returns the correct dict for a named item."""
    item = {
        'name': 'lookup_song.mp3',
        'path': '/path/lookup_song.mp3',
        'type': 'mp3',
        'duration': '2:30',
        'is_transcoded': False,
        'tags': {'title': 'Lookup Song', 'album': 'Test Album'}
    }
    db.insert_media(item)

    tags = db.get_media_tags('lookup_song.mp3')
    assert tags['title'] == 'Lookup Song'
    assert tags['album'] == 'Test Album'


def test_get_media_tags_missing(temp_db):
    """get_media_tags returns empty dict for unknown media name."""
    assert db.get_media_tags('nonexistent.mp3') == {}


def test_get_tags_by_key(temp_db):
    """get_tags_by_key returns all media sharing a tag key."""
    for i in range(3):
        db.insert_media({
            'name': f'song_{i}.mp3',
            'path': f'/path/song_{i}.mp3',
            'type': 'mp3',
            'duration': '3:00',
            'is_transcoded': False,
            'tags': {'artist': 'Same Artist', 'track': str(i + 1)}
        })

    results = db.get_tags_by_key('artist')
    assert len(results) == 3
    assert all(r['value'] == 'Same Artist' for r in results)
    names = {r['name'] for r in results}
    assert names == {'song_0.mp3', 'song_1.mp3', 'song_2.mp3'}


def test_get_tags_by_key_empty(temp_db):
    """get_tags_by_key returns empty list when no media has the key."""
    assert db.get_tags_by_key('nonexistent_key') == []


def test_update_tags_updates_dedicated_table(temp_db):
    """update_media_tags writes updated tags to the dedicated tags table."""
    import sqlite3 as _sqlite3
    item = {
        'name': 'editable.mp3',
        'path': '/path/editable.mp3',
        'type': 'mp3',
        'duration': '1:00',
        'is_transcoded': False,
        'tags': {'title': 'Before'}
    }
    db.insert_media(item)
    db.update_media_tags('editable.mp3', {'title': 'After', 'genre': 'Pop'})

    conn = _sqlite3.connect(db.DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT key, value FROM tags t JOIN media m ON m.id = t.media_id WHERE m.name = ?",
        ('editable.mp3',)
    )
    rows = {k: v for k, v in cursor.fetchall()}
    conn.close()

    assert rows.get('title') == 'After'
    assert rows.get('genre') == 'Pop'
    assert 'Before' not in rows.values()


def test_migration_from_json_blob(temp_db):
    """init_db migrates legacy JSON blob tags into the dedicated tags table."""
    import sqlite3 as _sqlite3
    import json as _json

    # Insert a row manually with a JSON tags blob but no tags-table entries
    conn = _sqlite3.connect(db.DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO media (name, path, type, duration, is_transcoded, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ('legacy.mp3', '/path/legacy.mp3', 'mp3', '2:00', 0,
          _json.dumps({'title': 'Legacy', 'artist': 'Old Artist'})))
    conn.commit()
    conn.close()

    # Re-run init_db to trigger migration
    db.init_db()

    conn = _sqlite3.connect(db.DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT key, value FROM tags t JOIN media m ON m.id = t.media_id WHERE m.name = ?",
        ('legacy.mp3',)
    )
    rows = {k: v for k, v in cursor.fetchall()}
    conn.close()

    assert rows.get('title') == 'Legacy'
    assert rows.get('artist') == 'Old Artist'
