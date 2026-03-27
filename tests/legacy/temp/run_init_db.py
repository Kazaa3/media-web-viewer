import sys
import os
from pathlib import Path

# Add src to sys.path
PROJECT_ROOT = Path("/home/xc/#Coding/gui_media_web_viewer")
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core.db import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully.")
