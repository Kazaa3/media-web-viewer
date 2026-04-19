import os
import sys
from pathlib import Path

# Dynamic Path Discovery (v1.46.132)
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

# Mock logger/environment
import logging
logging.basicConfig(level=logging.INFO)

try:
    from src.core import db
    from src.core import main, logger

    # Initialize environment for test
    logger.setup_logging(debug_mode=True)
except ImportError as e:
    print(f"[Error] Imports failed: {e}")
    sys.exit(1)

def test_rename_behavior():
    print("=== Testing Rename & Availability Tracking (v1.35.98) ===\n")
    
    # 1. Setup Test File
    test_media_dir = PROJECT_ROOT / "media"
    old_file = test_media_dir / "03_deichkind_-_remmidemmi_(yippie_yippie_yeah).wma"
    new_file = test_media_dir / "03_deichkind_-_remmidemmi_renamed.wma"
    
    # Ensure starting state
    if new_file.exists(): new_file.rename(old_file)
    if not old_file.exists():
        with open(old_file, "w") as f: f.write("mock content")

    # 2. Initial Scan
    print("Performing initial scan (Full Purge)...")
    main._scan_media_execution(clear_db=True)
    
    initial_items = db.get_library()
    item_before = next((i for i in initial_items if old_file.name in i['path']), None)
    
    if not item_before:
        print("[Error] Test file not indexed correctly.")
        return

    print(f"Initial: Found '{item_before['name']}' | Available: {item_before.get('available')}")

    # 3. Rename File (simulate user action)
    print(f"\nRenaming file on disk: {old_file.name} -> {new_file.name}")
    old_file.rename(new_file)

    # 4. Perform Incremental Rescan (clear_db=False)
    print("Performing incremental rescan...")
    main._scan_media_execution(clear_db=False)
    
    # 5. Verify results
    all_items = db.get_library()
    
    # The old entry should still exist but marked available=False
    stale_item = next((i for i in all_items if old_file.name in i['path']), None)
    # The new entry should exist and be available=True
    new_item = next((i for i in all_items if new_file.name in i['path']), None)
    
    print(f"\nVerification Results:")
    if stale_item:
        avail = stale_item.get('available', 'N/A')
        status = "OK" if avail is False else "FAIL (Still marked as available!)"
        print(f"  Old Entry (Stale): {stale_item['name']} | Available: {avail} -> {status}")
    else:
        print("  Old Entry (Stale): Missing from DB (Purged?)")
        
    if new_item:
        print(f"  New Entry (Found): {new_item['name']} | Available: {new_item.get('available')}")
    else:
        print("  New Entry (Found): NOT FOUND")

    # Cleanup
    if new_file.exists(): new_file.rename(old_file)
    print("\nTest Complete. Cleaned up.")

if __name__ == "__main__":
    test_rename_behavior()
