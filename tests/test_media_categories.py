import unittest
from pathlib import Path
from models import MediaItem
from parsers.format_utils import PARSER_CONFIG

class TestMediaCategories(unittest.TestCase):
    def setUp(self):
        # Ensure we don't trigger real scans if possible, but MediaItem calls extract_metadata
        pass

    def test_audio_category(self):
        # We can't easily mock the entire parser chain without a lot of setup,
        # so we'll test the detection logic if we can.
        # However, MediaItem.__init__ calls media_parser.extract_metadata.
        # Let's try to test the methods directly if possible or mock the extractor.
        from unittest.mock import patch
        with patch('parsers.media_parser.extract_metadata') as mock_extract:
            mock_extract.return_value = (180, {'title': 'Song', 'artist': 'Artist'})
            item = MediaItem('song.mp3', '/tmp/song.mp3')
            self.assertEqual(item.logical_type, 'Audio')
            self.assertEqual(item.category, 'Audio')

    def test_video_category(self):
        from unittest.mock import patch
        with patch('parsers.media_parser.extract_metadata') as mock_extract:
            mock_extract.return_value = (3600, {'title': 'Movie', 'artist': ''})
            item = MediaItem('movie.mp4', '/tmp/movie.mp4')
            self.assertEqual(item.logical_type, 'Video')
            self.assertEqual(item.category, 'Film')

    def test_hoerbuch_category(self):
        from unittest.mock import patch
        with patch('parsers.media_parser.extract_metadata') as mock_extract:
            mock_extract.return_value = (7200, {'title': 'Book', 'artist': 'Author'})
            item = MediaItem('book.m4b', '/tmp/book.m4b')
            # item.type is .m4b, so get_category should return 'Hörbuch'
            self.assertEqual(item.category, 'Hörbuch')

    def test_iso_image_category(self):
        from unittest.mock import patch
        with patch('parsers.media_parser.extract_metadata') as mock_extract:
            mock_extract.return_value = (0, {'pycdlib_volume_id': 'MY_DVD'})
            item = MediaItem('disc.iso', '/tmp/disc.iso')
            self.assertEqual(item.logical_type, 'Abbild')
            self.assertEqual(item.content_type, 'PAL DVD')

    def test_bilder_category(self):
        from unittest.mock import patch
        with patch('parsers.media_parser.extract_metadata') as mock_extract:
            mock_extract.return_value = (0, {})
            item = MediaItem('photo.jpg', '/tmp/photo.jpg')
            self.assertEqual(item.logical_type, 'Bilder')
            self.assertEqual(item.category, 'Bilder')

    def test_audio_extensions_coverage(self):
        """Test that all audio extensions are correctly categorized as 'Audio'."""
        from unittest.mock import patch
        audio_exts = ['.flac', '.ogg', '.wav', '.opus', '.aac', '.wma']
        with patch('parsers.media_parser.extract_metadata') as mock_extract:
            mock_extract.return_value = (180, {})
            for ext in audio_exts:
                item = MediaItem(f'test{ext}', f'/tmp/test{ext}')
                self.assertEqual(item.logical_type, 'Audio', f"Failed for {ext}")

    def test_container_metadata_extraction(self):
        """Test that the container parser correctly extracts video resolution and track counts."""
        from unittest.mock import patch, MagicMock
        from parsers.container_parser import parse
        
        # Test path and tags
        test_path = Path('/tmp/video.mp4')
        test_tags = {}
        
        # Mock MediaInfo.parse
        with patch('parsers.container_parser.MediaInfo.parse') as mock_mi_parse:
            # Create a mock MediaInfo object with tracks
            mock_mi = mock_mi_parse.return_value
            
            # Mock tracks
            mock_general = MagicMock(track_type='General', duration=3600000, format='MPEG-4', file_size=104857600, recorded_date='2024-03-10')
            mock_video = MagicMock(track_type='Video', width=1920, height=1080, frame_rate=24.0, format='AVC')
            mock_audio1 = MagicMock(track_type='Audio', format='AAC', sampling_rate=44100, bit_rate=192000, bit_depth=16, language='de')
            mock_audio2 = MagicMock(track_type='Audio', format='AC-3', language='en')
            mock_sub = MagicMock(track_type='Text', language='en')
            
            mock_mi.tracks = [mock_general, mock_video, mock_audio1, mock_audio2, mock_sub]
            
            result_tags = parse(test_path, '.mp4', test_tags, 'video.mp4')
            
            self.assertEqual(result_tags['duration'], 3600)
            self.assertEqual(result_tags['resolution'], '1920x1080')
            self.assertEqual(result_tags['video_codec'], 'avc')
            self.assertEqual(result_tags['fps'], '24')
            self.assertEqual(result_tags['audio_track_count'], 2)
            self.assertEqual(result_tags['subtitle_count'], 1)
            self.assertEqual(result_tags['subtitle_languages'], ['en'])
            self.assertEqual(result_tags['size'], '100 MB')

    def test_local_media_integration(self):
        """Integration test: scan the local media directory and verify all items."""
        media_dir = Path(__file__).resolve().parent.parent / 'media'
        if not media_dir.exists():
            self.skipTest("Local media directory not found")
        
        from parsers.media_parser import extract_metadata
        # Test files
        files = list(media_dir.glob('**/*'))
        files = [f for f in files if f.is_file() and not f.name.startswith('.')]
        
        for i, f in enumerate(files):
            # Skip very large files to avoid hanging in tests (e.g. 7GB ISOs)
            if f.stat().st_size > 1024 * 1024 * 1024:
                print(f"[{i+1}/{len(files)}] Überspringe große Datei: {f.name}")
                continue

            print(f"[{i+1}/{len(files)}] Verarbeite Datei: {f.name}")
            # Create MediaItem (which will call real extract_metadata)
            item = MediaItem(f.name, str(f))
            
            # We ensure they have a logical type and category.
            self.assertIn(item.logical_type, ['Audio', 'Video', 'Abbild', 'Bilder', 'E-Book', 'Dokument', 'Ordner', 'Unbekannt'])
            self.assertIsNotNone(item.category)
            print(f"  -> Logical: {item.logical_type}, Category: {item.category}")

        # Test directories (new requirement)
        dirs = [d for d in media_dir.glob('**/*') if d.is_dir() and not d.name.startswith('.')]
        for i, d in enumerate(dirs):
            print(f"[{i+1}/{len(dirs)}] Verarbeite Ordner: {d.name}")
            item = MediaItem(d.name, str(d))
            if (d / 'VIDEO_TS').exists() or (d / 'BDMV').exists():
                self.assertEqual(item.logical_type, 'Ordner')
                self.assertEqual(item.category, 'Film')
                print(f"  -> Korrekt als Ordner/Film erkannt: {d.name}")
            else:
                self.assertEqual(item.logical_type, 'Ordner')
                print(f"  -> Als normaler Ordner erkannt: {d.name}")

if __name__ == '__main__':
    unittest.main()
