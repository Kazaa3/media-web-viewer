#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from pathlib import Path
from models import MediaItem
from unittest.mock import patch, MagicMock

class TestMissingCoverCategory:
    """
    Tests for items without covers.
    """

    @patch('parsers.media_parser.extract_metadata')
    @patch('parsers.artwork_extractor.extractor.extract')
    def test_missing_cover_flag(self, mock_extract_art, mock_metadata):
        """Verify that items without artwork are flagged correctly."""
        mock_metadata.return_value = (0, {})
        # Case 1: Artwork found
        mock_extract_art.return_value = "/cache/art.jpg"
        
        with patch('models.Path.exists', return_value=True), \
             patch('models.Path.is_dir', return_value=False), \
             patch('models.Path.stat'):
            item = MediaItem("test.mp3", "/media/test.mp3")
            assert item.has_artwork is True
            assert item.is_missing_cover is False

        # Case 2: No artwork found
        mock_extract_art.return_value = None
        with patch('models.Path.exists', return_value=True), \
             patch('models.Path.is_dir', return_value=False), \
             patch('models.Path.stat'):
            item2 = MediaItem("no_art.mp3", "/media/no_art.mp3")
            assert item2.has_artwork is False
            assert item2.is_missing_cover is True

if __name__ == "__main__":
    pytest.main([__file__])
