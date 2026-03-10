import unittest
from pathlib import Path
import os

MEDIA_DIR = Path(__file__).parent.parent / "media"
ISO_SIZE_LIMIT_MB = 5000  # 5 GB

class TestMediaScan(unittest.TestCase):
    def test_scan_media_directory(self):
        self.assertTrue(MEDIA_DIR.exists(), "media directory does not exist")
        files = list(MEDIA_DIR.glob("*"))
        self.assertIsInstance(files, list)
        # At least one file or empty is valid

    def test_iso_size_protection(self):
        iso_files = list(MEDIA_DIR.glob("*.iso"))
        for iso in iso_files:
            size_mb = iso.stat().st_size / (1024 * 1024)
            self.assertLessEqual(size_mb, ISO_SIZE_LIMIT_MB,
                f"ISO file {iso.name} exceeds {ISO_SIZE_LIMIT_MB} MB limit ({size_mb:.2f} MB)")

if __name__ == '__main__':
    unittest.main()
