# PDF-Handling: Praxis-Tipps für gemischte PDF-Typen

## Typen in deiner Library
- **Scanned PDFs:** OCR nötig, Layout oft komplex (Unstructured empfohlen für Tabellen/Formeln)
- **Tabellenreiche PDFs:** PyMuPDF extrahiert Tabellenstrukturen und Positionen, Unstructured erkennt Tabellen explizit
- **Einfache PDFs:** PyMuPDF oder PyPDF – schnell, präzise, ausreichend für Metadaten/Text
- **Multi-Format:** PyMuPDF unterstützt auch EPUB, DOCX, ZIP, Images

---

## Praxis-Workflow für gemischte PDFs
1. **Router nutzen:**
   - `smart_pdf_processor(pdf_path, method)`
   - Methode dynamisch wählen: 'pymupdf' (Standard), 'unstructured' (bei OCR/Tabellen), 'pypdf' (Backup)

2. **Import in SQLite-DB:**
   - Metadaten/Text mit PyMuPDF extrahieren
   - Bei Layout-Problemen: Unstructured als Fallback

3. **Batch-Import:**
   - Ordner scannen, PDFs mit passender Methode verarbeiten
   - Ergebnisse in DB speichern (siehe Calibre-Style-Importer)

---

## Beispiel: Automatische Methode wählen
```python
@eel.expose
def auto_pdf_import(pdf_path):
    # Heuristik: Scanned/Tabellenreich → Unstructured, sonst PyMuPDF
    import fitz
    doc = fitz.open(pdf_path)
    if doc.is_scanned or 'Table' in doc.metadata.get('keywords', ''):
        return smart_pdf_processor(pdf_path, method='unstructured')
    else:
        return smart_pdf_processor(pdf_path, method='pymupdf')
```

---

## Empfehlung
- PyMuPDF als Standard für Geschwindigkeit und Qualität
- Unstructured für Spezialfälle (OCR, komplexe Layouts)
- PyPDF als minimalistisches Backup
- Alle Methoden über Eel/JS verfügbar

---

**Frage:**
Soll der Importer automatisch die beste Methode pro PDF wählen (Heuristik), oder möchtest du manuell pro Datei entscheiden?
