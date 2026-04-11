import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.core import db
all_media = db.get_all_media()

print(f"Total media: {len(all_media)}")
print("Paths:")
for item in all_media[:5]:
    path = item.get('path', '')
    print(f" - {path}")
