# MediaItem & Datenbank – Best Practices und Erweiterungen

## Übersicht
Die Media-Datenbank in Media Web Viewer basiert auf dem MediaItem-Modell (models.py) und db.py für SQLite-Operationen. Alle Zugriffe und Änderungen laufen zentral über db.py, um Konsistenz und Wartbarkeit zu gewährleisten.

## Grundstruktur
- Tabelle: `media_items`
- Spalten: id (Primärschlüssel), filename, filepath, filetype, duration, tags, metadata (JSON), added_at, updated_at
- MediaItem-Modell kapselt Attribute und Methoden für Mediendateien

## Best Practices
- Insert, Update, Delete und Suche immer über db.py
- Indexe auf filename, tags, filetype für schnelle Suche
- Metadaten als JSON oder strukturierte Spalten
- Validierung vor Insert/Update (Dateiexistenz, Typ)
- Unit-Tests für db.py und MediaItem-Logik

## Erweiterungen & Optimierungen
- Erweiterte Felder: rating, cover_art, deleted_at (Soft-Delete), History-Tabelle
- Foreign Keys: Verknüpfung mit Kategorien, Playlists
- Tagging-System: Separate Tags-Tabelle mit Many-to-Many-Beziehung
- Batch-Import mit Transaktionssicherheit
- Duplikaterkennung (Hash, Pfad, Metadaten)
- Migration/Schema-Update via db.py
- Performance: Indexe, optimierte Queries, Monitoring
- Backup/Restore-Funktionen
- API-Versionierung für DB- und Schnittstellen
- Export/Import als JSON/CSV
- UI-Integration: API-Funktionen für Listen, Filter, Bearbeiten

## Beispiel
```python
# models.py
class MediaItem:
    def __init__(self, filename, filepath, filetype, duration, tags, metadata):
        self.filename = filename
        self.filepath = filepath
        self.filetype = filetype
        self.duration = duration
        self.tags = tags
        self.metadata = metadata

# db.py
import sqlite3

def add_media_item(item: MediaItem):
    conn = sqlite3.connect('media.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO media_items (filename, filepath, filetype, duration, tags, metadata) VALUES (?, ?, ?, ?, ?, ?)",
        (item.filename, item.filepath, item.filetype, item.duration, ','.join(item.tags), json.dumps(item.metadata))
    )
    conn.commit()
    conn.close()
```

## Hinweise
- Alle Zugriffe und Änderungen sollten über db.py laufen.
- MediaItem dient als zentrale Datenstruktur für alle Medienoperationen.
- Erweiterbar für weitere Felder und Beziehungen.
- Monitoring und Logging für Debugging und Performance.

---
*Letzte Aktualisierung: 10. März 2026*
