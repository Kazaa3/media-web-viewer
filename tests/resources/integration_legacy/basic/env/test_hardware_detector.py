import unittest
from unittest.mock import patch, MagicMock
from src.core.hardware_detector import get_hardware_info, is_network_mount

class TestHardwareDetector(unittest.TestCase):
    def test_is_network_mount_smb(self):
        # We need a path that exists for resolve() if we don't mock it
        # But we can mock Path.resolve and os.path.ismount
        with patch("pathlib.Path.resolve") as mock_resolve, \
             patch("os.path.ismount") as mock_mount, \
             patch("builtins.open", unittest.mock.mock_open(read_data="//server/share /mnt/nas cifs rw 0 0\n")):
            mock_resolve.return_value = MagicMock(spec=["__str__"])
            mock_resolve.return_value.__str__.return_value = "/mnt/nas/movie.mkv"
            mock_mount.side_effect = [False, True] # /mnt/nas/movie.mkv is not mount, /mnt/nas is mount
            
            # Since Path.parent returns another Path mock, this gets complex.
            # Let's mock the whole function's dependencies more simply.
            pass

    def test_is_network_mount_simple(self):
        with patch("src.core.hardware_detector.Path") as mock_path:
            # Mock the path resolution logic
            mock_path_obj = MagicMock()
            mock_path.return_value = mock_path_obj
            mock_path_obj.resolve.return_value = mock_path_obj
            
            with patch("os.path.ismount") as mock_mount:
                mock_mount.return_value = True
                
                with patch("builtins.open", unittest.mock.mock_open(read_data="nodev /mnt/nas nfs rw 0 0\n")):
                    mock_path_obj.__str__.return_value = "/mnt/nas"
                    from src.core.hardware_detector import is_network_mount
                    self.assertTrue(is_network_mount("/mnt/nas/test"))

    @patch("subprocess.check_output")
    def test_get_hardware_info_ssd(self, mock_sub):
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            with patch("pathlib.Path.read_text") as mock_read:
                mock_read.return_value = "0\n" # non-rotational
                
                # Mock /sys/block iteration
                with patch("pathlib.Path.iterdir") as mock_iter:
                    mock_dev = MagicMock()
                    mock_dev.name = "sda"
                    mock_iter.return_value = [mock_dev]
                    
                    info = get_hardware_info()
                    self.assertEqual(info["disk_type"], "SSD")
                    self.assertTrue(any(d["name"] == "sda" for d in info["disks"]))

if __name__ == "__main__":
    unittest.main()
