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


# ---------------------------------------------------------------------------
# Step 1: Basic insert / retrieve
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Step 2: media_tags table populated on insert (v1.3.4)
# ---------------------------------------------------------------------------

def test_media_tags_table_populated_on_insert(temp_db):
    """Tags written to media_tags table when a new media item is inserted."""
    item = {
        'name': 'song.mp3',
        'path': '/music/song.mp3',
        'type': 'mp3',
        'duration': '4:00',
        'is_transcoded': False,
        'tags': {'title': 'Hello', 'artist': 'World', 'genre': 'Rock'}
    }
    db.insert_media(item)

    keys = db.get_all_tag_keys()
    assert 'title' in keys
    assert 'artist' in keys
    assert 'genre' in keys


def test_get_tag_value(temp_db):
    """get_tag_value returns the correct value for a given media item and key."""
    item = {
        'name': 'song.mp3',
        'path': '/music/song.mp3',
        'type': 'mp3',
        'duration': '4:00',
        'is_transcoded': False,
        'tags': {'title': 'Hello', 'artist': 'World'}
    }
    db.insert_media(item)

    assert db.get_tag_value('song.mp3', 'title') == 'Hello'
    assert db.get_tag_value('song.mp3', 'artist') == 'World'
    assert db.get_tag_value('song.mp3', 'missing_key') is None


# ---------------------------------------------------------------------------
# Step 3: Tag search / filtering (v1.3.4)
# ---------------------------------------------------------------------------

def test_search_media_by_tag(temp_db):
    """search_media_by_tag returns media items matching a tag key-value pair."""
    for name, artist in [('a.mp3', 'Queen'), ('b.mp3', 'Radiohead'), ('c.mp3', 'Queen')]:
        db.insert_media({
            'name': name,
            'path': f'/music/{name}',
            'type': 'mp3',
            'duration': '3:00',
            'is_transcoded': False,
            'tags': {'artist': artist}
        })

    results = db.search_media_by_tag('artist', 'Queen')
    assert sorted(results) == ['a.mp3', 'c.mp3']

    results = db.search_media_by_tag('artist', 'Radiohead')
    assert results == ['b.mp3']

    results = db.search_media_by_tag('artist', 'Unknown')
    assert results == []


def test_search_media_by_tag_partial_match(temp_db):
    """search_media_by_tag supports case-insensitive substring matching."""
    db.insert_media({
        'name': 'track.mp3',
        'path': '/music/track.mp3',
        'type': 'mp3',
        'duration': '3:00',
        'is_transcoded': False,
        'tags': {'genre': 'Alternative Rock'}
    })

    results = db.search_media_by_tag('genre', 'Rock')
    assert 'track.mp3' in results


# ---------------------------------------------------------------------------
# Step 4: Tag key/value enumeration (v1.3.4)
# ---------------------------------------------------------------------------

def test_get_all_tag_keys(temp_db):
    """get_all_tag_keys returns a sorted, unique list of all tag keys."""
    for name, tags in [
        ('a.mp3', {'title': 'A', 'artist': 'X'}),
        ('b.mp3', {'title': 'B', 'genre': 'Pop'}),
    ]:
        db.insert_media({
            'name': name,
            'path': f'/music/{name}',
            'type': 'mp3',
            'duration': '3:00',
            'is_transcoded': False,
            'tags': tags
        })

    keys = db.get_all_tag_keys()
    assert 'artist' in keys
    assert 'genre' in keys
    assert 'title' in keys
    assert keys == sorted(set(keys))  # sorted and unique


def test_get_tag_values(temp_db):
    """get_tag_values returns all distinct values for a given key."""
    for name, genre in [('a.mp3', 'Rock'), ('b.mp3', 'Pop'), ('c.mp3', 'Rock')]:
        db.insert_media({
            'name': name,
            'path': f'/music/{name}',
            'type': 'mp3',
            'duration': '3:00',
            'is_transcoded': False,
            'tags': {'genre': genre}
        })

    values = db.get_tag_values('genre')
    assert 'Rock' in values
    assert 'Pop' in values
    assert len(values) == 2  # distinct values only


# ---------------------------------------------------------------------------
# Step 5: Tags kept in sync when updating (v1.3.4)
# ---------------------------------------------------------------------------

def test_update_tags_syncs_media_tags_table(temp_db):
    """update_media_tags must keep media_tags table in sync."""
    item = {
        'name': 'song.mp3',
        'path': '/music/song.mp3',
        'type': 'mp3',
        'duration': '3:00',
        'is_transcoded': False,
        'tags': {'title': 'Old', 'artist': 'Old Artist'}
    }
    db.insert_media(item)

    db.update_media_tags('song.mp3', {'title': 'New', 'genre': 'Jazz'})

    assert db.get_tag_value('song.mp3', 'title') == 'New'
    assert db.get_tag_value('song.mp3', 'genre') == 'Jazz'
    # Old key that was not included in the update must be gone
    assert db.get_tag_value('song.mp3', 'artist') is None


# ---------------------------------------------------------------------------
# Step 6: media_tags cleaned up on delete (v1.3.4)
# ---------------------------------------------------------------------------

def test_delete_media_removes_tags(temp_db):
    """Deleting a media item must also remove its media_tags rows."""
    item = {
        'name': 'song.mp3',
        'path': '/music/song.mp3',
        'type': 'mp3',
        'duration': '3:00',
        'is_transcoded': False,
        'tags': {'title': 'Hello', 'artist': 'World'}
    }
    db.insert_media(item)
    db.delete_media('song.mp3')

    assert db.get_all_tag_keys() == []
    assert db.search_media_by_tag('title', 'Hello') == []


# ---------------------------------------------------------------------------
# Step 7: Migration from existing JSON tags (v1.3.4)
# ---------------------------------------------------------------------------

def test_migration_populates_media_tags(tmp_path):
    """
    When init_db() is called on a pre-v1.3.4 database that has tags stored
    only as a JSON blob, the migration must populate the media_tags table.
    """
    import sqlite3 as _sqlite3
    import json as _json

    legacy_db = str(tmp_path / "legacy.db")
    original_db = db.DB_FILENAME

    # Build a minimal pre-v1.3.4 database manually (no media_tags table)
    conn = _sqlite3.connect(legacy_db)
    conn.execute("""
        CREATE TABLE media (
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
    conn.execute("""
        INSERT INTO media (name, path, type, duration, is_transcoded, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ('old_song.mp3', '/music/old_song.mp3', 'mp3', '3:00', 0,
          _json.dumps({'title': 'Legacy Title', 'artist': 'Legacy Artist'})))
    conn.commit()
    conn.close()

    # Now let init_db() upgrade the database
    db.DB_FILENAME = legacy_db
    try:
        db.init_db()

        assert db.get_tag_value('old_song.mp3', 'title') == 'Legacy Title'
        assert db.get_tag_value('old_song.mp3', 'artist') == 'Legacy Artist'
        assert 'title' in db.get_all_tag_keys()
    finally:
        db.DB_FILENAME = original_db


# ---------------------------------------------------------------------------
# Step 8: get_db_stats includes tag entry count (v1.3.4)
# ---------------------------------------------------------------------------

def test_get_db_stats_includes_tag_count(temp_db):
    """get_db_stats must report total_tag_entries since v1.3.4."""
    item = {
        'name': 'song.mp3',
        'path': '/music/song.mp3',
        'type': 'mp3',
        'duration': '3:00',
        'is_transcoded': False,
        'tags': {'title': 'T', 'artist': 'A', 'genre': 'G'}
    }
    db.insert_media(item)

    stats = db.get_db_stats()
    assert 'total_tag_entries' in stats
    assert stats['total_tag_entries'] == 3
