#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Unit / Database / CRUD
# Eingabewerte: src/core/db.py, SQLite
# Ausgabewerte: Validierung CRUD-Operationen und Tabellenstruktur
# Testdateien: src/core/db.py
# ERWEITERUNGEN (TODO): [ ] Mocking für verschiedene DB-Versionen, [ ] Performance-Tests
# KOMMENTAR: Testet die grundlegenden Datenbankoperationen.
# VERWENDUNG: pytest tests/unit/core/test_db_crud.py

import pytest
import sqlite3
from src.core import db

def test_db_create_table():
    """
    Testet das Anlegen einer Tabelle in der Datenbank. / Tests creation of a table in the database.

    Returns:
        None
    """
    db.init_db()
    db_path = db.get_active_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='media'")
    assert cursor.fetchone() is not None
    conn.close()

def test_db_insert_and_read():
    """
    Testet das Einfügen und Auslesen eines Datensatzes. / Tests inserting and reading a record.

    Returns:
        None
    """
    test_item = {
        'name': 'test_audio_file.mp3',
        'path': '/test/path/test_audio_file.mp3',
        'type': 'audio',
        'duration': '180',
        'category': 'Music',
        'is_transcoded': False,
        'transcoded_format': None,
        'tags': {'artist': 'Test Artist', 'title': 'Test Title'},
        'extension': 'mp3',
        'container': 'MP3',
        'tag_type': 'ID3v2.4',
        'codec': 'mp3'
    }
    db.insert_media(test_item)
    known_names = db.get_known_media_names()
    assert test_item['name'] in known_names
    db.delete_media(test_item['name'])


def test_db_update_and_delete():
    """
    Testet das Aktualisieren und Löschen eines Datensatzes. / Tests updating and deleting a record.

    Returns:
        None
    """
    test_item = {
        'name': 'test_audio_file.mp3',
        'path': '/test/path/test_audio_file.mp3',
        'type': 'audio',
        'duration': '180',
        'category': 'Music',
        'is_transcoded': False,
        'transcoded_format': None,
        'tags': {'artist': 'Test Artist', 'title': 'Test Title'},
        'extension': 'mp3',
        'container': 'MP3',
        'tag_type': 'ID3v2.4',
        'codec': 'mp3'
    }
    db.insert_media(test_item)
    db.update_media_tags(test_item['name'], {'artist': 'Updated Artist'})
    all_media = db.get_all_media()
    updated_item = next((m for m in all_media if m['name'] == test_item['name']), None)
    assert updated_item is not None
    assert updated_item['tags'].get('artist') == 'Updated Artist'
    db.delete_media(test_item['name'])
    known_names = db.get_known_media_names()
    assert test_item['name'] not in known_names
