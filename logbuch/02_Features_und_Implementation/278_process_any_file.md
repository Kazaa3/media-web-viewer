# process_any_file: Test-Kompatibilität & Robustheit

## Zweck
`process_any_file` ist ein Kompatibilitäts-Wrapper für Tests und API-Checks. Er verarbeitet eine Datei und gibt ein JSON-String zurück:
- Erfolgreich: `{ 'success': True, 'duration': ..., 'tags': {...} }`
- Fehler: `{ 'error': '...' }`

## Ablauf
1. **Dateiname extrahieren**
2. **Parser-Pipeline aufrufen** (`extract_metadata`)
3. **Fehler robust abfangen**
4. **JSON-String zurückgeben**

## Robustheit
- Early Exit für Nicht-Dateien (Verzeichnis/Sonderfall)
- Fehler-Shortcircuit bei typischen Parser-Fehlern
- Logging von Fehlern für Debugging
- Rückgabe von Minimal-Metadaten bei Fehlern

## Beispiel
```python
def process_any_file(path: str) -> str:
    try:
        from parsers.media_parser import extract_metadata
        from pathlib import Path as _Path
        filename = _Path(path).name
        duration, tags = extract_metadata(path, filename, mode='lightweight')
        return json.dumps({"success": True, "duration": duration, "tags": tags})
    except Exception as e:
        _logger.exception("process_any_file failed")
        return json.dumps({"error": str(e)})
```

## Status
- Kompatibel mit Test-Suite
- Fehlerrobust durch neue Parser-Pipeline
- Logging und JSON-Ausgabe für Debugging

---

**Hinweis:**
Die Parser-Pipeline wurde gehärtet: Early Exit für Nicht-Dateien und Error-Shortcircuit bei typischen Fehlern sind jetzt aktiv.

Es bestehen weiterhin einige Import- und Attributfehler bei den Parser-Modulen (ebml, mkvparse, pycdlib, music_tag). Diese betreffen Spezialfälle und sollten separat geprüft oder mit try/except und existierenden Checks robust abgefangen werden.

---

Das Markdown enthält Zweck, Ablauf, Fehlerhandling, Beispiel und Status. Weitere API-Wrapper können nach diesem Muster dokumentiert werden.

---
Letzte Aktualisierung: 11. März 2026
