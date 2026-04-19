import unittest
import os
import subprocess
from pathlib import Path

# Fix paths for imports
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

class TestEnvironmentDeploy(unittest.TestCase):
    """
    DEPLOYMENT & ENVIRONMENT VERIFICATION SUITE
    Verifies that all required packages, binaries, and archives are present.
    """

    def test_package_structure(self):
        """Verifies the reorganized packages/ directory layout."""
        pkg_root = PROJECT_ROOT / "packages"
        self.assertTrue(pkg_root.exists(), "packages/ directory missing")
        
        subdirs = ["src", "bin", "deb"]
        for sd in subdirs:
            self.assertTrue((pkg_root / sd).exists(), f"Missing subdirectory: packages/{sd}")

    def test_source_archives(self):
        """Checks for essential source archives in packages/src."""
        src_dir = PROJECT_ROOT / "packages" / "src"
        files = list(src_dir.glob("Python-*.tgz"))
        self.assertGreater(len(files), 0, "Python source archive missing in packages/src")

    def test_binaries_archives(self):
        """Checks for pre-compiled binaries in packages/bin."""
        bin_dir = PROJECT_ROOT / "packages" / "bin"
        files = list(bin_dir.glob("mediamtx_*.tar.gz"))
        self.assertGreater(len(files), 0, "MediaMTX binary archive missing in packages/bin")

    def test_system_dependencies(self):
        """Checks for required system tools via command line."""
        tools = ["ffmpeg", "ffprobe", "mediainfo", "doxygen", "google-chrome"]
        for tool in tools:
            # google-chrome command might vary (google-chrome-stable)
            cmd = tool if tool != "google-chrome" else "google-chrome-stable"
            res = subprocess.run(["which", cmd], capture_output=True)
            self.assertEqual(res.returncode, 0, f"System tool missing: {tool}")

    def test_venv_integrity(self):
        """Verifies that core Python packages are importable."""
        core_deps = ["eel", "bottle", "mutagen", "psutil", "bs4"]
        for dep in core_deps:
            try:
                __import__(dep)
            except ImportError:
                self.fail(f"Required Python dependency missing: {dep}")

    def test_gitignore_coverage(self):
        """Ensures that the new packages/ subdirectories are still ignored."""
        gitignore = (PROJECT_ROOT / ".gitignore").read_text()
        self.assertIn("/packages/", gitignore, ".gitignore missing /packages/ entry")

if __name__ == "__main__":
    unittest.main()
