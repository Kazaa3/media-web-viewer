# Test-Suite Backend: Fehler-Meldung für Spezialfälle

## Ziel
Die Backend-Test-Suite prüft die Robustheit und Fehlerbehandlung der Parser-Pipeline und API-Wrapper. Spezialfälle (z.B. Import-/Attributfehler bei ebml, mkvparse, pycdlib, music_tag) werden erkannt und gemeldet, bleiben aber zunächst unbehandelt.

## Vorgehen
- **Standardfälle:** Erfolgreiche Verarbeitung und Metadaten-Extraktion werden getestet.
- **Spezialfälle:**
  - Nicht unterstützte Dateitypen, Verzeichnisse, fehlerhafte Formate
  - Import-/Attributfehler bei Spezialparsern
  - Fehler werden im Test-Log und als Meldung ausgegeben
- **Meldung:**
  - Fehler werden als JSON `{ "error": "..." }` zurückgegeben
  - Im Logbuch und Test-Log werden sie als "Spezialfall unbehandelt" markiert

## Beispiel-Testfall
```python
def test_special_parser_error():
    path = "/path/to/specialfile"
    result = process_any_file(path)
    assert "error" in result
    print("Spezialparser-Fehler erkannt und gemeldet:", result)
```

## Status
- Spezialparser-Fehler werden erkannt und gemeldet
- Behandlung erfolgt später (z.B. durch try/except oder eigene Checks)
- Test-Suite dokumentiert alle Spezialfälle im Logbuch

---
Letzte Aktualisierung: 11. März 2026
