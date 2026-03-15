# Beschreibung: JSONs im Projekt

## Was sind JSONs?
- JSON (JavaScript Object Notation) ist ein textbasiertes, plattformunabhängiges Datenformat zur Speicherung und zum Austausch strukturierter Daten.
- In Python werden dicts, list of dicts und dict of dicts häufig zu/von JSON serialisiert (mit `json.dumps()` und `json.loads()`).

## Typische Einsatzzwecke im Media Web Viewer
- **API-Kommunikation:**
  - Backend-APIs liefern und empfangen Daten als JSON (z.B. Media-Listen, Metadaten, Statusmeldungen)
- **Datenbank:**
  - Komplexe Felder wie `tags` oder `full_tags` werden als JSON-Strings in der SQLite-DB gespeichert
- **Test- und Artefakt-Reports:**
  - Ergebnisse von Performance- oder Integrationstests werden als JSON-Dateien abgelegt (z.B. `performance_audit_results.json`)
- **Konfigurationsdateien:**
  - (Optional) Einstellungen oder Mappings können als JSON gespeichert werden

## Vorteile
- Plattform- und sprachübergreifend
- Leicht lesbar und editierbar
- Standardformat für Web-APIs und viele Tools

## Beispiel
```python
import json
item = {"name": "Song1", "tags": {"genre": "Rock"}}
json_str = json.dumps(item)  # Serialisierung zu JSON
item2 = json.loads(json_str)  # Deserialisierung zurück zu dict
```

## Hinweise
- JSON ist das Standardformat für den Austausch zwischen Backend und Frontend
- Beim Speichern in der DB werden dicts mit `json.dumps()` serialisiert, beim Laden mit `json.loads()` zurückgewandelt
- Für große oder komplexe Daten empfiehlt sich ggf. eine Validierung (z.B. mit JSON Schema)

---

**Siehe auch:**
- Logbuch: item dict, list of dicts, dict of dicts
- src/core/db.py, API, tests/artifacts/
- https://www.json.org/
