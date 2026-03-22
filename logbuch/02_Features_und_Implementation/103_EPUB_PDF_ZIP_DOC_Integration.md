# EPUB, PDF, ZIP, DOC – Integration in Media Web Viewer

## Übersicht
Media Web Viewer unterstützt die Verarbeitung und Vorschau von EPUB, PDF, ZIP, DOCX und ähnlichen Formaten durch eine Kombination aus Python-Backend (Eel/Bottle) und JavaScript-Frontend. Python extrahiert Metadaten und Inhalte, JavaScript rendert die Vorschau im Browser.

## Python-Bibliotheken (Backend)
- **PyMuPDF (pymupdf):** EPUB, PDF, ZIP/CBZ, FB2 – Text, Bilder, Metadaten.
- **EbookLib:** EPUB2/3 erstellen/lesen/manipulieren.
- **python-docx:** DOC/DOCX lesen/schreiben.
- **zipfile:** ZIP entpacken/listen.

### Beispiel (Eel-expose)
```python
import eel
import pymupdf
from docx import Document
import zipfile
import json

@eel.expose
def process_file(filepath):
    data = {'metadata': {}, 'error': None}
    try:
        if filepath.endswith('.epub') or filepath.endswith('.pdf'):
            doc = pymupdf.open(filepath)
            data['pages'] = len(doc)
            data['title'] = doc.metadata.get('title', 'Unbekannt')
            doc.close()
        elif filepath.endswith('.docx'):
            d = Document(filepath)
            data['paragraphs'] = len(d.paragraphs)
        elif filepath.endswith('.zip'):
            with zipfile.ZipFile(filepath) as zf:
                data['files'] = zf.namelist()
        return json.dumps(data)
    except Exception as e:
        data['error'] = str(e)
        return json.dumps(data)
```

## JavaScript-Bibliotheken (Frontend)
- **epub.js:** EPUB rendern/paginate
- **pdf-lib/PDF.js:** PDF erstellen/anzeigen
- **zip.js:** ZIP handhaben
- **docx-preview/mammoth.js:** DOCX in HTML konvertieren

### Beispiel (JS, Eel-call)
```javascript
async function loadFile(filePath) {
    const result = await eel.process_file(filePath)();
    const data = JSON.parse(result);
    if (!data.error) {
        console.log('Metadaten:', data.metadata);
        // z.B. epub.js für Rendering: ePub(filePath).renderTo("viewer");
    } else {
        alert('Fehler: ' + data.error);
    }
}
```

## Integration-Workflow
1. JS sendet Dateipfad an Python (Eel-Bridge).
2. Python verarbeitet Datei, extrahiert Metadaten/Inhalte und gibt JSON zurück.
3. JS zeigt Vorschau oder Metadaten im Browser.

## Best Practices
- Python für Extraktion, JS für Vorschau/Rendering.
- Fehler robust abfangen und als JSON zurückgeben.
- Erweiterbar für weitere Formate (z.B. MOBI, FB2, CBR/CBZ).
- API-Design: Eel-expose für Dateiverarbeitung, JS für UI.

## Tools & Empfehlungen
- **Lesen:** Sumatra PDF, Icecream Ebook Reader, Adobe Acrobat Reader
- **Konvertieren:** HelpNDoc, FreePDFConvert, Bookize, Online-Konverter
- **ZIP:** Native OS-Unterstützung, zip.js, Python zipfile

---
*Letzte Aktualisierung: 10. März 2026*
