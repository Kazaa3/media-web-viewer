import sys
import os
import unittest
from pathlib import Path
from unittest.mock import patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Add src/core to path for logger/models internal imports if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/core')))

# Patch Path.mkdir BEFORE importing anything that might use it
with patch('pathlib.Path.mkdir'):
    from src.core.models import MediaItem

class TestParserTiming(unittest.TestCase):
    def setUp(self):
        self.dummy_path = Path("/tmp/test_media.mp3")

    @patch('src.core.models.media_parser.extract_metadata')
    def test_parser_timing_capture(self, mock_extract):
        # Simulate (tags, parser_times) return
        mock_tags = {'title': 'Test Song', 'duration': 120}
        mock_times = {'filename': 0.005, 'mutagen': 0.045}
        mock_extract.return_value = (mock_tags, mock_times)

        with patch('pathlib.Path.is_file', return_value=True), \
             patch('pathlib.Path.is_dir', return_value=False), \
             patch('parsers.artwork_extractor.extractor.extract', return_value=None):
            
            item = MediaItem("test_media.mp3", self.dummy_path)
            
            # Check if times are in tags
            self.assertIn('_parser_times', item.tags)
            self.assertEqual(item.tags['_parser_times'], mock_times)
            
            # Check to_dict preservation
            d = item.to_dict()
            self.assertIn('_parser_times', d['tags'])
            self.assertEqual(d['tags']['_parser_times'], mock_times)

if __name__ == '__main__':
    unittest.main()
