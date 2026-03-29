import sys
import os
from pathlib import Path

PROJECT_ROOT = Path("/home/xc/#Coding/gui_media_web_viewer")
sys.path.append(str(PROJECT_ROOT))

from src.core.main import scan_js_errors

results = scan_js_errors()
import json
print(json.dumps(results, indent=2))
