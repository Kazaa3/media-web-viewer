# Was in db.py rein und raus geht

## Eingaben (rein)
- **insert_media(item_dict):**
  - Erwartet ein item dict mit allen relevanten Feldern (z.B. name, path, type, duration, tags, ...)
  - Schreibt die Daten als neuen Eintrag in die Tabelle `media`
- **update_media_tags(name, tags_dict):**
  - Erwartet einen Mediennamen und ein tags-dict (Metadaten)
  - Aktualisiert die Tags eines bestehenden Eintrags
- **rename_media(old_name, new_name):**
  - Erwartet alten und neuen Namen, ändert den Namen eines Eintrags

## Ausgaben (raus)
- **get_all_media():**
  - Gibt eine Liste von item dicts zurück (alle Medien aus der DB)
- **get_media_path(name):**
  - Gibt den Dateipfad zu einem Mediennamen zurück
- **get_known_media_names():**
  - Gibt ein Set aller Mediennamen zurück
- **get_db_stats():**
  - Gibt ein dict mit Gesamtanzahl und Kategorien-Statistik zurück

## Zwischenschritt: list of dicts
- Beim Abruf aller Medien aus der Datenbank (z.B. mit `get_all_media()`) wird eine **Liste von item dicts** zurückgegeben.
- Diese list of dicts ist das zentrale Austauschformat zwischen DB, API und UI.
- Beispiel:

```python
media_list = get_all_media()
# media_list ist eine Liste wie:
[
    {"name": "Song1", "path": "/media/Song1.mp3", ...},
    {"name": "Song2", "path": "/media/Song2.mp3", ...},
    ...
]
```
- Die API liefert diese Liste als JSON an das Frontend oder andere Komponenten weiter.
- Auch für Tests und Exporte (z.B. Reports, CSV) wird dieses Format genutzt.

## Sonstiges
- **delete_media(name):**
  - Löscht einen Eintrag anhand des Namens
- **clear_media():**
  - Löscht alle Einträge aus der Tabelle `media`

## Datenfluss
- Die wichtigsten Schnittstellen sind item dicts (siehe eigene Beschreibung)
- Parser/Importer → insert_media(item_dict) → DB
- DB → get_all_media() → API/UI/Tests
- Tags/Metadaten können gezielt aktualisiert werden (update_media_tags)

---

**Siehe auch:**
- Logbuch: item dict Beschreibung
- src/core/db.py
