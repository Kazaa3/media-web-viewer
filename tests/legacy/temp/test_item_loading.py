
import sys
import os

# Add src to path
sys.path.append(os.path.abspath('src'))

from core import main
from core import db

# Force debug flags
main.DEBUG_FLAGS['scan'] = True
main.DEBUG_FLAGS['db'] = True
main.DEBUG_FLAGS['system'] = True
from core import logger
logger.set_debug_flags(main.DEBUG_FLAGS)

def test_items():
    print("Checking database...")
    all_media = db.get_all_media()
    print(f"Total items in DB: {len(all_media)}")
    
    if len(all_media) == 0:
        print("Database is empty. Running scan...")
        import json
        from core.main import PARSER_CONFIG
        print(f"PARSER_CONFIG indexed_categories: {PARSER_CONFIG.get('indexed_categories')}")
        # To avoid scanning everything, we might want to scan a small dummy dir
        # but let's see what happens with default scan
        main.scan_media()
        all_media = db.get_all_media()
        print(f"Items after scan: {len(all_media)}")
    
    print("Testing get_library()...")
    library = main.get_library()
    print(f"Items returned by get_library(): {len(library['media'])}")
    
    if len(library) == 0 and len(all_media) > 0:
        print("Mismatched! Filtering is likely too strict.")
        import json
        from core.main import PARSER_CONFIG
        print(f"PARSER_CONFIG: {json.dumps(PARSER_CONFIG, indent=2)}")
        
        # Check first item category
        if all_media:
            print(f"First item category: {all_media[0].get('category')}")

if __name__ == "__main__":
    test_items()
