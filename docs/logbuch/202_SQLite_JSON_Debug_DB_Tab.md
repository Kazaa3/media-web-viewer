# SQLite-Datenbank & JSON-Dict für Debug/DB-Tab

## Ziel
Stelle die SQLite-Datenbank und Metadaten als JSON-Dict im Debug- und DB-Tab deiner Media-Library-App bereit – oben links bis mittig, ohne andere Objekte zu blockieren.

## API-Funktionen (main.py)
- `get_environment_info_dict`: Liefert Umgebungsinfos als Dict
- `get_debug_console`: Liefert Logs, Env, Version, Debug-Flags als Dict
- `get_db_stats`: Liefert DB-Statistiken als Dict
- **Neu:** `get_db_json_dict`: Liefert vollständigen DB-Inhalt als JSON-Dict (non-blocking)

### Beispiel (Python, main.py)
```python
@eel.expose
def get_db_json_dict():
    """
    Returns the full database content as a JSON dict for debug/db tab display.
    Non-blocking: returns only dict, no objects.
    """
    import db
    return db.get_db_as_dict()  # db.py: Funktion liefert alle Media-Items als Dict/JSON
```

## Integration im Frontend
- JS ruft `eel.get_db_json_dict()` auf
- Zeigt JSON-Daten im Debug/DB-Tab (z.B. als Table, Tree oder Raw-JSON)
- Position: oben links bis mittig, ohne andere UI-Objekte zu blockieren

### Beispiel (JS)
```javascript
async function showDbJson() {
    const dbData = await eel.get_db_json_dict()();
    // Render als Table/Tree/JSON im Debug/DB-Tab
}
```

## Vorteile
- Non-blocking: Nur Dict/JSON, keine Python-Objekte
- Schnell, auch bei großen DBs
- Perfekt für Debugging, DB-Analyse, Export

---
*Letzte Aktualisierung: 10. März 2026*
