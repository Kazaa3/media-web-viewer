import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path("/home/xc/#Coding/gui_media_web_viewer/src/core")))

import main
from src.parsers.format_utils import PARSER_CONFIG, load_parser_config

print(f"Project Root (calculated): {main.PROJECT_ROOT}")
print(f"SCAN_MEDIA_DIR: {main.SCAN_MEDIA_DIR}")
print(f"BROWSER_DEFAULT_DIR: {main.BROWSER_DEFAULT_DIR}")

# Test if SCAN_MEDIA_DIR points to root/media
expected_media_dir = str((main.PROJECT_ROOT / "media").resolve())
if main.SCAN_MEDIA_DIR == expected_media_dir:
    print("SUCCESS: SCAN_MEDIA_DIR points to project root media folder.")
else:
    print(f"FAILURE: SCAN_MEDIA_DIR ({main.SCAN_MEDIA_DIR}) mismatch with expected ({expected_media_dir})")

# Test API update_browse_default_dir
test_path = "/tmp"
res = main.update_browse_default_dir(test_path)
print(f"API result: {res}")

if main.BROWSER_DEFAULT_DIR == test_path and PARSER_CONFIG.get("browse_default_dir") == test_path:
    print("SUCCESS: update_browse_default_dir updated both global and PARSER_CONFIG.")
else:
    print(f"FAILURE: update_browse_default_dir did not sync correctly. Global: {main.BROWSER_DEFAULT_DIR}, Config: {PARSER_CONFIG.get('browse_default_dir')}")

# Reset BROWSER_DEFAULT_DIR for next run if needed
main.update_browse_default_dir(str(Path.home()))
