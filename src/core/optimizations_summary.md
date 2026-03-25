# Modular Heart: Handler-Pattern & UI Optimizations

**Datum:** 25. März 2026

## Handler-Pattern Refactoring
- **Base MediaHandler:**
  - Erstellt: `src/core/handlers/media_handler.py` als einheitliches Interface für Media-Requests.
- **Spezialisierte Handler:**
  - Erstellt: `audio_handler.py` und `video_handler.py` für format-spezifische Logik (z.B. VLC-Fallback, Direct-Streaming, ISO/DVD-Erkennung).
- **MetadataPipeline:**
  - Orchestrator-Logik ausgelagert in `metadata_pipeline.py`.
- **main.py Refactoring:**
  - Fast 100 Zeilen komplexer if/elif-Logik in `get_play_source` und `analyze_media` entfernt und durch saubere Delegation an Handler ersetzt.

**Code Preview:**
```python
@eel.expose
def get_play_source(item_path: str, client: str = 'browser'):
    # ...
    handler = get_handler_for_file(full)
    return handler.process(client=client, relpath=item_path)
```

**Validierung:**
- Backend kompiliert und startet fehlerfrei (keine Circular Imports/Syntaxfehler).
- Routing-Logik entspricht funktional der Legacy-Implementierung (inkl. FFprobe-Checks).

---

## Logbuch Management Optimization
- **Backend Path Unification (`src/core/main.py`):**
  - Speichern/Löschen von Logbuch-Einträgen erfolgt jetzt konsistent im `logbuch`-Verzeichnis.
- **Frontend DOM Caching (`web/app.html`):**
  - `loadLogbuchTab` hält einen lokalen Cache (`currentLogbuchEntries`). Tab-Wechsel rendert synchron aus dem Speicher, keine unnötigen API-Calls.
- **Manual/Automatic Cache Bypass (`web/app.html`):**
  - 'Sync'-Button sowie 'Save'/'Delete' triggern ein forceRefresh und invalidieren den Cache gezielt.

---

## Video Player UI Fixes (MP4 Layout)
- **Video.js Initialization Mode (`web/app.html`):**
  - fluid: true → fill: true, damit der Player die CSS-Grenzen (16:9) korrekt ausfüllt.
- **Visibility Inheritance Bug (`web/app.html`):**
  - visibility: hidden; aus dem <video>-Tag entfernt, damit das Video korrekt angezeigt wird.

---

Alle Optimierungen wurden erfolgreich implementiert und getestet. Weitere Wünsche oder Feedback gerne melden!