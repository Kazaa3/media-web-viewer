import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.getcwd())

from src.core import db
from src.core.main import import_txt_to_db

# Mock pick_file
import src.core.main as main
original_pick_file = main.pick_file

def mock_pick_file(title=None, filetypes=None):
    return "/tmp/film_folders.txt"

main.pick_file = mock_pick_file

# Create test txt file with user's format
test_content = """
The Matrix (1999) [4K] - br
Interstellar (2014) [1080p] - blu ray
Inception (2010) - bd
# Some other line
Avatar (2009) [Extended]
"""
Path("/tmp/film_folders.txt").write_text(test_content.strip())

# Initialize DB
db.init_db()
db.clear_media()

# Test Import
print("Starting TXT Import for Film...")
result = import_txt_to_db("Film")
print(f"Result: {result}")

# Verify DB
items = db.get_all_media()
print(f"Items in DB: {len(items)}")
for item in items:
    print(f" - {item['name']} | Category: {item['category']} | Type: {item['type']}")

# Clean up
main.pick_file = original_pick_file
if result.get("status") == "ok" and result.get("imported") == 4:
    print("Verification SUCCESS")
else:
    print("Verification FAILED")
