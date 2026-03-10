#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure we can import local modules
sys.path.append(os.getcwd())

from models import MediaItem
from parsers import media_parser

class TestMKVParsing:
    """
    Tests specific to Matroska (MKV) container parsing.
    """

    @patch('models.MediaItem.extract_artwork', return_value=None)
    @patch('parsers.media_parser.extract_metadata')
    def test_mkv_basic_tags(self, mock_extract, mock_art):
        """Test basic metadata extraction for MKV."""
        mock_extract.return_value = (150.0, {
            'title': 'Test Movie',
            'artist': 'Producer A',
            'container': 'matroska',
            'codec': 'h264',
            'video_codec': 'h264',
            'audio_track_count': 2,
            'subtitle_count': 1,
            'subtitle_languages': 'ger, eng',
            'has_art': 'No'
        })
        
        path = Path("/media/test.mkv")
        
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'stat', return_value=MagicMock(st_size=1000, st_mode=33188)):
            item = MediaItem("test.mkv", str(path))
            
            assert item.logical_type == 'Video'
            assert item.category == 'Film'
            assert item.container == 'matroska'
            assert item.tags.get('audio_track_count') == 2

    @patch('models.MediaItem.extract_artwork', return_value=None)
    @patch('parsers.media_parser.extract_metadata')
    def test_mkv_serie_detection(self, mock_extract, mock_art):
        """Test that MKVs in specific folders are categorized as 'Serie'."""
        mock_extract.return_value = (600.0, {'title': 'Episode 01', 'container': 'matroska'})
        path = Path("/media/Series/TV/S01E01.mkv")
        
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'stat', return_value=MagicMock(st_size=1000, st_mode=33188)):
            item = MediaItem("S01E01.mkv", str(path))
            assert item.category == 'Serie'

    @patch('subprocess.run')
    @patch('parsers.media_parser.extract_metadata')
    def test_mkv_artwork_extraction_flow(self, mock_extract, mock_sub):
        """Test the logic for extracting artwork from an MKV file (flow check)."""
        mock_extract.return_value = (0, {
            'title': 'MKV with Cover',
            'has_art': 'Yes',
            'container': 'matroska'
        })
        
        path = Path("/media/cover_test.mkv")
        from parsers.format_utils import PARSER_CONFIG
        PARSER_CONFIG['ffmpeg_extract_thumbnails'] = True
        
        # We don't want to mock Path globally here, just verify MediaItem calls right stuff
        # exists calls: 
        # 1. art_file.exists() (cache check) -> False
        # 2. self.path.exists() (media check) -> True
        # 3. art_file.exists() (post-extraction check) -> True
        with patch('models.Path.exists', side_effect=[False, True, True, True, True, True]), \
             patch('models.Path.mkdir'), \
             patch('models.Path.stat', return_value=MagicMock(st_size=1000, st_mtime=123456, st_mode=33188)):
            
            item = MediaItem("cover_test.mkv", str(path))
            # Verify subprocess.run was called for ffmpeg
            assert mock_sub.called
            # Check if it tried attachment strategy
            found_attachment_cmd = False
            for call in mock_sub.call_args_list:
                cmd = call[0][0]
                if "-map" in cmd and "0:v" in cmd:
                    found_attachment_cmd = True
            assert found_attachment_cmd

if __name__ == "__main__":
    pytest.main([__file__])
