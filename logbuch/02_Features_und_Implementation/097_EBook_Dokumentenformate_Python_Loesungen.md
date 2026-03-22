# E-Book & Dokumentenformate: Python-Lösungen

## Übersicht
Diese Liste deckt die wichtigsten E-Book- und Dokumentenformate für eine vollständige Media-Library ab. Für jedes Format sind Häufigkeit, Python-Library und Installationshinweise angegeben. Ein universeller Router (Eel) ist als Codebeispiel enthalten.

---

## E-Book-Formate (Top-überschaut)
| Format      | Häufigkeit | Python-Library         | Installation                  |
|------------|------------|-----------------------|-------------------------------|
| MOBI/AZW3  | ⭐⭐⭐⭐⭐      | kindleunpack/calibre  | pip install ebooklib (Teil)   |
| ODT        | ⭐⭐⭐⭐       | odfpy                 | pip install odfpy             |
| RTF        | ⭐⭐⭐        | striprtf/unrtf        | pip install striprtf          |
| FB2        | ⭐⭐⭐        | fb2reader             | pip install pysimplegui + XML |
| CBZ/CBR    | ⭐⭐⭐        | zipfile/rarfile       | pip install rarfile           |

---

## Dokumente/Andere
| Format | Python-Library      | Installation           |
|--------|--------------------|------------------------|
| HTML   | beautifulsoup4     | pip install bs4        |
| TXT    | open() (stdlib)    | -                      |
| XLSX   | openpyxl           | pip install openpyxl   |
| PPTX   | python-pptx        | pip install python-pptx|

---

## Vollständiger Formate-Router (Eel)
```python
import fitz  # PyMuPDF (EPUB/PDF/CBZ)
from docx import Document
import odf.opendocument
from striprtf.striprtf import rtf_to_text
import zipfile
import rarfile
import json
import eel

@eel.expose
def process_any_file(filepath):
    ext = filepath.lower().split('.')[-1]
    try:
        if ext in ['epub', 'pdf', 'cbz']:
            doc = fitz.open(filepath)
            return json.dumps({
                'format': ext.upper(),
                'title': doc.metadata.get('title'),
                'pages': len(doc)
            })
        elif ext == 'docx':
            d = Document(filepath)
            return json.dumps({
                'format': 'DOCX',
                'title': d.core_properties.title,
                'paragraphs': len(d.paragraphs)
            })
        elif ext == 'odt':
            odt_doc = odf.opendocument.load(filepath)
            return json.dumps({
                'format': 'ODT',
                'title': odt_doc.meta.title,
                'text': odt_doc.text.get_text()
            })
        elif ext == 'rtf':
            with open(filepath, 'r') as f:
                text = rtf_to_text(f.read())
            return json.dumps({'format': 'RTF', 'text_preview': text[:1000]})
        elif ext == 'cbr':
            with rarfile.RarFile(filepath) as rf:
                files = rf.namelist()
            return json.dumps({'format': 'CBR', 'images': len([f for f in files if f.lower().endswith(('.jpg','.png'))])})
        elif ext == 'cbz':
            with zipfile.ZipFile(filepath) as zf:
                files = zf.namelist()
            return json.dumps({'format': 'CBZ', 'images': len([f for f in files if f.lower().endswith(('.jpg','.png'))])})
        elif ext == 'mobi':
            # Calibre-API oder kindlegen
            return json.dumps({'format': 'MOBI', 'note': 'Calibre konvertieren empfohlen'})
        else:
            return json.dumps({'error': f'Unbekanntes Format: .{ext}'})
    except Exception as e:
        return json.dumps({'error': str(e)})
```

---

## Installation (einmalig)
```bash
pip install pymupdf odfpy striprtf rarfile python-docx beautifulsoup4 openpyxl python-pptx
```

---

## Exotische Formate (optional)
- **DjVu:** `pip install djvulibre-python` (Scans/komprimierte PDFs)
- **CHM:** `pip install pyCHM` (Hilfe-Dateien)
- **PDB/PalmDOC:** Sehr alt → Calibre konvertieren

---

## Calibre-Integration für ALLES
```python
from calibre.library import db

db_obj = db("/Pfad/Calibre-Library").new_api
book_id = db_obj.import_book("datei.mobi", None)  # Auto-Metadaten
```

---

## Priorisierung & Tipps
- **MOBI/AZW3:** Für Kindle-Nutzer besonders relevant
- **ODT:** OpenOffice/LibreOffice, oft in Bibliotheken
- **CBZ/CBR:** Comics, Manga

---

**Frage:**
Welche Formate findest du in deinem Ordner? Für neue Formate einfach den Router erweitern!
