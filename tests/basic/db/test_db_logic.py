# Kategorie: Database Test
# Eingabewerte: Media-Dictionaries, Dateipfade
# Ausgabewerte: Datenbank-Einträge
# Testdateien: Temporäre SQLite DB
# Kommentar: Prüft CRUD Operationen auf der Media-Datenbank.

import pytest
import sys
import os

import src.core.db as db

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
