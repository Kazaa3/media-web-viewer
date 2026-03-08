#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: FFprobe Duration Extraction
# Eingabewerte: media/01-02-Oscar_Peterson-Easy_Does_It-LLS.m4a
# Ausgabewerte: FFprobe duration in Sekunden
# Testdateien: media/01-02-Oscar_Peterson-Easy_Does_It-LLS.m4a
# Kommentar: Testet FFprobe Stream-Duration-Extraktion aus M4A-Datei (subprocess mit Timeout, Error Handling).
"""
================================================================================
FFprobe Duration Extraction Test - Media Web Viewer
================================================================================

KATEGORIE:
----------
FFprobe Duration Extraction

ZWECK:
------
Validiert die FFprobe-basierte Dauer-Extraktion für ALAC-Dateien.
Schneller Funktionstest für FFprobe zum Auslesen der Spieldauer.

EINGABEWERTE:
-------------
- ALAC Dateien (media/sample.alac)
- FFprobe-Kommandozeilen-Parameter

AUSGABEWERTE:
-------------
- Dauer in Sekunden (stdout)
- Format: Dezimalzahl (z.B. "243.52")

TESTDATEIEN:
------------
- media/sample.alac (benötigt für Test)

ERWEITERUNGEN (TODO):
---------------------
- [ ] Teste verschiedene Audio-Formate (MP3, OPUS, M4B)
- [ ] Teste Fehlerbehandlung (fehlende Dateien)
- [ ] Füge pytest-Struktur hinzu
- [ ] Teste ungültige Dateien
- [ ] Vergleiche mit Mutagen-Ergebnissen

VERWENDUNG:
-----------
    python tests/test_stream.py
"""

import subprocess
import sys
from pathlib import Path


def test_ffprobe_duration_extraction():
    """
    @brief Test FFprobe duration extraction for ALAC files.
    @details Validates that FFprobe correctly extracts duration metadata.
    """
    media_file = Path("media/01-02-Oscar_Peterson-Easy_Does_It-LLS.m4a")
    
    if not media_file.exists():
        print(f"❌ Testdatei nicht gefunden: {media_file}")
        print("   Test FEHLGESCHLAGEN (Datei fehlt).")
        return False
    
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(media_file)
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        duration = result.stdout.strip()
        
        if duration and float(duration) > 0:
            print(f"✅ FFprobe Duration Extraction: {duration}s")
            return True
        else:
            print(f"❌ Keine gültige Dauer extrahiert: '{duration}'")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ FFprobe Timeout (>10s)")
        return False
    except FileNotFoundError:
        print("❌ FFprobe nicht installiert")
        print("   Installiere mit: sudo apt install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False


if __name__ == "__main__":
    success = test_ffprobe_duration_extraction()
    sys.exit(0 if success else 1)
