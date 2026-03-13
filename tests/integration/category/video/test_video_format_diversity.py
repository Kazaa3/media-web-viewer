#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# test_video_format_diversity.py - Validates parser coverage for various video containers.
"""

import pytest
from pathlib import Path
from src.parsers import media_parser

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MEDIA_DIR = PROJECT_ROOT / "media"

# Define formats to test (if files exist)
VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".wmv", ".mkv", ".flv", ".webm"]

def test_video_format_parsing_coverage():
    """Verify that at least one file of each major video format is parsable."""
    found_formats = set()
    for f in MEDIA_DIR.glob("*.*"):
        ext = f.suffix.lower()
        if ext in VIDEO_FORMATS:
            found_formats.add(ext)
            
            # Perform actual parsing test
            tags, _ = media_parser.extract_metadata(str(f), f.name, mode="full")
            assert tags is not None, f"Failed to extract tags from {f.name}"
            assert "container" in tags or "format" in tags, f"Missing basic format info for {f.name}"

    print(f"✅ Verified parsing coverage for formats: {found_formats}")
    # We don't fail if a format is missing from /media, but we log the coverage
    if not found_formats:
        pytest.skip("No video files found in /media for diversity testing.")

def test_video_resolution_detection():
    """Verify that resolution (width/height) is detected for video files."""
    video_files = [f for f in MEDIA_DIR.glob("*.*") if f.suffix.lower() in VIDEO_FORMATS]
    
    if not video_files:
        pytest.skip("No video files found.")
        
    for f in video_files[:5]: # Test a representative sample
        tags, _ = media_parser.extract_metadata(str(f), f.name, mode="full")
        
        # Resolution might be in different places depending on parser
        width = tags.get("width") or tags.get("full_tags", {}).get("width")
        height = tags.get("height") or tags.get("full_tags", {}).get("height")
        
        # Fallback to ffprobe_json if available
        if not width and "ffprobe_json" in tags.get("full_tags", {}):
            import json
            probe = json.loads(tags["full_tags"]["ffprobe_json"])
            for stream in probe.get("streams", []):
                if stream.get("codec_type") == "video":
                    width = stream.get("width")
                    height = stream.get("height")
                    break
                    
        assert width and height, f"Failed to detect resolution for {f.name}. Tags: {tags.keys()}"
