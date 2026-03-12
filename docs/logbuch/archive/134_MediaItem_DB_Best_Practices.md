# MediaItem & DB – Best Practices

## Übersicht
Für die Verwaltung von Mediendateien in Media Web Viewer empfiehlt sich die Nutzung des MediaItem-Modells (models.py) für ORM-ähnliche Logik und db.py für alle SQLite-Operationen.

## Vorgehen
- **MediaItem-Modell:** Kapselt alle relevanten Attribute (Dateiname, Pfad, Typ, Dauer, Tags, Metadaten) und Methoden für Media-Objekte.
- **db.py:** Stellt Funktionen für Insert, Update, Delete und Suche bereit. Alle Datenbankzugriffe laufen über diese Schnittstelle.

## Best Practices
- Jede Mediendatei wird als einzelne Zeile in der Tabelle `media_items` gespeichert.
- Nutze Primärschlüssel (id) für eindeutige Identifikation.
- Metadaten können als JSON-Feld oder separate Spalten gespeichert werden.
- Indexe auf häufig genutzte Felder (filename, tags, filetype) für schnelle Suche.
- Änderungen (Hinzufügen, Aktualisieren, Löschen) immer über db.py ausführen.
- Isolation und Konsistenz durch zentrale DB-Logik gewährleisten.

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
- Erweiterbar für weitere Felder (z.B. added_at, updated_at).

---
*Letzte Aktualisierung: 10. März 2026*
