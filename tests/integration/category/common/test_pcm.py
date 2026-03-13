#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: PCM Bit-Depth Detection
# Eingabewerte: PCM WAV-Dateien (16-bit und 24-bit)
# Ausgabewerte: Bit-Depth (16, 24) von parsers.ffmpeg_parser
# Testdateien: Zwei spezifische WAV-Dateien
# Kommentar: Testet PCM Bit-Depth-Erkennung für 16-bit und 24-bit WAV-Dateien (ffmpeg_parser mit Missing-File-Handling).
"""
================================================================================
PCM Audio Bit-Depth Test - Media Web Viewer
================================================================================

KATEGORIE:
----------
Audio Bit-Depth Test

ZWECK:
------
Validiert die Bit-Depth-Erkennung für PCM-Audio (WAV) durch den FFmpeg-Parser.
Prüft ob 16-bit, 24-bit und 32-bit korrekt identifiziert werden.

EINGABEWERTE:
-------------
- WAV Dateien (16-bit, 24-bit)
- media/*.wav als Test-Dateien
- FFmpeg-Parser-Modul

AUSGABEWERTE:
-------------
- Korrekte Bit-Depth Metadaten ('16 Bit', '24 Bit', '32 Bit')
- Parser-Ergebnisse mit vollständigen Metadaten

TESTDATEIEN:
------------
- media/20-The Emerald Abyss.wav (24-bit)
- media/02 Ludwig van Beethoven - Piano Concerto No. 5... .wav (16-bit)

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste 8-bit, 32-bit, 32-bit float
- [ ] Teste verschiedene Sample-Rates (44.1kHz, 48kHz, 96kHz, 192kHz)
- [ ] Teste Mono vs Stereo vs Multichannel
- [ ] Teste signierte vs unsignierte PCM
- [ ] Füge pytest-Struktur mit assertEqual hinzu
- [ ] Teste FLAC und andere verlustfreie Formate

VERWENDUNG:
-----------
    python tests/test_pcm.py
"""

import sys
from pathlib import Path

# Add parent directory to path for parser imports

try:
    from src.parsers import ffmpeg_parser
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False

def test_pcm_bitdepth_detection():
    """
    @brief Test PCM bit-depth detection for WAV files.
    @details Validates that FFmpeg parser correctly identifies 16-bit and 24-bit audio.
    """
    if not PARSER_AVAILABLE:
        print("❌ FFmpeg-Parser nicht verfügbar")
        return False
    
    # Test files
    file_24bit = Path("media/20-The Emerald Abyss.wav")
    file_16bit = Path("media/02 Ludwig van Beethoven - Piano Concerto No. 5 in E-flat major, "
                      "Op. 73 ''Emperor''- II. Adagio un poco mosso.wav")
    
    # Check if files exist
    missing = []
    if not file_24bit.exists():
        missing.append(str(file_24bit))
    if not file_16bit.exists():
        missing.append(str(file_16bit))
    
    if missing:
        print(f"❌ Testdateien nicht gefunden:")
        for f in missing:
            print(f"   - {f}")
        print("   Test FEHLGESCHLAGEN (Dateien fehlen).")
        return False
    
    print("\n🎵 PCM Bit-Depth Detection Test\n")
    
    # Test 24-bit
    try:
        tags_24 = {'codec': 'wav', 'bitdepth': '24 Bit'}
        res_24 = ffmpeg_parser.parse(file_24bit, ".wav", tags_24)
        
        if res_24 and '24' in str(res_24.get('bitdepth', '')):
            print(f"✅ 24-bit: {file_24bit.name}")
            print(f"   Result: {res_24.get('bitdepth', 'N/A')}")
            test_24_passed = True
        else:
            print(f"❌ 24-bit: Erwartet '24 Bit', Erhalten: {res_24.get('bitdepth', 'N/A')}")
            test_24_passed = False
    except Exception as e:
        print(f"❌ 24-bit Test fehlgeschlagen: {e}")
        test_24_passed = False
    
    # Test 16-bit
    try:
        tags_16 = {'codec': 'wav', 'bitdepth': '16 Bit'}
        res_16 = ffmpeg_parser.parse(file_16bit, ".wav", tags_16)
        
        if res_16 and '16' in str(res_16.get('bitdepth', '')):
            print(f"✅ 16-bit: {file_16bit.name[:60]}...")
            print(f"   Result: {res_16.get('bitdepth', 'N/A')}")
            test_16_passed = True
        else:
            print(f"❌ 16-bit: Erwartet '16 Bit', Erhalten: {res_16.get('bitdepth', 'N/A')}")
            test_16_passed = False
    except Exception as e:
        print(f"❌ 16-bit Test fehlgeschlagen: {e}")
        test_16_passed = False
    
    # Final result
    if test_24_passed and test_16_passed:
        print("\n✅ Alle PCM Bit-Depth Tests bestanden")
        return True
    else:
        print("\n❌ Einige Tests fehlgeschlagen")
        return False

if __name__ == "__main__":
    success = test_pcm_bitdepth_detection()
    sys.exit(0 if success else 1)
