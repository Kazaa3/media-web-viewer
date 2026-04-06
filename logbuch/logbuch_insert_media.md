# Logbuch: insert_media – Medien-Item in Datenbank einfügen

## Ziel
Dokumentation und Nachvollziehbarkeit der Funktion `insert_media(item_dict)`, die ein neues Medien-Item mit umfangreichen Metadaten in die Datenbank einfügt. Berücksichtigt werden alle relevanten Felder inkl. Mock-Status und Staging.

---

## Funktionsbeschreibung
```python
def insert_media(item_dict):
    """
    @brief Inserts a new media item into the database.
    @details Fügt ein neues Medien-Item in die Datenbank ein.
    @param item_dict Metadata dictionary / Dictionary mit Metadaten.
    """
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO media (name, path, type, duration, category, is_transcoded,
                             transcoded_format, tags, extension, container, tag_type, codec, 
                             has_artwork, art_path, full_tags, media_type, subtype, file_type,
                             isbn, imdb, tmdb, discogs, amazon_cover, parent_id, is_mock, mock_stage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_dict['name'],
            item_dict['path'],
            item_dict['type'],
            item_dict['duration'],
            item_dict.get('category', 'Audio'),
            item_dict['is_transcoded'],
            item_dict.get('transcoded_format'),
            json.dumps(item_dict['tags']),
            item_dict.get('extension'),
            item_dict.get('container'),
            item_dict.get('tag_type'),
            item_dict.get('codec'),
            1 if item_dict.get('has_artwork') else 0,
            item_dict.get('art_path'),
            json.dumps(item_dict.get('full_tags', {})),
            item_dict.get('media_type'),
            item_dict.get('subtype'),
            item_dict.get('file_type'),
            item_dict.get('isbn'),
            item_dict.get('imdb'),
            item_dict.get('tmdb'),
            item_dict.get('discogs'),
            item_dict.get('amazon_cover'),
            item_dict.get('parent_id'),
            item_dict.get('is_mock', 0),
            item_dict.get('mock_stage', 0)
        ))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except sqlite3.IntegrityError:
        conn.close()
        return None
```

---

## Felder/Bedeutung
- **name, path, type, duration**: Basis-Metadaten
- **category**: Standardmäßig 'Audio', kann überschrieben werden
- **is_transcoded, transcoded_format**: Transcoding-Status und Ziel-Format
- **tags, full_tags**: Metadaten als JSON (kompakt/komplett)
- **extension, container, tag_type, codec**: Technische Details
- **has_artwork, art_path**: Cover-Art-Status und Pfad
- **media_type, subtype, file_type**: Weitere Klassifizierungen
- **isbn, imdb, tmdb, discogs, amazon_cover**: IDs für Medien-Datenbanken
- **parent_id**: Hierarchie/Verknüpfung
- **is_mock, mock_stage**: Mock-Status und Staging für Testdaten

---

## Besonderheiten
- **Fehlerbehandlung**: Bei `sqlite3.IntegrityError` wird `None` zurückgegeben.
- **Datenkonsistenz**: JSON-Serialisierung für komplexe Felder (tags, full_tags).
- **Mock-Unterstützung**: Ermöglicht gezielte Tests und Staging von Medien-Items.

---

## Best Practices
- Immer alle Pflichtfelder im `item_dict` setzen.
- Für optionale Felder sinnvolle Defaults nutzen (`get`).
- Nach jedem Insert Rückgabewert (`last_id`/`None`) prüfen.
- Fehler im Log dokumentieren (optional).

---

## Fazit
`insert_media` ist die zentrale Funktion zum Einfügen neuer Medien-Items in die Datenbank – robust, flexibel und testbar durch Mock-Parameter. Sie bildet die Grundlage für alle Import-, Scan- und Test-Workflows im Media-Backend.
