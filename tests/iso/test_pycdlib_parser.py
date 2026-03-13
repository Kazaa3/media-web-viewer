#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: ISO / Parser / Unit
# Eingabewerte: ../../media/test.iso, pycdlib
# Ausgabewerte: Validierung des pycdlib-Parser-Ergebnisses
# Testdateien: ../../media/test.iso
# ERWEITERUNGEN (TODO): [ ] Erweiterung auf weitere ISO-Dateien, [ ] Fehlerfall-Tests
# KOMMENTAR: Testet den pycdlib-Parser für ISO-Dateien.
# VERWENDUNG: python3 tests/iso/test_pycdlib_parser.py
"""
Pycdlib Parser Unit Test Suite (DE/EN)
======================================

DE:
Testet den pycdlib-Parser für ISO-Dateien.

EN:
Tests pycdlib parser for ISO files.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

import pycdlib

def test_pycdlib_parser():
        """
        Testet den pycdlib-Parser für ISO-Dateien. / Tests pycdlib parser for ISO files.

        Returns:
            None
        """
    test_iso = Path('../../media/test.iso')
    tags = {}
    try:
        iso = pycdlib.PyCdlib()
        iso.open(str(test_iso))
        tags['pycdlib_volume_id'] = iso.get_volume_id()
        iso.close()
    except Exception as e:
        tags['pycdlib_error'] = str(e)
    print('pycdlib_parser test result:', tags)

if __name__ == '__main__':
    test_pycdlib_parser()
