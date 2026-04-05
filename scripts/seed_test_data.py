import sqlite3
import os
import time

def seed_db():
    print("[SEED] Starting Rapid-Seed (541 Items)...")
    db_path = os.path.join("data", "database.db")
    
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            path TEXT,
            relpath TEXT,
            category TEXT,
            tags TEXT,
            scanned_at REAL
        )
    ''')
    
    # Clear existing
    cursor.execute("DELETE FROM media")
    
    # Batch insertion for 541 items
    items = []
    for i in range(1, 542):
        name = f"Test-Track {i:03d} (Rapid Seed)"
        cat = "Audio" if i % 10 != 0 else "multimedia"
        # Mocking the essential columns
        items.append((
            name,
            f"/path/to/media/track_{i}.mp3",
            cat,
            '{"genre": "Sync-Test", "year": "2026"}',
            0  # is_mock = 0 (Real-looking data)
        ))
        
    cursor.executemany(
        "INSERT INTO media (name, path, category, tags, is_mock) VALUES (?, ?, ?, ?, ?)",
        items
    )
    
    conn.commit()
    count = cursor.execute("SELECT count(*) FROM media").fetchone()[0]
    conn.close()
    
    print(f"[SEED] SUCCESS: {count} items written to {db_path}.")

if __name__ == "__main__":
    seed_db()
