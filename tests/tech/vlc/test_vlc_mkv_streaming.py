import unittest
from unittest.mock import patch, MagicMock
import os
from pathlib import Path
import src.core.main as main

class TestVlcMkvStreaming(unittest.TestCase):
    
    @patch('shutil.which')
    def test_is_mkvtoolnix_available(self, mock_which):
        mock_which.return_value = '/usr/bin/mkvmerge'
        self.assertTrue(main.is_mkvtoolnix_available())
        
        mock_which.return_value = None
        self.assertFalse(main.is_mkvtoolnix_available())

    @patch('src.core.main.is_mkvtoolnix_available')
    @patch('subprocess.Popen')
    def test_stream_to_vlc(self, mock_popen, mock_available):
        mock_available.return_value = True
        
        # Mock Popen chain
        mock_p1 = MagicMock()
        mock_p2 = MagicMock()
        mock_popen.side_effect = [mock_p1, mock_p2]
        
        result = main.stream_to_vlc('test.mp4')
        
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(mock_popen.call_count, 2)
        
        # Verify first Popen call (mkvmerge)
        args1, _ = mock_popen.call_args_list[0]
        self.assertIn('mkvmerge', args1[0])
        self.assertIn('test.mp4', args1[0])
        self.assertIn('-o', args1[0])
        self.assertIn('-', args1[0])
        
        # Verify second Popen call (vlc)
        args2, _ = mock_popen.call_args_list[1]
        self.assertIn('vlc', args2[0])
        self.assertIn('-', args2[0])

    @patch('subprocess.Popen')
    def test_stream_iso_to_vlc(self, mock_popen):
        # Verify that ISO files use native dvd:// protocol
        result = main.stream_to_vlc('movie.iso')
        
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['mode'], 'vlc_dvd')
        self.assertEqual(mock_popen.call_count, 1)
        
        args, _ = mock_popen.call_args
        self.assertTrue(args[0][0].endswith('vlc'))
        self.assertIn('dvd://movie.iso', args[0])

    @patch('src.core.main.is_mkvtoolnix_available')
    @patch('subprocess.run')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.glob')
    def test_remux_mkv_batch(self, mock_glob, mock_is_dir, mock_run, mock_available):
        mock_available.return_value = True
        mock_is_dir.return_value = True
        
        # Mock finding one mp4 file
        mock_mp4 = MagicMock(spec=Path)
        mock_mp4.name = 'video.mp4'
        mock_mp4.suffix = '.mp4'
        mock_mp4.with_suffix.return_value = MagicMock(spec=Path)
        mock_mp4.with_suffix.return_value.exists.return_value = False
        mock_mp4.with_suffix.return_value.name = 'video.mkv'
        
        # Glob is called multiple times for different extensions
        mock_glob.side_effect = [[mock_mp4]] + [[] for _ in range(50)]
        
        result = main.remux_mkv_batch('/tmp/videos')
        
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['results']['success'], 1)
        self.assertEqual(mock_run.call_count, 1)
        
        # Verify mkvmerge command
        args, _ = mock_run.call_args
        self.assertIn('mkvmerge', args[0])
        self.assertIn('-o', args[0])

if __name__ == '__main__':
    unittest.main()
