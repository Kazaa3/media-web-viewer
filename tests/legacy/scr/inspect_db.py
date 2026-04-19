import sys
import os
from pathlib import Path

# Add project root to sys.path
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

try:
    from src.core import db
    print(f"db file: {db.__file__}")
    print(f"has get_media_by_id: {hasattr(db, 'get_media_by_id')}")
    print(f"has get_media_by_name: {hasattr(db, 'get_media_by_name')}")
    print(f"Attributes: {[attr for attr in dir(db) if not attr.startswith('__')]}")
except Exception as e:
    print(f"Error: {e}")
