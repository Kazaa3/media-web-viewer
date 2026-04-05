import sys, os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

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
