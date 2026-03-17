#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock
import json

import sys
import os
from pathlib import Path

# Fix paths for imports
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.main import get_library

class TestCategoryMapping(unittest.TestCase):
    @patch('src.core.main.db.get_all_media')
    @patch('src.core.main.PARSER_CONFIG', {"displayed_categories": ["audio"]})
    def test_podcast_category_filtering(self, mock_get_all):
        """
        Verify that entries with category 'Podcasts' or 'Podcast' are returned
        when the 'audio' filter is active.
        """
        mock_get_all.return_value = [
            {'name': 'Song1', 'category': 'Audio'},
            {'name': 'Podcast1', 'category': 'Podcasts'},
            {'name': 'Podcast2', 'category': 'Podcast'},
            {'name': 'Radio1', 'category': 'Radio'},
            {'name': 'Video1', 'category': 'Video'}
        ]
        
        result = get_library()
        media = result.get('media', [])
        names = [m['name'] for m in media]
        
        self.assertIn('Song1', names)
        self.assertIn('Podcast1', names)
        self.assertIn('Podcast2', names)
        self.assertIn('Radio1', names)
        self.assertNotIn('Video1', names)
        print("✅ Backend Category Mapping (including Podcasts/Radio) verified.")

if __name__ == "__main__":
    unittest.main()
