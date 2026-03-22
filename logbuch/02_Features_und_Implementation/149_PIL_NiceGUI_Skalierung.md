# PIL (Pillow) & GUI-Optimierung für 1 Mio. Bilder

## PIL-Optimierung: Batch-Processing mit Multiprocessing
- Thumbnails (200x200px) für 1 Mio. Bilder
- Multiprocessing für parallele Verarbeitung
- LANCZOS für scharfe, schnelle Skalierung
- RAM <1GB durch lazy open/save
- Progress mit tqdm

### Beispiel-Skript
```python
from PIL import Image
from pathlib import Path
import multiprocessing as mp
import os

def process_image(args):
    img_path, thumb_dir, size = args
    thumb_path = Path(thumb_dir) / f"{img_path.stem}_thumb.jpg"
    if thumb_path.exists(): return
    try:
        with Image.open(img_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumb_path, 'JPEG', quality=85, optimize=True)
    except: pass

def generate_thumbs(image_dir, thumb_dir, size=(200, 200), workers=None):
    os.makedirs(thumb_dir, exist_ok=True)
    images = list(Path(image_dir).glob('*.jpg')) + list(Path(image_dir).glob('*.png'))
    args = [(p, thumb_dir, size) for p in images]
    with mp.Pool(workers or mp.cpu_count()) as pool:
        pool.map(process_image, args)
# generate_thumbs('/volume1/ABC/01 Medien/covers/', 'thumbnails/', workers=8)
```
- Speichere thumb_path in DB

## GUI: Spotify/Plex-Style mit NiceGUI
- Dark-Mode, Grid, Infinite Scroll, Lazy-Loading
- NiceGUI (Vue-basiert, responsive, Plex-Look)
- Thumbnails als statische Files (app.add_static_files)

### Beispiel (NiceGUI)
```python
from nicegui import ui, app
import sqlite3

app.add_static_files('/thumbnails', 'thumbnails/')

grid_items = []  # DB-Query: SELECT cover_path LIMIT 100 OFFSET 0

with ui.grid(columns=5).classes('gap-2 w-full'):
    for item in grid_items:
        with ui.card().classes('w-full h-32 bg-gray-900 shadow-lg hover:scale-105 transition-all'):
            ui.image(f'/thumbnails/{item["thumb"]}', bg_image=True).classes('w-full h-full rounded object-cover')
            ui.label(item['title']).classes('text-white text-sm p-1')

@ui.page('/')
def index():
    ui.grid().classes('w-full min-h-screen bg-gradient-to-br from-gray-900 to-black p-4')
    ui.infinite_scroll(load_data).props('threshold=0.1')

def load_data(e):
    # SQL: OFFSET e.value * 100
    ui.notify('Geladen!')

ui.run(title='Media Library', dark=True)
```
- 60fps Scroll, Pagination, Lazy-Loading

## Eel-Alternative
- CSS Grid + IntersectionObserver für Lazy-Loading
- <img data-src> + JS observer

## Performance-Skala (1 Mio.)
| Komponente | Tipp | Zeit (8-Core) |
|------------|--------------------------|--------------|
| PIL Thumbs | Multiprocessing + LANCZOS | ~10h für 1M  |
| DB         | Indizes + WAL             | <5ms Query   |
| GUI        | Infinite Scroll + Static  | 60fps Scroll |
| Speicher   | Thumbs in SSD-Ordner      | <100GB total |

## Best Practices
- Worker-Skript separat laufen lassen
- GUI nur Thumbs anzeigen
- Für Plex-Full: Jellyfin integrieren

---
*Letzte Aktualisierung: 10. März 2026*
