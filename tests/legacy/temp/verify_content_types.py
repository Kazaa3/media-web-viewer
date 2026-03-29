import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.core.models import MediaItem
from src.parsers.filename_parser import parse as parse_filename
from src.parsers.format_utils import is_chrome_native

def test_filename_parser():
    print("\n=== Testing Filename Parser (Series & Folder Logic) ===")
    
    # Test cases: (path, filename, expected_tags)
    test_cases = [
        ("/media/Serienname S01E01.mkv", "Breaking Bad S01E01.mkv", {"season": 1, "episode": 1, "is_series": True}),
        ("/media/Show 1x05.mp4", "Show 1x05.mp4", {"season": 1, "episode": 5, "is_series": True}),
        ("/media/Pink Floyd - The Dark Side of the Moon (1973)/01 Speak to Me.mp3", "01 Speak to Me.mp3", {"artist": "Pink Floyd", "album": "The Dark Side of the Moon", "year": "1973"})
    ]
    
    for path_str, filename, expected in test_cases:
        path = Path(path_str)
        # Mock Path.parent.name for the album test
        tags = parse_filename(path, path.suffix, filename=filename)
        
        print(f"File: {filename}")
        for key, val in expected.items():
            actual = tags.get(key)
            if actual == val:
                print(f"  ✓ {key}: {actual}")
            else:
                print(f"  ✗ {key}: {actual} (expected {val})")

def test_content_type_detection():
    print("\n=== Testing Content Type Detection ===")
    
    # Create mock items and check category
    # (path, tags, expected_category)
    test_cases = [
        ("Series/Serieame S01E01.mkv", {"is_series": True}, "Serie"),
        ("Music/Pink Floyd - Dark Side (1973)/01.mp3", {"artist": "Pink Floyd", "album": "Dark Side"}, "Album"),
        ("Music/OST/Movie Soundtrack/01.mp3", {"album": "Original Motion Picture Soundtrack"}, "Soundtrack"),
        ("Playlists/Favorites.m3u", {}, "Playlist")
    ]
    
    for path_str, tags, expected in test_cases:
        # Mock MediaItem properties for testing categorization
        p = Path(path_str)
        item = MediaItem(p.name, p)
        item.tags = tags
        category = item.get_category()
        
        if category == expected:
            print(f"✓ {path_str} -> {category}")
        else:
            print(f"✗ {path_str} -> {category} (expected {expected})")

def test_chrome_native():
    print("\n=== Testing Chrome Native (Extension + Codec) ===")
    
    test_cases = [
        (".mp4", "h264", True),
        (".mp4", "hevc", False), # Usually not well supported natively in all Chromes without hardware
        (".webm", "vp9", True),
        (".mkv", "h264", False), # MKV is not a native container
        (".mp3", "mp3", True),
        (".flac", "flac", True)
    ]
    
    for ext, codec, expected in test_cases:
        result = is_chrome_native(ext, codec)
        if result == expected:
            print(f"✓ {ext}/{codec} -> {result}")
        else:
            print(f"✗ {ext}/{codec} -> {result} (expected {expected})")

if __name__ == "__main__":
    test_filename_parser()
    test_content_type_detection()
    test_chrome_native()
