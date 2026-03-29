import sqlite3
import os

DB_PATH = "mwv.db"

def verify_playback():
    print(f"[Verify] Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if missing (unlikely but safe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            path TEXT UNIQUE,
            category TEXT,
            tags TEXT,
            last_played REAL
        )
    """)

    # Clean existing mock data
    cursor.execute("DELETE FROM items WHERE filename LIKE 'MOCK_%'")

    # Insert Mock Audio
    mock_audio = (
        "MOCK_Audio_Test.mp3",
        "mock_audio.mp3",
        "Music",
        '{"title": "MOCK Audio Test", "artist": "Stability Team", "album": "Verification"}'
    )
    
    # Insert Mock Video
    mock_video = (
        "MOCK_Video_Test.mp4",
        "mock_video.mp4",
        "Movie",
        '{"title": "MOCK Video Test", "director": "Stabilization Bot"}'
    )

    try:
        cursor.execute("INSERT INTO items (filename, path, category, tags) VALUES (?, ?, ?, ?)", mock_audio)
        cursor.execute("INSERT INTO items (filename, path, category, tags) VALUES (?, ?, ?, ?)", mock_video)
        conn.commit()
        print("[Success] Mock items inserted.")
        print("  - Audio: MOCK_Audio_Test.mp3 (Category: Music)")
        print("  - Video: MOCK_Video_Test.mp4 (Category: Movie)")
    except sqlite3.IntegrityError:
        print("[Info] Mock items already exist.")
    
    conn.close()

if __name__ == "__main__":
    verify_playback()
