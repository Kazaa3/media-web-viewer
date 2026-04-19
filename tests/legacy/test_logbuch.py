 import sys
from pathlib import Path

# Add project root to path
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT / "src"))

import os

# Mock eel for standalone test if needed, or just import the function
from src.core.main import list_logbook_entries

try:
    entries = list_logbook_entries()
    print(f"Found {len(entries)} entries")
    if entries:
        print(f"First entry: {entries[0]['name']}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
