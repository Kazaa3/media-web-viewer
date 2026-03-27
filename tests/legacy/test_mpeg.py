
from pathlib import Path
import sys
import os

# Add src to path
PROJECT_ROOT = Path("/home/xc/#Coding/gui_media_web_viewer")
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "core"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "parsers"))

from src.core.models import MediaItem
from src.parsers.format_utils import VIDEO_EXTENSIONS

filename = "30. Pleisweiler Gespräch - Vortrag - Prof. Dr. Gertraud Teuchert-Noodt - 21. Oktober 2018 (720p_30fps_H264-192kbit_AAC).mpeg"
print(f"Testing filename: {filename}")
print(f"Extension: {Path(filename).suffix}")
print(f"Is .mpeg in VIDEO_EXTENSIONS: {'.mpeg' in VIDEO_EXTENSIONS}")

# Create dummy file
dummy_path = PROJECT_ROOT / "tests" / "dummy_mpeg.mpeg"
dummy_path.parent.mkdir(parents=True, exist_ok=True)
dummy_path.write_text("dummy content")

try:
    item = MediaItem(filename, dummy_path)
    print(f"Item Category: {item.category}")
    print(f"Item Logical Type: {item.logical_type}")
    print(f"Item Media Type: {item.media_type}")
    print(f"Item Extension: {item.extension}")
finally:
    if dummy_path.exists():
        dummy_path.unlink()
