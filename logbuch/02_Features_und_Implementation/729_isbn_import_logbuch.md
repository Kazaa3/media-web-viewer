---

## Logbuch-Eintrag: Formfaktor/cover-art-Typen für Medienobjekte

Die Unterscheidung des Formfaktors ist essenziell, da Cover/Art für Buch, CD, DVD, Blu-Ray, Vinyl oder Box optisch und metrisch unterschiedlich sind. Das Feld `form_factor` im Objekt-Schema sorgt für korrekte Darstellung und Metadaten.

### 1. Warum Formfaktor?
- Unterschiedliche Maße und Designs (Buch, CD, DVD, Blu-Ray, Vinyl)
- Korrekte Cover-Darstellung im Renderer/Web-Player
- Saubere Metadaten für Original-Format

### 2. Schema-Erweiterung
```json
{
  "id": "obj_123",
  "media_type": "container",
  "subtype": "album" | "dvd_video" | "bluray_video" | "book",
  "title": "<Titel>",
  "year": 2020,
  "form_factor": "cd" | "dvd" | "bluray" | "book_6x9" | "vinyl_lp"
}
```

### 3. Formfaktoren im Detail
- `cd`: Standard-CD-Album (12×12)
- `vinyl_lp`: Vinyl-LP (12")
- `dvd`: DVD-Box (13,5×18)
- `bluray`: Blu-Ray (13,5×18)
- `book`: Standard-Buch (6×9)
- `book_large`: Großformat, Bildband
- `box`: Box-Edition (z.B. Blu-Ray-Box, CD-Box)

### 4. Typen-Überblick mit Formfaktor
| Typ                | media_type | subtype         | form_factor         |
|--------------------|------------|-----------------|---------------------|
| Buch               | container  | book            | book/book_large     |
| CD-Album           | container  | album           | cd                  |
| Vinyl-LP           | container  | album           | vinyl_lp            |
| DVD-Video          | container  | dvd_video       | dvd                 |
| Blu-Ray-Video      | container  | bluray_video    | bluray              |
| Blu-Ray-Box        | container  | box             | bluray              |
| CD-Box             | container  | box             | cd                  |
| Hörbuch (MP3/m4b)  | cont./file | hoerbuch_mp3/m4b| book (falls Buch)   |

### 5. Praktische Nutzung
- Renderer/Player kann nach `form_factor` unterscheiden
- Suche/Filter nach Formfaktor möglich
- Automatisierte Metadatenpflege über externe APIs

### 6. Beispiel-Abfragen
```python
# Alle DVD-Releases
dvd_releases = [o for o in objects if o["form_factor"] == "dvd"]
# Alle CD-Releases
cd_releases = [o for o in objects if o["form_factor"] == "cd"]
# Blu-Ray-Videos
bluray_video = [o for o in objects if o["form_factor"] == "bluray" and o["subtype"] == "bluray_video"]
```

**Fazit:**
Mit `form_factor` im Schema kannst du alle Medienobjekte (CD, DVD, Blu-Ray, Buch, Vinyl, Box, etc.) korrekt und automatisiert verwalten – für perfekte Cover-Darstellung und saubere Metadaten, ohne konkrete Titel im Code.
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
