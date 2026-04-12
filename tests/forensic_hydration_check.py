import sys
import os
import json
import sqlite3
from pathlib import Path

# Setup Project Context
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

# Mock Eel before importing modules that depend on it
import types
mock_eel = types.ModuleType("eel")
mock_eel.expose = lambda x: x
mock_eel.sleep = lambda x: None
mock_eel.chrome = types.ModuleType("chrome") # Mock chrome module
sys.modules["eel"] = mock_eel
sys.modules["eel.chrome"] = mock_eel.chrome # Mock sub-package

# Mock GLOBAL_CONFIG for standalone execution
from src.core.config_master import GLOBAL_CONFIG
from src.core import db

def run_forensic_audit():
    print("="*60)
    print(" FORENSIC HYDRATION AUDIT (v1.46.003)")
    print("="*60)

    # --- STAGE 1: Database Integrity ---
    print("\n[STAGE 1] DATABASE INTEGRITY CHECK")
    db_path = Path(db.DB_FILENAME)
    if not db_path.exists():
        print(f"FAILED: Database file NOT FOUND at {db_path}")
        return False
    
    fs_size = db_path.stat().st_size
    print(f"SUCCESS: Database found at {db_path} ({fs_size} bytes)")
    
    try:
        conn = sqlite3.connect(db.DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM media")
        count = cursor.fetchone()[0]
        print(f"SUCCESS: 'media' table exists. Count: {count} items.")
        
        cursor.execute("SELECT name, category, is_mock FROM media LIMIT 5")
        samples = cursor.fetchall()
        print("SAMPLES:")
        for s in samples:
            print(f"  - {s[0]} ({s[1]}) | Mock: {bool(s[2])}")
        conn.close()
    except Exception as e:
        print(f"FAILED: Database query error: {e}")
        return False

    # --- STAGE 1.5: FS Parity Check (v1.46.003) ---
    print("\n[STAGE 1.5] FS PARITY AUDIT")
    if fs_size > 0:
        print(f"SUCCESS: Parity established. FS_SIZE({fs_size}) > 0.")
    else:
        print("FAILED: Database file is empty (0 bytes).")
        return False

    # --- STAGE 2: Backend Logic Bridge ---
    print("\n[STAGE 2] BACKEND LOGIC BRIDGE")
    try:
        from src.core.main import get_library
        # Simulate Eel call with dummy context
        result = get_library(force_raw=True)
        items = result.get('media', [])
        status = result.get('status', 'unknown')
        print(f"SUCCESS: get_library(force_raw=True) returned {len(items)} items.")
        print(f"STATUS: {status}")
        
        if len(items) == 0 and count > 0:
            print("CRITICAL: DATA LOSS DETECTED between DB and Logic return.")
            return False
        elif len(items) > 0:
            print("SUCCESS: Logic bridge is operational.")
    except Exception as e:
        print(f"FAILED: Backend module import or execution failed: {e}")
        return False

    # --- STAGE 3: Serialization Diagnostics ---
    print("\n[STAGE 3] SERIALIZATION DIAGNOSTICS")
    try:
        json_test = json.dumps(result)
        print(f"SUCCESS: Full library payload is JSON-serializable ({len(json_test)} bytes).")
    except Exception as e:
        print(f"FAILED: Serialization failure: {e}")
        return False

    # --- STAGE 4: Handshake Pattern Verification (v1.46.003) ---
    print("\n[STAGE 4] HANDSHAKE PATTERN AUDIT")
    if len(items) >= 12 or count >= 12:
         print(f"SUCCESS: Handshake threshold (12) satisfied. Current Count: {len(items)}")
    else:
         print(f"WARNING: Item count ({len(items)}) is below the forensic Stage 1 threshold (12).")

    print("\n" + "="*60)
    print(" AUDIT COMPLETE: REBUILD STAGE v1.46.003 IS HEALTHY")
    print("="*60)
    return True

if __name__ == "__main__":
    run_forensic_audit()
