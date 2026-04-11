---

## Logbuch-Eintrag: ISBN-Scan per Smartphone für Metadaten-Import

Das Scannen von ISBN-Barcodes per Smartphone ist eine effiziente Methode, um Bücher, Hörbücher, E-Books, Boxen und Bundles automatisiert mit Metadaten zu befüllen – ohne konkrete Titel im Code.

### 1. Prinzip: Smart-Scan-Funktion

- Nutzer öffnet die App und wählt „Scan ISBN“
- Kamera scannt den Barcode (ISBN-10/ISBN-13)
- App extrahiert die ISBN und sendet sie ans Backend

**Backend-Logik:**
```python
def scan_isbn(isbn: str):
  cleaned = normalize_isbn(isbn)
  obj = find_obj_by_isbn(cleaned) or create_obj_from_isbn_api(cleaned)
  return {
    "id": obj["id"],
    "title": obj["title"],
    "artist": obj["artist"],
    "year": obj["year"],
    "isbn": obj["isbn"],
    "amazon_cover": obj.get("amazon_cover"),
    "cover": obj.get("cover"),
    "media_type": obj["media_type"],
    "subtype": obj["subtype"]
  }
```

### 2. App-Integration

- Nutzer ruft „Scan ISBN“ auf, scannt Barcode
- App erkennt ISBN, sendet sie ans Backend
- Backend liefert existierendes oder neues Objekt mit Metadaten zurück

### 3. Beispiel-Datenfluss

1. Nutzer scannt ISBN `978-3-12-345678-9`
2. Backend sucht:
   ```python
   obj = find_obj_by_isbn("978-3-12-345678-9")
   ```
3. Existiert Objekt:
   ```json
   {
   "id": "obj_123",
   "media_type": "container",
   "subtype": "hoerbuch_mp3",
   "title": "<Titel>",
   "year": 2020,
   "isbn": "978-3-12-345678-9",
   "amazon_cover": "https://m.media-amazon.com/images/...",
   "cover": "/media_library/<Titel> (2020)/Cover.png",
   "files": [...]
   }
   ```
4. Existiert nicht, Backend holt Metadaten via ISBN-API:
   ```python
   metadata = fetch_from_isbn_api("978-3-12-345678-9")
   new_obj = {
     "id": "obj_456",
     "media_type": "container",
     "subtype": "book",
     "title": metadata["title"],
     "artist": metadata["author"],
     "year": metadata["year"],
     "isbn": "978-3-12-345678-9",
     "amazon_cover": metadata["cover_url"],
     "cover": None,
     "files": []
   }
   ```
5. Backend speichert das neue Objekt, App zeigt es an

### 4. Vorteile

- Schnelle, korrekte Metadaten (Titel, Autor, Jahr, Cover, Verlag, Sprache)
- Automatisierter Bibliotheksaufbau durch Barcode-Scan
- Einheitliche Typen: book, ebook, hoerbuch_mp3, album, dvd_video, bluray_video etc.
- ISBN-Liste als Backup/Cloud-Katalog nutzbar

### 5. Typen-Überblick mit ISBN-Scan

| Typ                | media_type | subtype                | ISBN-Scan sinnvoll? |
|--------------------|------------|------------------------|---------------------|
| Buch               | container  | book                   | Ja                  |
| E-Book             | file/cont. | ebook                  | Ja                  |
| Hörbuch (MP3/m4b)  | cont./file | hoerbuch_mp3/m4b       | Ja                  |
| Musik-Album        | container  | album                  | Ja (bei CD/Box)     |
| Musik-Single       | container  | single                 | Ja (bei CD)         |
| Klassik-Aufnahme   | container  | klassik                | Ja (bei CD-Box)     |
| DVD/Blu-Ray        | container  | dvd_video/bluray_video | Ja (bei Box/Bundle) |
| Box/Bundle         | container  | box/bundle             | Ja                  |

### 6. Implementierung

- App: „Scan ISBN“-Button, z.B. mit zxing-Scanner (Android/iOS/JS)
- Backend: API-Endpunkt `/api/scan_isbn`, der ISBN verarbeitet und Objekt liefert
```python
@app.route("/api/scan_isbn", methods=["POST"])
def scan_isbn():
  isbn = request.json.get("isbn")
  obj = find_obj_by_isbn(isbn)
  if not obj:
    obj = create_obj_from_isbn_api(isbn)
  return jsonify(obj)
```

### 7. Sicherheit & Datenschutz

- ISBNs sind öffentliche IDs, keine sensiblen Daten
- Optional: ISBNs in DB hashen/verschlüsseln, falls anonymisiert werden soll
- Keine persönlichen Daten mit ISBN verknüpfen, außer auf Nutzerwunsch

**Fazit:**
Mit ISBN-Scanning kannst du deine Mediathek automatisiert und metadatenreich befüllen – ohne konkrete Titel im Code, alles bleibt generisch und skalierbar.
---

## Logbuch-Eintrag: DVD/Blu-Ray-Objekte und Remote-IDs

### 1. Remote-IDs für Video-Disks

Für DVDs und Blu-Rays sind besonders sinnvoll:
- `imdb`           → für den Film/TV-Inhalt
- `tmdb`           → The-Movie-DB-ID
- `blu_ray_forum`  → individuelle Blu-Ray-Review-Seite / Disk-Verzeichnis (optional)
- `discogs`        → falls Limited Edition mit Musik/Box-Inhalten

### 2. Beispiel-Objekte

#### a) DVD-Video-Release
```json
{
  "id": "obj_789",
  "media_type": "container",
  "subtype": "dvd_video",
  "title": "...",
  "year": 2020,
  "imdb": "tt1234567",
  "tmdb": 12345,
  "blu_ray_forum": null,
  "folder": "/media_library/<Titel> (2020)",
  "cover": "/media_library/<Titel> (2020)/Cover.png",
  "files": ["file_001", "file_002", "file_003"]
}
```

#### b) Blu-Ray-Video-Release
```json
{
  "id": "obj_890",
  "media_type": "container",
  "subtype": "bluray_video",
  "title": "...",
  "year": 2020,
  "imdb": "tt1234567",
  "tmdb": 12345,
  "blu_ray_forum": "https://www.example-bluray-forum.com/disk/...",
  "folder": "/media_library/<Titel> (2020) - Blu-Ray",
  "cover": "/media_library/<Titel> (2020) - Blu-Ray/Cover.png",
  "files": ["file_101", "file_102", "file_103"]
}
```

### 3. Integration in Backend/Player

```python
def scan_dvd_bluray_dir(dir_path, media_type="video"):
    if "Blu-Ray" in dir_path:
        subtype = "bluray_video"
    else:
        subtype = "dvd_video"
    title, year = extract_title_year(dir_path)
    return {
        "id": f"obj_{hash(dir_path)}",
        "media_type": "container",
        "subtype": subtype,
        "title": title,
        "year": year,
        "imdb": extracted_imdb,   # optional
        "tmdb": extracted_tmdb,   # optional
        "blu_ray_forum": None,    # oder URL, falls Blu-Ray
        "folder": dir_path,
        "cover": find_cover(dir_path),
        "files": [item["id"] for item in scan_files(dir_path)]
    }
```

### 4. Typenüberblick mit Remote-IDs

| Objekt-Typ         | `media_type` | `subtype`        | Remote-IDs                        |
|--------------------|-------------|------------------|------------------------------------|
| Film               | container   | movie            | imdb, tmdb                        |
| Serie-Staffel      | container   | serie_staffel    | imdb, tmdb, serien_verzeichnis     |
| Video-DVD          | container   | dvd_video        | imdb, tmdb, blu_ray_forum (opt.)   |
| Blu-Ray-Video      | container   | bluray_video     | imdb, tmdb, blu_ray_forum          |
| Album              | container   | album            | discogs, musicbrainz               |
| Single             | container   | single           | discogs, musicbrainz               |
| Klassik            | container   | klassik          | discogs, musicbrainz               |
| Hörbuch (MP3/m4b)  | container/file | hoerbuch_mp3/hoerbuch_m4b | isbn, discogs         |

### 5. Vorteile

- Automatischer Metadatenabgleich (Cover, Titel, Jahr, Cast, Staffel-Infos)
- Eigene Disk-Review-DB möglich (blu_ray_forum)
- Keine konkreten Titel im Code nötig, alles generisch
---

## Logbuch-Eintrag: Amazon als Cover-Quelle für Medienobjekte

Amazon ist eine sehr praktische Quelle für hochwertige Cover-Bilder (Album-Art, Hörbuch, DVD/Blu-Ray, Bücher). Viele Releases werden dort mit großem, gutem Cover verkauft – ideal als Supplier für `cover`-URLs.

### 1. Prinzip: „Cover-URL“ + Metadatenfeld

Jedes Objekt kann optional eine Amazon-Cover-URL enthalten:

```json
{
  "id": "obj_123",
  "media_type": "container",
  "subtype": "album",
  "title": "<Titel>",
  "year": 2020,
  "cover": "/media_library/<Titel> (2020)/Cover.png",
  "amazon_cover": "https://m.media-amazon.com/images/...",
  "isbn": "978-...",
  "imdb": "tt123456",
  "tmdb": 12345,
  "discogs": "12345678",
  "files": [...]
}
```

- `amazon_cover`: Externe URL zu einem großen, hochwertigen Bild
- `cover`: Lokales Bild, falls vorhanden; `amazon_cover` als Fallback oder für Vorschau

### 2. Anwendung für verschiedene Typen

#### a) DVDs / Blu-Rays

```json
{
  "media_type": "container",
  "subtype": "dvd_video" | "bluray_video",
  "amazon_cover": "https://m.media-amazon.com/images/..."
}
```
- Nutze lokales Cover, falls vorhanden, sonst `amazon_cover` als Ersatz oder Vorschau

#### b) Hörbücher

```json
{
  "subtype": "hoerbuch_mp3",
  "amazon_cover": "https://m.media-amazon.com/images/...",
  "isbn": "978-..."
}
```
- Ergänze fehlendes Cover automatisch oder nutze als zusätzliche Bildquelle

#### c) Musik-Alben / Singles

```json
{
  "subtype": "album",
  "amazon_cover": "https://m.media-amazon.com/images/...",
  "discogs": "12345678"
}
```
- Album-/Box-/Limited-Edition-Cover direkt von Amazon als Vorschau oder Fallback

### 3. Vorteile

- Hochwertige, aktuelle Cover für alle Medientypen
- Automatische Ergänzung fehlender Cover
- Keine harten Titel oder Amazon-Namen im Code nötig
- Flexibel für DVD, Blu-Ray, Hörbuch, Musik, Buch

**Hinweis:**
- Die Integration von `amazon_cover` ist rein optional und ergänzt dein bestehendes Schema ohne Konflikte mit media_type, subtype oder files.
---

## Gruppierung: Items zu Objekten (Container vs. File)

Die Gruppierung von Items zu Objekten ist der Kern der Medienbibliothekslogik:

- **Item** = einzelne Datei + Metadaten (z.B. MP3, MKV, Hörbuch-Teil)
- **Objekt** = Container aus mehreren Items, die semantisch zusammengehören (z.B. Album, Serie-Staffel, Playlist, Compilation, Hörbuch-Reihe)

### 1. Zentrale Prinzipien

- Gruppierung nach Ordnername + Metadaten (z.B. "Künstler - Album (Jahr)")
- `container` = mehrere Items, `file` = einzelnes Item

### 2. Abstraktes Schema

#### Item (Datei)
```python
{
  "id": "item_123",
  "media_type": "audio" | "video",
  "file_type": "mp3" | "flac" | "mkv" | "mp4" | "m4b" | ...,
  "src": "/pfad/zur/datei.mp3",
  "title": "...",
  "artist": "...",
  "track": 1,
  "disc": 1,
  "duration": 234.5
}
```

#### Object (Container-Objekt)
```python
{
  "id": "obj_456",
  "media_type": "container",  # oder "file" bei Einzeldatei
  "subtype": "album" | "single" | "playlist" | "compilation" | "serie_staffel" | ...,
  "title": "<Titel>",
  "artist": "<Künstler>",
  "year": 2020,
  "folder": "/media_library/<Pfad>",
  "cover": "/media_library/<Pfad>/Cover.png",
  "items": ["item_123", "item_124", ...]
}
```

### 3. Gruppierungsregeln (Beispiele)

- **Album/Single/Compilation:** Alle Dateien im Ordner → ein Objekt mit passendem Subtyp, alle Tracks als Items
- **Playlist:** Manuell geordnete Track-Reihe, Reihenfolge aus Dateinamen oder Playlist-Datei
- **Klassik/Soundtrack:** Alle Sätze/Tracks im Ordner → ein Objekt, Items nach Tracknummer
- **Serien-Staffel:** Ordner mit Episoden → Objekt mit Subtyp "serie_staffel", Items = Episoden
- **Hörbuch:** MP3-Reihe = Container, m4b = Einzeldatei (kein Container)

### 4. Gruppierungslogik in Python (Regel-basiert)
```python
def scan_dir_to_object(dir_path):
  folder_name = os.path.basename(dir_path)
  # 1. Ordnername → Titel, Artist, Year, Subtype erkennen
  # 2. Files sammeln
  items = []
  for f in os.listdir(dir_path):
    full = os.path.join(dir_path, f)
    if is_media_file(full):
      item = scan_file(full)
      items.append(item)
  # 3. Für Hörbuch-m4b
  if len(items) == 1 and items[0]["file_type"] == "m4b":
    return {
      "id": f"file_{hash(...)}",
      "media_type": "file",
      "file_type": "hoerbuch-m4b",
      "src": items[0]["src"],
      "title": items[0]["title"],
      "cover": find_cover(dir_path)
    }
  # 4. Sonst Container
  return {
    "id": f"obj_{hash(folder_name)}",
    "media_type": "container",
    "subtype": subtype,
    "title": title,
    "artist": artist,
    "year": year,
    "folder": dir_path,
    "cover": find_cover(dir_path),
    "items": [item["id"] for item in items]
  }
```

### 5. Verwendung

- **Backend:** Objekte und Items als Tabelle/JSON, Relation über IDs
- **Web-Player:** Objekt → Playlist/Trackliste, File → Einzel-URL
- **Routing:** `get_play_plan`: Container = Playlist, File = Einzelquelle

### 6. Vorteile

- Gruppierung nach natürlichem Ordner-Layout, keine harten Namen im Code
- Single als eigener Subtyp, m4b-Hörbuch als File, MP3-Hörbuch als Container
## Übersicht: Medientypen und Untertypen (geordnet)

### Audio
| Haupttyp      | Subtyp(en)                                  | Beschreibung                                  |
|---------------|---------------------------------------------|-----------------------------------------------|
| file          | audio-file                                  | Einzelne MP3, FLAC, M4B, WAV etc.             |
| container     | album                                       | Musik-Album (mehrere Tracks)                  |
| container     | podcast                                     | Podcast-Staffel oder -Serie                   |
| container     | single                                      | Single-Release (1–3 Tracks, Remixe, Bonus)    |
| container     | compilation                                 | Best-of, Various Artists, Sampler             |
| container     | playlist                                    | Benutzerdefinierte Track-Liste                |
| container     | klassik                                     | Klassik-Werk, Opus, Konzert                   |
| container     | soundtrack                                  | Film-/Game-Soundtrack                         |
| container     | hoerbuch_mp3                                | Hörbuch als MP3-Reihe (mehrere Dateien)       |
| file          | hoerbuch-m4b                                | Hörbuch als Einzeldatei (M4B)                 |

### Video
| Haupttyp      | Subtyp(en)                                  | Beschreibung                                  |
|---------------|---------------------------------------------|-----------------------------------------------|
| file          | video-file                                  | Einzelnes Video (MKV, MP4, AVI, MOV etc.)     |
| container     | film                                        | Spielfilm, Movie                              |
| container     | serie                                       | Serie, Staffel, Episoden                      |
| container     | doku                                        | Dokumentation, Reportage                      |
| container     | tv                                          | TV-Aufzeichnung, Shows                        |
| container     | bonus                                       | Bonusmaterial, Extras, Deleted Scenes         |


### Abbild (Image/ISO)
| Haupttyp | Subtyp           | Beispiele/Endungen                | Beschreibung                                      |
|----------|------------------|-----------------------------------|---------------------------------------------------|
| file     | image-iso        | .iso, .bin, .img                  | Generisches Abbild (DVD/CD/BD, Master-Images)     |
| file     | daten-disc       | .iso, .img, .udf, .cue/.bin       | Daten-CD, Daten-DVD, Daten-Blu-ray                |
| file     | pal-dvd          | .iso, VIDEO_TS, PAL               | PAL-Video-DVD (Europa, Australien etc.)           |
| file     | ntsc-dvd         | .iso, VIDEO_TS, NTSC              | NTSC-Video-DVD (USA, Japan etc.)                  |
| file     | blu-ray          | .iso, BDMV, Blu-ray               | Blu-ray Disc (HD, FullHD, UHD)                    |
| file     | cd-audio         | .bin/.cue, .wav, .flac, .ape      | Audio-CD (CDDA, verlustfrei, Images)              |
| file     | cd-extra         | .bin/.cue, .iso                   | CD-Extra, Enhanced CD (Audio + Datenbereich)      |
| file     | super-audio-cd   | .iso, DSD                         | SACD, spezielle Player benötigt                   |
| file     | diverse-formate  | .iso, .bin, .img, .nrg, .vcd      | HD-DVD, VCD, SVCD, Mixed-Mode, Hybrid etc.        |

**Hinweis:**
- `image-iso` ist der Oberbegriff für alle Abbild-Typen.
- Die Subtypen spezifizieren das konkrete Disc- oder Audioformat (z.B. PAL/NTSC, Blu-ray, Audio-CD, Daten-Disc).
- Für Bilder (PNG, JPG, GIF, ...) siehe Abschnitt „Bilder“.

### Bilder (Sammlung)
| Haupttyp      | Subtyp(en)      | Beschreibung                                                    |
|---------------|-----------------|-----------------------------------------------------------------|
| file          | image           | Einzelbild: PNG, JPG, JPEG, GIF, WEBP, BMP, TIFF etc.           |
| container     | bilder          | Bildersammlung, Galerie, Ordner mit mehreren Bildern            |

### Dokument
| Haupttyp      | Subtyp(en)      | Beschreibung                                                    |
|---------------|-----------------|-----------------------------------------------------------------|
| file          | dokument        | Einzelnes Dokument (PDF, DOCX, TXT, etc.)                       |
| container     | dokumente       | Dokumentensammlung, z.B. Ordner mit PDFs                        |

**Hinweis:**
- `image-iso` ist ein einzelnes Abbild (ISO, IMG, BIN/CUE etc.).
- `image` steht für ein einzelnes Bild (PNG, JPG, GIF, ...).
- `bilder` ist ein Container für mehrere Bilder (z.B. Fotogalerie, Screenshots, Artwork-Sets).
- `dokument` für einzelne Dokumente, `dokumente` für Sammlungen.
### Abbild (Image/ISO)
| Haupttyp      | Subtyp(en)      | Beschreibung                                                    |
|---------------|-----------------|-----------------------------------------------------------------|
| file          | image-iso       | Einzelnes Abbild: ISO, BIN, IMG (z.B. DVD-/CD-/BD-Abbild)       |

### Bilder (Sammlung)
| Haupttyp      | Subtyp(en)      | Beschreibung                                                    |
|---------------|-----------------|-----------------------------------------------------------------|
| file          | image           | Einzelbild: PNG, JPG, JPEG, GIF, WEBP, BMP, TIFF etc.           |
| container     | bilder          | Bildersammlung, Galerie, Ordner mit mehreren Bildern            |

**Hinweis:**
- `image-iso` ist ein einzelnes Abbild (ISO, IMG, BIN/CUE etc.).
- `image` steht für ein einzelnes Bild (PNG, JPG, GIF, ...).
- `bilder` ist ein Container für mehrere Bilder (z.B. Fotogalerie, Screenshots, Artwork-Sets).
## Übersicht: Medientypen und Untertypen (geordnet)

### Audio
| Haupttyp      | Subtyp(en)                                  | Beschreibung                                  |
|---------------|---------------------------------------------|-----------------------------------------------|
| file          | audio-file                                  | Einzelne MP3, FLAC, M4B, WAV etc.             |
| container     | album                                       | Musik-Album (mehrere Tracks)                  |
| container     | podcast                                     | Podcast-Staffel oder -Serie                   |
| container     | single                                      | Single-Release (1–3 Tracks, Remixe, Bonus)    |
| container     | compilation                                 | Best-of, Various Artists, Sampler             |
| container     | playlist                                    | Benutzerdefinierte Track-Liste                |
| container     | klassik                                     | Klassik-Werk, Opus, Konzert                   |
| container     | soundtrack                                  | Film-/Game-Soundtrack                         |
| container     | hoerbuch_mp3                                | Hörbuch als MP3-Reihe (mehrere Dateien)       |
| file          | hoerbuch-m4b                                | Hörbuch als Einzeldatei (M4B)                 |

### Video
| Haupttyp      | Subtyp(en)                                  | Beschreibung                                  |
|---------------|---------------------------------------------|-----------------------------------------------|
| file          | video-file                                  | Einzelnes Video (MKV, MP4, AVI, MOV etc.)     |
| container     | film                                        | Spielfilm, Movie                              |
| container     | serie                                       | Serie, Staffel, Episoden                      |
| container     | doku                                        | Dokumentation, Reportage                      |
| container     | tv                                          | TV-Aufzeichnung, Shows                        |
| container     | bonus                                       | Bonusmaterial, Extras, Deleted Scenes         |

### Abbild (Image/ISO)
| Haupttyp      | Subtyp(en)      | Beschreibung                                      |
|---------------|-----------------|---------------------------------------------------|
| file          | image           | Einzelbild, z.B. JPG, PNG, GIF                    |
| file          | image-iso       | Image-ISO-Datei (z.B. DVD-/CD-/BD-Abbild)         |

### Bilder (Sammlung)
| Haupttyp      | Subtyp(en)      | Beschreibung                                      |
|---------------|-----------------|---------------------------------------------------|
| file          | image           | Einzelbild, z.B. JPG, PNG, GIF                    |
| container     | fotoalbum       | Bildersammlung, Galerie, Ordner mit mehreren Pics |

### Dokument
| Haupttyp      | Subtyp(en)      | Beschreibung                                      |
|---------------|-----------------|---------------------------------------------------|
| file          | dokument        | Einzelnes Dokument (PDF, DOCX, TXT, EBUB, etc.)         |
| container     | dokumente       | Dokumentensammlung, z.B. Ordner mit PDFs          |



**Hinweis:**
- `image` steht für ein einzelnes Bild (z.B. Cover, Poster, Artwork).
- `image-iso` ist ein einzelnes Abbild (ISO, IMG, BIN/CUE etc.).
- `bilder` ist ein Container für mehrere Bilder (z.B. Fotogalerie, Screenshots, Artwork-Sets).
- `dokument` für einzelne Dokumente, `dokumente` für Sammlungen.


## „Single“ als eigener Container-Subtyp

**Single** soll eine eigene Kategorie (`subtype`) unter `container` sein, da sie sich klar von Album, Compilation, Soundtrack usw. unterscheidet:

- Meist klein (1–3 Tracks, oft 1 Track + Remix + Bonus)
- Fokus auf ein Lied, Remixe, Extended/Instrumental/B-Sides

### 1. Schema für Single-Container

```python
{
  "media_type": "container",
  "subtype": "single",   # eigene Kategorie
  "title": "<Titel>",
  "artist": "<Künstler>",
  "year": 2020,
  "folder": "/media_library/<Künstler> - <Single> (2020)",
  "cover": "/media_library/<Künstler> - <Single> (2020)/Cover.png",
  "files": [
    {
      "src": ".../<Künstler> - <Single> (2020).mp3",
      "type": "audio-main",
      "track_title": "<Single-Titel>"
    },
    {
      "src": ".../<Künstler> - <Single> (2020)_remix1.mp3",
      "type": "audio-remix",
      "track_title": "<Single-Titel> (Remix 1)"
    },
    {
      "src": ".../<Künstler> - <Single> (2020)_bonus.mp3",
      "type": "audio-bonus",
      "track_title": "<B-Side/Bonus>"
    }
  ]
}
```

- `subtype: "single"` ist klar erkennbar in Backend und UI.
- Jeder Track erhält einen `type` (main/remix/bonus/instrumental/radio-edit) und einen `track_title`.

### 2. Unterschied zu Einzeldatei

Auch wenn eine Single manchmal nur eine Datei enthält, ist sie im System ein **Container**:

- CD/Digital-Singles haben meist mehrere Versionen (Radio-Edit, Extended, Instrumental, Remix, Live-Version) als Set.
- Beispiel: `Artist - Song (Edit).mp3`, `Artist - Song (Remix).mp3`, `Artist - Song (Instrumental).mp3` → zusammen eine Single-Release-Serie.
- Du speicherst also einen `single`-Container mit mehreren `audio-file`-Tracks, statt jede MP3 als eigenes `file`-Objekt.

### 3. UI- und Player-Folgen

- **UI**: Zeigt „Single“ als eigenes Subtype-Label, sortiert Tracks nach Art (main, remix, instrumental, bonus).
- **Player**: `get_play_plan(item, 'browser')` ergibt eine Playlist mit allen Tracks der Single. Optional: Start mit `audio-main`, dann Shuffle/Remix-Optionen.

### 4. Übersicht: Single im Typ-System

| Typ                   | `media_type` | `subtype` / `file_type`      |
|------------------------|-------------|------------------------------|
| Normales Musik-Album   | `container` | `album`                      |
| Single-Release         | `container` | `single`                     |
| Compilation (Various)  | `container` | `compilation`                |
| Playlist               | `container` | `playlist`                   |
| Soundtrack             | `container` | `soundtrack`                 |
| Klassik-Werk           | `container` | `klassik`                    |
| MP3-Hörbuch-Reihe      | `container` | `hoerbuch_mp3`               |
| Einzel-MP3 / MKV / m4b | `file`      | `audio-file` / `video-file` / `hoerbuch-m4b` |

So verhält sich **Single** wie ein kleines Album-Set mit Fokus auf Remix-/Bonus-Track-Dichte, bleibt aber klar getrennt von `album` und `compilation` und passt perfekt in die Audi-Typ-Welt – ohne konkrete Namen im Code.
---

## Zentrale Typ-Logik: Container vs. Einzeldatei

**Album-artige Strukturen** (Album, Playlist, Compilation, Soundtrack, Hörbuch-MP3-Reihen, Single-Reihen, Serien-Staffeln usw.) werden als **„playable containers“ mit mehreren Dateien** behandelt, während einzelne Standalone-Dateien (z.B. einzelnes MP3, einzelnes MKV, einzelnes m4b) als **`file`-Typ** laufen.

m4b-Hörbücher bleiben als Container-Audio-Item möglich, aber du solltest **nicht alle Audio-Objekte als „Album“ behandeln**, sondern klar trennen zwischen:

- **Container** (Album/Playlist/Compilation usw.)
- **Einzeldatei** (single file, typ `file`)

### 1. Zentrale Typ-Regel

Für alle wichtigen Audio-Objekte gilt:

- Wenn im Ordner **mehrere Tracks/Dateien** liegen, ist es ein **playable Container** (Album-Familie):
  - `album`, `playlist`, `compilation`, `klassik`, `soundtrack`, `hoerbuch_mp3`
- Wenn **nur ein einzelnes Audio-/Video-File** existiert, ist es ein **`file`** (Typ: `audio-file`, `video-file`, `hoerbuch-m4b`, etc.).
  - `m4b` bleibt als eigenständiges Item (z.B. `audio-hoerbuch-m4b`).
  - Single-MP3, einzelner Film, einzelner Konzert-MKV → `file`.

Damit deckst du alles ab, ohne jedes Audio-Objekt als „Album“ zu misshandeln.

### 2. Objekt-Schema mit `media_type` + `subtype` + `file_type`

```python
# Beispiel: Container (Album/Playlist/Compilation/Soundtrack/Klassik/Hoerbuch_mp3)
{
  "id": "container_123",
  "media_type": "container",
  "subtype": "album",  # oder "playlist", "compilation", ...
  "title": "<Titel>",
  "artist": "<Künstler>",
  "year": 2020,
  "folder": "/media_library/<Künstler> - <Album> (2020)",
  "cover": "/media_library/<Künstler> - <Album> (2020)/Cover.png",
  "files": [ ... ],
}

# Beispiel: Einzel-Datei (File-Typen)
{
  "id": "file_456",
  "media_type": "file",
  "file_type": "audio-file",  # oder "video-file", "hoerbuch-m4b"
  "title": "<Titel>",
  "artist": "<Künstler>",
  "year": 2020,
  "src": "/media_library/Single (2020)/Track - Single.mp3",
  "cover": "/media_library/Single (2020)/Cover.png",   # optional
}
```

- `media_type` = `container` vs. `file` ist die große Bruchstelle.
- `subtype` beschreibt nur Container-Varianten.
- `file_type` beschreibt nur Einzel-Datei-Varianten.

### 3. Konkrete Zuordnung (Audio-Welt)

| Konzept                         | `media_type` | `subtype` / `file_type`          |
|---------------------------------|-------------|----------------------------------|
| Album (MP3/FLAC)               | `container` | `album`                          |
| Playlist (Sortierte Track-Reihe)| `container` | `playlist`                       |
| Compilation (Various Artists)   | `container` | `compilation`                    |
| Klassik-Werk (Op. 1, 2, 3 …)   | `container` | `klassik`                        |
| Soundtrack (Film/TV/Spiel)     | `container` | `soundtrack`                     |
| Hörbuch als viele MP3-Tracks    | `container` | `hoerbuch_mp3`                   |
| Hörbuch als ein m4b-File       | `file`      | `hoerbuch-m4b`                   |
| Single-MP3 (1 File, Ordner mit Cover) | `file`      | `audio-file` (oder `music-single`) |
| Einzelner Konzert-MKV/Film      | `file`      | `video-file`                     |

### 4. Play-Plan-Logik in deiner App

- Für `media_type == "container"`:
  - `get_play_plan` erzeugt eine Playlist/Track-Timeline (z.B. Liste von URLs für `audio-mp3`/`audio-flac`/`video-mp4`).
  - Web-Player zeigt Cover + Track-Liste + Playlist-Control (Play-Entire-Container, random-Play-Modus, etc.).
- Für `media_type == "file"`:
  - `get_play_plan` erzeugt nur einen Source-Eintrag (`url`, `type`).
  - Web-Player verstehen:
    - Musik-`file_type` → Audio-Player-Modus.
    - Video-`file_type` → Video-Player-Modus.
    - `hoerbuch-m4b` → Audio-Player mit Lese-Fortsetzung (Resume-Support optional).

### 5. Kurz auf den Punkt gebracht

- **ALBUM-ähnliche Sachen** (Album, Playlist, Compilation, Soundtrack, Klassik, MP3-Hörbuch-Reihen, Serien-Staffeln, jede Struktur mit vielen Dateien) → `media_type: "container"`.
- **EINZELDATEIEN** (single-MP3, einzelner MKV, einzelner m4b, einzelner Film, einzelner Konzert) → `media_type: "file"` + `file_type`.
- **m4b-Hörbücher** bleiben als `file`, keine Album-Faux-Pas, keine Album-Semantik; nur ihre ganzen MP3-Reihen gehen als `container`.

Damit hast du die saubere innere Typ-Logik, nach der du deine Web-Player-Pipeline, VLC-Pfade, HLS/MP4-Routing, WebSocket-Events und deine Eel-UI sauber bauen kannst, ohne jemals konkrete Namen wie „Avengers“ oder „Künstlername“ im Code hardcoden zu müssen.
---

## Einheitliches Cover-Schema für Audio-Objekte

### 1. Allgemeines Cover-Schema

Für jeden audio-basierten Typ:

- Der `folder` des Items enthält `Cover.png` (oder `cover.jpg`).
- Im Objekt: Attribut `cover` statt `poster`.
- Backend extrahiert Cover-Path automatisch, z.B.:

```python
cover_path = os.path.join(folder, "Cover.png")
if not os.path.exists(cover_path):
    cover_path = os.path.join(folder, "cover.jpg")
```

Das ist flexibel, aber konsistent, egal ob es Film-/Album-/Hörbuch-Cover ist.

### 2. Objekt-Schema für Audio-Typen

Allen dieser Typen gibst du `media_type: "audio"` und `cover`:

```python
{
  "id": "audio_...",
  "title": "<Titel>",
  "artist": "<Künstler>",
  "year": 2020,
  "media_type": "audio",
  "subtype": "album",  # oder "single", "soundtrack" etc.
  "folder": "/media_library/<Künstler> - <Album> (2020)",
  "cover": "/media_library/<Künstler> - <Album> (2020)/Cover.png",
  "files": [...]
}
```

Unter `subtype` unterscheidest du:

- `album`        → Musik-Album
- `single`       → Einzelsingle (oft 1–3 Tracks, MP3/FLAC)
- `compilation`  → Best-of-/Various-Artists-Kollektion
- `soundtrack`   → Filmmusik-/Game-Soundtrack
- `klassik`      → Orchester/Chor-Klassik
- `hoerbuch_m4b` → Hörbuch-Container m4b
- `hoerbuch_mp3` → Multiple-MP3-Hörbuch-Tracks

### 3. Anwendung für diese Subtypen

#### a) Musik-Album / Single / Compilation / Klassik

- `cover` wird im Web-Player als Album-Cover verwendet.
- Audio-Tracks (FLAC/MP3) werden über Web-Audio-Player oder `<audio>`-Elemente abgespielt.
- Subtype-Logik zeigt z.B.:
  - `subtype == "album"` → Album-Liste mit Track-Timeline
  - `subtype == "compilation"` → Autor+Titel mixt, kein zentraler Interpret
  - `subtype == "klassik"` → Zusatz-Metadaten: Komponist, Orchester, Opus-Nummer

#### b) Hörbuch-Untertypen

- `hoerbuch_m4b`:

  ```python
  {
    "type": "audio-m4b",
    "preferred_client": "web-browser",
    "play_mode": "http-m4b"
  }
  ```

  MP4-basierter Audiobook-Container, unterstützt von vielen Browsern/Players.

- `hoerbuch_mp3`:

  ```python
  {
    "type": "audio-mp3-chapters",
    "preferred_client": "web-browser",
    "play_mode": "http-mp3-chaptered"
  }
  ```

  Meist viele MP3-Dateien, die du als „Hörbuch-Teile“ in einer Playlist-Timeline organisierst.

#### c) Soundtrack

- `subtype == "soundtrack"` → spezielle UI-Tags:
  - Track-Liste mit Film-/Serie-Titel,
  - ggf. Zeit-Offsets zum Video im Video-Tab.
- Aber `cover` bleibt gleich: Ein Bild pro Soundtrack-Ordner, wie bei jedem Album/Hörbuch.

### 4. Integration in deinen Code

- Backend-Scan:

  ```python
  def scan_audio_dir(dir_path, media_type="audio", subtype="album"):
      folder = dir_path
      title = ...
      artist = ...
      year = ...

      cover = find_cover(folder)  # Cover.png oder cover.jpg

      files = scan_files(folder)
      return {
          "id": slug(...),
          "artist": artist,
          "title": title,
          "year": year,
          "media_type": "audio",
          "subtype": subtype,
          "folder": folder,
          "cover": cover,
          "files": files
      }
  ```

- Routing-Logik:
  - Je nach `subtype` wählst du andere Player-Ansichten (Album-Liste, Hörbuch-Timeline, Soundtrack-Timeline).

### 5. Vorteil von „Cover statt Poster“

- Einheitliche Semantik:
  - `poster` → primär für Video (Filme, Serien).
  - `cover` → primär für Audio (Album, Hörbuch, Soundtrack).
- UI-Konsistenz:
  - Alle Audio-Untertypen nutzen `cover`.
  - Backend/Player-Code unterscheidet nur über `media_type` + `subtype`, ohne Umbenennung der Covers.

So kannst du `cover` sauber für alle deine Audio-Objekte (Album, Single, Compilation, Klassik, m4b-Hörbuch, MP3-Hörbuch, Soundtrack) einsetzen, ohne dass dein Web-Player-Layout oder dein Python-Code je Namen wie „Avengers“ oder ähnliche wissen muss.
[//]: # (FIKTIVES, LIVE-READY BEISPIEL ANS ENDE DER DATEI ANHÄNGEN)

---

## Konkretes, live-taugliches Beispiel (fiktiv)

### 1. Beispiel-Ordner + Datei-Ablauf

Ordner:

```
/media_library/ExampleMovie (2021)/
  Poster.png
  ExampleMovie (2021).iso
  ExampleMovie (2021).mkv
  ExampleMovie (2021)_h264.mp4
```

- `Poster.png` wird im UI als Cover genutzt.
- `.iso` steht für PAL/NTSC-DVD mit Menüs (VLC-DVD-Modus).
- `.mkv` ist der remuxte MPEG-2-Hauptfilm.
- `_h264.mp4` ist dein Web-Player-Ready-VOD-File (aus der DVD-Konvertierung).

---

### 2. Beispiel-Film-Objekt (fiktiv)

```python
{
  "id": "examplemovie_2021",
  "title": "ExampleMovie",
  "year": 2021,
  "media_type": "movie",
  "folder": "/media_library/ExampleMovie (2021)",
  "poster": "/media_library/ExampleMovie (2021)/Poster.png",
  "created": "2026-03-19T00:18:13.828569",
  "files": [
    {
      "src": "/media_library/ExampleMovie (2021)/ExampleMovie (2021).iso",
      "type": "dvd-iso",
      "preferred_client": "vlc-dvd",
      "play_mode": "bluray:///"
    },
    {
      "src": "/media_library/ExampleMovie (2021)/ExampleMovie (2021).mkv",
      "type": "dvd-mkv",
      "preferred_client": "vlc-file",
      "play_mode": "file"
    },
    {
      "src": "/media_library/ExampleMovie (2021)/ExampleMovie (2021)_h264.mp4",
      "type": "h264-vod",
      "preferred_client": "web-browser",
      "play_mode": "http-mp4"
    }
  ]
}
```

---

### 3. Nutzung in den Abspiel-Modi

- **Web-Player (MVP/Overkill):**
  - `get_play_plan(item, 'browser')` nimmt die `h264-vod`-Datei → Direct Play oder HLS
  - `player.src({ src: plan.url, type: "video/mp4" });`
- **VLC-DVD-Modus:**
  - `open_in_vlc(dvd_path)` mit `dvd:///` + Pfad zur `.iso`
- **VLC-Remux-Modus:**
  - `.mkv`-Datei an VLC übergeben, Deinterlace im Player schalten

---

### 4. Beispiel-Code: Film-Scan

```python
def scan_movie_dir(dir_path):
    name_with_year = os.path.basename(dir_path)
    title, year = split_title_year(name_with_year)
    poster = os.path.join(dir_path, "Poster.png")
    files = []
    for f in os.listdir(dir_path):
        full = os.path.join(dir_path, f)
        if f.lower().endswith(".iso"):
            files.append({
                "src": full,
                "type": "dvd-iso",
                "preferred_client": "vlc-dvd",
                "play_mode": "bluray:///"
            })
        elif f.lower().endswith(".mkv"):
            files.append({
                "src": full,
                "type": "dvd-mkv",
                "preferred_client": "vlc-file",
                "play_mode": "file"
            })
        elif f.lower().endswith("_h264.mp4"):
            files.append({
                "src": full,
                "type": "h264-vod",
                "preferred_client": "web-browser",
                "play_mode": "http-mp4"
            })
    return {
        "id": f"{slugify(title)}_{year}",
        "title": title,
        "year": year,
        "folder": dir_path,
        "poster": poster,
        "media_type": "movie",
        "files": files
    }
```

---

**Fazit:**
- Mit dieser Struktur kannst du in deiner App echte, greifbare Beispiele (Ordner + ISO/MKV/MP4 + Poster) für alle Abspiel-Modi und Features nutzen.
- Die Pipeline ist generisch, aber sofort „live-ready“ für echte Medien.
# Allgemeines Film-Objekt & Routing für Mediathek

**Ziel:**
Jeder Film-Ordner in der Mediathek folgt einem einheitlichen, generischen Schema – keine harten Titel im Code, alles dynamisch aus dem Ordnernamen extrahiert.

---

## 1. Beispielhafte Ordnerstruktur (allgemein)

```
/media_library/
  <Titel> (<Jahr>)/
    Poster.png
    <Titel> (<Jahr>).iso
    <Titel> (<Jahr>).mkv
    <Titel> (<Jahr>)_h264.mp4
```
- `<Titel> (<Jahr>)` wird dynamisch aus dem Ordnernamen verwendet.
- `Poster.png`: Cover für Web-UI
- `.iso`: PAL/NTSC-Video-DVD mit Menüs (VLC)
- `.mkv`: Remuxtes MPEG-2 (Hauptfilm)
- `_h264.mp4`: Für Web-Player-Direct-Play/HLS

---

## 2. Beispiel-Film-Objekt (ohne konkrete Namen)

```python
{
  "id": "film_73a9b1f",
  "title": "<Titel>",
  "year": 2020,   # aus Ordnernamen extrahiert
  "media_type": "movie",
  "folder": "/media_library/<Titel> (2020)",
  "poster": "/media_library/<Titel> (2020)/Poster.png",
  "created": "2026-03-19T00:20:00.123456",
  "files": [
    {
      "src": "/media_library/<Titel> (2020)/<Titel> (2020).iso",
      "type": "dvd-iso",
      "preferred_client": "vlc-dvd",
      "play_mode": "bluray:///"
    },
    {
      "src": "/media_library/<Titel> (2020)/<Titel> (2020).mkv",
      "type": "dvd-mkv",
      "preferred_client": "vlc-file",
      "play_mode": "file"
    },
    {
      "src": "/media_library/<Titel> (2020)/<Titel> (2020)_h264.mp4",
      "type": "h264-vod",
      "preferred_client": "web-browser",
      "play_mode": "http-mp4"
    }
  ]
}
```
- `title` und `year` werden aus dem Ordnernamen geparst.
- `id` wird aus slugify(title)+"_"+str(year) gebildet.

---

## 3. Nutzung in der App
- Scanner durchläuft alle `/media_library/*(<4-Ziffern>)*`-Ordner und erzeugt solche Objekte.
- `get_play_plan(item, client='browser')` wählt immer die `h264-vod`-Variante (falls vorhanden), `client='vlc'` die `dvd-iso` oder `dvd-mkv`-Variante.
- Im Video-Tab sieht man für jeden Film-Ordner denselben Aufbau, nur mit den echten `<Titel> (<Jahr>)`-Namen.

---

**Fazit:**
- Keine harten Filmtitel im Code
- Einheitliches, dynamisches Schema für alle Medienobjekte
- Routing und Playlist-Logik sind generisch und wartbar
