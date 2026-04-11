# Logbuch: Parser-Stalling – Ursachen & Fixes

## Problem
Beim Media Web Viewer kommt es gelegentlich zu "Stalling" (Hängenbleiben) im Parser, besonders bei großen oder fehlerhaften Dateien. Das kann die UI blockieren und die Batch-Verarbeitung verzögern.

## Ursachen
- Zu große Dateien oder langsame Streams
- Fehlerhafte oder inkompatible Formate
- Parser wartet auf externe Tools (ffprobe, mutagen, pymediainfo)
- Kein Timeout oder Fallback implementiert
- Fehlerhafte Exception-Handling-Logik

## Fixes & Best Practices
- **Timeouts einbauen:** Jeder Parser-Aufruf sollte ein Timeout haben (z.B. 10s)
- **Fallback-Logik:** Bei Timeout oder Fehler auf einen anderen Parser oder Minimal-Metadaten zurückgreifen
- **Async/Threading:** Parser in eigenen Threads oder async ausführen, UI nicht blockieren
- **Logging:** Stalling-Fälle im Logbuch dokumentieren, Fehlerbilder sammeln
- **Test-Suite:** Stalling gezielt testen (große, fehlerhafte Dateien)

## Beispiel (Python)
```python
import concurrent.futures

def safe_parse(file):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(parse_metadata, file)
        try:
            return future.result(timeout=10)
        except concurrent.futures.TimeoutError:
            log('Stalling/Timeout beim Parsen:', file)
            return minimal_metadata(file)
```

## Status
- Timeout- und Fallback-Logik ergänzen
- Async/Threading für Parser
- Stalling-Fälle im Logbuch dokumentieren


Letzte Aktualisierung: 11. März 2026
