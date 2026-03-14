# Offline Bücher-Sammlung: Barcode-Scanner + Supabase

## Setup
### 1. Hardware
- USB Barcode Scanner (~20€), Tastatur-Input
- App: zbarcam (Linux) oder Webcam + OpenCV

### 2. Python Offline Scanner
**Install:**
```bash
pip install isbnlib pyzbar opencv-python supabase
```
**book_scanner.py:**
```python
import isbnlib
from supabase import Client
import cv2
import pyzbar.pyzbar as pyzbar
isbn_db = isbnlib.get_canonical_isbn
cache_file = 'book_cache.json'
def scan_barcode_offline(image_source='webcam'):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            isbn = barcode.data.decode('utf-8')
            book_data = get_book_metadata(isbn)
            save_to_supabase(book_data)
            cv2.putText(frame, book_data['title'], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Book Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def get_book_metadata(isbn):
    try:
        metadata = isbnlib.meta(isbn, service='goob')
        return {
            'isbn': isbn,
            'title': metadata['Title'],
            'authors': metadata.get('Authors', []),
            'publisher': metadata.get('Publisher', ''),
            'year': metadata.get('Year', ''),
            'thumbnail': metadata.get('Cover', '')
        }
    except:
        book = supabase.table('books_cache').select('*').eq('isbn', isbn).execute()
        if book.data:
            return book.data[0]
        return {'isbn': isbn, 'title': 'Unbekannt', 'offline': True}
def save_to_supabase(book):
    supabase.table('physical_books').upsert(book).execute()
    ui.notify(f"📚 {book['title']} gespeichert!")
```

---

## USB Scanner (Keyboard-Input)
```python
import keyboard
def listen_for_isbn():
    buffer = ""
    def on_key(event):
        nonlocal buffer
        if event.event_type == 'down':
            if event.name.isdigit():
                buffer += event.name
            elif event.name == 'enter' and len(buffer) >= 10:
                book = get_book_metadata(buffer)
                save_to_supabase(book)
                print(f"Gefunden: {book['title']}")
                buffer = ""
    keyboard.hook(on_key)
listen_for_isbn()
```

---

## Calibre Integration (Offline Bulk)
```python
import subprocess
def bulk_scan_books(pdf_folder):
    subprocess.run(['calibredb', 'add', *glob.glob(f"{pdf_folder}/*.pdf"), '--library-path', CALIBRE_PATH])
    metadata = subprocess.check_output(['calibredb', 'list', '--for-machine', CALIBRE_PATH])
    books = json.loads(metadata)
    supabase.table('physical_books').insert(books).execute()
```

---

## GUI Scanner (NiceGUI)
```python
ui.video('webcam').props('playsinline muted')
ui.button('Scan ISBN', on_click=scan_barcode_offline)
async def load_physical_books():
    books = supabase.table('physical_books').select('*').limit(20).execute()
    ui.aggrid(books.data).classes('w-full')
```

---

## Workflow
- Scan ISBN (USB/Webcam) → isbnlib Cache → Supabase
- Offline: Local JSON-DB Fallback
- Bulk: Ordner → Calibre → Sync

---

## Test
- ISBN "978-3-16-148410-0" scannen → "Python Crash Course" found!

---

**Frage:**
Scanner kaufen oder Webcam-Test starten?
