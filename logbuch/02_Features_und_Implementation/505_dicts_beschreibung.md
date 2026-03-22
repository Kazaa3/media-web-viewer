# Beschreibung: dicts im Projekt

## Was sind dicts?
- In Python sind `dicts` (Dictionaries) zentrale Datenstrukturen, die Schlüssel-Wert-Paare speichern.
- Sie werden genutzt, um strukturierte, flexible und dynamisch erweiterbare Daten abzubilden.

## Typische Einsatzzwecke im Media Web Viewer
- **Konfigurationsdaten:**
  - Einstellungen für Parser, UI, Build-System etc. werden oft als dict gespeichert und verarbeitet.
- **Metadaten:**
  - Medien-Metadaten (z.B. aus Tag-Scannern, Parsern) werden als dicts zwischen Backend, Datenbank und UI übergeben.
- **Datenbank-Objekte:**
  - Zeilen aus der SQLite-Datenbank werden häufig als dicts geladen und weiterverarbeitet.
- **API-Kommunikation:**
  - Backend-APIs liefern und empfangen JSON-Objekte, die intern als dicts gehandhabt werden.
- **Testdaten und Mocks:**
  - Testfälle und Mock-Objekte nutzen dicts für flexible Testdatenstrukturen.

## Vorteile von dicts
- Schneller Zugriff auf Werte über Schlüssel
- Flexible Erweiterbarkeit (dynamisch neue Felder)
- Einfache Serialisierung (z.B. zu JSON)
- Gut geeignet für dynamische, schemalose Daten

## Beispiel
```python
media_info = {
    "title": "Songname",
    "artist": "Interpret",
    "duration": 215,
    "format": "mp3",
    "tags": {"genre": "Rock", "year": 2020}
}
```

## Hinweise
- Für komplexere, validierte Datenstrukturen werden im Projekt auch Klassen (z.B. MediaItem) verwendet.
- Dicts sind besonders nützlich für lose strukturierte Daten und schnelle Prototypen.

---

**Siehe auch:**
- Python-Dokumentation: https://docs.python.org/3/library/stdtypes.html#dict
- Projektdateien: models.py, parsers/, tests/
