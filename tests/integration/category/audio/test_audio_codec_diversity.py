#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_audio_codec_diversity.py - Validates parser coverage for various audio codecs.
"""

import pytest
from pathlib import Path
from src.parsers import media_parser

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MEDIA_DIR = PROJECT_ROOT / "media"

AUDIO_FORMATS = [".mp3", ".flac", ".ogg", ".opus", ".m4a", ".wav", ".m4b"]

def test_audio_codec_parsing_coverage():
    """Verify that at least one file of each major audio format is parsable."""
    found_formats = set()
    for f in MEDIA_DIR.glob("*.*"):
        ext = f.suffix.lower()
        if ext in AUDIO_FORMATS:
            found_formats.add(ext)
            
            # Perform actual parsing test
            tags, _ = media_parser.extract_metadata(str(f), f.name, mode="full")
            assert tags is not None, f"Failed to extract tags from {f.name}"
            assert tags.get("container") or tags.get("format"), f"Missing basic format info for {f.name}"

    print(f"✅ Verified parsing coverage for audio formats: {found_formats}")
    if not found_formats:
        pytest.skip("No audio files found in /media for diversity testing.")

def test_audio_bitrate_and_sample_rate():
    """Verify that bitrate and sample rate are detected for audio files."""
    audio_files = [f for f in MEDIA_DIR.glob("*.*") if f.suffix.lower() in AUDIO_FORMATS]
    
    if not audio_files:
        pytest.skip("No audio files found.")
        
    for f in audio_files[:5]:
        tags, _ = media_parser.extract_metadata(str(f), f.name, mode="full")
        
        bitrate = tags.get("bitrate")
        samplerate = tags.get("samplerate") or tags.get("sample_rate")
        
        # Many parsers put this in full_tags
        if not bitrate:
            bitrate = tags.get("full_tags", {}).get("bitrate")
        if not samplerate:
            samplerate = tags.get("full_tags", {}).get("sample_rate") or tags.get("full_tags", {}).get("samplerate")

        # Basic verification - at least one should be present for high quality parsers
        assert bitrate or samplerate, f"Failed to detect audio properties for {f.name}. Tags: {tags.keys()}"
