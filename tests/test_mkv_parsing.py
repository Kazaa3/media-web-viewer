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

    @patch('parsers.artwork_extractor.ArtworkExtractor._run_ffmpeg', return_value=True)
    @patch('parsers.media_parser.extract_metadata')
    def test_mkv_artwork_extraction_flow(self, mock_extract, mock_ffmpeg):
        """Test the logic for extracting artwork from an MKV file."""
        mock_extract.return_value = (0, {
            'title': 'MKV with Cover',
            'has_art': 'Yes',
            'container': 'matroska'
        })
        
        path = Path("/media/cover_test.mkv")
        from parsers.format_utils import PARSER_CONFIG
        PARSER_CONFIG['ffmpeg_extract_thumbnails'] = True
        
        with patch('parsers.artwork_extractor.Path.exists', side_effect=[True, False, True, True]), \
             patch('parsers.artwork_extractor.Path.mkdir'), \
             patch('parsers.artwork_extractor.Path.stat') as mock_stat:
            
            mock_stat.return_value.st_size = 1000
            mock_stat.return_value.st_mtime = 123456
            mock_stat.return_value.st_mode = 33188  # S_IFREG
            
            item = MediaItem("cover_test.mkv", str(path))
            # Verify ffmpeg was called for attachment/extraction
            assert mock_ffmpeg.called

if __name__ == "__main__":
    pytest.main([__file__])
