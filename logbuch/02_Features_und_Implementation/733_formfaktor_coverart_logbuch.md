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
