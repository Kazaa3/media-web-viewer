#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import sqlite3
import json
import os
from pathlib import Path
from src.core.db import init_db, insert_media, get_all_media, clear_media, DB_FILENAME, get_known_media_names

class TestDBOperations:
    """
    Comprehensive tests for database operations and schema consistency.
    """

    def setup_method(self):
        """Ensure a clean database for each test."""
        if os.path.exists(DB_FILENAME):
            os.remove(DB_FILENAME)
        init_db()

    def test_schema_columns(self):
        """Verify that all expected columns are present in the media table."""
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(media)")
        columns = {row[1] for row in cursor.fetchall()}
        
        expected = {
            'id', 'name', 'path', 'type', 'duration', 'category', 
            'is_transcoded', 'transcoded_format', 'tags', 
            'extension', 'container', 'tag_type', 'codec', 'has_artwork'
        }
        for col in expected:
            assert col in columns, f"Column {col} missing from schema"
        conn.close()

    def test_insert_and_retrieve(self):
        """Test full cycle of inserting an item and retrieving it."""
        item = {
            'name': 'test_song.mp3',
            'path': '/media/music/test_song.mp3',
            'type': 'Audio',
            'duration': '03:45',
            'category': 'Album',
            'is_transcoded': False,
            'tags': {'title': 'Test Song', 'artist': 'Test Artist'},
            'extension': 'mp3',
            'container': 'mp3',
            'tag_type': 'id3v2',
            'codec': 'mpeg layer 3',
            'has_artwork': True
        }
        
        insert_media(item)
        
        library = get_all_media()
        assert len(library) == 1
        fetched = library[0]
        
        assert fetched['name'] == item['name']
        assert fetched['category'] == 'Album'
        assert fetched['has_artwork'] is True
        assert fetched['tags']['title'] == 'Test Song'
        assert fetched['codec'] == item['codec']

    def test_unique_constraint(self):
        """Verify that duplicate names are handled (ignored via insert_media)."""
        item = {
            'name': 'unique.mp4',
            'path': '/path/1',
            'type': 'Video',
            'duration': '10',
            'is_transcoded': False,
            'tags': {}
        }
        insert_media(item)
        # Should NOT raise error, but ignore
        insert_media(item)
        
        assert len(get_all_media()) == 1

    def test_clear_and_known_names(self):
        """Test clearing the database and checking known names."""
        insert_media({
            'name': 'item1', 'path': 'p1', 'type': 'T', 'duration': '1', 
            'is_transcoded': False, 'tags': {}
        })
        
        names = get_known_media_names()
        assert 'item1' in names
        
        clear_media()
        assert len(get_all_media()) == 0
        assert len(get_known_media_names()) == 0

if __name__ == "__main__":
    pytest.main([__file__])
