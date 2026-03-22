# 7-Schritte Inventur-System für Offline Bücher in Supabase

## Workflow
1. **Hardware:** USB Barcode Scanner (~20€) oder Webcam
2. **Scan:** ISBN → Offline-Cache (isbnlib)
3. **Metadata:** Titel/Autor/Cover lokal/online
4. **Status:** Regal/Ausgeliehen/Verkauft
5. **Location:** Regal A1, B2 etc.
6. **Supabase:** Realtime Sync
7. **GUI:** Live-Grid + Suche

---

## Voll-Code Inventur-Scanner
**inventur.py:**
```python
import isbnlib
from supabase import Client
import keyboard
import json
from pathlib import Path
import pandas as pd
client = Client(SUPABASE_URL, SUPABASE_KEY)
cache_file = Path('book_cache.json')
def load_cache():
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    return {}
def save_cache(cache):
    cache_file.write_text(json.dumps(cache))
book_cache = load_cache()
buffer = ""
def on_scan():
    global buffer
    if len(buffer) >= 10 and buffer.isdigit():
        isbn = isbnlib.get_canonical_isbn(buffer)
        book = get_book(isbn)
        save_to_db(book)
        print(f"📚 {book['title']} | {book['status']} | Regal: {book['location']}")
    buffer = ""
def get_book(isbn):
    if isbn in book_cache:
        return book_cache[isbn]
    try:
        meta = isbnlib.meta(isbn)
        book = {
            'isbn': isbn,
            'title': meta.get('Title', 'Unbekannt'),
            'author': meta.get('Authors', ['Unbekannt'])[0],
            'status': 'in_regal',
            'location': 'A1',
            'scan_date': '2026-03-10'
        }
        book_cache[isbn] = book
        save_cache(book_cache)
        return book
    except:
        return {'isbn': isbn, 'title': 'Scan-Fehler', 'status': 'manual'}
def save_to_db(book):
    existing = client.table('physical_books').select('isbn').eq('isbn', book['isbn']).execute()
    if not existing.data:
        client.table('physical_books').insert(book).execute()
    else:
        client.table('physical_books').update(book).eq('isbn', book['isbn']).execute()
keyboard.add_hotkey('enter', on_scan)
print("🔥 Scanner bereit! ISBN eingeben + Enter")
def export_inventory():
    data = client.table('physical_books').select('*').execute()
    df = pd.DataFrame(data.data)
    df.to_csv('buch_inventur.csv', index=False)
    print("📊 Export: buch_inventur.csv")
export_inventory()
```

---

## Realtime Inventur-GUI (NiceGUI)
```python
from nicegui import ui
import asyncio
async def refresh_inventory():
    data = client.table('physical_books').select('*').order('scan_date', desc=True).limit(50).execute()
    ui.aggrid(data.data, columns=[{'field': 'title', 'sortable': True}, {'field': 'author'}, {'field': 'status', 'editable': True}, {'field': 'location'}]).classes('w-full')
ui.button('Inventur starten', on_click=lambda: asyncio.create_task(start_scan_mode()))
ui.button('Export CSV', on_click=export_inventory)
ui.timer(1.0, refresh_inventory)
ui.run()
```

---

## Praxis
- Scanner anschließen, python inventur.py
- Scan: Buch → ISBN → Auto-Metadata
- Status setzen: in_regal, ausgeliehen, verkauft
- Location: Regal-Aufkleber (z.B. "A1")
- GUI live: NiceGUI zeigt Scans realtime
- Export: CSV für Excel/Druck
- Suche: client.table('physical_books').select('*').ilike('title', '%python%')

---

## Beispiel Inventur
| isbn           | title                   | author              | status      | location   | scan_date   |
|--------------- |------------------------ |---------------------|------------ |----------- |------------ |
| 9783161484100  | Python Crash Course     | Eric Matthes        | in_regal    | Regal A1   | 2026-03-10  |
| 9783836227399  | Clean Code              | Robert C. Martin    | ausgeliehen | Peter      | 2026-03-09  |
| 9783492700444  | The Pragmatic Programmer| Andrew Hunt         | in_regal    | Regal B2   | 2026-03-10  |

---

**Frage:**
Scanner kaufen (Amazon: "USB Barcode Scanner drahtlos" ~25€) oder Webcam? Code testen?
