#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys
from pathlib import Path

# Ensure we can import local modules
sys.path.append(os.getcwd())

from models import MediaItem

def test_image_item_categorization():
    """Test that actual image files are correctly categorized."""
    # These should have been created by create_mocks.py
    image_paths = [
        Path("media/Bilder/test1.jpg"),
        Path("media/Bilder/test2.png"),
        Path("media/Bilder/test3.bmp")
    ]
    
    for p in image_paths:
        if p.exists():
            item = MediaItem(p.name, str(p))
            assert item.logical_type == 'Bilder'
            assert item.category == 'Bilder'
            assert item.media_type == 'Bilder'
            print(f"Verified {p.name}")

if __name__ == "__main__":
    test_image_item_categorization()
