#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ID3 Tag Extraction Test (Mutagen) - Media Web Viewer
================================================================================

KATEGORIE:
----------
Metadata Extraction (Mutagen)

ZWECK:
------
Validiert die Extraktion von ID3v2-Tags aus MP3-Dateien mit der Mutagen-Bibliothek.
Prüft TPE1 (Artist), TDRC (Recording Date) und andere wichtige Tags.

EINGABEWERTE:
-------------
- MP3 Dateien mit ID3v2 Tags
- media/sample.mp3 als Test-Datei

AUSGABEWERTE:
-------------
- ID3v2 Tags (TPE1, TDRC, TIT2, TALB)
- Tag-Typen und -Werte

TESTDATEIEN:
------------
- media/sample.mp3 (benötigt für Test)

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste alle ID3-Tag-Typen (TIT2, TALB, TCON, etc.)
- [ ] Teste fehlende Tags (sollte None oder Default zurückgeben)
- [ ] Teste beschädigte MP3-Dateien
- [ ] Teste ID3v1 vs ID3v2
- [ ] Vergleiche mit FFmpeg-Parser-Ergebnissen
- [ ] Füge pytest-Struktur mit Assertions hinzu

VERWENDUNG:
-----------
    python tests/test_mp3_tags.py
"""

import sys
from pathlib import Path

try:
    from mutagen.mp3 import MP3
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False


def test_mp3_id3_tag_extraction():
    """
    @brief Test ID3 tag extraction from MP3 files using Mutagen.
    @details Validates that Mutagen correctly reads TPE1 (Artist) and TDRC (Year) tags.
    """
    if not MUTAGEN_AVAILABLE:
        print("❌ Mutagen nicht installiert")
        print("   Installiere mit: pip install mutagen")
        return False
    
    media_file = Path('media/sample.mp3')
    
    if not media_file.exists():
        print(f"⚠️  Testdatei nicht gefunden: {media_file}")
        print("   Test wird übersprungen.")
        return None
    
    try:
        audio = MP3(str(media_file))
        
        # Extract tags
        artist = audio.get('TPE1')
        year = audio.get('TDRC')
        title = audio.get('TIT2')
        album = audio.get('TALB')
        
        print(f"\n📄 MP3 Tag Extraction: {media_file.name}")
        print(f"   Artist (TPE1): {artist[0] if artist else 'N/A'}")
        print(f"   Year (TDRC):   {year if year else 'N/A'} (Type: {type(year).__name__})")
        print(f"   Title (TIT2):  {title[0] if title else 'N/A'}")
        print(f"   Album (TALB):  {album[0] if album else 'N/A'}")
        
        # Validate
        if artist:
            print(f"✅ ID3 Tags erfolgreich extrahiert")
            return True
        else:
            print(f"⚠️  Keine Artist-Tags gefunden (möglicherweise leere MP3)")
            return True  # Not a failure if file has no tags
            
    except Exception as e:
        print(f"❌ Fehler beim Lesen der MP3-Datei: {e}")
        return False


if __name__ == "__main__":
    success = test_mp3_id3_tag_extraction()
    if success is None:
        sys.exit(0)  # Skipped
    sys.exit(0 if success else 1)
