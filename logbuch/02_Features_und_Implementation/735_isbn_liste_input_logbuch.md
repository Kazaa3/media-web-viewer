---

# Logbuch-Eintrag: ISBN-Liste als Input für automatisierten Metadaten-Import

Eine **ISBN‑Liste als Input** ist für deine Mediathek ein sehr sauberer, automatischer Weg, um Metadaten (Titel, Autor, Cover, Erscheinungsjahr, Typ, etc.) zu befüllen – ohne dass du jedes Buch/Hörbuch manuell eingeben musst.

## 1. Mögliche Input‑Formate

Du kannst ISBN‑Listen in verschiedenen Formaten erhalten (z.B. von Apps wie CLZ Books, Libib, oder manuell erstellt). Typische Formate:

- **Reine ISBN‑Liste (Text/CSV)**

```text
978-3-12-345678-9
978-3-12-987654-3
978-1-234-56789-0
...
```

- **CSV‑Datei mit zusätzlichem Metadaten**

```csv
isbn, title, author, year, type
978-3-12-345678-9, Beispielbuch 1, Autor 1, 2020, book
978-3-12-987654-3, Beispielhörbuch, Sprecher 1, 2021, hoerbuch_mp3
...
```

- **JSON‑Export (z.B. von CLZ Books, Libib, LibraryThing)**

```json
[
  {"isbn": "978-3-12-345678-9", "title": "...", "author": "...", "year": 2020, "type": "book"},
  {"isbn": "978-3-12-987654-3", "title": "...", "author": "...", "year": 2021, "type": "hoerbuch_mp3"}
]
```

## 2. Backend‑Logik: ISBN‑Liste als Input

### a) Import‑Funktion (Python/Flask/Bottle)

```python
from flask import Flask, request, jsonify
import csv
import json
from app import metadata_fetcher  # z.B. fetch_from_isbn_api()

app = Flask(__name__)

@app.route("/import_isbn_list", methods=["POST"])
def import_isbn_list():
    # Get input (JSON, CSV, or raw text)
    content_type = request.headers.get("Content-Type")
    if "json" in content_type:
        data = request.json
        # [{ "isbn": "978-3-12-345678-9", ... }]
    elif "csv" in content_type:
        data = csv.DictReader(request.stream.read().decode().splitlines())
    else:
        # Raw text with one ISBN per line
        lines = request.get_data().decode("utf-8").splitlines()
        data = [{"isbn": isbn.strip()} for isbn in lines]

    results = []
    for item in data:
        isbn = item["isbn"]
        # Normalize ISBN (remove dashes, etc.)
        cleaned = normalize_isbn(isbn)

        # Fetch metadata from ISBN API (e.g., Amazon, ISBN‑DB, etc.)
        metadata = fetch_from_isbn_api(cleaned)

        # Create or update object in your database
        obj = create_obj_from_metadata(metadata)
        results.append(obj)

    return jsonify(results)
```

Hier:

- `request` enthält deine ISBN‑Liste (JSON, CSV, oder Text).  
- `metadata_fetcher.fetch_from_isbn_api(cleaned)` ruft externe API auf.  
- `create_obj_from_metadata(metadata)` erzeugt `objekt` mit `isbn`, `title`, `artist`, `year`, `media_type`, `subtype`, `cover`, `amazon_cover`, `imdb`, `tmdb`, `discogs`, etc.

## 3. Datensatz‑Beispiel (ohne konkrete Namen)

`input.json` (Beispiel):

```json
[
  {
    "isbn": "978-3-12-345678-9",
    "type": "book"
  },
  {
    "isbn": "978-3-12-987654-3",
    "type": "hoerbuch_mp3"
  },
  {
    "isbn": "978-1-234-56789-0",
    "type": "album"
  }
]
```

Backend‑Ergebnis (z.B. `results`):

```json
[
  {
    "id": "obj_123",
    "media_type": "container",
    "subtype": "book",
    "title": "<Titel>",
    "artist": "<Autor>",
    "year": 2020,
    "isbn": "978-3-12-345678-9",
    "cover": "/media_library/<Titel> (2020)/Cover.png",
    "amazon_cover": "https://m.media‑amazon.com/images/...",
    "imdb": "tt1234567",
    "tmdb": 12345,
    "files": []
  },
  {
    "id": "obj_456",
    "media_type": "container",
    "subtype": "hoerbuch_mp3",
    "title": "<Titel>",
    "artist": "<Sprecher>",
    "year": 2021,
    "isbn": "978-3-12-987654-3",
    "cover": "/media_library/<Titel> (2021)/Cover.png",
    "amazon_cover": "https://m.media‑amazon.com/images/...",
    "files": [...]
  },
  {
    "id": "obj_789",
    "media_type": "container",
    "subtype": "album",
    "title": "<Titel>",
    "artist": "<Künstler>",
    "year": 2022,
    "isbn": "978-1-234-56789-0",
    "cover": "/media_library/<Titel> (2022)/Cover.png",
    "amazon_cover": "https://m.media‑amazon.com/images/...",
    "discogs": "12345678",
    "files": []
  }
]
```

## 4. Praktische Nutzen

- **Automatisierte Bibliotheksaufbau**  
  - Nutzer scannt ISBN‑Liste aus App → lädt sie hoch → Backend baut Mediathek.  
- **Einheitliche Typen**  
  - `book`, `audio‑book`, `music‑album`, `soundtrack`, `dvd_video`, `bluray_video`, `serien_staffel` – alle mit ISBN/Remote‑IDs.  
- **Cloud‑Backup‑Katalog**  
  - ISBN‑Liste kann als Backup deiner Bibliothek dienen, falls du Datenbank‑Restore brauchst.  
- **Cross‑Referenzierung**  
  - `isbn` → `imdb`/`tmdb`/`discogs`/`amazon_cover` für Cover, Metadaten, Beschreibungen, Erscheinungsjahr, etc.

## 5. Typen‑Überblick mit ISBN‑Liste

| Typ                        | `media_type` | `subtype`             | ISBN‑sinnvoll? |
|---------------------------|-------------|------------------------|----------------|
| Buch                      | `container` | `book`                | Ja             |
| E‑Book                    | `file`/`container` | `ebook`           | Ja             |
| Hörbuch (MP3, m4b, CD)    | `container`/`file` | `hoerbuch_mp3`/`hoerbuch_m4b` | Ja          |
| Musik‑Album               | `container` | `album`                | Ja (falls Box/CD‑Release) |
| Musik‑Single              | `container` | `single`               | Ja (falls CD‑Release)    |
| Klassik                   | `container` | `klassik`              | Ja (falls CD‑Box)        |
| DVD/Blu‑Ray               | `container` | `dvd_video`/`bluray_video` | Ja          |
| Box/Bundle                | `container` | `box`/`bundle`         | Ja (meist jede Edition)  |

## 6. Beispiel‑Integration in deiner App

- **Frontend (z.B. Bottle/Eel, Mobile):**  
  - Nutzer lädt CSV/JSON/Text‑Datei mit ISBN‑Liste hoch.  
  - Oder nutzt „Scan ISBN“ in App, exportiert Liste als CSV/JSON, lädt sie hoch.  
  - App sendet `POST /import_isbn_list` mit der Liste.  

- **Backend:**  
  - Verarbeitet ISBN‑Liste, holt Metadaten, erstellt/aktualisiert `objekt`‑Daten.  
  - Gibt fertige Objekte zurück, die du in deiner Mediathek darstellst.  

Mit ISBN‑Liste als Input kannst du deine Mediathek vollständig automatisiert befüllen, ohne dass du jemals konkrete Namen wie „Avengers“, „Matrix“, „Harry Potter“, etc. im Code festlegen musst – alles bleibt allgemein, modular, und skalierbar.
