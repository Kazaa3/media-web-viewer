import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from parsers.media_parser import extract_metadata, PARSER_MAPPING

class TestParserMapping(unittest.TestCase):
    def setUp(self):
        self.test_file = "test.mp3"
        self.test_path = "/tmp/test.mp3"
        
        # Mock PARSER_CONFIG to have a known chain
        self.mock_config = {
            "parser_chain": ["filename", "mutagen", "isoparser"],
            "parser_mode": "full", # Use full to avoid "has_essential" early exit
            "enable_isoparser_parser": True
        }

    @patch('pathlib.Path.is_file')
    @patch('parsers.format_utils.PARSER_CONFIG')
    @patch('parsers.filename_parser.parse')
    @patch('parsers.mutagen_parser.parse')
    @patch('parsers.isoparser_parser.parse')
    def test_mp3_mapping(self, mock_iso, mock_mutagen, mock_filename, mock_config, mock_is_file):
        """Test that only mapped parsers are called for .mp3"""
        mock_is_file.return_value = True
        mock_config.get.side_effect = self.mock_config.get
        
        # We need to mock the return values so the loop continues
        mock_filename.return_value = {}
        mock_mutagen.return_value = {}
        
        # .mp3 is mapped to ["filename", "mutagen", ...] but NOT "isoparser"
        extract_metadata(self.test_path, self.test_file, mode='full')
        
        self.assertTrue(mock_filename.called)
        self.assertTrue(mock_mutagen.called)
        self.assertFalse(mock_iso.called)

    @patch('pathlib.Path.is_file')
    @patch('parsers.format_utils.PARSER_CONFIG')
    @patch('parsers.isoparser_parser.parse')
    @patch('parsers.filename_parser.parse')
    def test_iso_mapping(self, mock_filename, mock_iso, mock_config, mock_is_file):
        """Test that isoparser is called for .iso"""
        mock_is_file.return_value = True
        mock_config.get.side_effect = self.mock_config.get
        
        mock_filename.return_value = {}
        mock_iso.return_value = {}
        
        extract_metadata("/tmp/test.iso", "test.iso", mode='full')
        
        self.assertTrue(mock_filename.called)
        self.assertTrue(mock_iso.called)

    @patch('pathlib.Path.is_file')
    @patch('parsers.format_utils.PARSER_CONFIG')
    @patch('parsers.filename_parser.parse')
    @patch('parsers.mutagen_parser.parse')
    def test_unknown_extension_fallback(self, mock_mutagen, mock_filename, mock_config, mock_is_file):
        """Test that unknown extensions fall back to trying all parsers in chain"""
        mock_is_file.return_value = True
        mock_config.get.side_effect = self.mock_config.get
        
        mock_filename.return_value = {}
        mock_mutagen.return_value = {}
        
        # .xyz is not in PARSER_MAPPING
        extract_metadata("/tmp/test.xyz", "test.xyz", mode='full')
        
        # Both should be called because mapping is bypassed
        self.assertTrue(mock_filename.called)
        self.assertTrue(mock_mutagen.called)

if __name__ == '__main__':
    unittest.main()
