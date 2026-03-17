# Logbuch: Video Player & Media Handling Overhaul (März 2026)

## Zusammenfassung
Umfassende Überarbeitung der Video-Player-Pipeline, der Medienerkennung und der UI zur Unterstützung von nativen Remux-Streams, verbesserter DVD-Bundle-Erkennung und einer zentralisierten Advanced-Tools-Oberfläche.

---

## 1. UI / Layout
- Alle "Advanced Tools"-Sektionen (HandBrake, WebM, VLC Stream, VLC Playlist) sind jetzt in einem gemeinsamen `#tools-tab`-Container mit `.tab-content`-Klasse gruppiert.
- Die Funktion `switchTab` wurde geprüft und stellt sicher, dass alle Komponenten des aktiven Tabs korrekt gerendert werden.
- Alle MediaItems in Sidebar und Bibliothek verfügen über aktive Play-Trigger.

## 2. Scanner & Models
- `scan_directories` erkennt jetzt "DVD Bundles": Ordner mit dem Muster `Title (Year)` und genau einer `.iso` werden als einzelnes Film-MediaItem behandelt.
- Verbesserte Logging-Ausgabe für VLC-Pipe-Operationen: stderr wird in einen dedizierten Logpuffer oder eine Datei geschrieben.

## 3. Playback & Streaming
- Neue Route `/video-remux-stream/<item_id>`:
    - Nutzt `mkvmerge` oder `ffmpeg -c copy` für On-the-fly-Remux nach Matroska.
    - Pipe-Ausgabe wird direkt an die HTTP-Response gestreamt (Chrome Native Playback).
- `open_video` unterstützt jetzt `mode="native-remux"` und verwendet die neue Streaming-Route.
- "Native Remux" wurde zur Player-Mode-Auswahl in der UI hinzugefügt.
- `playMedia` wurde angepasst, um die neue Streaming-Route zu unterstützen.

## 4. Verifikation & Tests
- Selenium-Tests in `tests/e2e/selenium/` wurden aktualisiert, um neue Player-Modes und Bundle-Erkennung zu prüfen.
- Unit-Test für die `/video-remux-stream`-Route hinzugefügt.
- Manuelle Verifikation:
    - DVD-Ordner `Title (Year)` mit `.iso` getestet (wird als Film erkannt und abgespielt).
    - "Advanced Tools"-Tab zeigt alle Inhalte korrekt an.
    - VLC-Logs während problematischer Playbacks geprüft.

---

## Fazit
- Die Advanced-Tools-Oberfläche ist jetzt konsistent und vollständig sichtbar.
- DVD-Bundles werden automatisch erkannt und als Filme behandelt.
- Chrome Native Remux-Streaming verbessert die Kompatibilität und reduziert VLC-Popups.
- Logging für Pipe-Fehler ist deutlich verbessert.

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
