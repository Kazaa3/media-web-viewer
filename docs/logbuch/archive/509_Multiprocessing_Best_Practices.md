# Multiprocessing in Python – Best Practices für Media-Library

## Übersicht
Multiprocessing ermöglicht parallele Verarbeitung großer Datenmengen (z.B. 1 Mio. Bilder, Album Art, Thumbnails) und beschleunigt Batch-Jobs enorm. Ideal für Media-Library-Workflows: PIL, mutagen, API-Fetches.

## Vorteile
- Volle CPU-Auslastung (Multi-Core)
- Batch-Processing für Thumbnails, Metadaten, Art-Fetch
- Skalierbar für Millionen Dateien

## Grundstruktur
```python
import multiprocessing as mp

def worker(args):
    # Verarbeitung (z.B. PIL, mutagen, API)
    pass

if __name__ == "__main__":
    files = [...]  # Liste der Pfade
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(worker, files)
```

## Rate-Limiting für APIs
- ratemate (pip install ratemate) für API-Limits (z.B. MusicBrainz, Discogs)
- Proc-safe, besser als time.sleep

```python
from ratemate import RateLimit
api_limit = RateLimit(max_count=1, per=1)

def worker(args):
    api_limit()  # Limiter
    # API-Call
```

## PIL/Mutagen
- Thread-safe, ideal für parallele Bild- und Audioverarbeitung
- Beispiel: Thumbnails, Album Art

## Batch-Processing mit Pool
```python
from PIL import Image
from pathlib import Path

def process_image(args):
    img_path, thumb_dir, size = args
    thumb_path = Path(thumb_dir) / f"{img_path.stem}_thumb.jpg"
    if thumb_path.exists(): return
    with Image.open(img_path) as img:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(thumb_path, 'JPEG', quality=85, optimize=True)

if __name__ == "__main__":
    images = list(Path('images/').glob('*.jpg'))
    args = [(p, 'thumbnails/', (200,200)) for p in images]
    with mp.Pool() as pool:
        pool.map(process_image, args)
```

## API-Batch mit Limiter
```python
def process_single_file(args):
    audio_path, output_dir = args
    api_limit()  # Rate-Limit
    # Album Art extrahieren/fetchen
    # PIL Thumb
    return audio_path, art_path
```

## Eel-Expose für On-Demand
```python
@eel.expose
def process_file_batch(file_paths):
    with mp.Pool(4) as pool:
        results = pool.map(process_single_file, [(p, 'covers/') for p in file_paths])
    return results
```

## Best Practices
- Logging, Resume, Checkpoint-DB für große Batches
- Pool-Größe an CPU und API-Limit anpassen
- Fehler robust abfangen (try/except)
- Für reine CPU-Jobs: Pool voll ausnutzen
- Für API-Jobs: Limiter + weniger Worker

---
*Letzte Aktualisierung: 10. März 2026*
