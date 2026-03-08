import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import os

# Ensure project root is in path to import main and models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

class TestLogbookParsing(unittest.TestCase):
    """
    @brief Tests for backend logbook entry parsing.
    @details Verifies that various markdown formats and filenames are correctly parsed.
    """

    @patch('main.Path.glob')
    @patch('builtins.open')
    def test_filename_with_spaces(self, mock_open, mock_glob):
        """
        @test Verify that filenames with spaces (like '43 VLC.md') are handled.
        @details Checks if the parser correctly handles filenames with common spaces, 
                 ensuring 'f.stem' and 'f.name' don't break the list_logbook_entries loop.
        """
        mock_file = MagicMock(spec=Path)
        mock_file.name = "43 VLC.md"
        mock_file.stem = "43 VLC"
        mock_glob.return_value = [mock_file]

        # Mock reading the file
        file_content = [
            "Category: Feature\n",
            "Status: COMPLETED\n",
            "# 43 VLC Integration\n",
            "Summary: Test summary\n"
        ] + (["\n"] * 16)
        
        mock_handle = MagicMock()
        mock_handle.readline.side_effect = file_content
        mock_open.return_value.__enter__.return_value = mock_handle

        entries = main.list_logbook_entries()
        
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['name'], "43 VLC")
        self.assertEqual(entries[0]['title'], "43 VLC Integration")
        self.assertEqual(entries[0]['category'], "Feature")
        self.assertEqual(entries[0]['status'], "COMPLETED")

    @patch('main.Path.glob')
    @patch('builtins.open')
    def test_metadata_extraction_variants(self, mock_open, mock_glob):
        """
        @test Verify extraction with HTML comment style metadata: <!-- Category: Bug -->
        @details Ensures the parser correctly extracts Category, Status, and Summary 
                 from both plain text and HTML-style markdown comments.
        """
        mock_file = MagicMock(spec=Path)
        mock_file.name = "fix_bug.md"
        mock_file.stem = "fix_bug"
        mock_glob.return_value = [mock_file]

        file_content = [
            "<!-- Category: Bug -->\n",
            "<!-- Status: ACTIVE -->\n",
            "<!-- Summary: Fixing a critical bug -->\n",
            "# Bugfix Title\n"
        ] + (["\n"] * 16)
        
        mock_handle = MagicMock()
        mock_handle.readline.side_effect = file_content
        mock_open.return_value.__enter__.return_value = mock_handle

        entries = main.list_logbook_entries()
        
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['category'], "Bug")
        self.assertEqual(entries[0]['status'], "ACTIVE")
        self.assertEqual(entries[0]['summary'], "Fixing a critical bug")
        self.assertEqual(entries[0]['name'], "fix_bug")
        self.assertEqual(entries[0]['title'], "Bugfix Title")

    @patch('main.Path.glob')
    @patch('builtins.open')
    def test_fallback_logic(self, mock_open, mock_glob):
        """
        @test Verify fallback logic when no metadata is provided.
        @details Confirms that Sonstiges/COMPLETED defaults are applied and 
                 the title falls back to the filename stem if no # header is found.
        """
        mock_file = MagicMock(spec=Path)
        mock_file.name = "plain.md"
        mock_file.stem = "plain"
        mock_glob.return_value = [mock_file]

        file_content = ["Just some text without tags or headers\n"] * 20
        
        mock_handle = MagicMock()
        mock_handle.readline.side_effect = file_content
        mock_open.return_value.__enter__.return_value = mock_handle

        entries = main.list_logbook_entries()
        
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['name'], "plain") # Falls back to stem
        self.assertEqual(entries[0]['category'], "Sonstiges") # Default
        self.assertEqual(entries[0]['status'], "COMPLETED") # Default

if __name__ == '__main__':
    # Add a simple summary if run as script
    print("Running Logbook Parsing Tests...")
    unittest.main()
