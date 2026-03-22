# Bilder-Handling für große Media-Library (10.000+ Bilder)

## DB-Optimierung (SQLite)
- Indizes auf filename, path für schnelle Suche
```python
conn.execute("CREATE INDEX IF NOT EXISTS idx_filename ON media(filename)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_path ON media(path)")
conn.execute("ANALYZE media")
```
- Transaktionen batchen: conn.executemany() für Bulk-Inserts
- WAL-Modus: PRAGMA journal_mode=WAL; für paralleles Lesen/Schreiben
- Partitionierung: Separate DBs pro Ordner/Medientyp

## Thumbnails generieren (Pillow)
- Kleine Vorschauen (z.B. 200x200px) beim Scan
- Speichere in thumbnails/-Ordner, Pfad in DB
```python
from PIL import Image
import os

def create_thumbnail(image_path, thumb_path, size=(200, 200)):
    if not os.path.exists(image_path): return
    with Image.open(image_path) as img:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(thumb_path, 'JPEG', quality=85, optimize=True)
```
- Batch-Verarbeitung mit multiprocessing für viele Bilder
- Thumbnails <50KB, DB <1GB bei 100k Bildern

## Frontend-Optimierung (Eel/JS)
- Lazy-Loading: Bilder erst laden, wenn sichtbar
```javascript
const images = document.querySelectorAll('img[data-src]');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.src = entry.target.dataset.src;
        }
    });
});
images.forEach(img => observer.observe(img));
```
- Grid mit Pagination: Zeige 50 Bilder pro Seite, lade via Eel-Expose (OFFSET/LIMIT in SQL)
- Serve static: Thumbnails in web/bilder/ für direkte URLs

## Weitere Tipps
| Aspekt   | Maßnahme                        | Effekt                  |
|----------|----------------------------------|-------------------------|
| Speicher | Thumbs <50KB, Pfade statt Blobs  | DB <1GB bei 100k Bildern|
| CPU      | Parallel thumbnails (Pool)       | 10x schneller           |
| Query    | LIMIT/OFFSET + Indizes           | <10ms pro Seite         |
| Cache    | browser.cache/Redis (optional)   | Kein Neuladen           |

- EXPLAIN QUERY PLAN in sqlite3 CLI für Analyse
- Für Extremfälle: PostgreSQL migrieren

---
*Letzte Aktualisierung: 10. März 2026*
