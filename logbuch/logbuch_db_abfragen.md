## 1. get_media_by_id(media_id)
- **Beschreibung:**
  - Liefert das vollständige Medienobjekt anhand der eindeutigen Datenbank-ID.
- **Ablauf:**
  - Initialisiert DB, sucht mit `SELECT * FROM media WHERE id = ?`.
  - Gibt ein Dictionary mit allen Feldern zurück (inkl. Metadaten, Tags, Playback-Status).
- **Verwendung:**
  - Direktes Nachschlagen eines Items (z.B. für Detailansicht, Bearbeitung, Playback).

---

## 2. get_media_by_path(path)
- **Beschreibung:**
  - Liefert das vollständige Medienobjekt anhand des Dateisystempfads.
- **Ablauf:**
  - Initialisiert DB, sucht mit `SELECT * FROM media WHERE path = ?`.
  - Gibt ein Dictionary mit allen Feldern zurück.
- **Verwendung:**
  - Für Scans, Duplikatprüfung, direkte Dateizugriffe.

---

## 3. get_media_by_remote_id(field, value)
- **Beschreibung:**
  - Liefert ein Medienobjekt anhand eines Remote-Identifier-Felds (isbn, imdb, tmdb, discogs).
- **Ablauf:**
  - Prüft Feld, sucht mit `SELECT * FROM media WHERE {field} = ?`.
  - Gibt ein Dictionary mit allen Feldern zurück.
- **Verwendung:**
  - Für Metadaten-Anreicherung, externe API-Integrationen, Cover-Suche.

---

## 4. Rückgabeformat
- Immer ein Dictionary mit:
  - Basisdaten: id, name, path, type, duration, category, extension, container, tag_type, codec
  - Artwork: art_path, has_artwork
  - Transcoding: is_transcoded, transcoded_format
  - Metadaten: tags, full_tags (JSON)
  - Playback: playback_position, last_played, duration_sec
- Bei Nicht-Fund: `None`

---

## 5. Best Practices
- Immer auf `None` prüfen (nicht gefunden).
- Für komplexe Abfragen (z.B. nach parent_id, Typen) eigene Query-Funktionen nutzen.
- JSON-Felder (tags, full_tags) immer dekodieren.

---

## Fazit
Die Funktionen get_media_by_id, get_media_by_path und get_media_by_remote_id sind zentrale Bausteine für den gezielten Zugriff auf einzelne Medienobjekte in der Datenbank – für UI, API, Metadaten-Import und Playback-Workflows.

---

## Hinweis zur ID-Funktionalität

Das Feld `id` ist in der Tabelle `media` als `INTEGER PRIMARY KEY AUTOINCREMENT` korrekt definiert. Die Funktion `get_media_by_id` arbeitet direkt und zuverlässig mit diesem Feld: Sie sucht gezielt nach der eindeutigen ID, gibt sie im Rückgabeobjekt aus und nutzt die automatische Vergabe durch die Datenbank. Insert- und andere Abfragen sind konsistent darauf abgestimmt. Die ID ist somit eindeutig, automatisch vergeben und voll funktionsfähig für gezielte Abfragen und alle Workflows.

---

## Hinweis: Automatische Vergabe der ID beim Insert

Du musst die `id` beim Einfügen eines neuen Medien-Items **nicht** selbst definieren – die Datenbank vergibt die ID automatisch. Das Feld `id` ist als `INTEGER PRIMARY KEY AUTOINCREMENT` definiert. Bei jedem `INSERT` erzeugt SQLite selbstständig eine eindeutige, fortlaufende ID.

**Beispiel:**
```python
item_dict = {
  'name': 'Testvideo',
  'path': '/media/testvideo.mkv',
  'type': 'Video',
  'duration': '01:30:00',
  # ... weitere Felder ...
}
insert_media(item_dict)  # id wird automatisch gesetzt
```
Du kannst das Feld beim Insert einfach weglassen; es wird automatisch gesetzt und ist danach über `get_media_by_id` abfragbar.


---

## Konkretes Beispiel: Automatische ID-Vergabe (Autoincrement)

Wenn du mehrere Medien-Items einfügst, vergibt die Datenbank die ID automatisch fortlaufend (Autoincrement):

```python
item1 = {
  'name': 'Video 1',
  'path': '/media/video1.mkv',
  'type': 'Video',
  'duration': '00:10:00',
}
item2 = {
  'name': 'Video 2',
  'path': '/media/video2.mkv',
  'type': 'Video',
  'duration': '00:20:00',
}
id1 = insert_media(item1)  # z.B. 1
id2 = insert_media(item2)  # z.B. 2
id3 = insert_media(item2)  # z.B. 3 (bei erneutem Insert)
```

**Autoincrement bedeutet:** Die ID startet bei 1 (oder 0, je nach DB-Engine) und wird bei jedem neuen Eintrag um 1 erhöht: 1, 2, 3, ...
Du musst dich nicht um die Vergabe kümmern – die Datenbank garantiert Eindeutigkeit und Reihenfolge.
# Logbuch: Media-Datenbank – Abfragefunktionen (get_media_by_id, get_media_by_path, get_media_by_remote_id)

## Ziel
Dokumentation der wichtigsten Abfragefunktionen für einzelne Medienobjekte in der Media-Library-Datenbank. Fokus: Zugriff per ID, Pfad oder Remote-Identifier (ISBN, IMDB, TMDB, Discogs).

---