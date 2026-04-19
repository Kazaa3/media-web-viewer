import sys
import os
from pathlib import Path

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT))

from src.core import db
all_media = db.get_all_media()

print(f"Total media: {len(all_media)}")
print("Paths:")
for item in all_media[:5]:
    path = item.get('path', '')
    print(f" - {path}")
