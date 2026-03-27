import sys
import os
sys.path.append('/home/xc/#Coding/gui_media_web_viewer')
from src.core import db

def inject_mocks():
    db.init_db()
    db.clear_media()
    
    mocks = [
        {
            'name': 'Big Buck Bunny (4K)',
            'path': '/home/xc/#Coding/gui_media_web_viewer/tests/assets/test_video.mp4',
            'type': 'video/mp4',
            'duration': '00:10:34',
            'category': 'Film',
            'is_transcoded': False,
            'tags': {'genre': 'Animation', 'year': '2008'},
            'extension': 'mp4',
            'container': 'mov',
            'has_artwork': False
        },
        {
            'name': 'Sample House Music',
            'path': '/home/xc/#Coding/gui_media_web_viewer/tests/assets/test_audio.mp3',
            'type': 'audio/mpeg',
            'duration': '00:03:45',
            'category': 'Audio',
            'is_transcoded': False,
            'tags': {'artist': 'Various', 'album': 'Summer Hits'},
            'extension': 'mp3',
            'container': 'mp3',
            'has_artwork': False
        }
    ]
    
    for m in mocks:
        db.insert_media(m)
    print(f"Injected {len(mocks)} mock items.")

if __name__ == "__main__":
    inject_mocks()
