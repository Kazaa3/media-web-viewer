# Video Player Routing & UI Fixes (MP4)

**Datum:** 25. März 2026

## Problem
MP4-Dateien im Playlist-Queue wurden nicht korrekt als Videos erkannt und konnten nicht abgespielt werden, insbesondere wenn Metadaten wie `item.extension` oder `item.relpath` fehlten.

## Lösung
- **Robuste Video-Erkennung:**
  - Die Funktion `play()` in `web/app.html` prüft jetzt zusätzlich den Dateinamen oder die URL, falls `item.extension` fehlt, um Video-Dateien zuverlässig zu erkennen.
- **Pfad-Resolution Fallback:**
  - Die Funktion `playVideo()` verwendet nun als Fallback den übergebenen Mediapfad, falls `item.relpath` oder `item.path` nicht gesetzt sind.

## Ergebnis
- MP4-Dateien werden jetzt unabhängig von der Metadaten-Vollständigkeit korrekt an den Video-Player und das Backend geroutet.
- Die Video-Wiedergabe funktioniert sowohl aus der Queue als auch aus anderen Player-Views zuverlässig.

Weitere Details sind in der `walkthrough.md` dokumentiert.
