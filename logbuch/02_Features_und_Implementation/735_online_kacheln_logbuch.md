---

# Logbuch-Eintrag: Online-Kacheln für dynamische Cover-Darstellung

## Ziel

- Jede Kachel repräsentiert ein **Online-Cover** (Amazon, IMDb, Discogs, etc.), nicht das lokale `Cover.png`.
- Kacheln werden **dynamisch** vom Server geladen.
- Kacheln sind **formfaktor-sensibel** (CD, DVD, Blu-Ray, Buch, ...).

---

## 1. Schema für Online-Kacheln

Jede Kachel = ein Online-Cover mit Metadaten:

```json
{
  "id": "tile_123",
  "obj_id": "obj_456",
  "source": "amazon" | "imdb" | "discogs" | "tmdb",
  "source_id": "123456",
  "url": "https://m.media-amazon.com/images/...",
  "height": 1000,
  "width": 700,
  "form_factor": "cd" | "dvd" | "bluray" | "book",
  "created_at": "2026-03-19T01:55:00.000000Z"
}
```

- `obj_id`: Verknüpfung zum Medienobjekt
- `source`: Amazon, IMDb, Discogs, ...
- `source_id`: z.B. ASIN, IMDb-ID, Discogs-ID
- `url`: direkte URL zum Online-Bild
- `form_factor`: CD, DVD, Blu-Ray, Buch, ...

---

## 2. Beispiel-Kacheln (ohne konkrete Namen)

```json
[
  {
    "id": "tile_123",
    "obj_id": "obj_456",
    "source": "amazon",
    "source_id": "B07XGTMF3Q",
    "url": "https://m.media-amazon.com/images/...",
    "height": 1000,
    "width": 700,
    "form_factor": "cd"
  },
  {
    "id": "tile_456",
    "obj_id": "obj_789",
    "source": "imdb",
    "source_id": "tt1234567",
    "url": "https://storyline.story-line.org/...",
    "height": 1800,
    "width": 1200,
    "form_factor": "dvd"
  },
  {
    "id": "tile_789",
    "obj_id": "obj_789",
    "source": "bluray_com",
    "source_id": "12345",
    "url": "https://www.bluray.com/...",
    "height": 1350,
    "width": 1800,
    "form_factor": "bluray"
  },
  {
    "id": "tile_101",
    "obj_id": "obj_123",
    "source": "goodreads",
    "source_id": "123456",
    "url": "https://www.goodreads.com/...",
    "height": 600,
    "width": 400,
    "form_factor": "book"
  }
]
```

---

## 3. Backend-Logik für Kacheln

- **Import-Funktion**
  - `fetch_online_covers(obj_id)` holt alle Covers von externen Quellen und speichert sie als Kacheln in der `tiles`-Tabelle.

```python
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from app.models import Base, Obj

class Tile(Base):
    __tablename__ = "tiles"

    id = Column(String, primary_key=True)
    obj_id = Column(Integer, ForeignKey("objs.id"))
    source = Column(String)          # z.B. "amazon"
    source_id = Column(String)       # z.B. ASIN/ID
    url = Column(String)             # URL zum Bild
    height = Column(Integer)
    width = Column(Integer)
    form_factor = Column(String)     # cd, dvd, bluray, book, vinyl_lp
    created_at = Column(DateTime, default=lambda: datetime.now())
```

- **Abfrage-Funktion**
  - `get_tiles_by_obj(obj_id)` liefert alle Online-Covers für ein Objekt.

```python
@app.route("/tiles/<obj_id>", methods=["GET"])
def get_tiles(obj_id):
    tiles = [tile for tile in tiles_table if tile["obj_id"] == obj_id]
    return jsonify(tiles)
```

---

## 4. Frontend (z.B. Bottle/Eel, Web-Player)

```html
<div id="online_tiles_container" class="tile_grid">
  <!-- Leeres Container für Online-Kacheln -->
</div>
```

```javascript
function load_online_tiles(obj_id) {
  fetch(`/tiles/${obj_id}`)
    .then(response => response.json())
    .then(tiles => {
      const container = document.getElementById("online_tiles_container");
      container.innerHTML = "";

      tiles.forEach(tile => {
        const img = document.createElement("img");
        img.src = tile.url;
        img.alt = `Online Tile ${tile.id}`;
        img.height = tile.height;
        img.width = tile.width;
        img.classList.add("tile");

        // Optional: Formfaktor-Klasse
        if (tile.form_factor) img.classList.add(`form_factor_${tile.form_factor}`);

        container.appendChild(img);
      });
    });
}
```

---

## 5. Typen-Überblick mit Online-Kacheln

| Typ                        | `media_type` | `subtype`             | `form_factor`          | `source`                |
|---------------------------|-------------|------------------------|------------------------|-------------------------|
| Buch                      | `container` | `book`                | `book`                 | `amazon`, `goodreads`   |
| CD-Album                  | `container` | `album`               | `cd`                   | `amazon`, `discogs`, `musicbrainz` |
| Vinyl-LP                  | `container` | `album`               | `vinyl_lp`             | `discogs`, `vinyl`      |
| Vinyl-Single              | `container` | `single`              | `vinyl_single`         | `discogs`               |
| DVD-Video                 | `container` | `dvd_video`           | `dvd`                  | `amazon`, `bluray_com`, `imdb` |
| Blu-Ray-Video             | `container` | `bluray_video`        | `bluray`               | `bluray_com`, `imdb`    |
| Blu-Ray-UHD               | `container` | `bluray_video`        | `bluray_4k`            | `bluray_com`            |
| Blu-Ray-Box               | `container` | `box`                 | `bluray`               | `bluray_com`            |
| CD-Box                    | `container` | `box`                 | `cd`                   | `amazon`                |
| Hörbuch (MP3, m4b, etc.)  | `container`/`file` | `hoerbuch_mp3`/`hoerbuch_m4b` | `book` (falls Buch-Basis) | `amazon`, `goodreads` |

---

## 6. Vorteil für deine Mediathek

- **Präzise Online-Cover-Darstellung**  
  - CD, DVD, Blu-Ray, Buch, Vinyl – alle mit korrekter Formfaktor-Basis.  
- **Automatisierte Metadaten**  
  - Covers werden automatisch von externen Quellen abgerufen, keine manuelle Eingabe.  
- **Cloud-Backup-Kacheln**  
  - Kachel-Liste kann als Backup deiner Mediathek dienen, falls du Cover-Datenbank-Restore brauchst.  
- **Einheitliche Typen**  
  - `form_factor` + `source` bilden ein komplettes Schema für deine Online-Kacheln.
