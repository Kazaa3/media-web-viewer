# Calibre-Style PDF-Import & Sortierung mit Python

## 1. Calibre-API nutzen (empfohlen)
- Voraussetzung: Calibre installiert
- Skript mit calibre-debug ausführbar

**Beispiel:**
```python
# calibre_pdf_importer.py
from calibre.library import db
from calibre.ebooks.metadata import MetaInformation
import fitz  # PyMuPDF für PDF-Metadaten
LIBRARY_PATH = "/Pfad/zu/deiner/Calibre-Library"
db_obj = db(LIBRARY_PATH).new_api

@eel.expose
def import_pdf_calibre_style(pdf_path):
    doc = fitz.open(pdf_path)
    meta_dict = dict(doc.metadata)
    mi = MetaInformation(
        title=meta_dict.get('title', 'Unbekannt'),
        authors=[meta_dict.get('author', 'Unbekannt')],
        tags=meta_dict.get('keywords', '').split(', ')
    )
    book_id = db_obj.import_book(pdf_path, [mi])
    db_obj.set_metadata(book_id, mi)
    db_obj.set_authors(book_id, mi.authors)
    db_obj.dirty_canonical_names()
    doc.close()
    return {'success': True, 'book_id': book_id, 'info': mi.to_dict()}
```
**Ausführen:**
```bash
calibre-debug -e calibre_pdf_importer.py /Pfad/zu/deiner/library ~/Dokumente/mein_buch.pdf
```

---

## 2. Eigene DB (SQLite + PyMuPDF) – Calibre-nachgebaut

**Schema:**
```python
import sqlite3
import fitz
import os
import eel
from datetime import datetime
DB_PATH = "media_library.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        authors TEXT,
        tags TEXT,
        publisher TEXT,
        pub_year INTEGER,
        path TEXT UNIQUE,
        size INTEGER,
        added_date TEXT,
        sort_key TEXT
    )
    ''')
    conn.commit()
    conn.close()

@eel.expose
def import_pdf_custom(pdf_path):
    doc = fitz.open(pdf_path)
    meta = dict(doc.metadata)
    title = meta.get('title', os.path.basename(pdf_path))
    authors = meta.get('author', 'Unbekannt')
    tags = meta.get('keywords', '')
    publisher = meta.get('producer', '')
    sort_key = f"{authors.split()[-1].lower()}, {title.lower()}"
    doc.close()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
        INSERT INTO books (title, authors, tags, publisher, pub_year, path, size, added_date, sort_key)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            title, authors, tags, publisher, None, pdf_path,
            os.path.getsize(pdf_path), datetime.now().isoformat(), sort_key
        ))
        book_id = c.lastrowid
        conn.commit()
        return {'success': True, 'id': book_id, 'title': title}
    except sqlite3.IntegrityError:
        return {'success': False, 'error': 'Datei bereits vorhanden'}
    finally:
        conn.close()

@eel.expose
def get_sorted_books(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM books ORDER BY sort_key, added_date DESC LIMIT ?', (limit,))
    books = [{'id': row[0], 'title': row[1], 'authors': row[2], 'path': row[6]} for row in c.fetchall()]
    conn.close()
    return json.dumps(books)
```

---

## Vollständiger Importer (Ordner scannen)
```python
import glob
import os
@eel.expose
def import_folder(folder_path):
    pdf_files = glob.glob(os.path.join(folder_path, "**/*.pdf"), recursive=True)
    results = []
    for pdf in pdf_files:
        result = import_pdf_custom(pdf)
        results.append(result)
    return {'imported': len([r for r in results if r['success']]), 'total': len(pdf_files)}
```

---

## JS-Integration (Eel-App)
```javascript
async function importPdfs(folder) {
    const result = await eel.import_folder(folder)();
    console.log(`${result.imported}/${result.total} PDFs importiert!`);
    const books = await eel.get_sorted_books()();
    displayBooks(JSON.parse(books));
}
```

---

## Calibre-Features nachgebaut
| Feature     | Calibre         | Python-Lösung         |
|-------------|-----------------|-----------------------|
| Metadaten   | PDF-XMP liest   | PyMuPDF doc.metadata   |
| Auto-Sort   | Author_sort     | sort_key = "Nachname, Titel" |
| Tags/Series | Keywords → Tags | Direkt aus Metadata    |
| Duplicates  | UNIQUE path     | SQLite UNIQUE constraint |
| Export      | OPF/CSV         | Pandas/CSV             |

---

## Vorteile deiner Lösung
- Keine Calibre-Abhängigkeit nötig
- Voll integriert in Eel/Vue.js
- Erweiterbar für Audio (mutagen) + EPUB/DOCX

---

**Start:**
- init_db() aufrufen, dann PDFs importieren

**Frage:**
Wie viele PDFs sollen importiert werden? (Batch-Import möglich!)
