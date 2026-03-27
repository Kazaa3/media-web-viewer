import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(os.getcwd())

from src.core import db

# Initialize DB
db.init_db()
db.clear_media()

# Insert test items
test_items = [
    {
        'name': 'Test Video 1',
        'path': '/tmp/test_video1.mp4',
        'type': 'Video',
        'duration': '00:01:00',
        'category': 'Film',
        'is_transcoded': False,
        'tags': {'isbn': '1234567890'},
        'isbn': '1234567890'
    },
    {
        'name': 'Test Audio 1',
        'path': '/tmp/test_audio1.mp3',
        'type': 'Audio',
        'duration': '00:03:00',
        'category': 'Audio',
        'is_transcoded': False,
        'tags': {'artist': 'Test Artist'},
    }
]

for item in test_items:
    db.insert_media(item)

print("--- Testing get_media_by_remote_id ---")
isbn_match = db.get_media_by_remote_id('isbn', '1234567890')
if isbn_match and isbn_match['name'] == 'Test Video 1':
    print("SUCCESS: ISBN lookup works")
else:
    print(f"FAILED: ISBN lookup. Result: {isbn_match}")

print("--- Testing get_media_by_category ---")
films = db.get_media_by_category('Film')
if len(films) == 1 and films[0]['name'] == 'Test Video 1':
    print("SUCCESS: Category lookup works")
else:
    print(f"FAILED: Category lookup. Results: {len(films)}")

print("--- Testing search_media ---")
results = db.search_media('Audio')
if len(results) == 1 and results[0]['name'] == 'Test Audio 1':
    print("SUCCESS: Search works")
else:
    print(f"FAILED: Search. Results: {len(results)}")

print("--- Testing get_media_by_path ---")
path_match = db.get_media_by_path('/tmp/test_video1.mp4')
if path_match and path_match['name'] == 'Test Video 1':
    print("SUCCESS: Path lookup works")
else:
    print(f"FAILED: Path lookup. Result: {path_match}")

