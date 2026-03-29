# Beschreibung: item dict im Projekt

## Was ist das item dict?
- Das `item dict` ist ein zentrales Dictionary, das alle relevanten Informationen zu einem einzelnen Media-Objekt (Media Item) im Projekt bündelt.
- Es wird genutzt, um Metadaten, Status und technische Details eines Mediums zwischen Backend, Datenbank und UI auszutauschen.

## Typische Felder im item dict
- `id`: Eindeutige ID des Media Items (z.B. aus der Datenbank)
- `title`: Titel des Mediums
- `artist`: Interpret/Künstler
- `album`: Albumname (optional)
- `duration`: Spieldauer in Sekunden
- `format`: Dateiformat (z.B. mp3, flac)
- `path`: Dateipfad
- `tags`: Verschachteltes dict mit weiteren Metadaten (z.B. Genre, Jahr)
- `barcode`: (optional) Barcode/Identifier für physische Medien
- `parser`: Name des verwendeten Parsers
- `imported_at`: Zeitstempel des Imports
- `status`: Status (z.B. "imported", "error", "pending")

## Beispiel
```python
item = {
    "id": 42,
    "title": "Songname",
    "artist": "Interpret",
    "album": "Albumname",
    "duration": 215,
    "format": "mp3",
    "path": "/media/music/song.mp3",
    "tags": {"genre": "Rock", "year": 2020},
    "barcode": "1234567890123",
    "parser": "mutagen",
    "imported_at": "2026-03-15T12:34:56Z",
    "status": "imported"
}
```

## Verwendung
- Übergabe zwischen Parser, Datenbank, API und UI
- Grundlage für Anzeige, Suche und Bearbeitung von Medien
- Serialisierung zu JSON für API- und UI-Kommunikation

## Herkunft und Ziel des item dict

### Herkunft (Erzeugung)
- Das item dict wird typischerweise durch die Parser-Module erzeugt, z.B. in:
  - `parsers/media_parser.py` (Funktion: `extract_metadata()`)
  - Einzelne Format-Parser wie `ffprobe_parser.py`, `mutagen_parser.py`
- Es entsteht beim Einlesen/Scannen einer Mediendatei (Audio, Video etc.)
- Initiale Daten können auch aus der Datenbank (`db.py`) oder externen Quellen (z.B. Tag-Scanner, Barcode) stammen

### Ziel (Verwendung und Weitergabe)
- Das item dict wird weitergegeben an:
  - Die Datenbank (Speicherung/Update via `db.py`)
  - Die API/Backend-Logik (z.B. für UI-Anfragen, Eel-API)
  - Die UI/Frontend (Anzeige, Bearbeitung, Suche)
  - Test- und Mock-Objekte (z.B. in `tests/`)
- Es dient als Transport- und Austauschformat zwischen den Schichten Parser → DB → API → UI
- Bei komplexeren Operationen wird es oft in ein `MediaItem`-Objekt (models.py) überführt

## Hinweise
- Die genaue Struktur kann je nach Parser und Medienart variieren.
- Für komplexere Logik wird das item dict oft in ein MediaItem-Objekt (models.py) überführt.

---

**Siehe auch:**
- Logbuch: dicts Beschreibung
- models.py, parsers/media_parser.py, tests/
