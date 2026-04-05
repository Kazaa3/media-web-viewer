#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add project root to path

from src.core.main import get_library
from src.parsers.format_utils import PARSER_CONFIG

class TestIndexingVsDisplay(unittest.TestCase):
    def setUp(self):
        # Mock data returned by DB
        self.mock_media = [
            {'name': 'song.mp3', 'category': 'Audio'},
            {'name': 'movie.mp4', 'category': 'Film'},
            {'name': 'book.pdf', 'category': 'E-Book'},
            {'name': 'image.jpg', 'category': 'Bilder'},
            {'name': 'doc.txt', 'category': 'Dokument'},
            {'name': 'disk.iso', 'category': 'Abbild'}
        ]

    @patch('src.core.db.get_all_media')
    def test_default_display_audio_only(self, mock_get_all):
        """Verify that by default only audio items are returned."""
        mock_get_all.return_value = self.mock_media
        
        # Ensure default displayed_categories is ["audio"]
        with patch.dict(PARSER_CONFIG, {"displayed_categories": ["audio"]}):
            result = get_library()
            media = result['media']
            
            # Should only contain 'song.mp3' (Audio)
            self.assertEqual(len(media), 1)
            self.assertEqual(media[0]['name'], 'song.mp3')

    @patch('src.core.db.get_all_media')
    def test_display_video_and_audio(self, mock_get_all):
        """Verify that multiple display categories work."""
        mock_get_all.return_value = self.mock_media
        
        with patch.dict(PARSER_CONFIG, {"displayed_categories": ["audio", "video"]}):
            result = get_library()
            media = result['media']
            
            # Should contain 'song.mp3' (Audio) and 'movie.mp4' (Film mapped to video)
            self.assertEqual(len(media), 2)
            names = [item['name'] for item in media]
            self.assertIn('song.mp3', names)
            self.assertIn('movie.mp4', names)

    @patch('src.core.db.get_all_media')
    def test_display_all(self, mock_get_all):
        """Verify that displaying all categories works."""
        mock_get_all.return_value = self.mock_media
        
        all_cats = ["audio", "video", "images", "documents", "ebooks", "abbild"]
        with patch.dict(PARSER_CONFIG, {"displayed_categories": all_cats}):
            result = get_library()
            media = result['media']
            
            # All 6 mock items should be returned
            self.assertEqual(len(media), 6)

    @patch('src.core.db.get_all_media')
    def test_display_none(self, mock_get_all):
        """Verify that an empty display list returns nothing."""
        mock_get_all.return_value = self.mock_media
        
        with patch.dict(PARSER_CONFIG, {"displayed_categories": []}):
            result = get_library()
            media = result['media']
            
            self.assertEqual(len(media), 0)

if __name__ == '__main__':
    unittest.main()
