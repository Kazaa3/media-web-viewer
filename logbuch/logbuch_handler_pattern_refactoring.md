# Logbuch: Handler-Pattern Refactoring Plan

**Datum:** 25. März 2026

## Ziel
Die Komplexität und Größe von `main.py` (aktuell über 7.300 Zeilen) wird drastisch reduziert, indem die Media-Logik in spezialisierte Handler-Klassen ausgelagert wird. Dies folgt dem Modular Heart Handler-Pattern, wie im Logbuch-Eintrag beschrieben.

## Wichtige Entscheidung
**User Review erforderlich:**  
Bevor die massive Refaktorisierung startet, bitte bestätigen, ob die Extraktion in folgende neue Module erfolgen soll:
- `media_handler.py`
- `audio_handler.py`
- `video_handler.py`
- `metadata_pipeline.py`

**Frage:**  
Sollen bestimmte Funktionen (z.B. `play_media`, UI-Endpunkte, File-Scan-Routen) zuerst extrahiert werden?

## Vorgeschlagene Änderungen

### Core Handlers
- **[NEU] src/core/handlers/media_handler.py**  
  Basisklasse `MediaHandler` mit Interface für Request-Processing, Metadaten-Parsing und Playback-URL-Vorbereitung.
- **[NEU] src/core/handlers/audio_handler.py**  
  Subklasse für Audioformate (.mp3, .flac, etc.), inkl. Album-Art-Extraktion und Audio-Normalisierung.
- **[NEU] src/core/handlers/video_handler.py**  
  Subklasse für Videoformate (.mp4, .mkv, etc.), inkl. VLC-Fallback und FFmpeg-Streaming.
- **[NEU] src/core/handlers/metadata_pipeline.py**  
  Orchestrator, der die bestehenden Parser (mutagen_parser, ffmpeg_parser, etc.) als Pipeline für die Handler bereitstellt.

### Refactoring main.py
- Entfernen der großen Routing-/Parsing-Blöcke für Media-Dateien.
- Ersetzen durch saubere Delegation an die neuen Handler:
  ```python
  handler = get_handler_for_file(filepath)
  return handler.process()
  ```
- `main.py` bleibt fokussiert auf Bottle-Routing, Eel-Setup und Websocket-Lifecycle.

## Verifikationsplan

### Automatisierte Tests
- Bestehende pytest-Suiten (insb. `test_selenium_session.py` und Unit-Tests in `tests/`) laufen lassen, um sicherzustellen, dass die Endpunkte nach der Extraktion das gleiche JSON-Format liefern.
- Sicherstellen, dass die Selenium-Tests für Audio- und Videowiedergabe weiterhin bestehen.

### Manuelle Verifikation
- Anwendung starten (`run.sh`).
- Prüfen, ob das Abspielen einer MP3 im Browser funktioniert.
- Prüfen, ob MKV korrekt zu MP4 oder VLC-Fallback geroutet wird.
