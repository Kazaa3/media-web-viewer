# Python-docx – Erweiterte Features für Media-Library

## Tabellen: Erstellen, Lesen, Mergen
```python
from docx import Document
from docx.shared import Cm

doc = Document()
table = doc.add_table(rows=3, cols=4)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Datei'
hdr_cells[1].text = 'Dauer'
hdr_cells[2].text = 'Album'
hdr_cells[3].text = 'Cover'
for row_idx, track in enumerate([('01 - Intro.flac', '3:45', 'Album1', 'ja'), ('02 - Main.mp3', '4:20', 'Album1', 'nein')]):
    row = table.rows[row_idx + 1].cells
    row[0].text = track[0]
    row[1].text = track[1]
    row[2].text = track[2]
    row[3].text = track[3]
table.rows[2].cells[0].merge(table.rows[2].cells[1])
doc.save('tracks_table.docx')
```

## Bilder einfügen & Hyperlink
```python
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture('cover.jpg', width=Cm(5))
# Hyperlink zum Bild (Workaround)
def add_hyperlink_image(paragraph, url, image_path, width=Cm(5)):
    run = paragraph.add_run()
    run.add_picture(image_path, width=width)
    r_id = paragraph.part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = docx.oxml.shared.OxmlElement('a:hlinkClick')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id)
    run._element.insert(0, hyperlink)
add_hyperlink_image(p, 'https://example.com/album', 'cover.jpg')
doc.save('cover_with_link.docx')
```

## Erweiterte Metadaten
```python
from docx import Document
doc = Document('example.docx')
props = doc.core_properties
metadata = {
    'title': props.title,
    'author': props.author,
    'company': props.company,
    'category': props.category,
    'keywords': props.keywords,
    'comments': props.comments,
    'created': str(props.created) if props.created else None,
    'modified': str(props.modified) if props.modified else None
}
try:
    for custom in props.custom_properties:
        metadata[f'custom_{custom.name}'] = custom.value
except:
    pass
print(metadata)
```

## DOCX zu PDF konvertieren
```bash
pip install docx2pdf
```
```python
from docx2pdf import convert
convert('input.docx', 'output.pdf')
convert('meine_docs/')
@eel.expose
def docx_to_pdf(input_path, output_path):
    try:
        convert(input_path, output_path)
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

## Vollständige Media-Export-Funktion
```python
@eel.expose
def export_library_to_docx(tracks_data):
    doc = Document()
    doc.add_heading('Media Library Export', 0)
    table = doc.add_table(rows=1, cols=2)
    table.cell(0, 0).text = 'Gesamt Tracks'
    table.cell(0, 1).text = str(len(tracks_data))
    for track in tracks_data:
        p = doc.add_paragraph(f"{track['name']} ({track['duration']})")
        p.add_run(f" - {track['album']}").italic = True
        if 'cover_path' in track and track['cover_path']:
            run = p.add_run()
            run.add_picture(track['cover_path'], width=Cm(2))
    doc.save('library_export.docx')
    return {'success': True, 'file': 'library_export.docx'}
```

## Best Practices
- Tabellen für strukturierte Exporte (z.B. Tracklisten)
- Bilder und Hyperlinks für visuelle und interaktive Dokumente
- Erweiterte Metadaten für Archivierung und Suche
- DOCX zu PDF für universellen Export
- Fehler robust abfangen, Eel-Expose für UI-Integration

---

## Pro-Tipps
- Performance: Bei großen DOCX-Dateien nur Metadaten/Text laden, nicht alles (z.B. keine Bilder oder Tabellen).
- Fehlerbehandlung: Immer try/except nutzen, um korrupte oder inkompatible Dateien abzufangen.
- Alternative für komplexe PDFs: pypandoc oder LibreOffice CLI für DOCX→PDF-Konvertierung (z.B. bei Formatierungsproblemen).

---
Was möchtest du als Nächstes? (z.B. EPUB, PDF-Handling oder Voll-Export-Skript?)

*Letzte Aktualisierung: 10. März 2026*
