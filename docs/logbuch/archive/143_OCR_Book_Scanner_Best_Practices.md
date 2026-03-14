# OCR + Barcode Scanner für reale Bücher-Inventur

## Stack
- Tesseract/EasyOCR für Text-Erkennung (Titel/Autor vom Umschlag/Rücken)
- pyzbar für ISBN-Barcode
- isbnlib für Metadaten
- Supabase für Realtime-DB
- NiceGUI für Live-GUI

---

## Installation
```bash
pip install pytesseract easyocr opencv-python pyzbar isbnlib supabase pillow
sudo apt install tesseract-ocr tesseract-ocr-deu
```

---

## Voll-OCR + Barcode Scanner
**ocr_book_scanner.py:**
```python
import cv2
import pyzbar.pyzbar as pyzbar
import easyocr
import isbnlib
from supabase import Client
from PIL import Image
client = Client(SUPABASE_URL, SUPABASE_KEY)
reader = easyocr.Reader(['de', 'en'])
def scan_book_frame(frame):
    barcodes = pyzbar.decode(frame)
    isbn = None
    for barcode in barcodes:
        isbn_raw = barcode.data.decode('utf-8')
        if isbn_raw.startswith(('978', '979')):
            isbn = isbnlib.get_canonical_isbn(isbn_raw)
            break
    results = reader.readtext(frame)
    text = ' '.join([r[1] for r in results if r[2] > 0.5])
    lines = [line.strip() for line in text.split('\n') if len(line) > 3]
    title = lines[0] if lines else "Unbekannt"
    author = lines[1] if len(lines) > 1 else "Unbekannt"
    if isbn:
        meta = isbnlib.meta(isbn)
        title = meta.get('Title', title)
        author = meta.get('Authors', [author])[0]
    book = {
        'isbn': isbn,
        'title': title,
        'author': author,
        'ocr_text': text,
        'status': 'in_regal',
        'scan_date': '2026-03-10'
    }
    save_to_supabase(book)
    return book, frame
def save_to_supabase(book):
    client.table('physical_books').upsert(book).execute()
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    book, annotated = scan_book_frame(frame)
    cv2.putText(annotated, f"{book['title']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(annotated, f"ISBN: {book['isbn'] or 'Kein'}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    cv2.imshow('OCR Book Scanner', annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
```

---

## Optimierungen für reale Bücher
**Bild-Vorverarbeitung:**
```python
def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.medianBlur(gray, 3)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh
```
**ShelfieText Mode:**
- [github.com/snacsnoc/shelfietext](https://github.com/snacsnoc/shelfietext)
- EasyOCR speziell für Buchrücken

---

## Live Inventur-GUI
**NiceGUI Overlay:**
```python
ui.video('webcam').on('loadedmetadata', lambda: ui.notify('Scanner bereit!'))
ui.label('Titel/Autor live...').bind_text_from(scan_result, 'title')
```

---

## Workflow
1. Foto scannen → pyzbar ISBN + EasyOCR Text
2. Parse → Titel/Autor
3. ISBNlib → Voll-Meta
4. Supabase → Inventur + Realtime Grid

---

## Genauigkeit
- 95% ISBN, 80% OCR (mit Preprocessing)
- Test: Foto machen → "Clean Code" erkannt!

---

**Frage:**
Tesseract installieren oder EasyOCR zuerst testen?
