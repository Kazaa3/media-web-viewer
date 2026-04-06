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
    
    # Create table if not exists (Canonical v1.35.96 Schema)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            path TEXT,
            type TEXT,
            duration TEXT,
            category TEXT,
            is_transcoded BOOLEAN,
            transcoded_format TEXT,
            tags TEXT,
            extension TEXT,
            container TEXT,
            tag_type TEXT,
            codec TEXT,
            has_artwork BOOLEAN DEFAULT 0,
            art_path TEXT,
            full_tags TEXT,
            media_type TEXT,
            subtype TEXT,
            file_type TEXT,
            isbn TEXT,
            imdb TEXT,
            tmdb TEXT,
            discogs TEXT,
            amazon_cover TEXT,
            parent_id INTEGER,
            playback_position REAL DEFAULT 0,
            last_played TEXT,
            duration_sec REAL,
            is_mock BOOLEAN DEFAULT 0,
            mock_stage INTEGER DEFAULT 0
        )
    ''')
    
    # Clear existing
    cursor.execute("DELETE FROM media")
    
    # Batch insertion for 541 items
    items = []
    for i in range(1, 542):
        name = f"[MOCK] Test-Track {i:03d} (Rapid Seed)"
        cat = "Audio" if i % 10 != 0 else "multimedia"
        # Mocking the essential columns
        items.append((
            name,
            f"/path/to/media/track_{i}.mp3",
            cat,
            '{"genre": "Sync-Test", "year": "2026"}',
            1, # is_mock = 1 (CORRECTED: Explicitly Mark as Mock)
            1  # mock_stage = 1 (Rapid-Seed Stage)
        ))
        
    cursor.executemany(
        "INSERT INTO media (name, path, category, tags, is_mock, mock_stage) VALUES (?, ?, ?, ?, ?, ?)",
        items
    )
    
    conn.commit()
    count = cursor.execute("SELECT count(*) FROM media").fetchone()[0]
    conn.close()
    
    print(f"[SEED] SUCCESS: {count} items written to {db_path}.")

if __name__ == "__main__":
    seed_db()
