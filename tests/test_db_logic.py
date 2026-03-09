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


# ===========================================================================
# v1.3.7 Tests – media_type / subtype / identifiers / disc / titles / covers
# ===========================================================================

# ---------------------------------------------------------------------------
# Step 17: media_type and subtype stored on insert
# ---------------------------------------------------------------------------

def test_insert_release_media_type_and_subtype(temp_db):
    rid = db.insert_release('Kind of Blue', release_type='Music', year=1959,
                             media_type='Audio', subtype='Album')
    r = db.get_release(rid)
    assert r['media_type'] == 'Audio'
    assert r['subtype'] == 'Album'


def test_insert_release_derives_media_type_from_release_type(temp_db):
    cases = [('Music', 'Audio'), ('Film', 'Video'), ('EBook', 'Document')]
    for rtype, expected in cases:
        rid = db.insert_release(f'Test {rtype}', release_type=rtype)
        assert db.get_release(rid)['media_type'] == expected, \
            f"Expected {expected} for release_type={rtype!r}"


def test_insert_release_audio_subtypes(temp_db):
    for sub in ['Album', 'Compilation', 'Audiobook', 'Classical', 'Soundtrack',
                'Single', 'EP', 'Live']:
        rid = db.insert_release(f'{sub} release', media_type='Audio', subtype=sub)
        assert db.get_release(rid)['subtype'] == sub


def test_insert_release_video_subtypes(temp_db):
    for sub in ['Film', 'Series', 'Documentary', 'Trailer', 'BonusContent', 'Short']:
        rid = db.insert_release(f'{sub} release', release_type='Film',
                                 media_type='Video', subtype=sub)
        r = db.get_release(rid)
        assert r['media_type'] == 'Video' and r['subtype'] == sub


def test_insert_release_document_subtype(temp_db):
    rid = db.insert_release('Clean Code', release_type='EBook',
                             media_type='Document', subtype='EBook', year=2008)
    r = db.get_release(rid)
    assert r['media_type'] == 'Document' and r['subtype'] == 'EBook'


# ---------------------------------------------------------------------------
# Step 18: Video-specific fields (video_standard, region, container_type, …)
# ---------------------------------------------------------------------------

def test_video_pal_de_release(temp_db):
    rid = db.insert_release('Der Pate', release_type='Film', year=1972,
                             media_type='Video', subtype='Film',
                             video_standard='PAL', region='DE',
                             container_type='PAL DVD', disc_format='ISO',
                             total_discs=2)
    r = db.get_release(rid)
    assert r['video_standard'] == 'PAL'
    assert r['region'] == 'DE'
    assert r['container_type'] == 'PAL DVD'
    assert r['disc_format'] == 'ISO'
    assert r['total_discs'] == 2


def test_video_ntsc_us_release(temp_db):
    rid = db.insert_release('Blade Runner', release_type='Film', year=1982,
                             media_type='Video', subtype='Film',
                             video_standard='NTSC', region='US',
                             container_type='NTSC DVD', disc_format='ISO')
    r = db.get_release(rid)
    assert r['video_standard'] == 'NTSC'
    assert r['region'] == 'US'


def test_bluray_release(temp_db):
    rid = db.insert_release('Dune', release_type='Film', year=2021,
                             media_type='Video', subtype='Film',
                             container_type='Blu-ray', disc_format='ISO',
                             total_discs=3)
    r = db.get_release(rid)
    assert r['container_type'] == 'Blu-ray'
    assert r['total_discs'] == 3


def test_video_standard_defaults_none(temp_db):
    rid = db.insert_release('Basic Release', media_type='Audio', subtype='Album')
    r = db.get_release(rid)
    assert r['video_standard'] is None
    assert r['region'] is None


# ---------------------------------------------------------------------------
# Step 19: parent_release_id for bonus content
# ---------------------------------------------------------------------------

def test_parent_release_id(temp_db):
    parent = db.insert_release('Dune', media_type='Video', subtype='Film', year=2021)
    bonus  = db.insert_release('Dune – Behind the Scenes', media_type='Video',
                                subtype='BonusContent', parent_release_id=parent)
    r = db.get_release(bonus)
    assert r['parent_release_id'] == parent
    assert r['subtype'] == 'BonusContent'


def test_parent_release_id_default_none(temp_db):
    rid = db.insert_release('Normal Album', media_type='Audio', subtype='Album')
    assert db.get_release(rid)['parent_release_id'] is None


# ---------------------------------------------------------------------------
# Step 20: Multi-disc releases (disc_number, disc_type, disc_label)
# ---------------------------------------------------------------------------

def _film_item(name, ext='iso'):
    return {
        'name': name, 'path': f'/films/{name}', 'type': ext,
        'duration': '2:00:00', 'is_transcoded': False, 'tags': {},
    }


def test_multi_disc_release(temp_db):
    """A film release can span Disc 1 (Film), Disc 2 (Bonus), Disc 3 (Soundtrack)."""
    rid = db.insert_release('Blade Runner 2049', media_type='Video', subtype='Film',
                             total_discs=3)
    for fname, disc, dtype, label in [
        ('br2049_d1.iso', 1, 'Film',       'Disc 1 – Film'),
        ('br2049_d2.iso', 2, 'Bonus',      'Disc 2 – Bonus'),
        ('br2049_d3.flac', 3, 'Soundtrack', 'Disc 3 – Soundtrack CD'),
    ]:
        db.insert_media(_film_item(fname, fname.split('.')[-1]))
        db.assign_item_to_release(rid, fname, position=disc,
                                   disc_number=disc, disc_type=dtype, disc_label=label)

    items = db.get_release_items(rid)
    assert len(items) == 3
    disc1 = next(i for i in items if i['disc_number'] == 1)
    assert disc1['disc_type'] == 'Film'
    assert disc1['disc_label'] == 'Disc 1 – Film'
    disc3 = next(i for i in items if i['disc_number'] == 3)
    assert disc3['disc_type'] == 'Soundtrack'


def test_multi_disc_ordering(temp_db):
    """Items are ordered by disc_number then position."""
    rid = db.insert_release('Film', media_type='Video')
    for disc in [3, 1, 2]:
        name = f'disc{disc}.iso'
        db.insert_media(_film_item(name))
        db.assign_item_to_release(rid, name, position=1, disc_number=disc)
    items = db.get_release_items(rid)
    assert [i['disc_number'] for i in items] == [1, 2, 3]


def test_document_multi_format(temp_db):
    """An EBook purchase can have PDF, EPUB and MOBI as separate items (Disc=format)."""
    rid = db.insert_release('Clean Code', media_type='Document', subtype='EBook')
    for fmt, pos in [('pdf', 1), ('epub', 2), ('mobi', 3)]:
        name = f'clean_code.{fmt}'
        db.insert_media({
            'name': name, 'path': f'/books/{name}', 'type': fmt,
            'duration': '', 'is_transcoded': False, 'tags': {},
        })
        db.assign_item_to_release(rid, name, position=pos,
                                   disc_type='Document', disc_label=fmt.upper())
    items = db.get_release_items(rid)
    assert len(items) == 3
    labels = [i['disc_label'] for i in items]
    assert 'PDF' in labels and 'EPUB' in labels


# ---------------------------------------------------------------------------
# Step 21: release_identifiers (ISBN, UPC, Barcode, IMDb, …)
# ---------------------------------------------------------------------------

def test_add_and_get_identifiers(temp_db):
    rid = db.insert_release('Clean Code', media_type='Document', subtype='EBook')
    db.add_release_identifier(rid, 'ISBN-13', '9780132350884')
    db.add_release_identifier(rid, 'ASIN',    'B001GSTOAM')

    ids = db.get_release_identifiers(rid)
    assert len(ids) == 2
    imap = {i['id_type']: i['value'] for i in ids}
    assert imap['ISBN-13'] == '9780132350884'


def test_barcode_as_identifier(temp_db):
    rid = db.insert_release('The Dark Knight', media_type='Video', subtype='Film')
    db.add_release_identifier(rid, 'Barcode', '5051429701172')
    db.add_release_identifier(rid, 'IMDb',    'tt0468569')
    ids = db.get_release_identifiers(rid)
    types = [i['id_type'] for i in ids]
    assert 'Barcode' in types and 'IMDb' in types


def test_duplicate_identifier_returns_false(temp_db):
    rid = db.insert_release('Album', media_type='Audio')
    db.add_release_identifier(rid, 'UPC', '123456789012')
    assert db.add_release_identifier(rid, 'UPC', '123456789012') is False
    assert len(db.get_release_identifiers(rid)) == 1


def test_multiple_isbn_editions(temp_db):
    rid = db.insert_release('Lord of the Rings', media_type='Document', subtype='EBook')
    for isbn in ['9780618640157', '9780544003415']:
        db.add_release_identifier(rid, 'ISBN-13', isbn)
    vals = [i['value'] for i in db.get_release_identifiers(rid) if i['id_type'] == 'ISBN-13']
    assert len(vals) == 2


def test_remove_identifier(temp_db):
    rid = db.insert_release('Book', media_type='Document')
    db.add_release_identifier(rid, 'ISBN-13', '9780132350884')
    db.add_release_identifier(rid, 'ASIN', 'B001GSTOAM')
    assert db.remove_release_identifier(rid, 'ASIN', 'B001GSTOAM') is True
    ids = db.get_release_identifiers(rid)
    assert len(ids) == 1 and ids[0]['id_type'] == 'ISBN-13'


def test_get_releases_by_identifier(temp_db):
    r1 = db.insert_release('Album 1', media_type='Audio')
    r2 = db.insert_release('Album 2', media_type='Audio')
    db.add_release_identifier(r1, 'MusicBrainz', 'mb-001')
    db.add_release_identifier(r2, 'MusicBrainz', 'mb-001')
    results = db.get_releases_by_identifier('MusicBrainz', 'mb-001')
    assert len(results) == 2


def test_get_release_includes_identifiers(temp_db):
    rid = db.insert_release('Dune', media_type='Document', subtype='EBook')
    db.add_release_identifier(rid, 'ISBN-13', '9780441013593')
    r = db.get_release(rid)
    assert 'identifiers' in r
    assert r['identifiers'][0]['value'] == '9780441013593'


def test_delete_release_removes_identifiers(temp_db):
    rid = db.insert_release('Book', media_type='Document')
    db.add_release_identifier(rid, 'ISBN-13', '9780000000000')
    db.delete_release(rid)
    assert db.get_release_identifiers(rid) == []


# ---------------------------------------------------------------------------
# Step 22: release_subtypes (user-editable, seeded with defaults)
# ---------------------------------------------------------------------------

def test_default_subtypes_seeded(temp_db):
    audio = db.get_release_subtypes('Audio')
    names = [s['name'] for s in audio]
    assert 'Album' in names and 'Audiobook' in names and 'EP' in names


def test_default_video_subtypes_seeded(temp_db):
    video = db.get_release_subtypes('Video')
    names = [s['name'] for s in video]
    assert 'Film' in names and 'Series' in names and 'BonusContent' in names


def test_add_custom_subtype(temp_db):
    assert db.add_release_subtype('Video', 'Extended Cut', sort_order=15) is True
    video = db.get_release_subtypes('Video')
    names = [s['name'] for s in video]
    assert 'Extended Cut' in names


def test_add_duplicate_subtype_returns_false(temp_db):
    assert db.add_release_subtype('Audio', 'Album') is False


def test_remove_subtype(temp_db):
    db.add_release_subtype('Video', 'TestType', sort_order=99)
    assert db.remove_release_subtype('Video', 'TestType') is True
    names = [s['name'] for s in db.get_release_subtypes('Video')]
    assert 'TestType' not in names


def test_get_all_subtypes(temp_db):
    all_subs = db.get_release_subtypes()
    media_types = {s['media_type'] for s in all_subs}
    assert {'Audio', 'Video', 'Document', 'Image'}.issubset(media_types)


# ---------------------------------------------------------------------------
# Step 23: release_titles (multi-language)
# ---------------------------------------------------------------------------

def test_set_and_get_release_titles(temp_db):
    rid = db.insert_release('The Godfather', media_type='Video', subtype='Film')
    db.set_release_title(rid, 'en', 'The Godfather')
    db.set_release_title(rid, 'de', 'Der Pate')
    db.set_release_title(rid, 'original', 'The Godfather')

    titles = db.get_release_titles(rid)
    assert titles['de'] == 'Der Pate'
    assert titles['en'] == 'The Godfather'
    assert titles['original'] == 'The Godfather'


def test_replace_release_title(temp_db):
    rid = db.insert_release('Test', media_type='Video')
    db.set_release_title(rid, 'de', 'Alt')
    db.set_release_title(rid, 'de', 'Neu')
    assert db.get_release_titles(rid)['de'] == 'Neu'


def test_remove_release_title(temp_db):
    rid = db.insert_release('Film', media_type='Video')
    db.set_release_title(rid, 'en', 'Film')
    db.set_release_title(rid, 'de', 'Film DE')
    assert db.remove_release_title(rid, 'de') is True
    assert 'de' not in db.get_release_titles(rid)
    assert 'en' in db.get_release_titles(rid)


def test_get_release_includes_titles(temp_db):
    rid = db.insert_release('Fight Club', media_type='Video', subtype='Film')
    db.set_release_title(rid, 'en', 'Fight Club')
    db.set_release_title(rid, 'de', 'Fight Club')
    r = db.get_release(rid)
    assert 'titles' in r
    assert r['titles']['en'] == 'Fight Club'


def test_delete_release_removes_titles(temp_db):
    rid = db.insert_release('Film', media_type='Video')
    db.set_release_title(rid, 'en', 'Film')
    db.delete_release(rid)
    assert db.get_release_titles(rid) == {}


# ---------------------------------------------------------------------------
# Step 24: release_covers
# ---------------------------------------------------------------------------

def test_add_and_get_cover(temp_db):
    rid = db.insert_release('Thriller', media_type='Audio', subtype='Album')
    cid = db.add_release_cover(release_id=rid, cover_type='front',
                                path='/covers/thriller_front.jpg',
                                source='local', width=600, height=600)
    assert isinstance(cid, int) and cid > 0

    covers = db.get_release_covers(release_id=rid)
    assert len(covers) == 1
    assert covers[0]['cover_type'] == 'front'
    assert covers[0]['width'] == 600


def test_multiple_covers_per_release(temp_db):
    rid = db.insert_release('Album', media_type='Audio')
    db.add_release_cover(release_id=rid, cover_type='front',
                          url='https://example.com/front.jpg', source='musicbrainz')
    db.add_release_cover(release_id=rid, cover_type='back',
                          url='https://example.com/back.jpg', source='musicbrainz')
    covers = db.get_release_covers(release_id=rid)
    assert len(covers) == 2
    types = {c['cover_type'] for c in covers}
    assert 'front' in types and 'back' in types


def test_cover_from_imdb(temp_db):
    rid = db.insert_release('The Godfather', media_type='Video', subtype='Film')
    db.add_release_cover(release_id=rid, cover_type='poster',
                          url='https://m.media-amazon.com/images/M/MV5BMWMwM.jpg',
                          source='imdb')
    covers = db.get_release_covers(release_id=rid)
    assert covers[0]['source'] == 'imdb'


def test_remove_cover(temp_db):
    rid = db.insert_release('Album', media_type='Audio')
    cid = db.add_release_cover(release_id=rid, cover_type='front',
                                path='/covers/front.jpg')
    assert db.remove_release_cover(cid) is True
    assert db.get_release_covers(release_id=rid) == []


def test_delete_release_removes_covers(temp_db):
    rid = db.insert_release('Album', media_type='Audio')
    db.add_release_cover(release_id=rid, cover_type='front', path='/c/f.jpg')
    db.delete_release(rid)
    assert db.get_release_covers(release_id=rid) == []


# ---------------------------------------------------------------------------
# Step 25: scraper_sources (plugin registry)
# ---------------------------------------------------------------------------

def test_default_scraper_sources_seeded(temp_db):
    sources = db.get_scraper_sources()
    names = [s['name'] for s in sources]
    assert 'IMDb' in names
    assert 'TMDb' in names
    assert 'MusicBrainz' in names
    assert 'OpenLibrary' in names


def test_scraper_sources_filter_by_media_type(temp_db):
    video = db.get_scraper_sources(media_type='Video')
    names = [s['name'] for s in video]
    assert 'IMDb' in names
    assert 'MusicBrainz' not in names


def test_register_custom_scraper_source(temp_db):
    sid = db.register_scraper_source('MyIMDbPlugin', media_type='Video',
                                      base_url='https://api.example.com',
                                      priority=5)
    assert isinstance(sid, int)
    sources = db.get_scraper_sources(media_type='Video')
    names = [s['name'] for s in sources]
    assert 'MyIMDbPlugin' in names


def test_disable_scraper_source(temp_db):
    assert db.set_scraper_source_enabled('IMDb', False) is True
    enabled = db.get_scraper_sources(media_type='Video', enabled_only=True)
    names = [s['name'] for s in enabled]
    assert 'IMDb' not in names


def test_enable_scraper_source(temp_db):
    db.set_scraper_source_enabled('IMDb', False)
    db.set_scraper_source_enabled('IMDb', True)
    enabled = db.get_scraper_sources(media_type='Video', enabled_only=True)
    names = [s['name'] for s in enabled]
    assert 'IMDb' in names


# ---------------------------------------------------------------------------
# Step 26: get_all_releases and search_releases with new filters
# ---------------------------------------------------------------------------

def test_get_all_releases_filter_by_media_type(temp_db):
    db.insert_release('Album A', media_type='Audio', subtype='Album')
    db.insert_release('Film B',  media_type='Video', subtype='Film')
    assert len(db.get_all_releases(media_type='Audio')) == 1
    assert len(db.get_all_releases(media_type='Video')) == 1


def test_get_all_releases_filter_by_subtype(temp_db):
    db.insert_release('Album A', media_type='Audio', subtype='Album')
    db.insert_release('Comp B',  media_type='Audio', subtype='Compilation')
    assert len(db.get_all_releases(subtype='Album')) == 1
    assert len(db.get_all_releases(subtype='Compilation')) == 1


def test_search_releases_media_type_filter(temp_db):
    db.insert_release('Dark Shadows', media_type='Video', subtype='Film')
    db.insert_release('Dark Side',    media_type='Audio', subtype='Album')
    video = db.search_releases('Dark', media_type='Video')
    assert len(video) == 1 and video[0]['title'] == 'Dark Shadows'


def test_search_releases_subtype_filter(temp_db):
    db.insert_release('Breaking Bad',    media_type='Video', subtype='Series')
    db.insert_release('Breaking Point',  media_type='Video', subtype='Film')
    series = db.search_releases('Breaking', subtype='Series')
    assert len(series) == 1 and series[0]['subtype'] == 'Series'


# ---------------------------------------------------------------------------
# Step 27: Migration – v1.3.5 database upgraded automatically
# ---------------------------------------------------------------------------

def test_migration_v135_to_v137(tmp_path):
    """
    A v1.3.5 database without the new columns is upgraded transparently by
    init_db(): new columns appear, media_type is populated from type, and
    release_subtypes / scraper_sources tables are created and seeded.
    """
    import sqlite3 as _sqlite3

    legacy_db = str(tmp_path / "legacy.db")
    original_db = db.DB_FILENAME

    conn = _sqlite3.connect(legacy_db)
    conn.execute("""
        CREATE TABLE media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE, path TEXT, type TEXT, duration TEXT,
            category TEXT, is_transcoded BOOLEAN, transcoded_format TEXT,
            tags TEXT, extension TEXT, container TEXT, tag_type TEXT, codec TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE releases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'Music',
            year INTEGER, cut TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            scraper_data TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE release_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id INTEGER NOT NULL, media_id INTEGER NOT NULL,
            position INTEGER, UNIQUE(media_id)
        )
    """)
    conn.execute("""
        CREATE TABLE media_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT,
            UNIQUE(media_id, key)
        )
    """)
    conn.execute("""INSERT INTO releases (title, type) VALUES ('Legacy Album', 'Music')""")
    conn.execute("""INSERT INTO releases (title, type) VALUES ('Legacy Film', 'Film')""")
    conn.commit()
    conn.close()

    db.DB_FILENAME = legacy_db
    try:
        db.init_db()

        releases = {r['title']: r for r in db.get_all_releases()}
        assert releases['Legacy Album']['media_type'] == 'Audio'
        assert releases['Legacy Film']['media_type'] == 'Video'

        # New tables must exist and be seeded
        audio_subs = db.get_release_subtypes('Audio')
        assert any(s['name'] == 'Album' for s in audio_subs)

        scrapers = db.get_scraper_sources()
        assert any(s['name'] == 'IMDb' for s in scrapers)
    finally:
        db.DB_FILENAME = original_db
