# pyzbar ISBN + EasyOCR Text: Aufnahme für Buch-Inventur

## Workflow für Aufnahme
1. **Bild aufnehmen** (Webcam/Scanner)
2. **pyzbar**: ISBN-Barcode dekodieren
3. **EasyOCR**: Titel/Autor vom Umschlag/Rücken extrahieren
4. **isbnlib**: Metadaten ergänzen (offline/online)
5. **Supabase**: Speicherung, Realtime-GUI

---

## Beispiel-Code für Aufnahme
```python
import cv2
import pyzbar.pyzbar as pyzbar
import easyocr
import isbnlib
from supabase import Client
client = Client(SUPABASE_URL, SUPABASE_KEY)
reader = easyocr.Reader(['de', 'en'])
def scan_and_record():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        # 1. pyzbar: ISBN
        barcodes = pyzbar.decode(frame)
        isbn = None
        for barcode in barcodes:
            isbn_raw = barcode.data.decode('utf-8')
            if isbn_raw.startswith(('978', '979')):
                isbn = isbnlib.get_canonical_isbn(isbn_raw)
                break
        # 2. EasyOCR: Text
        results = reader.readtext(frame)
        text = ' '.join([r[1] for r in results if r[2] > 0.5])
        lines = [line.strip() for line in text.split('\n') if len(line) > 3]
        title = lines[0] if lines else "Unbekannt"
        author = lines[1] if len(lines) > 1 else "Unbekannt"
        # 3. isbnlib: Metadaten
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
        client.table('physical_books').upsert(book).execute()
        cv2.putText(frame, f"{book['title']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"ISBN: {book['isbn'] or 'Kein'}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        cv2.imshow('OCR Book Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
```

---

## Aufnahme-Tipps
- Gute Beleuchtung, Buchrücken/Umschlag klar sichtbar
- Vorverarbeitung: Graustufen, Kontrast, Threshold für OCR
- Realtime-GUI: NiceGUI Overlay für Live-Feedback

---

**Frage:**
Möchten Sie weitere Aufnahme-Optimierungen oder GUI-Beispiele?
