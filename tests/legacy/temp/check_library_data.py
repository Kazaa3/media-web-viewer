import sys
import os
sys.path.append('/home/xc/#Coding/gui_media_web_viewer')
from src.core import db
from src.core.main import PARSER_CONFIG

print(f"Total media in DB: {len(db.get_all_media())}")
print(f"PARSER_CONFIG displayed_categories: {PARSER_CONFIG.get('displayed_categories')}")
