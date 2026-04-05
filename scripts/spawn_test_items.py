
import os
import sys
import json
import sqlite3
from pathlib import Path

# Set up PYTHONPATH so we can import src.core.db
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

from src.core.db import insert_media, get_all_media, get_active_db_path, clear_media

def spawn_items():
    print(f"Using database: {get_active_db_path()}")
    
    # 1. Clear existing items and reset DB schema
    try:
        from src.core.db import factory_reset
        factory_reset()
        print("  [OK]  Database factory reset performed.")
    except Exception as e:
        print(f"  [ERR] Reset failed: {e}")
        # clear_media()
    
    items = [
        {
            'name': 'Test MP4 Video',
            'path': str(PROJECT_ROOT / 'media' / '30. Pleisweiler Gespräch - Vortrag - Prof. Dr. Gertraud Teuchert-Noodt - 21. Oktober 2018 (720p_30fps_H264-192kbit_AAC).mp4'),
            'type': 'Video',
            'duration': '01:00:00',
            'category': 'Video',
            'is_transcoded': False,
            'tags': {'title': 'Test MP4', 'artist': 'Antigravity'}
        },
        {
            'name': 'Test MP3 Audio',
            'path': str(PROJECT_ROOT / 'media' / '01 - Einfach & Leicht.mp3'),
            'type': 'Audio',
            'duration': '00:03:45',
            'category': 'Audio',
            'is_transcoded': False,
            'tags': {'title': 'Test MP3', 'artist': 'Antigravity'}
        },
        {
            'name': 'Mock Movie',
            'path': '/mock/movie.mkv',
            'type': 'Video',
            'duration': '01:30:00',
            'category': 'Film',
            'is_transcoded': False,
            'tags': {'title': 'Mock Movie', 'genre': 'Sci-Fi'}
        }
    ]
    
    print(f"Spawning {len(items)} items...")
    for item in items:
        # Fill missing keys with defaults to avoid KeyErrors in insert_media
        full_item = {
            'name': item['name'],
            'path': item['path'],
            'type': item['type'],
            'duration': item['duration'],
            'category': item.get('category', 'Audio'),
            'is_transcoded': item.get('is_transcoded', False),
            'transcoded_format': item.get('transcoded_format', None),
            'tags': item.get('tags', {}),
            'extension': item.get('extension', '.mp4'),
            'container': item.get('container', 'mp4'),
            'tag_type': item.get('tag_type', 'ID3'),
            'codec': item.get('codec', 'h264'),
            'has_artwork': item.get('has_artwork', False),
            'art_path': item.get('art_path', None),
            'full_tags': item.get('full_tags', {}),
            'media_type': item.get('media_type', 'File'),
            'subtype': item.get('subtype', 'Standard'),
            'file_type': item.get('file_type', 'Media'),
            'isbn': item.get('isbn', None),
            'imdb': item.get('imdb', None),
            'tmdb': item.get('tmdb', None),
            'discogs': item.get('discogs', None),
            'amazon_cover': item.get('amazon_cover', None),
            'parent_id': item.get('parent_id', None),
            'is_mock': item.get('is_mock', False),
            'mock_stage': item.get('mock_stage', 0)
        }
        try:
            insert_media(full_item)
            print(f"  [OK]  {item['name']}")
        except Exception as e:
            print(f"  [ERR] {item['name']}: {e}")

    final_count = len(get_all_media())
    print(f"Total items in DB now: {final_count}")

if __name__ == "__main__":
    spawn_items()
