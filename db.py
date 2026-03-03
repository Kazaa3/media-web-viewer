import sqlite3
import os

DB_FILENAME = "media_library.db"

def init_db():
    """
    Initialisiert die Datenbank und erstellt die benötigten Tabellen, falls diese noch nicht existieren.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    # Tabelle für Medien
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            path TEXT,
            duration TEXT,
            title TEXT,
            artist TEXT,
            album TEXT,
            year TEXT,
            genre TEXT,
            track TEXT,
            codec TEXT,
            bitrate TEXT,
            samplerate TEXT,
            is_transcoded BOOLEAN
        )
    """)

    # Tabelle für Playlists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    # Verknüpfungstabelle Medien <-> Playlists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_media (
            playlist_id INTEGER,
            media_id INTEGER,
            position INTEGER,
            FOREIGN KEY(playlist_id) REFERENCES playlists(id),
            FOREIGN KEY(media_id) REFERENCES media(id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Datenbank '{DB_FILENAME}' erfolgreich initialisiert.")

def query_example():
    """ Placeholder-Funktion für spätere Datenbankzugriffe. """
    pass
