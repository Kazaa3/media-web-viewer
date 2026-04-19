import sys
import os
from pathlib import Path

# Dynamic Path Discovery (v1.46.132)
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

from core import db

if __name__ == "__main__":
    test_video = "persistence_test_video_e2e"
    print(f"Testing persistence for: {test_video}")
    
    # 1. Update position
    new_pos = 456.78
    db.update_playback_position(test_video, new_pos)
    print(f"Updated position to: {new_pos}")
    
    # 2. Retrieve position
    retrieved = db.get_playback_position(test_video)
    print(f"Retrieved position: {retrieved}")
    
    if retrieved == new_pos:
        print("SUCCESS: Persistence E2E test passed.")
    else:
        print(f"FAILED: Persistence E2E test failed. Got: {retrieved}")
        
    # Clean up
    conn = db.sqlite3.connect(db.DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM media WHERE name = ?", (test_video,))
    conn.commit()
    conn.close()
