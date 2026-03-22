---

# Logbuch-Eintrag: ISBN-Liste als Input für automatisierten Metadaten-Import

Eine ISBN-Liste als Input ist ein effizienter, automatischer Weg, um Metadaten (Titel, Autor, Cover, Jahr, Typ, etc.) für Bücher, Hörbücher, Alben, DVDs/Blu-Rays usw. zu befüllen – ohne manuelle Einzeleingabe oder konkrete Titel im Code.

## 1. Mögliche Input-Formate

- **Reine ISBN-Liste (Text/CSV)**
  ```text
  978-3-12-345678-9
  978-3-12-987654-3
  978-1-234-56789-0
  ...
  ```
- **CSV mit Metadaten**
  ```csv
  isbn, title, author, year, type
  978-3-12-345678-9, Beispielbuch 1, Autor 1, 2020, book
  978-3-12-987654-3, Beispielhörbuch, Sprecher 1, 2021, hoerbuch_mp3
  ...
  ```
- **JSON-Export**
  ```json
  [
    {"isbn": "978-3-12-345678-9", "title": "...", "author": "...", "year": 2020, "type": "book"},
    {"isbn": "978-3-12-987654-3", "title": "...", "author": "...", "year": 2021, "type": "hoerbuch_mp3"}
  ]
  ```

## 2. Backend-Logik: Import-Funktion

```python
@app.route("/import_isbn_list", methods=["POST"])
def import_isbn_list():
    content_type = request.headers.get("Content-Type")
    if "json" in content_type:
        data = request.json
    elif "csv" in content_type:
        data = csv.DictReader(request.stream.read().decode().splitlines())
    else:
        lines = request.get_data().decode("utf-8").splitlines()
        data = [{"isbn": isbn.strip()} for isbn in lines]
    results = []
    for item in data:
        isbn = item["isbn"]
        cleaned = normalize_isbn(isbn)
        metadata = fetch_from_isbn_api(cleaned)
        obj = create_obj_from_metadata(metadata)
        results.append(obj)
    return jsonify(results)
```

- Unterstützt JSON, CSV und Text-Listen als Input
- Holt Metadaten per ISBN-API, erzeugt/aktualisiert Objekte

## 3. Beispiel-Datensatz (ohne konkrete Namen)

**input.json**
```json
[
  {"isbn": "978-3-12-345678-9", "type": "book"},
  {"isbn": "978-3-12-987654-3", "type": "hoerbuch_mp3"},
  {"isbn": "978-1-234-56789-0", "type": "album"}
]
```

**Backend-Ergebnis:**
```json
[
  {"id": "obj_123", "media_type": "container", "subtype": "book", "title": "<Titel>", "artist": "<Autor>", "year": 2020, "isbn": "978-3-12-345678-9", "cover": "/media_library/<Titel> (2020)/Cover.png", "amazon_cover": "https://m.media-amazon.com/images/...", "imdb": "tt1234567", "tmdb": 12345, "files": []},
  {"id": "obj_456", "media_type": "container", "subtype": "hoerbuch_mp3", "title": "<Titel>", "artist": "<Sprecher>", "year": 2021, "isbn": "978-3-12-987654-3", "cover": "/media_library/<Titel> (2021)/Cover.png", "amazon_cover": "https://m.media-amazon.com/images/...", "files": [...]},
  {"id": "obj_789", "media_type": "container", "subtype": "album", "title": "<Titel>", "artist": "<Künstler>", "year": 2022, "isbn": "978-1-234-56789-0", "cover": "/media_library/<Titel> (2022)/Cover.png", "amazon_cover": "https://m.media-amazon.com/images/...", "discogs": "12345678", "files": []}
]
```

## 4. Vorteile

- Automatisierter Bibliotheksaufbau durch ISBN-Listen-Import
- Einheitliche Typen und Metadaten für alle Medienobjekte
- ISBN-Liste als Backup/Cloud-Katalog
- Cross-Referenzierung zu imdb, tmdb, discogs, amazon_cover etc.

## 5. Typen-Überblick mit ISBN-Liste

| Typ                | media_type | subtype                | ISBN-sinnvoll? |
|--------------------|------------|------------------------|----------------|
| Buch               | container  | book                   | Ja             |
| E-Book             | file/cont. | ebook                  | Ja             |
| Hörbuch (MP3/m4b)  | cont./file | hoerbuch_mp3/m4b       | Ja             |
| Musik-Album        | container  | album                  | Ja (bei CD/Box)|
| Musik-Single       | container  | single                 | Ja (bei CD)    |
| Klassik-Aufnahme   | container  | klassik                | Ja (bei CD-Box)|
| DVD/Blu-Ray        | container  | dvd_video/bluray_video | Ja (bei Box)   |
| Box/Bundle         | container  | box/bundle             | Ja             |

## 6. Integration in deine App

- Frontend: Nutzer lädt ISBN-Liste (CSV/JSON/Text) hoch oder scannt sie per App
- Backend: Verarbeitet Liste, holt Metadaten, erstellt/aktualisiert Objekte
- Ergebnis: Mediathek ist automatisiert und metadatenreich befüllt – ohne konkrete Titel im Code
