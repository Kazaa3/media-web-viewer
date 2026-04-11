# Beschreibung: Datenbank (DB) im Projekt

## Typ und Speicherort
- Verwendet wird eine **SQLite**-Datenbank (Dateibasierte DB, keine Server-Installation nötig)
- Standardpfad: `data/database.db` (bzw. `~/.media-web-viewer/media_library.db` als Fallback)

## Struktur
- Zentrale Tabelle: `media`
  - Felder: id, name, path, type, duration, category, is_transcoded, transcoded_format, tags (JSON), extension, container, tag_type, codec, has_artwork, full_tags (JSON)
- Weitere Tabellen: `playlists`, `playlist_media`

## Ein- und Ausgaben
- **insert_media(item_dict):** Fügt ein Media-Item (dict) als neuen Eintrag ein
- **get_all_media():** Gibt eine list of dicts (alle Media-Items) zurück
- **update_media_tags(), rename_media(), delete_media()**: Aktualisieren, umbenennen oder löschen Einträge
- **tags** und **full_tags** werden als JSON-Strings gespeichert (Serialisierung/Deserialisierung mit `json.dumps()`/`json.loads()`)

## Datenfluss
- Parser/Importer → item dict → insert_media() → DB
- DB → get_all_media() → list of dicts → API/UI
- Einzelne Felder (z.B. tags) können gezielt aktualisiert werden

## Vorteile von SQLite
- Keine Server-Installation nötig, portabel
- Einfache Sicherung und Migration (Datei kopieren)
- SQL-Standard, unterstützt komplexe Abfragen

## Hinweise
- Migrationen: Neue Felder werden bei Bedarf per ALTER TABLE ergänzt
- Legacy-DBs werden erkannt und können bereinigt werden
- Für große Datenmengen oder Multi-User-Betrieb wäre ein Server-DBMS (z.B. PostgreSQL) nötig

---

**Siehe auch:**
- Logbuch: db.py IO Beschreibung
- src/core/db.py, data/
- https://www.sqlite.org/
