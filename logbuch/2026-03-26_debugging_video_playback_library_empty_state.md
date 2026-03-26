# Task-Status: Media Library Expansion & Video Library (26.03.2026)

## Status
- Video Player Sichtbarkeit repariert (redundante Tags entfernt)
- Bug bei absoluter Pfadauflösung im /direct/-Route behoben
- get_routing_suite_report via Eel bereitgestellt
- Video Player Architektur im Logbuch dokumentiert
- Routing Test Suite erweitert
- Video Library & Persistence:
	- Backend: Spalten playback_position, last_played, duration_sec zur media-Tabelle hinzugefügt
	- Backend: Persistence-API in db.py implementiert
	- Backend: Persistence-API in main.py via Eel bereitgestellt
	- Debugging: Leere Video-Library (Streaming-Tab) analysiert und Filter-Logik in renderVideoStreamingView auf isVideoItem umgestellt
	- CATEGORY_MAP['video'] um weitere Kategorien ergänzt
	- Frontend: "Videos"-Sub-Tab in der Bibliothek ergänzt
	- Frontend: Video Streaming Grid mit Hover-Preview umgesetzt
	- Frontend: Video.js an Persistence-API angebunden (Progress speichern/laden)

## Verifikation & Final Polish
- End-to-End-Test der Persistence (Schema und Backend-Logik verifiziert)
- Debugging MP4-Playback: Fehlerursache war ein doppeltes media/-Präfix in serve_direct_media
- serve_direct_media Pfadauflösung korrigiert
- Universal Tab Switching für Videos umgesetzt
- onPlaylistItemClick für Sidebar/Playlists vereinheitlicht
- Walkthrough mit Video-Library-Demo aktualisiert
- Media-Duration-Sync für exakte Fortschrittsbalken

## Details: Video Streaming Library
- Dedizierter Sub-Tab in der Bibliothek
- YouTube-ähnliches Card-Layout mit Hover-to-Play-Vorschau
- Fortschrittsbalken auf Video-Karten für angefangene Inhalte
- Automatische Positionswiederherstellung beim Starten der Wiedergabe
- Dynamisches Duration-Syncing für stets akkurate Fortschrittsanzeigen

## Details: Media Routing Tests
- Validierung der direct-, transcode- und hls-Logik
- Funktionaler Test für alle wichtigen Streaming-Endpunkte
# Debugging: Video Playback & Library Empty State

**Datum:** 26. März 2026

## Problemstellung
- Die Video-Library bleibt leer, obwohl Videos mit passenden Kategorien/Extensions vorhanden sind.
- MP4-Videos starten nicht beim Klick, obwohl die Dateien existieren.

## Analyse
- Der Container streaming-grid-container ist im HTML vorhanden.
- In renderVideoStreamingView wurde fälschlicherweise mit `i.type === 'video'` gefiltert, was zu einer leeren Anzeige führte. Die Filterung muss auf isVideoItem(item) umgestellt werden.
- Die Funktion playVideo setzt für direct-Mode den Typ immer auf video/mp4, was bei anderen Formaten zu Problemen führen kann.
- Die Hilfsfunktionen is_direct_play_capable und is_chrome_native wurden geprüft.
- Die Berechnung von relpath im Media-Scanner wird untersucht, da sie Einfluss auf das Abspielen von MP4-Videos hat.
- startEmbeddedVideo in app.html wurde geprüft, insbesondere ob vjsPlayer.play() nach dem Setzen der Quelle aufgerufen wird.
- Die Route für statische Dateien (bottle.static_file) in main.py wurde analysiert.

## Nächste Schritte
- Filter in renderVideoStreamingView auf isVideoItem(item) umstellen.
- playVideo anpassen, sodass der Typ dynamisch anhand der Extension gesetzt wird.
- relpath-Berechnung im Media-Scanner prüfen und ggf. korrigieren.
- Sicherstellen, dass vjsPlayer.play() nach dem Setzen der Quelle aufgerufen wird.
- Weitere Tests und Debugging der Abspiel- und Routing-Logik.

## Status
Fehlerquellen identifiziert, Anpassungen an Filter- und Play-Logik werden umgesetzt und getestet. task.md und walkthrough.md werden fortlaufend aktualisiert.
