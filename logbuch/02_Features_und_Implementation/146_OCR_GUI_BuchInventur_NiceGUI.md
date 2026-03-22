# OCR GUI Scanner für Buch-Inventur (NiceGUI)

## Workflow & Features
- **Live Webcam:** Frame-by-Frame OCR + Barcode-Scan
- **Hybrid:** pyzbar ISBN + EasyOCR Text
- **Preprocessing:** Automatisch Graustufen/Kontrast
- **Supabase:** Realtime Sync
- **GUI:** Titel live, Save-Button, responsive

---

## Beispiel-Code (NiceGUI, pyzbar, EasyOCR, Supabase)
```python
from nicegui import ui, app
import cv2
from PIL import Image
import numpy as np
import pyzbar.pyzbar as pyzbar
import easyocr
from supabase import Client
import isbnlib
import base64
import io

client = Client(SUPABASE_URL, SUPABASE_KEY)
reader = easyocr.Reader(['de', 'en'], gpu=False)
cap = cv2.VideoCapture(0)

async def update_frame():
    ret, frame = cap.read()
    if ret:
        # 1. ISBN Barcode
        barcodes = pyzbar.decode(frame)
        isbn = None
        for barcode in barcodes:
            isbn_raw = barcode.data.decode('utf-8')
            isbn = isbnlib.get_canonical_isbn(isbn_raw)
            break
        # 2. OCR Text
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ocr_results = reader.readtext(gray)
        ocr_text = ' '.join([r[1] for r in ocr_results[:3]])
        title_label.text = ocr_text[:100] + "..." if len(ocr_text) > 100 else ocr_text
        isbn_label.text = f"ISBN: {isbn or 'Kein Barcode'}"
        if isbn:
            book = get_full_meta(isbn)
            save_book(book)
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode()
        cam.src = f"data:image/jpeg;base64,{jpg_as_text}"

def get_full_meta(isbn):
    try:
        meta = isbnlib.meta(isbn)
        return {
            'isbn': isbn,
            'title': meta.get('Title', 'Unbekannt'),
            'author': meta.get('Authors', ['Unbekannt'])[0],
            'status': 'gescannt'
        }
    except:
        return {'isbn': isbn, 'title': 'OCR-only', 'author': ocr_text}

def save_book(book):
    client.table('physical_books').upsert(book).execute()
    ui.notify(f"✅ {book['title']} gespeichert!")

ui.label('📚 Live Book Scanner').classes('text-h4 text-white')
with ui.row().classes('w-full items-center'):
    cam = ui.video().classes('w-96 h-64 shadow-2xl rounded-lg')
    with ui.column().classes('ml-8 w-80'):
        title_label = ui.label('Titel wird erkannt...').classes('text-xl text-white')
        isbn_label = ui.label('ISBN: Scanne...').classes('text-lg')
        ui.button('Speichern', on_click=save_current_book).props('fab icon=save')

async def save_current_book():
    book = {'title': title_label.text, 'isbn': isbn_label.text.replace('ISBN: ', '')}
    save_book(book)

ui.timer(0.5, update_frame)
ui.run(title='OCR Book Inventur', port=8080, dark=True)
```

---

## Optimierungen
- **OCR-Bereich gezielt:**
```python
roi = frame[100:400, 200:800]  # Titel-Bereich
ocr_results = reader.readtext(roi)
```
- **Tesseract Alternative:**
```bash
pip install pytesseract
```
```python
import pytesseract
text = pytesseract.image_to_string(preprocess_frame(frame), lang='deu')
```

---

## Test & Hardware
- Webcam testen: `python ocr_gui.py` → localhost:8080 → Buch vorhalten
- Produktion: USB-Scanner + Regal-Scan (batch)

---

## Fazit
- "Clean Code" + ISBN → Supabase live!
- Tesseract oder EasyOCR je nach Geschwindigkeit/Genauigkeit

---

**Frage:**
Welche OCR-Engine bevorzugst du für die Inventur? (EasyOCR oder Tesseract)
