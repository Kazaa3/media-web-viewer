# Calibre Python-API: Batch-Sort/Add für Eel-App

## Beste Python-APIs für Batch

### 1. calibredb (Offiziell, CLI-wrapper)
- Kein pip install calibre nötig!
- Robust, schnell, CLI-basiert

**Beispiel:**
```python
import subprocess
import json
LIBRARY_PATH = "/home/user/Calibre-Library"

def add_pdf_batch(pdf_paths):
    cmd = ['calibredb', 'add'] + pdf_paths + [
        '--library-path', LIBRARY_PATH,
        '--automerge', '--duplicates'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def set_metadata_batch(book_ids, title=None, author=None):
    for book_id in book_ids:
        cmd = ['calibredb', 'set_metadata', book_id,
               '--library-path', LIBRARY_PATH,
               '--title', title or '',
               '--authors', author or '']
        subprocess.run(cmd)

def search_books(query):
    cmd = ['calibredb', 'search', query, '--library-path', LIBRARY_PATH, '--for-machine']
    output = subprocess.run(cmd, capture_output=True, text=True).stdout
    return json.loads(output)

@eel.expose
def batch_import_pdfs(pdf_paths):
    success = add_pdf_batch(pdf_paths)
    if success:
        books = search_books("path:*")
    return books
```
**Speed:** 100 PDFs/min, auto-sort nach Autor/Titel

---

### 2. PyCalibre (pip install pycalibre)
- Python-Library, weniger robust als CLI

**Beispiel:**
```python
from pycalibre import Library
with Library(LIBRARY_PATH) as lib:
    lib.add_books(pdf_paths)
    for book in lib.books:
        book.set_metadata(title="KI-Sortiert", tags="pdf,wissen")
    sorted_books = lib.search("tags:pdf", sort_by="title")
```

---

### 3. Direkt DB-Zugriff (fortgeschritten)
- Für Custom-Sort aus SQLite (z.B. ai_tags)

**Beispiel:**
```python
from calibre.db.backend import DB
from calibre.db.cache import Cache
db = DB(LIBRARY_PATH)
cache = Cache(db)
books = list(cache.all_book_ids())
# Batch sortieren: cache.set_metadata(...)
db.close()
```

---

## Batch-Sort in Eel-App
**Voll-Beispiel:**
```python
@eel.expose
def smart_sort_pdfs(pdf_paths, ai_tags=None):
    add_pdf_batch(pdf_paths)
    book_ids = search_books("path:" + pdf_paths[0])['book_ids']
    if ai_tags:
        set_metadata_batch(book_ids, tags=",".join(ai_tags))
    for book in search_books("id:" + ",".join(map(str, book_ids))):
        insert_to_media_db(book['path'], book['title'], book['tags'])
    return "Sortiert & synced!"
```
**JS:**
```javascript
eel.smart_sort_pdfs(['/pdf1.pdf'], ['wissen', 'ki'])
```

---

## Automatisierung
**Cron:** Neue PDFs sortieren
```bash
0 * * * * calibredb list --library-path ~/Calibre-Library --for-machine --fields title,authors | python sync_to_sqlite.py
```

---

## Empfehlung
- calibredb für Batch – robust, keine Lib-Probleme
- PyCalibre für Python-only
- Direkt DB für Custom-Sync

---

**Frage:**
Möchtest du zuerst calibredb testen oder PyCalibre pip ausprobieren?
