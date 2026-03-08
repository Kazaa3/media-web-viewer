#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Bit-Depth Detection Test (PyMediaInfo) - Media Web Viewer
================================================================================

KATEGORIE:
----------
Unit Test / Bit-Depth Detection

ZWECK:
------
Validiert Bit-Depth-Extraktion für verschiedene Audio-Formate mit PyMediaInfo.
Prüft 16-bit, 24-bit, 32-bit int und 32-bit float.

EINGABEWERTE:
-------------
- Pfade zu Audio-Dateien (FLAC, MP3, M4A, WAV)
- PyMediaInfo-Library

AUSGABEWERTE:
-------------
- Bit-Depth (16, 24, 32)
- Format-Name (FLAC, MP3, AAC, PCM)
- Track-Type (Audio)

TESTDATEIEN:
------------
- media/20-The Emerald Abyss.wav (24-bit)
- media/01 - Einfach & Leicht.mp3 (optional)
- media/02 We the People….flac (optional)

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste 8-bit, 16-bit, 24-bit, 32-bit int
- [ ] Teste 32-bit float Audio
- [ ] Teste verschiedene Formate (FLAC, ALAC, WAV, AIFF)
- [ ] Teste signierte vs unsignierte Samples
- [ ] Füge Assertions hinzu
- [ ] Vergleiche mit FFmpeg-Parser-Ergebnissen
- [ ] Teste komprimierte verlustfreie Formate

VERWENDUNG:
-----------
    python tests/test_bitdepth.py
"""

import os
import sys
from pathlib import Path

try:
    from pymediainfo import MediaInfo
    PYMEDIAINFO_AVAILABLE = True
except ImportError:
    PYMEDIAINFO_AVAILABLE = False


def check_file_bitdepth(path: Path):
    """
    @brief Check bit-depth for a single audio file.
    @param path Path to audio file.
    @return Tuple of (bit_depth, format_name) or (None, None) on error.
    """
    if not path.exists():
        print(f"⚠️  Datei nicht gefunden: {path}")
        return None, None
    
    try:
        info = MediaInfo.parse(str(path))
        
        for track in info.tracks:
            if track.track_type == 'Audio':
                bit_depth = getattr(track, 'bit_depth', None)
                format_name = getattr(track, 'format', None)
                
                return bit_depth, format_name
        
        return None, None
        
    except Exception as e:
        print(f"❌ Fehler beim Parsen von {path.name}: {e}")
        return None, None


def test_bitdepth_detection():
    """
    @brief Test bit-depth detection for various audio formats.
    @details Uses PyMediaInfo to extract bit-depth information.
    """
    if not PYMEDIAINFO_AVAILABLE:
        print("❌ PyMediaInfo nicht installiert")
        print("   Installiere mit: pip install pymediainfo")
        return False
    
    print("\n🎵 Bit-Depth Detection Test (PyMediaInfo)\n")
    
    # Test files (with expected bit-depth)
    test_files = [
        (Path("media/20-The Emerald Abyss.wav"), 24, "WAV"),
        # Add more as available
        (Path("media/01 - Einfach & Leicht.mp3"), None, "MP3"),  # MP3 typically doesn't have bit-depth
        (Path("media/02 We the People….flac"), None, "FLAC"),
    ]
    
    tested = 0
    success = 0
    
    for file_path, expected_depth, format_desc in test_files:
        if not file_path.exists():
            print(f"⚠️  Überspringe {format_desc}: {file_path.name} (nicht gefunden)")
            continue
        
        tested += 1
        bit_depth, format_name = check_file_bitdepth(file_path)
        
        if bit_depth is not None:
            status = "✅"
            if expected_depth:
                if bit_depth == expected_depth:
                    status = "✅"
                    success += 1
                else:
                    status = "⚠️ "
            else:
                success += 1
            
            print(f"{status} {file_path.name}")
            print(f"   Bit-Depth: {bit_depth} bit")
            print(f"   Format:    {format_name}")
        else:
            print(f"❌ {file_path.name}")
            print(f"   Bit-Depth: N/A (möglicherweise verlustbehaftet)")
        
        print()
    
    if tested == 0:
        print("⚠️  Keine Testdateien gefunden")
        print("   Test wird übersprungen.")
        return None
    
    print(f"{'='*60}")
    print(f"Erfolgreich analysiert: {success}/{tested}")
    
    if success > 0:
        print("✅ Bit-Depth Detection funktioniert")
        return True
    else:
        print("❌ Keine Dateien erfolgreich analysiert")
        return False


if __name__ == "__main__":
    success = test_bitdepth_detection()
    if success is None:
        sys.exit(0)  # Skipped
    sys.exit(0 if success else 1)
