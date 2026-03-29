# JSONs im Code: Verwendung und Muster

## Laden von JSONs
- Mit `json.load()` werden JSON-Dateien in Python als dict geladen:
  ```python
  import json
  with open("web/config.json", "r") as f:
      config = json.load(f)
  # config ist jetzt ein dict
  ```
- Für Strings: `json.loads(json_str)`

## Speichern von JSONs
- Mit `json.dump()` wird ein dict als JSON-Datei gespeichert:
  ```python
  with open("output.json", "w") as f:
      json.dump(data, f, indent=2)
  ```
- Für Strings: `json.dumps(data)`

## Typische Muster im Projekt
- **Konfigurationsdateien:**
  - Werden beim Start geladen und als dict im Code verwendet (z.B. für Feature-Flags, Kategorien)
- **DB-Felder:**
  - Komplexe Felder wie `tags` oder `full_tags` werden mit `json.dumps()` serialisiert und mit `json.loads()` wieder als dict geladen
- **API-Responses:**
  - Daten werden als dict oder list of dicts vorbereitet und mit `json.dumps()` als JSON an das Frontend gesendet
- **Test- und Artefakt-Reports:**
  - Ergebnisse werden als dict/list of dicts erzeugt und als JSON-Datei gespeichert

## Beispiel: Serialisierung und Deserialisierung
```python
import json
item = {"name": "Song1", "tags": {"genre": "Rock"}}
# Speichern als JSON-String
json_str = json.dumps(item)
# Laden aus JSON-String
item2 = json.loads(json_str)
```

## Hinweise
- Immer doppelte Anführungszeichen in JSON!
- Für große Daten empfiehlt sich `indent=2` für bessere Lesbarkeit
- Fehler beim Laden/Speichern abfangen (`try/except`)

---

**Siehe auch:**
- Logbuch: JSONs Beschreibung, JSON-Konfigs, Serialisierung
- src/core/db.py, web/config.json, API, tests/
- https://docs.python.org/3/library/json.html
