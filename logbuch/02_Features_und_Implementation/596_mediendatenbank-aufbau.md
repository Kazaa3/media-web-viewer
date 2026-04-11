# Logbuch: Aufbau einer Mediendatenbank

**Datum:** 16. März 2026

---

## Ziel
Eine Mediendatenbank ermöglicht das zentrale Verwalten, Durchsuchen und Streamen von Video-, Audio- und Bilddateien. Sie dient als Backend für Player, Streaming-Server (MediaMTX), und Web-GUIs.

---

## Schritte zum Aufbau

### 1. Datenbank wählen
- SQLite (einfach, portabel)
- PostgreSQL/MySQL (für größere Installationen)

### 2. Datenbankstruktur
- Tabelle `media_items`:
  - id (INTEGER, PRIMARY KEY)
  - filename (TEXT)
  - filepath (TEXT)
  - filetype (TEXT)
  - duration (FLOAT)
  - resolution (TEXT)
  - tags (TEXT)
  - date_added (DATETIME)
  - metadata (JSON)

### 3. Medien einlesen & erfassen
- Python-Skript mit `os`, `ffprobe`, `mutagen`, `pymediainfo`:
  - Verzeichnisse scannen
  - Metadaten extrahieren
  - Einträge in DB speichern

### 4. Beispiel-Code (Python, SQLite)
```python
import sqlite3, os
from datetime import datetime
conn = sqlite3.connect('media.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS media_items (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    filepath TEXT,
    filetype TEXT,
    duration FLOAT,
    resolution TEXT,
    tags TEXT,
    date_added DATETIME,
    metadata TEXT
)''')
for root, dirs, files in os.walk('/media'):  # Medienverzeichnis
    for file in files:
        path = os.path.join(root, file)
        # Metadaten mit ffprobe etc. extrahieren
        c.execute('INSERT INTO media_items (filename, filepath, filetype, date_added) VALUES (?, ?, ?, ?)',
                  (file, path, os.path.splitext(file)[1], datetime.now()))
conn.commit()
```

---

## Erweiterungen
- Web-Frontend (Eel/Bottle/Flask): Suche, Filter, Play
- API: REST-Endpunkte für Medienabfrage
- Streaming-Integration: MediaMTX, ffmpeg, HLS
- Tagging, Bewertung, Playlists

---

## Best Practices
- Automatisches Scannen (Cron, Watchdog)
- Metadaten regelmäßig aktualisieren
- Backups der Datenbank
- Performance: Index auf `filename`, `tags`

---

## Beispiel-Queries
- Alle Videos:
  ```sql
  SELECT * FROM media_items WHERE filetype IN ('.mp4', '.mkv', '.avi');
  ```
- Suche nach Tag:
  ```sql
  SELECT * FROM media_items WHERE tags LIKE '%urlaub%';
  ```

---

**Nächster Schritt:**
- Python-Skript für Metadaten-Import erweitern
- Web-GUI anbinden
- Streaming-Server (MediaMTX) mit DB verknüpfen
