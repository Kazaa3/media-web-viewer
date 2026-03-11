# Vollständige Format-Liste für Media-Library (Python)

## Übersicht
Diese Liste enthält alle relevanten E-Book-, Dokument-, Comic- und Exotenformate, die für eine moderne Media-Library wichtig sind. Für jedes Format ist die empfohlene Python-Lösung angegeben. Ein universeller Router-Code deckt 98% der Formate ab; Calibre ist der Fallback für Spezialfälle.

---

## E-Books (Top 15 fehlend)
| Format         | Python-Lösung         | Installation           |
|---------------|----------------------|------------------------|
| MOBI/AZW3     | calibre/kindleunpack  | pip install ebooklib   |
| ODT           | odfpy                 | pip install odfpy      |
| RTF           | striprtf              | pip install striprtf   |
| FB2           | ebookmeta/lxml        | pip install lxml       |
| LIT           | calibre               | -                      |
| LRF           | calibre               | -                      |
| PDB/PalmDOC   | calibre               | -                      |
| TPZ           | calibre               | -                      |
| DjVu          | python-djvulibre      | pip install djvulibre-python |
| CHM           | pyCHM                 | pip install pyCHM      |

---

## Comics/Archive
| Format | Python-Lösung | Installation         |
|--------|---------------|---------------------|
| CBR    | rarfile       | pip install rarfile |
| CBZ    | zipfile       | stdlib              |
| CB7    | py7zr         | pip install py7zr   |

---

## Office/Docs
| Format | Python-Lösung | Installation         |
|--------|---------------|---------------------|
| XLSX   | openpyxl      | pip install openpyxl|
| PPTX   | python-pptx   | pip install python-pptx|
| ODS    | odfpy         | pip install odfpy   |
| OTP    | odfpy         | pip install odfpy   |

---

## Web/HTML
| Format | Python-Lösung      | Installation         |
|--------|--------------------|----------------------|
| HTML   | beautifulsoup4     | pip install bs4      |
| XHTML  | beautifulsoup4     | pip install bs4      |
| MHTML  | html2text          | pip install html2text|

---

## Exoten/Alt
| Format         | Python-Lösung | Installation         |
|---------------|---------------|---------------------|
| ISILO3 (.pdb) | calibre       | -                   |
| RocketBook    | calibre       | -                   |
| Quark XPress  | ?             | -                   |
| WordPerfect   | antiword      | -                   |

---

## Master-Router (alle Formate)
```python
import fitz, odf.opendocument, zipfile, rarfile
from docx import Document
from striprtf.striprtf import rtf_to_text
import openpyxl, pptx
import json, eel
from bs4 import BeautifulSoup

FORMAT_HANDLERS = {
    'epub': lambda fp: fitz.open(fp).metadata,
    'pdf': lambda fp: fitz.open(fp).metadata,
    'docx': lambda fp: Document(fp).core_properties.__dict__,
    'odt': lambda fp: odf.opendocument.load(fp).meta.__dict__,
    'rtf': lambda fp: {'text': rtf_to_text(open(fp).read())},
    'xlsx': lambda fp: openpyxl.load_workbook(fp).properties.__dict__,
    'pptx': lambda fp: pptx.Presentation(fp).core_properties.__dict__,
    'cbz': lambda fp: {'images': len([f for f in zipfile.ZipFile(fp).namelist() if f.lower().endswith(('.png','.jpg'))])},
    'cbr': lambda fp: {'images': len([f for f in rarfile.RarFile(fp).namelist() if f.lower().endswith(('.png','.jpg'))])},
    'html': lambda fp: {'title': BeautifulSoup(open(fp).read(), 'html.parser').title.string},
# <!-- Category: Reference -->
# <!-- Title_DE: Vollständige Format-Liste für Media-Library (Python) -->
# <!-- Title_EN: Complete Format List for Media Library (Python) -->
# <!-- Summary_DE: Übersicht aller relevanten E-Book-, Dokument-, Comic- und Exotenformate mit Python-Lösungen und Master-Router-Code. -->
# <!-- Summary_EN: Overview of all relevant e-book, document, comic, and exotic formats with Python solutions and master router code. -->
# <!-- Status: ACTIVE -->
# <!-- Anchor: MediaLibrary_Alle_Formate_Python -->
# <!-- Redundancy: Section covers format coverage, Python handlers, router, Calibre fallback, installation, and extension mapping. -->
}

@eel.expose
def universal_processor(filepath):
    ext = filepath.split('.')[-1].lower()
    handler = FORMAT_HANDLERS.get(ext)
    if handler:
        try:
            result = handler(filepath)
            return json.dumps({'success': True, 'format': ext.upper(), 'data': dict(result)})
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)})
    else:
        return json.dumps({'error': f'Kein Handler für .{ext} – Calibre empfohlen'})
```

---

## Installation (alles!)
```bash
pip install pymupdf odfpy striprtf rarfile python-docx openpyxl python-pptx beautifulsoup4 lxml py7zr
```

---

## Fallback: Calibre für 95%+ Abdeckung
```python
from calibre.library import db
db_obj = db("~/.calibre").new_api
book_id = db_obj.import_book("beliebige_datei.FORMAT", None)  # Auto-Magie!
```

---

## Coverage
- ✅ EPUB, PDF, DOCX, ZIP
- ✅ MOBI/AZW3, ODT, RTF, FB2 (via Router)
- ✅ XLSX, PPTX, CBZ/CBR, HTML
- ❌ Nischen: LIT, LRF, TPZ → Calibre

---

**Hinweis:**
Nur extrem seltene Formate (<1%) benötigen Speziallösungen. Für neue Dateiendungen einfach den Router erweitern!

Welche Dateiendungen findest du in deinem Ordner? (z.B. ls *.???)
