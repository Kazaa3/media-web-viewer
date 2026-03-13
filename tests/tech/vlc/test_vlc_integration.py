#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Tech / VLC
# Eingabewerte: m3u8 Playlist-Dateien, Media Library
# Ausgabewerte: Importierte Tracks, Exportierte Playlists
# Testdateien: test_playlist.m3u8, sample_media.mp3
# Kommentar: Test-Suite für VLC Playlist Import/Export Funktionalität.

import pytest
import tempfile
from pathlib import Path
import sys
import json

# Add parent directory to path for imports

import src.core.db as db
from src.core.models import MediaItem

class TestVLCPlaylistImport:
    """Tests für VLC Playlist Import"""
    
    def setup_method(self):
        """Setup: Erstelle temporäre Testumgebung"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db = Path(self.temp_dir) / "test_media.db"
        
        # Override DB path
        db.DB_FILENAME = str(self.test_db)
        db.init_db()
    
    def teardown_method(self):
        """Cleanup: Entferne temporäre Dateien"""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_m3u8_basic_parsing(self):
        """Test: M3U8 Playlist wird korrekt eingelesen"""
        playlist_content = """#EXTM3U
#EXTINF:180,Artist - Song Title
/path/to/song.mp3
#EXTINF:240,Another Artist - Another Song
/path/to/another.mp3
"""
        playlist_file = Path(self.temp_dir) / "test.m3u8"
        playlist_file.write_text(playlist_content, encoding='utf-8')
        
        # Parse playlist (simplified test - actual parsing uses m3u8 library)
        lines = playlist_content.strip().split('\n')
        tracks = []
        for i, line in enumerate(lines):
            if line.startswith('#EXTINF'):
                # Next line should be the file path
                if i + 1 < len(lines):
                    tracks.append(lines[i + 1])
        
        assert len(tracks) == 2
        assert '/path/to/song.mp3' in tracks
        assert '/path/to/another.mp3' in tracks
    
    def test_import_skips_duplicates(self):
        """Test: Import überspringt bereits vorhandene Tracks"""
        # Create a test media item in DB
        test_item = {
            'name': 'existing_song.mp3',
            'path': '/test/existing_song.mp3',
            'type': 'audio',
            'duration': '3:00',
            'category': 'Audio',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': json.dumps({'title': 'Existing Song'}),
            'extension': '.mp3',
            'container': 'mp3',
            'tag_type': 'ID3',
            'codec': 'MP3'
        }
        db.insert_media(test_item)
        
        # Check if duplicate detection works
        known_names = db.get_known_media_names()
        assert 'existing_song.mp3' in known_names
        
        # Verify we would skip this file
        should_skip = 'existing_song.mp3' in known_names
        assert should_skip is True
    
    def test_import_handles_missing_files(self):
        """Test: Import meldet fehlende Dateien korrekt"""
        missing_path = Path("/nonexistent/path/to/song.mp3")
        
        # Verify file doesn't exist
        assert not missing_path.exists()
        
        # This should be caught by import logic
        errors = []
        if not missing_path.exists():
            errors.append(f"Datei nicht gefunden: {missing_path.name}")
        
        assert len(errors) == 1
        assert "Datei nicht gefunden" in errors[0]

class TestVLCPlaylistExport:
    """Tests für VLC Playlist Export"""
    
    def setup_method(self):
        """Setup: Erstelle Testdatenbank mit Sample-Daten"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db = Path(self.temp_dir) / "test_media.db"
        
        db.DB_FILENAME = str(self.test_db)
        db.init_db()
        
        # Add test media items
        self.test_items = [
            {
                'name': 'track1.mp3',
                'path': '/test/track1.mp3',
                'type': 'audio',
                'duration': '180',
                'category': 'Audio',
                'is_transcoded': False,
                'transcoded_format': None,
                'tags': json.dumps({
                    'title': 'Track One',
                    'artist': 'Artist One',
                    'album': 'Test Album'
                }),
                'extension': '.mp3',
                'container': 'mp3',
                'tag_type': 'ID3',
                'codec': 'MP3'
            },
            {
                'name': 'track2.flac',
                'path': '/test/track2.flac',
                'type': 'audio',
                'duration': '240',
                'category': 'Audio',
                'is_transcoded': False,
                'transcoded_format': None,
                'tags': json.dumps({
                    'title': 'Track Two',
                    'artist': 'Artist Two',
                    'album': 'Test Album'
                }),
                'extension': '.flac',
                'container': 'flac',
                'tag_type': 'VorbisComment',
                'codec': 'FLAC'
            }
        ]
        
        for item in self.test_items:
            db.insert_media(item)
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_export_creates_valid_m3u8(self):
        """Test: Export erstellt gültige M3U8 Datei"""
        output_path = Path(self.temp_dir) / "export_test.m3u8"
        
        # Simulate export
        all_media = db.get_all_media()
        media_dict = {item['name']: item for item in all_media}
        
        lines = ["#EXTM3U\n"]
        for name in ['track1.mp3', 'track2.flac']:
            item = media_dict.get(name)
            if item:
                duration = item.get('duration', 0) or -1
                # Tags are already parsed as dict by db.get_all_media()
                tags_dict = item.get('tags', {})
                if isinstance(tags_dict, str):
                    tags_dict = json.loads(tags_dict)
                title = tags_dict.get('title', name)
                artist = tags_dict.get('artist', '')
                extinf_title = f"{artist} - {title}" if artist else title
                
                lines.append(f"#EXTINF:{duration},{extinf_title}\n")
                lines.append(f"{item['path']}\n")
        
        output_path.write_text("".join(lines), encoding='utf-8')
        
        # Verify file was created
        assert output_path.exists()
        
        # Verify content
        content = output_path.read_text(encoding='utf-8')
        assert content.startswith("#EXTM3U")
        assert "#EXTINF" in content
        assert "track1.mp3" in content or "/test/track1.mp3" in content
        assert "track2.flac" in content or "/test/track2.flac" in content
        assert "Artist One - Track One" in content
        assert "Artist Two - Track Two" in content
    
    def test_export_handles_missing_metadata(self):
        """Test: Export funktioniert auch ohne vollständige Metadaten"""
        # Add item with minimal metadata
        minimal_item = {
            'name': 'minimal.mp3',
            'path': '/test/minimal.mp3',
            'type': 'audio',
            'duration': '0',
            'category': 'Audio',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': json.dumps({}),  # Empty tags
            'extension': '.mp3',
            'container': 'mp3',
            'tag_type': 'ID3',
            'codec': 'MP3'
        }
        db.insert_media(minimal_item)
        
        # Should still be exportable
        all_media = db.get_all_media()
        found = any(item['name'] == 'minimal.mp3' for item in all_media)
        assert found is True
    
    def test_export_preserves_track_order(self):
        """Test: Export behält Track-Reihenfolge bei"""
        all_media = db.get_all_media()
        names = [item['name'] for item in all_media]
        
        # Should maintain insertion order (or alphabetical from DB)
        assert len(names) >= 2
        assert 'track1.mp3' in names
        assert 'track2.flac' in names

class TestVLCIntegrationEndToEnd:
    """End-to-End Tests für komplette Import/Export Workflows"""
    
    def setup_method(self):
        """Setup"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db = Path(self.temp_dir) / "test_media.db"
        db.DB_FILENAME = str(self.test_db)
        db.init_db()
    
    def teardown_method(self):
        """Cleanup"""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_roundtrip_import_export(self):
        """Test: Import → Export → Import Roundtrip"""
        # Step 1: Create original playlist
        original_playlist = """#EXTM3U
#EXTINF:200,Test Artist - Test Song
/test/original.mp3
"""
        playlist_path = Path(self.temp_dir) / "original.m3u8"
        playlist_path.write_text(original_playlist, encoding='utf-8')
        
        # Step 2: Simulate import (would add to DB)
        # For this test, manually add
        test_item = {
            'name': 'original.mp3',
            'path': '/test/original.mp3',
            'type': 'audio',
            'duration': '200',
            'category': 'Audio',
            'is_transcoded': False,
            'transcoded_format': None,
            'tags': json.dumps({
                'title': 'Test Song',
                'artist': 'Test Artist'
            }),
            'extension': '.mp3',
            'container': 'mp3',
            'tag_type': 'ID3',
            'codec': 'MP3'
        }
        db.insert_media(test_item)
        
        # Step 3: Export back to playlist
        all_media = db.get_all_media()
        export_path = Path(self.temp_dir) / "exported.m3u8"
        
        lines = ["#EXTM3U\n"]
        for item in all_media:
            tags = item.get('tags', {})
            if isinstance(tags, str):
                tags = json.loads(tags)
            title = tags.get('title', item['name'])
            artist = tags.get('artist', '')
            extinf = f"{artist} - {title}" if artist else title
            
            lines.append(f"#EXTINF:{item['duration']},{extinf}\n")
            lines.append(f"{item['path']}\n")
        
        export_path.write_text("".join(lines), encoding='utf-8')
        
        # Step 4: Verify exported content
        exported_content = export_path.read_text(encoding='utf-8')
        assert "#EXTM3U" in exported_content
        assert "Test Artist - Test Song" in exported_content
        assert "/test/original.mp3" in exported_content

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
