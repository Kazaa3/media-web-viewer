# odfpy vs odfdo: Voll-Vergleich & Media-Library Integration

## Feature-Vergleich
| Feature   | odfpy         | odfdo         | Gewinner |
|----------|---------------|--------------|----------|
| Ease     | Raw XML       | OOP API      | odfdo    |
| Aktiv    | Stabil        | Neu/Modern   | odfdo    |
| Docs     | OK            | Besser       | odfdo    |
| Size     | Klein         | Mittel       | odfpy    |

**Empfehlung:** odfdo für Media-Library (einfacher Code, moderne API)

---

## Installation
```bash
pip install odfdo supabase
```

---

## Media-Library Integration (odfdo)
```python
from odfdo import Document, DocumentMeta
from supabase import Client
import json
from pathlib import Path

client = Client(SUPABASE_URL, SUPABASE_KEY)

def process_odf_file(odf_path):
    """ODF → Supabase (Metadata + Text + Tables)"""
    doc = Document(odf_path)
    # 1. Metadaten
    meta = doc.meta
    data = {
        'path': str(odf_path),
        'type': 'odf',
        'format': odf_path.suffix,
        'title': meta.title or 'Unbekannt',
        'creator': meta.initial_creator or 'Unbekannt',
        'subject': meta.subject or '',
        'keywords': meta.keyword or '',
        'created': meta.creation_date,
        'language': meta.language
    }
    # 2. Volltext
    full_text = doc.full_text()
    data['text_preview'] = full_text[:1000]
    # 3. Tabellen
    tables = doc.body.get_tables()
    table_data = []
    for table in tables:
        rows = []
        for row in table.rows:
            cells = [cell.full_text() for cell in row.cells]
            rows.append(cells)
        table_data.append(rows)
    data['tables'] = json.dumps(table_data) if table_data else None
    # Supabase
    client.table('media').upsert(data).execute()
    print(f"✅ {data['title']} verarbeitet!")
    return data

# Batch
for odf in Path('odf_folder').glob('*.od[tps]'):
    process_odf_file(odf)
```

---

## odfpy Alternative (Raw XML)
```python
from odf.opendocument import load
from odf import teletype

doc = load('document.odt')
text = teletype.extractText(doc.getElementsByType(teletype.Paragraph))
meta = doc.meta
print(meta.title.textContent)
```

---

## ODF → Andere Formate (Calibre)
```python
import subprocess
subprocess.run(['ebook-convert', 'document.odt', 'document.pdf'])
```

---

## NiceGUI ODF Viewer + OCR
```python
ui.upload('ODF hochladen', on_upload=lambda e: process_odf_file(e.name))
ui.label('Vorschau:').bind_text_from(odf_preview, 'text_preview')

# OCR Umschlag + ODF Meta
async def scan_odf_cover():
    book = scan_book_frame(frame)  # Webcam
    odf_meta = process_odf_file('book.odt')
    combined = {**book, **odf_meta}
    client.table('physical_odf').upsert(combined).execute()
```

---

## Use-Cases
- .odt: Reports, Notizen → Text-Suche
- .ods: Tabellen → Pandas Import
- Inventur: Scan + ODF Meta validieren
- Test: .odt laden → Supabase

---

**Empfehlung:** odfdo first, odfpy fallback bei Spezialfällen.
