import sqlite3
import os
import json
from pathlib import Path

# Dynamic Path Discovery (v1.46.132)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_FILENAME = PROJECT_ROOT / "data" / "database.db"

def verify_persistence():
    print("--- Persistence Verification ---")
    if not os.path.exists(DB_FILENAME):
        print(f"ERROR: Database file not found at {DB_FILENAME}")
        return

    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Check table schema
    cursor.execute("PRAGMA table_info(media)")
    columns = {row['name']: row['type'] for row in cursor.fetchall()}
    required = ['playback_position', 'last_played', 'duration_sec']
    
    for col in required:
        if col not in columns:
            print(f"FAILED: Missing column: {col}")
        else:
            print(f"SUCCESS: Column '{col}' present ({columns[col]}).")

    # 2. Test update logic
    test_name = "persistence_test_video_v2"
    # Ensure columns exist before update
    try:
        cursor.execute("INSERT OR REPLACE INTO media (name, type, playback_position, duration_sec) VALUES (?, ?, ?, ?)", 
                       (test_name, 'video', 123.45, 1000.0))
        conn.commit()
        
        cursor.execute("SELECT playback_position, duration_sec FROM media WHERE name = ?", (test_name,))
        row = cursor.fetchone()
        if row and abs(row['playback_position'] - 123.45) < 0.01:
            print(f"SUCCESS: Playback position saved and retrieved correctly: {row['playback_position']}")
        else:
            print(f"FAILED: Playback position mismatch or not found. Got: {row['playback_position'] if row else 'None'}")
            
        if row and row['duration_sec'] == 1000.0:
            print(f"SUCCESS: Duration_sec saved and retrieved correctly: {row['duration_sec']}")
        else:
            print(f"FAILED: Duration_sec mismatch or not found. Got: {row['duration_sec'] if row else 'None'}")

    except Exception as e:
        print(f"ERROR during test: {e}")
    finally:
        # Clean up
        cursor.execute("DELETE FROM media WHERE name = ?", (test_name,))
        conn.commit()

    conn.close()
    print("--- Verification Complete ---")

if __name__ == "__main__":
    verify_persistence()
