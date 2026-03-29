import unittest
from pathlib import Path
from src.parsers.format_utils import detect_file_format

class TestImageDifferentiation(unittest.TestCase):
    def test_dvd_detection(self):
        # 4_KOENIGE.iso is 6.8GB -> DVD
        p = Path("./media/4 Könige (2015) - DVD/4_KOENIGE.iso")
        if p.exists():
            fmt = detect_file_format(p)
            self.assertEqual(fmt, "DVD (Abbild)")

    def test_small_dvd_detection(self):
        # Going Raw is 1.2GB -> DVD
        p = Path("./media/Going Raw - JUDITA_169_OPTION.ISO")
        if p.exists():
            fmt = detect_file_format(p)
            self.assertEqual(fmt, "DVD (Abbild)")

    def test_cd_rom_detection(self):
        # 1411_c_von_a_bis.iso is 134MB -> CD-ROM
        p = Path("./media/1411_c_von_a_bis.iso")
        if p.exists():
            fmt = detect_file_format(p)
            self.assertEqual(fmt, "CD-ROM (Abbild)")

    def test_bin_detection(self):
        # S3gold1_g.bin is 735MB -> CD-ROM (heuristic)
        p = Path("./media/S3gold1_g.bin")
        if p.exists():
            fmt = detect_file_format(p)
            self.assertEqual(fmt, "CD-ROM (Abbild)")

    def test_small_image_detection(self):
        # OLE_DB_ODBC.iso is 24MB -> Disk-Abbild (too small for CD-ROM heuristic > 100MB)
        # Wait, my heuristic was > 0.1 GB (100MB). 24MB will be "Disk-Abbild"
        p = Path("./media/OLE_DB_ODBC.iso")
        if p.exists():
            fmt = detect_file_format(p)
            self.assertEqual(fmt, "Disk-Abbild")

if __name__ == "__main__":
    unittest.main()
