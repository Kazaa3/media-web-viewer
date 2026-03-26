# Logbuch: Modular Heart – Handler-Pattern Optimization

**Datum:** 25. März 2026

## Zusammenfassung
Die Optimierung des "Handler-Pattern" wurde erfolgreich abgeschlossen. Die monolithische Komplexität von `main.py` wurde signifikant reduziert, indem die Media-Routing- und Metadaten-Orchestrierungslogik in spezialisierte Klassen ausgelagert wurde.

## Was wurde geändert?
- **Base MediaHandler:**
  - Erstellt: `src/core/handlers/media_handler.py` als einheitliches Interface für die Verarbeitung von Media-Requests.
- **Spezialisierte Handler:**
  - Erstellt: `audio_handler.py` und `video_handler.py`.
  - Kapseln die spezifische Logik für verschiedene Formate, z.B. VLC-Fallback, Direct-Streaming-Erkennung und ISO/DVD-Erkennung für Videoformate.
- **MetadataPipeline:**
  - Extrahiert: Orchestrator-Logik in `metadata_pipeline.py`.
- **main.py Refactoring:**
  - Fast 100 Zeilen komplexer if/elif-Logik in `get_play_source` und `analyze_media` entfernt.
  - Ersetzt durch moderne, saubere Delegation an die neuen Handler via Factory-Methode.

## Code Preview
Neuer Routing-Endpunkt in `main.py`:
```python
@eel.expose
def get_play_source(item_path: str, client: str = 'browser'):
    # ...
    handler = get_handler_for_file(full)
    return handler.process(client=client, relpath=item_path)
```

## Validierungsergebnisse
- Backend kompiliert und startet erfolgreich mit der neuen Konfiguration – keine Circular Imports oder Syntaxfehler nach der Extraktion.
- Die neue Routing-Logik entspricht funktional der Legacy-Logik (inkl. FFprobe-Checks).
