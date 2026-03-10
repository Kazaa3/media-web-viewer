import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Mock modules that might trigger environment validation or are missing
mock_eel = MagicMock()
def mock_expose(func):
    return func
mock_eel.expose = mock_expose
sys.modules['eel'] = mock_eel
sys.modules['env_handler'] = MagicMock()
sys.modules['vlc'] = MagicMock()
sys.modules['m3u8'] = MagicMock()
sys.modules['psutil'] = MagicMock()
sys.modules['db'] = MagicMock()
sys.modules['models'] = MagicMock()

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Patch before importing main to prevent side effects
with patch('os.execv'), \
     patch('subprocess.run') as mock_sub, \
     patch('sys.exit'), \
     patch('main.logger'):
    
    # Import main - the patches above should prevent it from re-execing or exiting
    import main

class TestPipInstall(unittest.TestCase):

    @patch('subprocess.run')
    @patch('main.logger')
    def test_pip_install_packages_success(self, mock_logger, mock_run):
        # Setup mock
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Successfully installed Pillow"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Reset cache to ensure our function runs
        main._ENV_INFO_CACHE["data"] = "some data"
        main._ENV_INFO_CACHE["ts"] = 123.456
        
        # Call function
        packages = ["Pillow"]
        result = main.pip_install_packages(packages)
        
        # Verify
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["installed"], packages)
        
        # Verify cache was cleared
        self.assertIsNone(main._ENV_INFO_CACHE["data"])
        self.assertEqual(main._ENV_INFO_CACHE["ts"], 0.0)
        
        mock_run.assert_called_once_with(
            [sys.executable, "-m", "pip", "install", "Pillow"],
            capture_output=True,
            text=True,
            timeout=300
        )

    @patch('subprocess.run')
    @patch('main.logger')
    def test_pip_install_packages_error(self, mock_logger, mock_run):
        # Setup mock
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Could not find a version that satisfies the requirement invalid-package"
        mock_run.return_value = mock_result
        
        # Call function
        packages = ["invalid-package"]
        result = main.pip_install_packages(packages)
        
        # Verify
        self.assertEqual(result["status"], "error")
        self.assertIn("Could not find a version", result["error"])

    @patch('subprocess.run')
    @patch('main.logger')
    def test_pip_install_packages_empty(self, mock_logger, mock_run):
        # Call function with empty list
        result = main.pip_install_packages([])
        
        # Verify
        self.assertEqual(result["status"], "ok")
        mock_run.assert_not_called()

if __name__ == '__main__':
    unittest.main()
