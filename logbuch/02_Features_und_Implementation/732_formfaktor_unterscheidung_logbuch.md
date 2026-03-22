---

# Logbuch-Eintrag: Formfaktor-Unterscheidung für Cover/Art in Medienobjekten

Ja, **Formfaktor zu unterscheiden** ist wichtig, weil **Cover/Art** für ein Buch, eine CD, eine DVD, eine Blu‑Ray, einen Vinyl‑Record oder eine Box oft optisch und metrisch unterschiedlich sind.  Vor allem bei **DVD/CD‑Covers** solltest du Formfaktor sauber im Typen‑Schema mitführen, damit du z.B. nicht versehentlich ein CD‑Cover als Box‑Cover nutzt.

## 1. Warum Formfaktor‑Unterscheidung sinnvoll ist

- Ein **Buch** ist ein Rechteck (6×9‑Format), ein **CD‑Cover** eher 11,5×11,5, ein **DVD‑/Blu‑Ray‑Cover** 13,5×18, usw.  
- Viele Plattformen zeigen diese Formate unterschiedlich an (z.B. Renderer passt Cover‑Größe an).

Damit hilfst du deinem System:

- **Korrekte Cover‑Darstellung** (z.B. Box‑Ansicht vs. CD‑/DVD‑Rip).  
- **Saubere Metadaten** (z.B. „Original‑Format“ des Releases).

---

## 2. Schema‑Erweiterung: `form_factor`

Ergänze dein Objekt‑Schema um ein `form_factor`‑Feld:

```json
{
  "id": "obj_123",
  "media_type": "container",
  "subtype": "album" | "dvd_video" | "bluray_video" | "book",
  "title": "<Titel>",
  "year": 2020,
  "isbns": [...],        // optional
  "imdb": "tt123456",    // optional
  "tmdb": 12345,         // optional
  "cover": "/media_library/<Titel> (2020)/Cover.png",
  "amazon_cover": "https://m.media‑amazon.com/images/...",

  "form_factor": "cd" | "dvd" | "bluray" | "book_6x9" | "vinyl_lp"
}
```

---

## 3. Formfaktoren im Detail (auch für CD/DVD)

### a) Audio‑/Album‑Formfaktoren

- `cd`  
  - Standard‑CD‑Album (12×12‑Art, oft mit Booklet).  
- `vinyl_lp`  
  - Vinyl‑Vinyl‑LP (großes Cover, 12″).  
- `booklet`  
  - Nur Booklet/Flap (z.B. für Box‑Editionen).

```json
{
  "media_type": "container",
  "subtype": "album",
  "form_factor": "cd"
}
```

### b) Video‑Formfaktoren

- `dvd`  
  - DVD‑Video‑Box, 13,5×18‑Cover.  
- `bluray`  
  - Blu‑Ray‑Cover (13,5×18, oft mit Box).  
- `dvd_4k` / `bluray_4k`  
  - UHD‑Veröffentlichung.

```json
{
  "media_type": "container",
  "subtype": "dvd_video",
  "form_factor": "dvd"
}
```

```json
{
  "media_type": "container",
  "subtype": "bluray_video",
  "form_factor": "bluray"
}
```

### c) Bücher

- `book`  
  - Standard‑Buch, 6×9‑Format (Deutschland, Japan, etc.).  
- `book_large` / `book_8x10`  
  - Graphic Novel, Bildband, etc.

```json
{
  "media_type": "container",
  "subtype": "book",
  "form_factor": "book"
}
```

---

## 4. Warum das bei CD/DVD‑Covers besonders wichtig ist

- **Cover‑Größe und Design**  
  - DVD/Blu‑Ray‑Cover ist größer als CD‑Cover.  
  - Rendern in deinem Web‑Player (z.B. 3D‑Box‑View, Serien‑Staffel‑Ansicht) braucht dieses Wissen.  

- **Blur‑Ray‑/DVD‑Box vs. CD‑Box**  
  - Wenn du „Box‑Editionen“ hast, brauchst du klare Unterscheidung zwischen `form_factor: "cd"` und `form_factor: "dvd" | "bluray"`.  

Beispiel:

```json
{
  "media_type": "container",
  "subtype": "box",
  "title": "<Box‑Titel>",
  "form_factor": "bluray",
  "cover": "/media_library/<Box‑Titel> (2025)/Cover.png",
  "isbns": ["978-3-12-345678-9"],
  "imdb": "tt1234567",
  "files": [...]
}
```

---

## 5. Praktische Nutzung in deiner Mediathek

- **Cover‑Renderer in deinem Web‑Player**  
  - `if (form_factor === "cd") { ... }`  
  - `else if (form_factor === "dvd") { ... }`  
  - `else if (form_factor === "bluray") { ... }`  

- **Metadaten‑Funktionen**  
  - Suche nach `form_factor: "cd"` liefert alle CD‑Releases.  
  - Suche nach `form_factor: "dvd"` liefert alle DVD‑Veröffentlichungen.  

---

## 6. Typen‑Überblick mit Formfaktor

| Typ                        | `media_type` | `subtype`             | `form_factor`          |
|---------------------------|-------------|------------------------|------------------------|
| Buch                      | `container` | `book`                | `book` / `book_large`  |
| CD‑Album                  | `container` | `album`               | `cd`                   |
| Vinyl‑LP                  | `container` | `album`               | `vinyl_lp`             |
| Vinyl‑Single              | `container` | `single`              | `vinyl_single`         |
| DVD‑Video                 | `container` | `dvd_video`           | `dvd`                 |
| Blu‑Ray‑Video             | `container` | `bluray_video`        | `bluray`              |
| Blu‑Ray‑UHD               | `container` | `bluray_video`        | `bluray_4k`           |
| Blu‑Ray‑Box               | `container` | `box`                 | `bluray`              |
| CD‑Box                    | `container` | `box`                 | `cd`                  |
| Hörbuch (MP3, m4b, etc.)  | `container`/`file` | `hoerbuch_mp3`/`hoerbuch_m4b` | `book` (falls Buch‑Basis) |

---

## 7. Beispiel‑Abfrage

```python
# Suche nach allen DVD‑Releases
dvd_releases = [o for o in objects if o["form_factor"] == "dvd"]

# Suche nach allen CD‑Releases
cd_releases = [o for o in objects if o["form_factor"] == "cd"]

# Suche nach Blu‑Ray‑Videos
bluray_video = [o for o in objects if o["form_factor"] == "bluray" and o["subtype"] == "bluray_video"]
```

---

## 8. Vorteil für deine Mediathek

- **Präzise Cover‑Darstellung**  
  - CD, DVD, Blu‑Ray, Book, Vinyl – alle mit korrekter Formfaktor‑Basis.  
- **Einheitliche Typen**  
  - `form_factor` + `media_type`/`subtype` bilden ein komplettes Schema für deine Mediathek.  
- **Automatisierte Metadaten**  
  - Formfaktor‑Info kann über externe APIs (z.B. Amazon, ISBN‑DB, IMDb, Discogs) erweitert werden.

Damit kannst du deine Mediathek vollständig automatisiert befüllen, mit klaren Unterscheidungen zwischen CD, DVD, Blu‑Ray, Vinyl, Buch, Hörbuch, Box, etc. – alles ohne konkrete Namen im Code.
