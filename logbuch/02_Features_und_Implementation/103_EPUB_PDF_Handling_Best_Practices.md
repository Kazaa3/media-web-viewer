# EPUB & PDF Handling in Python – Best Practices für Media-Library

## Installation
```bash
pip install pymupdf ebooklib epub-meta
```

## EPUB: Metadaten und Text extrahieren
```python
import fitz  # PyMuPDF
import json
import eel

@eel.expose
def process_epub(filepath):
    doc = fitz.open(filepath)
    metadata = {
        'title': doc.metadata.get('title', 'Unbekannt'),
        'author': doc.metadata.get('author', '-'),
        'creator': doc.metadata.get('creator', '-'),
        'subject': doc.metadata.get('subject', '-'),
        'pages': len(doc),
        'language': doc.metadata.get('language', '-')
    }
    full_text = ""
    for page in doc:
        full_text += page.get_text()[:5000]
    doc.close()
    return json.dumps({
        'success': True,
        'metadata': metadata,
        'text_preview': full_text[:5000],
        'toc': doc.get_toc()
    })
```

## Alternative mit epub-meta
```python
import epub_meta
metadata = epub_meta.get_epub_metadata('book.epub', read_cover=True, read_toc=True)
print(metadata['title'], metadata['authors'], metadata['toc'])
```

## PDF: Text, Bilder, Metadaten
```python
import fitz
@eel.expose
def process_pdf(filepath):
    doc = fitz.open(filepath)
    metadata = dict(doc.metadata)
    text = ""
    images = []
    for page_num, page in enumerate(doc):
        text += page.get_text()
        img_list = page.get_images()
        for img_idx, img in enumerate(img_list):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:
                pix.save(f"page_{page_num}_img_{img_idx}.png")
                images.append(f"page_{page_num}_img_{img_idx}.png")
            pix = None
    doc.close()
    return json.dumps({
        'success': True,
        'metadata': metadata,
        'pages': len(doc),
        'text_preview': text[:5000],
        'images_extracted': len(images)
    })
```

## Vollständiger Media-Exporter (DOCX + EPUB + PDF)
```python
import eel
import fitz
from docx import Document
from docx.shared import Cm

@eel.expose
def export_library_multi(tracks):
    doc = Document()
    doc.add_heading('Media Library - Voll-Export', 0)
    for track in tracks:
        doc.add_heading(track['name'], level=1)
        if track['type'] == 'epub' or track['type'] == 'pdf':
            epub_doc = fitz.open(track['path'])
            meta = dict(epub_doc.metadata)
            epub_doc.close()
        elif track['type'] == 'docx':
            docx_d = Document(track['path'])
            meta = {
                'title': docx_d.core_properties.title,
                'author': docx_d.core_properties.author,
                'paragraphs': len(docx_d.paragraphs)
            }
        table = doc.add_table(rows=1, cols=2)
        table.cell(0, 0).text = 'Titel'
        table.cell(0, 1).text = meta.get('title', '-')
        doc.add_paragraph(f"Autor: {meta.get('author', '-')}")
        if 'cover_path' in track:
            p = doc.add_paragraph()
            run = p.add_run()
            run.add_picture(track['cover_path'], width=Cm(3))
    doc.save('full_library_export.docx')
    return {'success': True, 'file': 'full_library_export.docx'}
```

## JS-Frontend (Vue.js/Eel)
```javascript
async function scanFiles(files) {
    const results = [];
    for (let file of files) {
        let result;
        if (file.name.endsWith('.epub') || file.name.endsWith('.pdf')) {
            result = await eel.process_epub_or_pdf(file.path)();
        } else if (file.name.endsWith('.docx')) {
            result = await eel.extract_docx_metadata(file.path)();
        }
        results.push(JSON.parse(result));
    }
    await eel.export_library_multi(results)();
    alert('Export erfolgreich!');
}
```

## Vorteile
- PyMuPDF: Einheitlich für EPUB/PDF/ZIP/CBZ – extrahiert Text/Bilder/TOC superschnell
- Begrenze Text auf 5k Zeichen für UI
- Erweiterbar: mutagen-Integration für Audio

---
*Letzte Aktualisierung: 10. März 2026*
