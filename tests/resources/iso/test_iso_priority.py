#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: ISO / Parser / Priority
# Eingabewerte: src/parsers/media_parser.py, src/parsers/format_utils.py
# Ausgabewerte: Validierung der Parser-Priorität für ISO-Dateien
# Testdateien: src/parsers/media_parser.py, src/parsers/format_utils.py
# ERWEITERUNGEN (TODO): [ ] Erweiterung auf weitere Formate, [ ] Fehlerfall-Tests
# KOMMENTAR: Testet die Priorität von pycdlib und isoparser.
# VERWENDUNG: python3 tests/iso/test_iso_priority.py

"""
KATEGORIE: ISO / Parser / Priority
ZWECK: Testet die Priorität von pycdlib und isoparser für ISO-Dateien im Parser-Modul.
EINGABEWERTE: src/parsers/media_parser.py, src/parsers/format_utils.py
AUSGABEWERTE: Validierung der Parser-Priorität für ISO-Dateien
TESTDATEIEN: src/parsers/media_parser.py, src/parsers/format_utils.py
ERWEITERUNGEN (TODO): [ ] Erweiterung auf weitere Formate, [ ] Fehlerfall-Tests
KOMMENTAR: Testet die Priorität von pycdlib und isoparser.
VERWENDUNG: python3 tests/iso/test_iso_priority.py
"""

import unittest
from src.parsers.media_parser import PARSER_MAPPING
from src.parsers.format_utils import PARSER_CONFIG

class TestISOPriority(unittest.TestCase):
    """
    DE:
    Testet die Priorität von pycdlib und isoparser für ISO-Dateien.

    EN:
    Tests priority of pycdlib and isoparser for ISO files.
    """
    def test_mapping_priority(self):
        """Ensures pycdlib comes before isoparser in the .iso mapping."""
        mapping = PARSER_MAPPING.get(".iso", [])
        self.assertIn("pycdlib", mapping)
        self.assertIn("isoparser", mapping)
        
        pycd_idx = mapping.index("pycdlib")
        iso_idx = mapping.index("isoparser")
        
        self.assertLess(pycd_idx, iso_idx, "pycdlib should have higher priority than isoparser in mapping")

    def test_chain_priority(self):
        """Ensures pycdlib comes before isoparser in the global parser chain."""
        print(f"DEBUG: PARSER_CONFIG={PARSER_CONFIG}")
        chain = PARSER_CONFIG.get("parser_chain", [])
        print(f"DEBUG: chain={chain}")
        self.assertIn("pycdlib", chain)
        self.assertIn("isoparser", chain)
        
        pycd_idx = chain.index("pycdlib")
        iso_idx = chain.index("isoparser")
        
        self.assertLess(pycd_idx, iso_idx, "pycdlib should have higher priority than isoparser in chain")

if __name__ == "__main__":
    unittest.main()
