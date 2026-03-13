#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Parser Test
# Eingabewerte: Dateinamen, Pfade
# Ausgabewerte: Extrahierte Tags (Artist, Title)
# Testdateien: Keine (Dateinamen-Simulation)
# Kommentar: Prüft die RegEx-basierte Extraktion von Metadaten aus Dateinamen (filename_parser.py Modul).
"""
================================================================================
Filename Parser Logic Test - Media Web Viewer
================================================================================

KATEGORIE:
----------
Parser Test

ZWECK:
------
Validiert die RegEx-basierte Extraktion von Metadaten aus Dateinamen.
Prüft filename_parser.py Modul-Funktionalität.

EINGABEWERTE:
-------------
- Dateinamen (simuliert)
- Pfade (Path-Objekte)
- Leere Tag-Dictionaries

AUSGABEWERTE:
-------------
- Extrahierte Tags:
  - artist (Künstler)
  - title (Titel)
  - album (optional)
  - track (optional)

TESTDATEIEN:
------------
- Keine (Dateinamen-Simulation)

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste alle Parser-Helper-Funktionen
- [ ] Teste Parser-Selection-Logic (welcher Parser für welches Format)
- [ ] Teste Fallback-Mechanismen
- [ ] Füge pytest-Struktur hinzu mit assertEqual
- [ ] Teste komplexe Dateinamen:
  - "01. Artist - Title (feat. Guest) [Remix].mp3"
  - "Track 12 - Artist feat. Other - Title (Radio Edit).flac"
  - "CD1/02 - Band Name - Song Title.m4a"
- [ ] Teste Unicode und Sonderzeichen
- [ ] Teste sehr lange Dateinamen
- [ ] Mock-Tests für alle Parser-Module

VERWENDUNG:
-----------
    python tests/test_parser_logic.py
"""

import sys
import os
from pathlib import Path

# Add project root to path

try:
    from src.parsers import filename_parser
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False

def test_filename_parser_simple():
    """
    @brief Test simple filename parsing (Artist - Title.mp3).
    @details Validates basic artist/title extraction.
    """
    name = "Artist - Title.mp3"
    path = Path("/path/to/" + name)
    
    tags = filename_parser.parse(path, file_type="unknown", tags={}, filename=name)
    
    artist_ok = 'artist' in tags and "Artist" in tags['artist']
    title_ok = 'title' in tags and "Title" in tags['title']
    
    if artist_ok and title_ok:
        print(f"✅ Simple: {name}")
        print(f"   Artist: {tags.get('artist', 'N/A')}")
        print(f"   Title:  {tags.get('title', 'N/A')}")
        return True
    else:
        print(f"❌ Simple: {name}")
        print(f"   Artist: {tags.get('artist', 'MISSING')} (erwartet: 'Artist')")
        print(f"   Title:  {tags.get('title', 'MISSING')} (erwartet: 'Title')")
        return False

def test_filename_parser_complex():
    """
    @brief Test complex filename parsing (with track number and extras).
    @details Validates handling of leading numbers and parentheticals.
    """
    name = "01-Artist - Title (Remix).flac"
    path = Path("/path/to/" + name)
    
    tags = filename_parser.parse(path, file_type="unknown", tags={}, filename=name)
    
    artist_ok = 'artist' in tags and "Artist" in str(tags['artist'])
    title_ok = 'title' in tags and "Title" in str(tags['title'])
    
    if artist_ok and title_ok:
        print(f"✅ Complex: {name}")
        print(f"   Artist: {tags.get('artist', 'N/A')}")
        print(f"   Title:  {tags.get('title', 'N/A')}")
        return True
    else:
        print(f"❌ Complex: {name}")
        print(f"   Artist: {tags.get('artist', 'MISSING')} (sollte 'Artist' enthalten)")
        print(f"   Title:  {tags.get('title', 'MISSING')} (sollte 'Title' enthalten)")
        return False

def test_filename_parser():
    """
    @brief Run all filename parser tests.
    @details Tests various filename patterns and edge cases.
    """
    if not PARSER_AVAILABLE:
        print("❌ Filename-Parser nicht verfügbar")
        print("   Stelle sicher, dass parsers/filename_parser.py existiert.")
        return False
    
    print("\n📝 Filename Parser Logic Test\n")
    
    tests = [
        ("Simple Pattern", test_filename_parser_simple),
        ("Complex Pattern", test_filename_parser_complex),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}: Exception - {e}")
            failed += 1
        print()
    
    print(f"{'='*60}")
    print(f"Tests: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ Alle Filename Parser Tests bestanden")
        return True
    else:
        print(f"❌ {failed} Test(s) fehlgeschlagen")
        return False

if __name__ == "__main__":
    success = test_filename_parser()
    sys.exit(0 if success else 1)
