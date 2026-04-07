
import sys
import os
from pathlib import Path
import sqlite3
import time

# Add project root to sys.path
root = Path("/home/xc/#Coding/gui_media_web_viewer").resolve()
sys.path.insert(0, str(root))

# Force lightweight environment BEFORE imports
os.environ["MWV_PARSER_MODE"] = "lightweight"
os.environ["MWV_DIAG_MODE"] = "0"

from src.core import db
from src.core import main
from src.core.config_master import GLOBAL_CONFIG

def run_fast_rehydrate():
    print("🚀 [FAST-REHYDRATOR] Round 5 Emergency Recovery Starting...")
    
    # Force global config to fastest settings
    GLOBAL_CONFIG["parser_mode"] = "lightweight"
    GLOBAL_CONFIG["diag_mode"] = False
    
    db.init_db()
    
    media_dir = str(root / "media")
    print(f"📂 [FAST-REHYDRATOR] Target: {media_dir}")
    
    # 1. Atomic Purge of Real Items
    conn = sqlite3.connect(db.DB_FILENAME)
    conn.execute("DELETE FROM media WHERE is_mock = 0")
    conn.commit()
    conn.close()
    print("🧹 [FAST-REHYDRATOR] Old 'Real' items purged.")
    
    # 2. Trigger Optimized Scan
    t0 = time.time()
    # We call the internal execution directly to bypass Eel
    main._scan_media_execution(dir_path=media_dir, clear_db=False)
    t1 = time.time()
    
    # 3. Stats Check
    conn = sqlite3.connect(db.DB_FILENAME)
    real_count = conn.execute("SELECT count(*) FROM media WHERE is_mock = 0").fetchone()[0]
    mock_count = conn.execute("SELECT count(*) FROM media WHERE is_mock = 1").fetchone()[0]
    conn.close()
    
    print(f"✅ [FAST-REHYDRATOR] Recovery Complete in {t1-t0:.2f} seconds!")
    print(f"📊 [FAST-REHYDRATOR] Final Library -> Real: {real_count} | Mock: {mock_count}")
    print("👉 [FAST-REHYDRATOR] You can now restart the main application.")

if __name__ == "__main__":
    run_fast_rehydrate()
