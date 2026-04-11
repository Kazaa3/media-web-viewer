
import sys
import os
from pathlib import Path

# Fix imports for the project structure
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'home', 'xc', '#Coding', 'gui_media_web_viewer'))
# wait, cleaner to just use absolute paths provided in the task
repo_path = "/home/xc/#Coding/gui_media_web_viewer"

sys.path.insert(0, repo_path)
sys.path.insert(0, os.path.join(repo_path, "src"))
sys.path.insert(0, os.path.join(repo_path, "src", "core"))

from core import db
from core.models import MediaItem

def verify():
    print("Initializing DB...")
    db.init_db()
    
    # Create a mock podcast file
    media_dir = Path(repo_path) / "media" / "Podcasts"
    media_dir.mkdir(parents=True, exist_ok=True)
    podcast_file = media_dir / "test_podcast.mp3"
    if not podcast_file.exists():
        with open(podcast_file, "wb") as f:
            f.write(b"ID3\x03\x00\x00\x00\x00\x00\x00") # Dummy MP3 header
    
    # Manually create a MediaItem and test category
    item = MediaItem(podcast_file.name, str(podcast_file.absolute()))
    print(f"Detected category for {podcast_file.name}: {item.category}")
    
    # Test DB insertion
    db.insert_media(item.to_dict())
    print("Inserted mock podcast into DB.")
    
    # Retrieve and check art_path
    retrieved = db.get_media_by_name(item.name)
    if retrieved:
        print(f"Retrieved from DB: {retrieved['name']}")
        print(f"Art Path: {retrieved.get('art_path')}")
        print(f"Category: {retrieved.get('category')}")
    else:
        print("Failed to retrieve item from DB!")

if __name__ == "__main__":
    verify()
