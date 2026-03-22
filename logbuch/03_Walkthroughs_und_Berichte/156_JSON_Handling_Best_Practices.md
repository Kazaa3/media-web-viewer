# JSON Handling – Best Practices und Beispiele

## Übersicht
JSON (JavaScript Object Notation) ist ein weit verbreitetes Format für den Datenaustausch zwischen Anwendungen. In Python wird das Modul `json` für das Parsen, Serialisieren und Validieren von JSON-Daten verwendet.

## Typische Anwendungsfälle
- Konfigurationsdateien
- API-Kommunikation (z.B. REST)
- Speicherung von Datenstrukturen
- Austausch zwischen Frontend und Backend

## Beispielcode
```python
import json

# JSON-String zu Python-Dict
json_str = '{"name": "Alice", "age": 30}'
data = json.loads(json_str)

# Python-Dict zu JSON-String
json_out = json.dumps(data, indent=2)

# Datei lesen/schreiben
with open('data.json', 'r') as f:
    data = json.load(f)

with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## Best Practices
- Immer Fehlerbehandlung nutzen (`try/except` für `json.JSONDecodeError`).
- Für große Dateien: Streaming oder `ijson` verwenden.
- Validierung mit `jsonschema` möglich.
- UTF-8 als Standard-Encoding.
- Bei API-Tests: Response mit `response.json()` direkt parsen.

## Integration in Media Web Viewer
- JSON wird für Konfiguration, API-Antworten und Metadaten genutzt.
- Typische Dateien: `VERSION_SYNC.json`, Konfigurationsdateien im Projekt.
- Für Tests: Mocking von JSON-Daten und Response-Objekten.

## Fortgeschrittene Beispiele
### Fehlerbehandlung
```python
import json

try:
    data = json.loads('{bad json}')
except json.JSONDecodeError as e:
    print(f"Fehler: {e}")
```

### Validierung mit jsonschema
```python
import jsonschema
schema = {"type": "object", "properties": {"name": {"type": "string"}}}
data = {"name": "Alice"}
jsonschema.validate(instance=data, schema=schema)
```

---
**Weitere Ressourcen:**
- [Python json-Dokumentation](https://docs.python.org/3/library/json.html)
- [jsonschema-Dokumentation](https://python-jsonschema.readthedocs.io/)
