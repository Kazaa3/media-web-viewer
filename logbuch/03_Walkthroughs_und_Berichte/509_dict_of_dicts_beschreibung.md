# Beschreibung: dict of dicts im Projekt

## Was ist ein dict of dicts?
- Ein "dict of dicts" ist ein verschachteltes Dictionary, bei dem die Werte selbst wieder Dictionaries sind.
- Struktur: `{key1: {subkey1: value, ...}, key2: {...}, ...}`

## Typische Einsatzzwecke im Media Web Viewer
- **Vollständige Metadaten (full_tags):**
  - Komplexe Metadaten zu einem Medium werden als dict of dicts gespeichert, z.B. für verschiedene Tag-Quellen oder Parser.
  - Beispiel:
    ```python
    full_tags = {
        "mutagen": {"genre": "Rock", "year": 2020},
        "ffprobe": {"bitrate": 320000, "channels": 2}
    }
    ```
- **Konfigurationsstrukturen:**
  - Einstellungen, die nach Kategorie oder Modul gruppiert sind (z.B. parser_config = {"audio": {...}, "video": {...}})
- **Datenbank (DB):**
  - Das Feld `full_tags` in der Tabelle `media` ist ein dict of dicts (wird als JSON gespeichert)

## Vorteile
- Klare Trennung und Gruppierung von Metadaten oder Einstellungen
- Ermöglicht das Speichern von Daten aus mehreren Quellen oder mit mehreren Ebenen
- Flexibel und erweiterbar

## Beispiel
```python
item = {
    "name": "Song1",
    "full_tags": {
        "mutagen": {"genre": "Rock", "year": 2020},
        "ffprobe": {"bitrate": 320000, "channels": 2}
    }
}
```

## Hinweise
- dict of dicts werden häufig zu/von JSON serialisiert (z.B. für DB, API, Reports)
- Für einfache Metadaten reicht oft ein einfaches dict; dict of dicts ist für komplexere, mehrdimensionale Daten gedacht

---

**Siehe auch:**
- Logbuch: item dict Beschreibung
- Logbuch: db.py IO Beschreibung
- src/core/db.py, parsers/, tests/
