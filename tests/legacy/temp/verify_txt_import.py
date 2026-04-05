import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.getcwd())

from src.core import db
from src.core.main import import_txt_to_db

# Mock pick_file to return a temporary txt file
import src.core.main as main
original_pick_file = main.pick_file

def mock_pick_file(title=None, filetypes=None):
    return "/tmp/test_import.txt"

main.pick_file = mock_pick_file

# Create test txt file
test_content = """
/path/to/video1.mp4
/path/to/video2.mkv
# comment line
/path/to/movie.avi
"""
Path("/tmp/test_import.txt").write_text(test_content.strip())

# Initialize DB
db.init_db()
db.clear_media()

# Test Import
print("Starting TXT Import for Video...")
result = import_txt_to_db("Video")
print(f"Result: {result}")

# Verify DB
items = db.get_all_media()
print(f"Items in DB: {len(items)}")
for item in items:
    print(f" - {item['name']} ({item['category']})")

# Clean up
main.pick_file = original_pick_file
if result.get("status") == "ok" and result.get("imported") == 3:
    print("Verification SUCCESS")
else:
    print("Verification FAILED")
