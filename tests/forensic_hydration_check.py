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
sys.modules["eel"] = mock_eel

# Mock GLOBAL_CONFIG for standalone execution
from src.core.config_master import GLOBAL_CONFIG
from src.core import db

def run_forensic_audit():
    print("="*60)
    print(" FORENSIC HYDRATION AUDIT (v1.46.12)")
    print("="*60)

    # --- STAGE 1: Database Integrity ---
    print("\n[STAGE 1] DATABASE INTEGRITY CHECK")
    db_path = Path(db.DB_FILENAME)
    if not db_path.exists():
        print(f"FAILED: Database file NOT FOUND at {db_path}")
        return False
    
    print(f"SUCCESS: Database found at {db_path} ({db_path.stat().st_size} bytes)")
    
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
        elif len(items) > 0:
            print("SUCCESS: Logic bridge is operational.")
    except Exception as e:
        print(f"FAILED: Backend module import or execution failed: {e}")
        return False

    # --- STAGE 3: Serialization Diagnostics ---
    print("\n[STAGE 3] SERIALIZATION DIAGNOSTICS")
    try:
        # Eel handles serialization automatically, but we check for JSON-breaking types
        json_test = json.dumps(result)
        print(f"SUCCESS: Full library payload is JSON-serializable ({len(json_test)} bytes).")
    except Exception as e:
        print(f"FAILED: Serialization failure (potential circular ref or invalid type): {e}")
        return False

    print("\n" + "="*60)
    print(" AUDIT COMPLETE: BACKEND IS HEALTHY")
    print(" TARGET NEXT: Frontend Hydration Pulse (JS)")
    print("="*60)
    return True

if __name__ == "__main__":
    run_forensic_audit()
