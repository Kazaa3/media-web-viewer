#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure we can import local modules
sys.path.append(os.getcwd())

from parsers.artwork_extractor import extractor

class TestArtworkExtraction:
    """
    Comprehensive tests for the ArtworkExtractor module.
    """

    def test_video_mkv_attachment_flow(self):
        """Test that MKV uses attachment strategy first."""
        path = Path("/tmp/test.mkv")
        mock_tags = {'has_art': 'No'}
        
        # Patch Path.stat on the instance or globally
        with patch.object(Path, 'stat') as mock_stat, \
             patch.object(Path, 'exists') as mock_exists, \
             patch('parsers.artwork_extractor.Path.mkdir'), \
             patch('parsers.artwork_extractor.extractor._run_ffmpeg', return_value=True) as mock_ffmpeg:
            
            mock_stat.return_value.st_size = 1000
            mock_stat.st_mtime = 12345
            
            # side_effect for exists:
            # 1. path.exists() -> True
            # 2. art_file.exists() -> False (to trigger extraction)
            # 3. out_path.exists() (inside ffmpeg check) -> True
            # 4. final success check -> True
            mock_exists.side_effect = [True, False, True, True, True]
            
            res = extractor.extract(path, mock_tags, 'Video')
            
            assert mock_ffmpeg.called
            args = mock_ffmpeg.call_args_list[0][0][0]
            assert "-map" in args

    def test_audio_mutagen_extraction(self):
        """Test that mutagen is used for audio files."""
        path = Path("/tmp/test.mp3")
        
        mock_audio = MagicMock()
        mock_pic = MagicMock()
        mock_pic.data = b"fake_image_data"
        mock_audio.tags.getall.return_value = [mock_pic]
        
        with patch.object(Path, 'stat') as mock_stat, \
             patch.object(Path, 'exists') as mock_exists, \
             patch('parsers.artwork_extractor.Path.mkdir'), \
             patch('mutagen.File', return_value=mock_audio), \
             patch('builtins.open', MagicMock()) as mock_open:
            
            mock_stat.return_value.st_size = 1000
            mock_stat.st_mtime = 12345
            mock_exists.side_effect = [True, False, True, True, True]
            
            res = extractor.extract(path, {}, 'Audio')
            assert mock_open.called

if __name__ == "__main__":
    pytest.main([__file__])
