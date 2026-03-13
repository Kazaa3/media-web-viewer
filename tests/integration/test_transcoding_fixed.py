# =============================================================================
# Kategorie: FFmpeg Transcoding Fix Test
# Eingabewerte: app_bottle.py, models.py, Logbuch 52
# Ausgabewerte: Transcoding-Status, Fehlerbehandlung, Log-Einträge
# Testdateien: test_transcoding_fixed.py
# Kommentar: Testet die Behebung des Transcoding-Bugs und Optimierung.
# Startbefehl: pytest tests/test_transcoding_fixed.py -v
# =============================================================================
"""
FFmpeg Transcoding Fix Test Suite (DE/EN)
=========================================

DE:
Testet die Behebung des Transcoding-Bugs und die Optimierung der Parameter für FFmpeg und ALAC-Erkennung.

EN:
Tests the fix for the transcoding bug and optimization of parameters for FFmpeg and ALAC detection.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0

Startbefehl/Run command:
    pytest tests/test_transcoding_fixed.py -v
"""

import pytest
import re
from pathlib import Path

def test_01_app_bottle_no_transcode_format_bug():
    """
    Ensure the 'transcode_format = None' bug is removed from app_bottle.py
    """
    app_bottle_path = Path(__file__).parents[3] / 'web' / 'app_bottle.py'
    content = app_bottle_path.read_text()
    
    # Check for duplicate detection code
    transcode_detections = content.count("if filepath.endswith('.flac_transcoded'):")
    assert transcode_detections == 1, f"Expected 1 detection block, found {transcode_detections} (duplicate code?)"
    
    # Check that 'transcode_format = None' does not appear after detection
    lines = content.splitlines()
    detection_line = None
    none_assignment_line = None
    
    for i, line in enumerate(lines):
        if "filepath.endswith('.flac_transcoded')" in line:
            detection_line = i
        if detection_line and i > detection_line and "transcode_format = None" in line:
            none_assignment_line = i
            break
    
    assert none_assignment_line is None, \
        f"Bug still exists: 'transcode_format = None' found after detection at line {none_assignment_line}"

def test_02_ffmpeg_optimized_parameters():
    """
    Verify that FFmpeg uses optimized parameters for transcoding
    """
    app_bottle_path = Path(__file__).parents[3] / 'web' / 'app_bottle.py'
    content = app_bottle_path.read_text()
    
    # Check for FLAC optimization
    assert '-c:a' in content or '-c:a flac' in content, "Missing explicit audio codec"
    assert '-compression_level' in content, "Missing compression_level parameter"
    
    # Check for audio stream mapping (can be '-map 0:a:0' or as list ['-map', '0:a:0'])
    has_map_flag = "'-map'" in content or '"-map"' in content
    has_audio_stream = "'0:a:0'" in content or '"0:a:0"' in content
    assert has_map_flag and has_audio_stream, "Missing audio stream mapping"
    
    # Check for Opus optimization
    assert 'libopus' in content, "Missing Opus codec"
    assert '-vbr' in content, "Missing VBR flag for Opus"

def test_03_error_handling_improvements():
    """
    Validate improved error handling in transcoding logic
    """
    app_bottle_path = Path(__file__).parents[3] / 'web' / 'app_bottle.py'
    content = app_bottle_path.read_text()
    
    # Check for timeout parameter
    assert 'timeout=' in content, "Missing timeout parameter for subprocess"
    
    # Check for TimeoutExpired handling
    assert 'TimeoutExpired' in content, "Missing timeout exception handling"
    
    # Check for output validation
    assert '.stat().st_size' in content or 'st_size' in content, \
        "Missing output file size validation"

def test_04_logbuch_52_created():
    """
    Ensure Logbuch 52 documentation exists
    """
    logbuch_path = Path(__file__).parents[3] / 'logbuch' / '52_FFmpeg_Transcoding_Fix_and_Optimization.md'
    assert logbuch_path.exists(), "Logbuch 52 not found"
    
    content = logbuch_path.read_text()
    assert 'Root Cause Analysis' in content, "Missing RCA section"
    assert 'FFmpeg-Optimierung' in content or 'FFmpeg Optimization' in content, "Missing optimization section"
    assert 'FFprobe' in content, "Missing future optimization (FFprobe)"

def test_05_transcoding_models_integration():
    """
    Verify that models.py correctly detects ALAC files for transcoding
    """
    models_path = Path(__file__).parents[3] / 'src.core.models.py'
    content = models_path.read_text()
    
    # Check ALAC detection logic
    assert "'ALAC' in codec" in content or '"ALAC" in codec' in content, \
        "ALAC detection missing in models.py"
    
    # Check transcoded_format assignment
    assert "transcoded_format = 'FLAC'" in content, \
        "FLAC transcoding format not set for ALAC files"
    
    # Check is_transcoded flag
    assert 'is_alac or is_wma' in content, \
        "Transcoding flag logic incomplete"

def test_06_serve_media_logging():
    """
    Ensure proper logging is added for debugging transcoding issues
    """
    app_bottle_path = Path(__file__).parents[3] / 'web' / 'app_bottle.py'
    content = app_bottle_path.read_text()
    
    # Check for detailed transcoding logging
    assert 'needs_transcoding=' in content, "Missing transcoding status logging"
    assert 'TRANSCODING SUCCESS' in content, "Missing success log"
    assert 'TRANSCODING FAILED' in content or 'Transcoding failed' in content, \
        "Missing failure log"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
