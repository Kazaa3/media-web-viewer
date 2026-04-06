# Logbuch: Objekt-Rework – DVD-Objekt, Image-Obertyp, Album, etc.

## Ziel
Die Datenbank- und Objektstruktur wird überarbeitet, um verschiedene Medientypen wie DVD-Images, Alben, Sammlungen und generische Images/Obertypen klarer und flexibler abzubilden. Ziel ist eine bessere Typisierung, Hierarchie und Erweiterbarkeit für Medienobjekte.

---

## 1. Motivation
- Bisher: Medienobjekte (z.B. DVD, Album, Image) werden oft als generische Items behandelt.
- Problem: Unklare Typisierung, eingeschränkte Abfragen, wenig Flexibilität für neue Medientypen.
- Ziel: Einführung klarer Obertypen (z.B. "image", "album", "collection"), spezifischer Subtypen (z.B. "dvd", "bluray", "iso", "photo_album") und Hierarchie (parent_id, group_id).

---

## 2. Neue Objektstruktur (Beispiel)
- **media_type**: Obertyp (z.B. "image", "album", "track", "video", "collection")
- **subtype**: Feintyp (z.B. "dvd", "bluray", "iso", "photo_album", "boxset")
- **file_type**: Technischer Typ (z.B. "iso", "mkv", "flac")
- **parent_id**: Hierarchie (z.B. Album → Track, Image → Einzelbild, Boxset → Disc)
- **group_id**: Optionale Gruppierung (z.B. für Sammlungen, Multi-Disc-Alben)
- **album, disc_number, track_number**: Für Musik/Audio-Objekte
- **image_info**: Für Images/ISOs (z.B. Dateisystem, Label, Größe, Book-Standard)

---

## 3. Beispiel: DVD-Image als Objekt
```json
{
  "media_type": "image",
  "subtype": "dvd",
  "file_type": "iso",
  "name": "Star Wars Episode IV",
  "path": "/media/StarWarsIV.iso",
  "image_info": {
    "filesystem": "UDF",
    "label": "STAR_WARS_IV",
    "book": "DVD-Video",
    "size": 4700000000
  },
  "parent_id": null,
  "group_id": "boxset_123"
}
```

---

## 4. Beispiel: Album/Track
```json
{
  "media_type": "album",
  "subtype": "audio_album",
  "name": "Abbey Road",
  "artist": "The Beatles",
  "parent_id": null,
  "group_id": null
}
{
  "media_type": "track",
  "subtype": "audio_track",
  "name": "Come Together",
  "album": "Abbey Road",
  "track_number": 1,
  "parent_id": "album_456"
}
```

---

## 5. Vorteile
- **Klarere Typisierung**: Abfragen und UI können gezielt auf Ober-/Subtypen reagieren.
- **Hierarchie**: Abbildung von Alben, Boxsets, Multi-Disc-Images, Sammlungen.
- **Erweiterbarkeit**: Neue Medientypen (z.B. "photo_album", "game_collection") einfach ergänzbar.
- **Metadaten**: Spezifische Felder für Images, Alben, Tracks, etc.

---

## 6. ToDo/Nächste Schritte
- Datenbankschema anpassen (media_type, subtype, group_id, image_info, ...)
- Insert/Update-Logik in Backend anpassen (z.B. insert_media)
- UI/Frontend: Typen und Hierarchie visualisieren
- Migration bestehender Daten

---

## Fazit
Mit dem Objekt-Rework werden DVD-Images, Alben, Tracks und weitere Medientypen sauber und flexibel abgebildet. Die neue Struktur ist zukunftssicher, hierarchisch und erleichtert die Erweiterung und Pflege der Media-Library.
