#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: ISO / Disk / Spezialfälle
# Eingabewerte: src/core/models.py, media_parser, verschiedene ISO/BIN-Dateien
# Ausgabewerte: Validierung der Disk-Kategorisierung und Speziallogik
# Testdateien: src/core/models.py
# ERWEITERUNGEN (TODO): [ ] Erweiterung auf weitere Spezialfälle, [ ] Fehlerfall-Tests
# KOMMENTAR: Testet Spezialfälle für Disk-Kategorisierung.
# VERWENDUNG: python3 tests/iso/test_special_disks.py
"""
Special Disk Categorization Test Suite (DE/EN)
==============================================

DE:
Testet Spezialfälle für Disk-Kategorisierung.

EN:
Tests special cases for disk categorization.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path

from src.core.models import MediaItem

class TestSpecialDisks(unittest.TestCase):
    """
    DE:
    Testet Spezialfälle für Disk-Kategorisierung.

    EN:
    Tests special cases for disk categorization.
    """
    def test_pc_game_detection_by_volid(self):
        """Test detection of PC games using Volume ID in tags."""
        p = Path("/tmp/s3gold.iso")
        tags = {'pycdlib_volume_id': 'S3GOLD1_G'}
        
        # Mock extract_metadata to return our tags
        with patch('src.parsers.media_parser.extract_metadata', return_value=(0, tags)):
            # Mock logical_type to 'Abbild'
            with patch.object(MediaItem, 'detect_logical_type', return_value='Abbild'):
                item = MediaItem("s3gold.iso", p)
                self.assertEqual(item.category, 'Spiel')

    def test_pc_game_detection_by_path(self):
        """Test detection of PC games using keywords in path."""
        p = Path("/home/user/games/the_sims.bin")
        
        with patch('src.parsers.media_parser.extract_metadata', return_value=(0, {})):
            with patch.object(MediaItem, 'detect_logical_type', return_value='Abbild'):
                item = MediaItem("the_sims.bin", p)
                self.assertEqual(item.category, 'Spiel')

    def test_book_disc_detection(self):
        """Test detection of book-accompanying discs."""
        p = Path("/usb/backup/Beigabe_Buch_Python_Programming.iso")
        
        with patch('src.parsers.media_parser.extract_metadata', return_value=(0, {})):
            with patch.object(MediaItem, 'detect_logical_type', return_value='Abbild'):
                item = MediaItem("Beigabe_Buch_Python_Programming.iso", p)
                self.assertEqual(item.category, 'Beigabe')

    def test_dvd_iso_categorization(self):
        """Test that ISO with PAL volid or VIDEO_TS structure is categorized as DVD/Film."""
        p = Path("/tmp/video_dvd.iso")
        tags = {'pycdlib_volume_id': 'MY_PAL_DVD'}
        
        with patch('src.parsers.media_parser.extract_metadata', return_value=(0, tags)):
            with patch.object(MediaItem, 'detect_logical_type', return_value='Abbild'):
                item = MediaItem("video_dvd.iso", p)
                # content_type will be PAL DVD, category will be PAL DVD
                self.assertEqual(item.content_type, 'PAL DVD')
                self.assertIn('DVD', item.category)

    def test_generic_disk_image(self):
        """Test that generic disk images still fall back to 'Abbild'."""
        p = Path("/data/backup_linux.img")
        
        with patch('src.parsers.media_parser.extract_metadata', return_value=(0, {})):
            with patch.object(MediaItem, 'detect_logical_type', return_value='Abbild'):
                item = MediaItem("backup_linux.img", p)
                self.assertEqual(item.category, 'Abbild')

if __name__ == '__main__':
    unittest.main()
