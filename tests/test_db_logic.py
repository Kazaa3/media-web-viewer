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


# ===========================================================================
# Release tests (v1.3.5)
# ===========================================================================

# ---------------------------------------------------------------------------
# Step 9: Create and retrieve releases
# ---------------------------------------------------------------------------

def test_insert_and_get_release(temp_db):
    """insert_release returns an id; get_release returns the record."""
    rid = db.insert_release('Dark Side of the Moon', release_type='Music', year=1973)
    assert isinstance(rid, int) and rid > 0

    r = db.get_release(rid)
    assert r is not None
    assert r['title'] == 'Dark Side of the Moon'
    assert r['type'] == 'Music'
    assert r['year'] == 1973
    assert r['status'] == 'pending'
    assert r['scraper_data'] is None


def test_get_release_unknown_id(temp_db):
    """get_release returns None for a non-existent id."""
    assert db.get_release(9999) is None


def test_insert_film_release_with_cut(temp_db):
    """Film releases store cut information."""
    rid = db.insert_release("Blade Runner", release_type='Film', year=1982,
                             cut="Director's Cut")
    r = db.get_release(rid)
    assert r['cut'] == "Director's Cut"
    assert r['type'] == 'Film'


# ---------------------------------------------------------------------------
# Step 10: scraper_data (JSON) round-trip
# ---------------------------------------------------------------------------

def test_update_release_scraper_data(temp_db):
    """update_release_scraper_data stores and deserialises the JSON blob."""
    rid = db.insert_release('Thriller', release_type='Music', year=1982)

    payload = {
        'musicbrainz_id': 'abc-123',
        'cover_art_url': 'https://example.com/cover.jpg',
        'genres': ['Pop', 'R&B'],
        'label': 'Epic Records',
    }
    db.update_release_scraper_data(rid, payload)

    r = db.get_release(rid)
    assert r['status'] == 'scraped'
    assert r['scraper_data']['musicbrainz_id'] == 'abc-123'
    assert r['scraper_data']['genres'] == ['Pop', 'R&B']


def test_update_release_status(temp_db):
    """update_release_status changes only the status field."""
    rid = db.insert_release('Test Album', release_type='Music')
    db.update_release_status(rid, 'verified')
    assert db.get_release(rid)['status'] == 'verified'


# ---------------------------------------------------------------------------
# Step 11: Assign items to a release
# ---------------------------------------------------------------------------

def _make_item(name, track=None):
    return {
        'name': name,
        'path': f'/music/{name}',
        'type': 'mp3',
        'duration': '3:30',
        'is_transcoded': False,
        'tags': {'title': name, 'track': str(track)} if track else {'title': name},
    }


def test_assign_item_to_release(temp_db):
    """Items can be assigned to a release with a track position."""
    rid = db.insert_release('Abbey Road', release_type='Music', year=1969)
    db.insert_media(_make_item('come_together.mp3', track=1))
    db.insert_media(_make_item('something.mp3', track=2))

    assert db.assign_item_to_release(rid, 'come_together.mp3', position=1)
    assert db.assign_item_to_release(rid, 'something.mp3', position=2)

    items = db.get_release_items(rid)
    assert len(items) == 2
    assert items[0]['name'] == 'come_together.mp3'
    assert items[0]['position'] == 1
    assert items[1]['name'] == 'something.mp3'
    assert items[1]['position'] == 2


def test_assign_nonexistent_item_returns_false(temp_db):
    """Assigning an unknown media name returns False."""
    rid = db.insert_release('Test', release_type='Music')
    assert db.assign_item_to_release(rid, 'ghost.mp3') is False


def test_get_item_release(temp_db):
    """get_item_release returns the release an item belongs to."""
    rid = db.insert_release('Kind of Blue', release_type='Music', year=1959)
    db.insert_media(_make_item('so_what.mp3'))
    db.assign_item_to_release(rid, 'so_what.mp3', position=1)

    r = db.get_item_release('so_what.mp3')
    assert r is not None
    assert r['title'] == 'Kind of Blue'


def test_get_item_release_unassigned(temp_db):
    """get_item_release returns None for an item that has no release."""
    db.insert_media(_make_item('no_release.mp3'))
    assert db.get_item_release('no_release.mp3') is None


# ---------------------------------------------------------------------------
# Step 12: Remove item from release
# ---------------------------------------------------------------------------

def test_remove_item_from_release(temp_db):
    """remove_item_from_release unlinks the item from its release."""
    rid = db.insert_release('Test Album', release_type='Music')
    db.insert_media(_make_item('track1.mp3'))
    db.assign_item_to_release(rid, 'track1.mp3', position=1)

    assert db.remove_item_from_release('track1.mp3') is True
    assert db.get_item_release('track1.mp3') is None
    assert db.get_release_items(rid) == []


# ---------------------------------------------------------------------------
# Step 13: Delete release cascades to release_items
# ---------------------------------------------------------------------------

def test_delete_release_removes_items(temp_db):
    """Deleting a release removes its release_items rows."""
    rid = db.insert_release('Doomed Album', release_type='Music')
    db.insert_media(_make_item('song_a.mp3'))
    db.assign_item_to_release(rid, 'song_a.mp3', position=1)

    db.delete_release(rid)
    assert db.get_release(rid) is None
    assert db.get_item_release('song_a.mp3') is None
    # The media item itself must still exist
    media = db.get_all_media()
    assert any(m['name'] == 'song_a.mp3' for m in media)


# ---------------------------------------------------------------------------
# Step 14: get_all_releases with type/status filters
# ---------------------------------------------------------------------------

def test_get_all_releases_filter(temp_db):
    """get_all_releases can filter by type and status."""
    db.insert_release('Album A', release_type='Music')
    db.insert_release('Film B', release_type='Film', year=2020)
    rid_c = db.insert_release('Album C', release_type='Music')
    db.update_release_status(rid_c, 'verified')

    music = db.get_all_releases(release_type='Music')
    assert len(music) == 2

    films = db.get_all_releases(release_type='Film')
    assert len(films) == 1
    assert films[0]['title'] == 'Film B'

    verified = db.get_all_releases(status='verified')
    assert len(verified) == 1
    assert verified[0]['title'] == 'Album C'


# ---------------------------------------------------------------------------
# Step 15: Search releases by title
# ---------------------------------------------------------------------------

def test_search_releases(temp_db):
    """search_releases performs a substring match on release titles."""
    db.insert_release('The Dark Knight', release_type='Film', year=2008)
    db.insert_release('Dark Side of the Moon', release_type='Music')
    db.insert_release('Gladiator', release_type='Film', year=2000)

    results = db.search_releases('Dark')
    assert len(results) == 2

    results = db.search_releases('Dark', release_type='Film')
    assert len(results) == 1
    assert results[0]['title'] == 'The Dark Knight'

    results = db.search_releases('nonexistent')
    assert results == []


# ---------------------------------------------------------------------------
# Step 16: Film release – multiple ISO / MKV items
# ---------------------------------------------------------------------------

def test_film_release_multiple_formats(temp_db):
    """A film release can contain multiple file items (ISO, MKV, etc.)."""
    rid = db.insert_release('Dune', release_type='Film', year=2021,
                             cut='Theatrical Cut',
                             scraper_data={'tmdb_id': 438631})

    for fname, pos in [('dune.mkv', 1), ('dune_extras.mkv', 2), ('dune.iso', 3)]:
        db.insert_media({
            'name': fname,
            'path': f'/films/{fname}',
            'type': fname.split('.')[-1],
            'duration': '2:35:00',
            'is_transcoded': False,
            'tags': {},
        })
        db.assign_item_to_release(rid, fname, position=pos)

    r = db.get_release(rid)
    assert r['scraper_data']['tmdb_id'] == 438631
    assert r['cut'] == 'Theatrical Cut'

    items = db.get_release_items(rid)
    assert len(items) == 3
    assert items[0]['name'] == 'dune.mkv'
