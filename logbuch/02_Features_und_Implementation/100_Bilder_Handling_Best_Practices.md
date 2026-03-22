# Bilder-Handling in Media Web Viewer (Eel/Bottle)

## Anzeige im Frontend
- Bilder im web/bilder/ Ordner ablegen
- Mit Eel <img>-Tag und Python-Expose-Funktion anzeigen

### Beispiel (Python)
```python
import eel

eel.init('web')

@eel.expose
def get_image_path(filename):
    return f'/bilder/{filename}'

eel.start('index.html', size=(800, 600))
```

### Beispiel (HTML/JS)
```html
<img id="bild" src="" width="300" height="200" alt="Bild">
<button onclick="loadBild('cover.jpg')">Bild laden</button>
<script>
    async function loadBild(filename) {
        const path = await eel.get_image_path(filename)();
        document.getElementById('bild').src = path;
    }
</script>
```

## Dynamische Bilder (Base64)
- Für Bilder außerhalb von web/ oder dynamische Covers
- Base64-Encoding für kleine Bilder (<1MB)

### Beispiel (Python)
```python
import base64
from pathlib import Path
import eel

@eel.expose
def get_base64_image(image_path):
    with open(image_path, 'rb') as f:
        img_data = base64.b64encode(f.read()).decode()
    return f'data:image/jpeg;base64,{img_data}'
```

## Bilder in der Datenbank
- Speichere Pfade (cover_path, thumbnail_path) und Metadaten in SQLite
- Keine Binärdaten, außer für kleine Icons (BLOB)

### DB-Schema (SQLite)
```sql
CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    filename TEXT UNIQUE,
    path TEXT,
    cover_path TEXT,
    thumbnail_path TEXT,
    metadata JSON
);
```

### Beispiel (Python CRUD)
```python
import sqlite3
import json
from pathlib import Path
import base64

DB_PATH = 'media_library.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS media
                    (id INTEGER PRIMARY KEY, filename TEXT UNIQUE, path TEXT,
                     cover_path TEXT, thumbnail_path TEXT, metadata TEXT)''')
    conn.commit()
    conn.close()

def add_media(filename, full_path, cover_path=None, metadata=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO media (filename, path, cover_path, metadata) VALUES (?, ?, ?, ?)",
                (filename, str(full_path), cover_path, json.dumps(metadata or {})))
    conn.commit()
    conn.close()

def get_media_by_id(media_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM media WHERE id=?", (media_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        row = list(row)
        row[5] = json.loads(row[5])
        return row
    return None

def get_cover_base64(media_id):
    media = get_media_by_id(media_id)
    if media:
        cover_path = media[3]
        if Path(cover_path).exists():
            with open(cover_path, 'rb') as f:
                return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return None
```

## Integration in Eel/Bottle
- Metadaten/Cover mit mutagen/pymediainfo extrahieren
- Pfade in DB speichern
- JS ruft Eel-Funktion auf, zeigt Bild im <img>-Tag

## Thumbnails
- Mit Pillow (pip install pillow) erstellen, Pfad speichern

## Vorteile
- Pfade statt Blobs: Skalierbar, einfach zu backupen
- Blobs nur für kleine Icons

---
*Letzte Aktualisierung: 10. März 2026*
