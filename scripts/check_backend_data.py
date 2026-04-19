import sys, os
from pathlib import Path

# Add project root to path
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

# Import db module
try:
    from src.core import db
    print(f"[TEST] Using DB Path: {db.DB_FILENAME}")
    
    items = db.get_all_media()
    print(f"[TEST] Found {len(items)} items in DB.")
    
    if len(items) > 0:
        print(f"[TEST] First item: {items[0]['name']}")
    else:
        print("[TEST] WARNING: Database is reported as EMPTY.")
        
except Exception as e:
    print(f"[TEST] ERROR: {e}")
