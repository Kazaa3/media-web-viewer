# Beschreibung: list of dicts im Projekt

## Was ist eine list of dicts?
- Eine "list of dicts" ist eine Python-Liste, deren Elemente jeweils Dictionaries sind.
- Struktur: `[dict1, dict2, ...]`

## Typische Einsatzzwecke im Media Web Viewer
- **Sammlung von Media Items:**
  - Beim Abruf aller Medien aus der Datenbank (`get_all_media()`) wird eine Liste von item dicts zurückgegeben.
- **API- und UI-Kommunikation:**
  - Die API liefert eine list of dicts als JSON an das Frontend (z.B. für die Anzeige der Mediathek).
- **Testdaten und Reports:**
  - Testfälle, Exporte und Reports nutzen dieses Format für strukturierte, tabellarische Daten.

## Vorteile
- Einfache Iteration und Verarbeitung (z.B. in for-Schleifen)
- Gut geeignet für tabellarische oder listenartige Daten
- Leicht zu serialisieren (z.B. zu JSON, CSV)

## Beispiel
```python
media_list = [
    {"name": "Song1", "path": "/media/Song1.mp3", "tags": {"genre": "Rock"}},
    {"name": "Song2", "path": "/media/Song2.mp3", "tags": {"genre": "Pop"}}
]
```

## Hinweise
- Die einzelnen dicts in der Liste folgen meist einer gemeinsamen Struktur (z.B. item dict)
- Die list of dicts ist das Standardformat für den Austausch von mehreren Objekten zwischen DB, API und UI

---

**Siehe auch:**
- Logbuch: item dict Beschreibung
- Logbuch: db.py IO Beschreibung
- src/core/db.py, API, UI
