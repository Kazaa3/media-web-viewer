# Calibredb: Robust Batch-Import für Media-Library

## Empfehlung
- **calibredb**: Offiziell, robust, keine pip-Abhängigkeit, ideal für 1M+ PDFs
- **PyCalibre**: Pure Python, als Alternative/wrapper

---

## Schnell-Test: Calibredb

### 1. Library vorbereiten
```bash
mkdir ~/Test-Calibre
calibredb add /path/to/test.pdf --library-path ~/Test-Calibre
```

### 2. Batch-Add + Auto-Sort (Python)
```python
import subprocess
import glob
LIBRARY_PATH = "~/Calibre-Library"
def test_calibredb_batch():
    pdfs = glob.glob("/volume1/ABC/01 Medien/PDFs/*.pdf")[:10]
    cmd = ['calibredb', 'add', *pdfs,
           '--library-path', LIBRARY_PATH,
           '--automerge', '--duplicates',
           '--field', 'tags:pdf,wissen']
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Erfolg:", result.returncode == 0)
    print("Output:", result.stdout)
test_calibredb_batch()
```
- Sortiert automatisch nach Autor/Titel (Calibre-Magie)

### 3. Suche/Sort
```bash
calibredb list --library-path ~/Calibre-Library --search "tags:wissen" --sort-by "title"
```

---

## PyCalibre: pip-API (Alternative)
```bash
pip install pycalibre
```
```python
from pycalibre import Library
def pycalibre_batch():
    lib = Library(LIBRARY_PATH)
    pdf_paths = ["/pdf1.pdf", "/pdf2.pdf"]
    new_books = lib.add_books(pdf_paths)
    for book in new_books:
        book.tags = ["pdf", "ebook", "wissen"]
        book.save()
    sorted_books = lib.get_books(sort_by="title")
    return [(b.title, b.path) for b in sorted_books]
@eel.expose
def calibre_sort_batch(pdf_paths):
    return pycalibre_batch(pdf_paths)
```
- Einfacher, aber calibredb stabiler für Bulk

---

## Voll-Test-Skript (Eel-ready)
```python
def full_test():
    print("=== Calibredb Test ===")
    test_calibredb_batch()
    print("=== PyCalibre Test ===")
    try:
        pycalibre_batch()
        print("✓ Beide funktionieren!")
    except ImportError:
        print("PyCalibre: pip install pycalibre")
full_test()
```
- Kopiere 5 PDFs → python test.py → Check ~/Calibre-Library

---

## Entscheidung
| Methode     | Pro                  | Contra         |
|-------------|----------------------|--------------- |
| calibredb   | Offiziell, robust    | CLI-Wrapper    |
| PyCalibre   | Pure Python          | Weniger mature |

---

## Start
- Beginne mit calibredb (5-Min-Setup), dann Eel-Expose
- Test-Skript laufen oder calibre-server + API sync

---

**Frage:**
Soll das Test-Skript ausgeführt werden oder direkt calibre-server + API-Sync eingerichtet werden?
