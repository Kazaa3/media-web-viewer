# DOCX in Python – Lesen, Schreiben, Metadaten & Eel-Integration

## Installation
```bash
pip install python-docx
```

## DOCX Lesen
```python
from docx import Document

doc = Document('example.docx')

# Paragraphen
for paragraph in doc.paragraphs:
    print(f"Text: {paragraph.text}")
    print(f"Style: {paragraph.style.name}")

# Tabellen
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
```

## Metadaten extrahieren
```python
print(doc.core_properties.title)
print(doc.core_properties.author)
print(doc.core_properties.subject)
print(doc.core_properties.created)
print(doc.core_properties.modified)

page_count = len(doc.sections)
word_count = sum(len(p.text.split()) for p in doc.paragraphs)
para_count = len(doc.paragraphs)
```

## DOCX Schreiben/Erstellen
```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor

doc = Document()
doc.add_heading('Mein Dokument', 0)
para = doc.add_paragraph('Dies ist ein Absatz.')
para.style = 'List Bullet'
doc.add_heading('Abschnitt 1', level=1)
doc.add_paragraph('Normaler Text hier.')
table = doc.add_table(rows=2, cols=3)
table.style = 'Light Grid Accent 1'
header_cells = table.rows[0].cells
header_cells[0].text = 'Dateiname'
header_cells[1].text = 'Größe'
header_cells[2].text = 'Typ'
row_cells = table.rows[1].cells
row_cells[0].text = 'track.flac'
row_cells[1].text = '150 MB'
row_cells[2].text = 'Audio'
doc.add_picture('cover.png', width=Inches(2.5))
doc.add_page_break()
doc.save('output.docx')
```

## Formatting: Bold, Italic, Farbe
```python
para = doc.add_paragraph()
para.add_run('Normaler Text ')
run = para.add_run('Fett Text')
run.bold = True
para.add_run(' und ')
run2 = para.add_run('Kursiv')
run2.italic = True
run3 = para.add_run(' und Rot')
run3.font.color.rgb = RGBColor(255, 0, 0)
run3.font.size = Pt(14)
```

## Eel-Integration für Media-Library
```python
import eel
from docx import Document
import json

@eel.expose
def extract_docx_metadata(filepath):
    try:
        doc = Document(filepath)
        metadata = {
            'title': doc.core_properties.title or 'Unbekannt',
            'author': doc.core_properties.author or '-',
            'subject': doc.core_properties.subject or '-',
            'created': str(doc.core_properties.created),
            'modified': str(doc.core_properties.modified),
            'paragraphs': len(doc.paragraphs),
            'tables': len(doc.tables),
            'words': sum(len(p.text.split()) for p in doc.paragraphs),
        }
        return json.dumps({'success': True, 'data': metadata})
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})

@eel.expose
def extract_docx_text(filepath):
    try:
        doc = Document(filepath)
        text = '\n\n'.join([p.text for p in doc.paragraphs])
        return json.dumps({'success': True, 'text': text[:5000]})
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
```

## JavaScript/Vue.js-Call
```javascript
async function loadDocx(filePath) {
    const meta = await eel.extract_docx_metadata(filePath)();
    const text = await eel.extract_docx_text(filePath)();
    console.log('Metadaten:', meta);
    console.log('Text-Preview:', text);
    // In UI anzeigen...
}
```

## Best Practices
- Für große DOCX-Dateien Text begrenzen (Performance).
- Vorschau im Frontend als reiner Text rendern.
- Fehler robust abfangen und als JSON zurückgeben.
- Für Konvertierung zu PDF: python-docx unterstützt dies nicht direkt, aber mit ReportLab oder docx2pdf möglich.

---
*Letzte Aktualisierung: 10. März 2026*
