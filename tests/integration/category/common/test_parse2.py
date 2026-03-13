#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: MediaItem Metadata Extraction
# Eingabewerte: AAC Dateien in /media
# Ausgabewerte: Samplerate, Bitrate, Dateigröße, Codec, TagType
# Testdateien: media/*.aac
# Kommentar: Gezielter Test der Metadaten-Extraktion für das AAC-Containerformat (MediaItem-Klasse mit Parser-Integration).
"""
================================================================================
MediaItem Metadata Extraction Test (AAC) - Media Web Viewer
================================================================================

KATEGORIE:
----------
MediaItem Metadata Extraction

ZWECK:
------
Gezielter Test der Metadaten-Extraktion für AAC-Container-Format.
Validiert MediaItem-Klasse und Parser-Integration.

EINGABEWERTE:
-------------
- AAC Dateien in /media
- MediaItem-Klasse
- Parser-System

AUSGABEWERTE:
-------------
- Samplerate (z.B. 44100 Hz)
- Bitrate (z.B. 128 kb/s)
- Dateigröße (bytes)
- Codec (aac)
- TagType (ID3, AAC, etc.)

TESTDATEIEN:
------------
- media/*.aac

ERWEITERUNGEN (TODO):
---------------------
- [ ] Erweitere zu umfassender Parser-Suite
- [ ] Teste alle unterstützten Formate (MP3, OPUS, M4B, FLAC)
- [ ] Füge Assertions hinzu (assertEqual)
- [ ] Teste Fehlerbehandlung für beschädigte Dateien
- [ ] Vergleiche Parser-Ergebnisse (FFmpeg vs Mutagen vs Pymediainfo)
- [ ] Benchmark Parser-Performance
- [ ] Füge pytest-Struktur hinzu

VERWENDUNG:
-----------
    python tests/test_parse2.py
"""

import os
import glob
import sys
from pathlib import Path

# Add project root to path

try:
    from src.core.main import MediaItem
    MEDIAITEM_AVAILABLE = True
except ImportError:
    MEDIAITEM_AVAILABLE = False

def test_aac_metadata_extraction():
    """
    @brief Test metadata extraction for AAC files.
    @details Validates MediaItem class and parser integration for AAC format.
    """
    if not MEDIAITEM_AVAILABLE:
        print("❌ MediaItem nicht importierbar")
        print("   Stelle sicher, dass main.py vorhanden ist.")
        return False
    
    media_dir = Path('media')
    
    if not media_dir.exists():
        print(f"❌ Media-Verzeichnis nicht gefunden: {media_dir}")
        print("   Test FEHLGESCHLAGEN (Verzeichnis fehlt).")
        return False
    
    # Find AAC files
    aac_files = list(media_dir.glob('*.aac'))
    
    if not aac_files:
        print("❌ Keine AAC-Dateien gefunden in media/")
        print("   Test FEHLGESCHLAGEN (Dateien fehlen).")
        return False
    
    print(f"\n🎵 AAC Metadata Extraction Test\n")
    print(f"Gefundene AAC-Dateien: {len(aac_files)}\n")
    
    success_count = 0
    
    for file_path in aac_files:
        name = file_path.name
        
        try:
            media_item = MediaItem(name, file_path)
            tags = media_item.tags
            
            samplerate = tags.get('samplerate', 'MISSING')
            bitrate = tags.get('bitrate', 'MISSING')
            filesize = tags.get('filesize', 'MISSING')
            codec = tags.get('codec', 'MISSING')
            tagtype = tags.get('tagtype', 'MISSING')
            
            print(f"✅ {name}")
            print(f"   Samplerate: {samplerate}")
            print(f"   Bitrate:    {bitrate}")
            print(f"   Filesize:   {filesize}")
            print(f"   Codec:      {codec}")
            print(f"   TagType:    {tagtype}")
            print()
            
            # Basic validation - mindestens ein wichtiges Feld sollte vorhanden sein
            if samplerate != 'MISSING' or bitrate != 'MISSING' or codec != 'MISSING':
                success_count += 1
            
        except Exception as e:
            print(f"❌ {name}: Fehler - {e}\n")
    
    print(f"\n{'='*60}")
    print(f"Erfolgreich geparst: {success_count}/{len(aac_files)}")
    
    if success_count > 0:
        print("✅ AAC Metadata Extraction funktioniert")
        return True
    else:
        print("❌ Keine Dateien erfolgreich geparst")
        return False

if __name__ == "__main__":
    success = test_aac_metadata_extraction()
    sys.exit(0 if success else 1)
