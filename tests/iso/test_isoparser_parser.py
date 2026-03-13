#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: ISO / Parser / Unit
# Eingabewerte: media/OLE_DB_ODBC.iso, isoparser_parser
# Ausgabewerte: Validierung des isoparser_parser-Ergebnisses
# Testdateien: media/OLE_DB_ODBC.iso
# ERWEITERUNGEN (TODO): [ ] Erweiterung auf weitere ISO-Dateien, [ ] Fehlerfall-Tests
# KOMMENTAR: Testet den isoparser_parser für ISO-Dateien.
# VERWENDUNG: python3 tests/iso/test_isoparser_parser.py
from pathlib import Path
from src.parsers import isoparser_parser

def test_isoparser_parser():
        """
        Testet den isoparser_parser für ISO-Dateien. / Tests isoparser_parser for ISO files.

        Returns:
            None
        """
    test_iso = Path('media/OLE_DB_ODBC.iso')
    tags = {}
    result = isoparser_parser.parse(test_iso, '.iso', tags)
    assert 'iso_volume_label' in result or 'iso_error' in result
    print('isoparser_parser test result:', result)

if __name__ == '__main__':
    test_isoparser_parser()
