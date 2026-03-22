# isbnlib: Python-Bibliothek für ISBN und Buch-Metadaten

## Überblick
isbnlib ist eine leistungsstarke Python-Bibliothek zur Verarbeitung, Validierung und Abfrage von ISBNs sowie zum Abrufen von Buch-Metadaten – ideal für Offline- und Hybrid-Bücherei-Apps.

---

## Installation
```bash
pip install isbnlib
```

---

## Hauptfunktionen
- **Validierung:**
  - `isbnlib.is_isbn10(isbn)` – Prüft ISBN-10
  - `isbnlib.is_isbn13(isbn)` – Prüft ISBN-13
- **Standardisierung:**
  - `isbnlib.get_canonical_isbn(isbn)` – Wandelt ISBN in kanonisches Format
- **Metadaten-Abfrage:**
  - `isbnlib.meta(isbn, service='goob')` – Holt Buchdaten (Google Books, cached)
  - `isbnlib.meta(isbn, service='openl')` – Holt Buchdaten (OpenLibrary)
- **Barcode-Integration:**
  - Kombinierbar mit pyzbar/opencv für Barcode-Scanner

---

## Beispiel
```python
import isbnlib
isbn = '978-3-16-148410-0'
if isbnlib.is_isbn13(isbn):
    meta = isbnlib.meta(isbn, service='goob')
    print(meta['Title'], meta['Authors'])
```

---

## Workflow für Offline/Hybrid-Bücherei
1. Scan ISBN (USB-Scanner/Webcam)
2. Validierung mit isbnlib
3. Metadaten aus Cache oder Online-Service
4. Speicherung in Supabase/SQLite

---

## Integrationstipps
- Für große Sammlungen: Lokaler Cache (JSON/DB)
- Fallback: Google Books/OpenLibrary für fehlende Daten
- Kombinierbar mit Calibre, Supabase, NiceGUI

---

**Frage:**
Möchten Sie weitere Beispiele für Barcode-Scanner oder Metadaten-Workflow?
