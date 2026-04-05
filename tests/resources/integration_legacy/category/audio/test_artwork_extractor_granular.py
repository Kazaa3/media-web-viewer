#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.parsers.artwork_extractor import ArtworkExtractor

class TestArtworkExtractorGranular:
    """
    Granular tests for artwork extraction by tool and category.
    """

    def setup_method(self):
        self.extractor = ArtworkExtractor()

    @patch('src.parsers.artwork_extractor.Path.exists', return_value=True)
    def test_category_bilder_short_circuit(self, mock_exists):
        """Category 'Bilder' should return the original path immediately."""
        path = Path("/media/photos/vacation.jpg")
        res = self.extractor.extract(path, {}, 'Bilder')
        assert res == str(path)

    @patch('src.parsers.artwork_extractor.Path.exists', return_value=True)
    @patch('src.parsers.artwork_extractor.Path.stat')
    @patch('src.parsers.artwork_extractor.Path.mkdir')
    @patch('mutagen.File')
    @patch('builtins.open', new_callable=MagicMock)
    def test_tool_mutagen_mp3_front_cover(self, mock_open, mock_mutagen, mock_mkdir, mock_stat, mock_exists):
        """Verify Mutagen tool prioritizes Front Cover (Type 3) in MP3."""
        path = Path("/media/music/song.mp3")
        mock_stat.return_value.st_size = 5000
        mock_stat.return_value.st_mtime = 100
        
        # Mock Mutagen tags with multiple pictures
        mock_audio = MagicMock()
        pic_back = MagicMock(type=4, data=b"back_data")
        pic_front = MagicMock(type=3, data=b"front_data")
        mock_audio.tags.getall.return_value = [pic_back, pic_front]
        mock_mutagen.return_value = mock_audio
        
        # Mock art_file.exists check inside extraction
        # exists calls: 1. path.exists, 2. art_file.exists (cache), 3. out_path exists check
        mock_exists.side_effect = [True, False, True, True]
        
        res = self.extractor.extract(path, {}, 'Audio')
        
        # Verify open was called with front_data
        handle = mock_open.return_value.__enter__.return_value
        handle.write.assert_called_with(b"front_data")

    @patch('src.parsers.artwork_extractor.Path.exists', return_value=True)
    @patch('src.parsers.artwork_extractor.Path.stat')
    @patch('src.parsers.artwork_extractor.ArtworkExtractor._run_ffmpeg')
    def test_category_video_mkv_stream_extraction(self, mock_ffmpeg, mock_stat, mock_exists):
        """Verify Video category uses FFmpeg stream extraction for MKV."""
        path = Path("/media/movies/film.mkv")
        mock_stat.return_value.st_size = 500000
        mock_stat.return_value.st_mtime = 200
        mock_exists.side_effect = [True, False, True, True]
        mock_ffmpeg.return_value = True
        
        res = self.extractor.extract(path, {}, 'Video')
        
        assert mock_ffmpeg.called
        # First call should be stream extraction (map 0:v)
        args = mock_ffmpeg.call_args_list[0][0][0]
        assert "-map" in args
        assert "0:v" in args
        assert "copy" in args

    @patch('src.parsers.artwork_extractor.Path.exists', return_value=True)
    @patch('src.parsers.artwork_extractor.Path.stat')
    @patch('src.parsers.artwork_extractor.ArtworkExtractor._run_ffmpeg')
    def test_tool_ffmpeg_thumbnail_fallback(self, mock_ffmpeg, mock_stat, mock_exists):
        """Verify FFmpeg fallback to thumbnailing if stream extraction fails."""
        path = Path("/media/movies/clip.mp4")
        mock_stat.return_value.st_size = 100000
        mock_stat.return_value.st_mtime = 300
        
        # 1. path.exists
        # 2. art_file.exists (cache check)
        # 3. out_path check for result of extraction 1
        # 4. out_path check for result of extraction 2
        mock_exists.side_effect = [True, False, False, True, True]
        
        # First call (stream) fails, second call (thumb) succeeds
        mock_ffmpeg.side_effect = [False, True]
        
        res = self.extractor.extract(path, {}, 'Video')
        
        assert mock_ffmpeg.call_count == 2
        thumb_cmd = mock_ffmpeg.call_args_list[1][0][0]
        assert "-ss" in thumb_cmd
        assert "scale" in thumb_cmd

if __name__ == "__main__":
    pytest.main([__file__])
