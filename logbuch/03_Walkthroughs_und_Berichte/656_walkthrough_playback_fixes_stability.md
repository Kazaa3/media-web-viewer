# Walkthrough: Playback Fixes & Stability Improvements (März 2026)

## Zusammenfassung
Die gemeldeten Wiedergabeprobleme wurden behoben. Die Stabilität der VLC-Pipes, die MP4-Wiedergabe und das Kontextmenü wurden gezielt verbessert. Die Media-Library-App bietet jetzt zuverlässige Wiedergabe für DVD-Ordner, ISOs und MP4-Dateien – inklusive intelligenter Kontextmenüs und ffplay-Integration.

---

## 1. VLC Pipe & Verzeichnis-Erkennung
- Fehlerhafte Flags (`--no-mjpeg-demux`) entfernt
- Automatische Fallbacks: Wenn mkvmerge fehlschlägt, wird ffmpeg als Pipe-Quelle genutzt
- Verzeichnisse (z.B. VIDEO_TS) werden korrekt erkannt und direkt via `dvd://` an VLC übergeben (kein Pipe-Fehler mehr)

## 2. MP4 Black Screen Fix
- In `app.html` wird nach Player-Initialisierung ein verzögerter Resize-Trigger ausgelöst
- Stellt sicher, dass Video.js den Player korrekt rendert und keine schwarzen Bildschirme mehr auftreten

## 3. FFplay-Integration
- ffplay als leichtgewichtige, standalone Alternative im Kontextmenü verfügbar
- Ideal für schnelle Tests und als Fallback bei komplexen Formaten

## 4. Intelligentes Kontextmenü
- Kontextmenü erkennt jetzt Verzeichnisse und "Film"-Kategorien
- Zeigt passende Optionen für DVD/ISO-Wiedergabe, ffplay, VLC etc. an

---

## Testempfehlung
- Wiedergabe von DVD-Ordnern (VIDEO_TS) und MP4-Dateien erneut testen
- Kontextmenü-Optionen für verschiedene Medientypen prüfen

---

## Weitere Verbesserungen
- Transcoding & Auto-Detection mit HW-Beschleunigung weiterhin integriert und produktiv

---

**Details siehe:** walkthrough.md (aktualisiert)

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
