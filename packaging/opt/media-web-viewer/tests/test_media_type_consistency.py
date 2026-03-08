import unittest
from pathlib import Path
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import MediaItem

class TestMediaTypeConsistency(unittest.TestCase):
    """
    @brief Tests for media type categorization.
    @details Ensures that audio and video files are consistently identified.
    """

    def test_audio_categorization(self):
        """
        @test Verify that common audio extensions are categorized as 'audio'.
        @details Checks mp3, flac, wav, etc. to ensure they return media_type='audio' 
                 and that to_dict() provides the correct type for the frontend.
        """
        audio_exts = ['.mp3', '.flac', '.wav', '.m4a', '.ogg', '.opus', '.alac', '.aiff']
        for ext in audio_exts:
            fname = f"test_audio{ext}"
            item = MediaItem(fname, Path(fname))
            self.assertEqual(item.media_type, 'audio', f"Extension {ext} should be audio")
            self.assertEqual(item.to_dict()['type'], 'audio', f"to_dict for {ext} should return type='audio'")

    def test_video_categorization(self):
        """
        @test Verify that common video extensions are categorized as 'video'.
        @details Checks mp4, mkv, avi, etc. to ensure they consistently return 
                 media_type='video', enabling correct routing in the UI.
        """
        video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.m4v']
        for ext in video_exts:
            fname = f"test_video{ext}"
            item = MediaItem(fname, Path(fname))
            self.assertEqual(item.media_type, 'video', f"Extension {ext} should be video")
            self.assertEqual(item.to_dict()['type'], 'video', f"to_dict for {ext} should return type='video'")

    def test_extension_extraction(self):
        """
        @test Verify extension field is always lowercased without leading dot.
        @details Ensures 'MP3' becomes 'mp3' and that the media_type is correctly 
                 derived from the normalized extension.
        """
        fname = "test_file.MP3"
        item = MediaItem(fname, Path(fname))
        self.assertEqual(item.extension, "mp3")
        self.assertEqual(item.media_type, "audio")

    def test_unknown_extension_fallback(self):
        """Verify fallback behavior for unknown extensions."""
        fname = "readme.txt"
        item = MediaItem(fname, Path(fname))
        # Default in current models.py is 'audio' if not in video list
        self.assertEqual(item.media_type, 'audio')

if __name__ == '__main__':
    print("Running Media Type Consistency Tests...")
    unittest.main()
