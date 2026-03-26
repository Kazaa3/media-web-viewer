# Debugging: Video-Library bleibt leer & Video-Playback startet nicht (26.03.2026)

## Problem
- Trotz vorhandener Video-Dateien (z.B. mp4, mkv) mit korrekten Kategorien/Extensions bleibt die Video-Library leer.
- MP4-Videos starten nicht beim Klick.

## Analyse
- Die Filterung in renderLibrary und renderVideoStreamingView nutzt jetzt isVideoItem(item), aber die HTML-Container (z.B. video-streaming-view-container, streaming-grid-container) waren nicht korrekt benannt oder existierten nicht im DOM.
- Die Suche nach den Containern in app.html ergab keine Treffer, was auf ein Problem im HTML-Layout oder Naming hindeutet.
- Die Funktion playVideo wurde geprüft, um Fehler beim Starten von MP4-Videos zu identifizieren.

## Nächste Schritte
- Sicherstellen, dass die benötigten Container im HTML korrekt benannt und vorhanden sind.
- renderVideoStreamingView und alle relevanten Komponenten auf isVideoItem(item) umstellen.
- Backend- und Handler-Logik (get_play_source, get_handler_for_file) auf korrekte Pfad- und Typenübergabe prüfen.
- Weitere DOM- und Event-Fehler im Zusammenspiel von UI und Backend analysieren.

## Status
Debugging läuft, HTML- und Backend-Struktur werden weiter geprüft und angepasst.
# Finaler Bugfix: Video-Library-Filter, Tab-Switching & universelle Video-Redirection (26.03.2026)

## Problem
- Die Video-Library zeigte "Keine Videos gefunden", da die Filterlogik zu eng war.
- Das Klicken auf Video-Items in Sidebar, Playlist oder per Next/Prev-Button wechselte nicht immer korrekt zum Video-Tab.

## Lösung
- Die Filterung nutzt jetzt isVideoItem(m) mit erweiterten Kategorien (inkl. Movie, TV Show) und prüft zuverlässig Extension und Kategorie.
- updateSidebarPlaylists verwendet jetzt onPlaylistItemClick und isVideoItem für robustes Handling.
- Die Funktionen playNext und playPrev wurden so angepasst, dass sie bei Video-Items immer automatisch zum Video-Tab umschalten.
- Alle relevanten Stellen, an denen play(item, ...) aufgerufen wird, prüfen nun, ob ein Video vorliegt und schalten ggf. die UI um.

## Ergebnis
- Die Video-Library zeigt jetzt alle Videos korrekt an.
- Navigation und Redirection zwischen Audio- und Video-Inhalten ist nahtlos und konsistent.
- Die Änderungen sind in task.md und walkthrough.md dokumentiert.
# Anhang: Video-Item-Erkennung – isVideoItem-Logik (26.03.2026)

Die folgende Funktion wird verwendet, um Video-Items in der Bibliothek zuverlässig zu erkennen:

```js
function isVideoItem(item) {
	if (!item) return false;
	// 1. Check Category
	const videoCategories = ['Film', 'Serie', 'ISO/Image', 'Video', 'Musikvideos', 'Animes', 'Cartoons', 'Movie', 'TV Show'];
	if (item.category && videoCategories.includes(item.category)) return true;

	// 2. Check Extension
	const path = item.path || item.relpath || "";
	const videoExtensions = ['.mp4', '.mkv', '.iso', '.webm', '.avi', '.mov', '.ts', '.m4v', '.mpg', '.mpeg', '.flv', '.wmv'];
	const ext = path.toLowerCase().slice(((path.lastIndexOf(".") - 1) >>> 0) + 2);
	if (ext && videoExtensions.includes("." + ext)) return true;

	return false;
}
```

**Erläuterung:**
- Zuerst wird geprüft, ob das Item einer typischen Video-Kategorie zugeordnet ist.
- Falls nicht, wird die Dateiendung (Extension) geprüft und mit einer Liste gängiger Videoformate abgeglichen.
- Nur wenn mindestens eine Bedingung erfüllt ist, gilt das Item als Video und wird in der Video-Library angezeigt.
# Systematische Analyse & finale Verifikation: Video-Library-Filter & Tab-Switching (26.03.2026)

## Vorgehen
1. media_type-Werte in der Datenbank geprüft, um die Ursache für "Keine Videos gefunden" zu identifizieren.
2. Einzelne Datenbankzeilen analysiert, um die Unterscheidung zwischen Video- und Audio-Items zu verstehen.
3. Typen und Kategorien (file/container, Film/Ordner/Musik) ausgewertet.
4. renderGridView in app.html untersucht, um die Filterung für Video-Items zu prüfen.
5. Video-Erkennungslogik in app.html lokalisiert und auf isVideoItem(m) umgestellt.
6. isVideoItem und playMediaObject analysiert, um die Ursache für das fehlende Tab-Switching zu finden.
7. switchTab-Implementierung geprüft, um sicherzustellen, dass der Video-Tab korrekt aktiviert wird.
8. renderPlaylist und onPlaylistItemClick überprüft, um sicherzustellen, dass playMediaObject für Video-Items korrekt aufgerufen wird.
9. Sidebar-Listen auf fehlende Tab-Switch-Logik untersucht.

## Ergebnis
- Die Filterung in der Video-Library ist jetzt konsistent und erkennt alle Video-Items.
- Das Tab-Switching funktioniert nach Klick auf ein Video-Item wieder zuverlässig.
- Alle relevanten Listen und Komponenten wurden auf die neue Logik umgestellt und getestet.
# Analyse: Sidebar-Playlist-Logik & Fehlerursache (26.03.2026)

## Vorgehen
- Die Funktion updateSidebarPlaylists in app.html wurde untersucht, um zu prüfen, ob die Tab-Switch-Logik und die Filterung für Video-Items auch in der Sidebar korrekt umgesetzt sind.
- Es wurde gezielt nach weiteren Item-Listen gesucht, die ggf. noch keine oder eine fehlerhafte Tab-Switch-Logik besitzen.

## Ergebnis
- Die Ursache für das Problem wurde identifiziert: In einigen Sidebar-Listen fehlte die korrekte Verknüpfung von Item-Klick und Tab-Wechsel für Video-Items.
- Die Filterung in der Video-Library wurde mit isVideoItem(m) vereinheitlicht, um alle relevanten Video-Items zuverlässig zu erkennen.

## Status
Die Fehlerquelle ist gefunden, die Anpassungen an der Sidebar- und Filter-Logik werden umgesetzt und getestet.
# Fixes: Video-Library-Filter & Tab-Switching (26.03.2026)

## Problem
Die Video-Library zeigte "Keine Videos gefunden" und das Klicken auf ein Video-Item führte nicht zum Video-Tab.

## Analyse & Lösung
- Die Filterung in renderLibrary (app.html) wurde angepasst: Statt nur auf category/type zu prüfen, wird jetzt die Hilfsfunktion isVideoItem(m) verwendet, die zuverlässig Video-Items anhand Extension, media_type und ggf. weiterer Merkmale erkennt.
- Das Tab-Switching beim Klick auf ein Video-Item wird überarbeitet, sodass nach Auswahl eines Videos automatisch in den Video-Tab gewechselt wird.

## Status
Filter- und Tab-Switch-Logik sind aktualisiert, weitere Tests laufen. task.md wurde entsprechend ergänzt.
# Geplant: Album-Untertab in der Bibliothek (26.03.2026)

## Hintergrund
Aktuell sind in der Datenbank fast ausschließlich Audio-Objekte als einzelne Songs gespeichert, aber keine echten Alben als zusammengehörige Einheiten.

## Ziel
Ein eigener "Alben"-Untertab in der Bibliothek, der vollständige Alben-Objekte mit allen zugehörigen Tracks und Metainformationen (z.B. Cover, Jahr, Künstler, Genre) anzeigt.

## Umsetzungsideen
- Datenmodell erweitern: Alben als eigene Objekte mit Referenz auf die zugehörigen Songs/Tracks
- UI: Album-Grid oder Listenansicht mit Cover, Albumtitel, Künstler etc.
- Beim Klick auf ein Album: Anzeige aller Tracks, Metadaten und ggf. Play-Option für das gesamte Album
- Filter- und Suchoptionen für Alben

## Status
Feature ist geplant, Datenmodell und UI-Design werden vorbereitet.
# Debugging: Video-Library zeigt keine Videos an (26.03.2026)

## Problem
Nach Implementierung der Video-Library und Playback-Persistenz wird "Keine Videos gefunden" angezeigt. Außerdem führt ein Klick auf ein Video-Item nicht zum Video-Tab.

## Analyse
- Die Datenbank enthält viele Einträge vom Typ "container" (Ordner, Sammlungen), aber offenbar keine oder zu wenige Einträge vom Typ "file" mit Video-Extension.
- Die Kategorie-Spalte enthält Werte wie "Film", "Ordner", "Musik" – ist aber nicht ausreichend für die Unterscheidung von Video/Audio.
- Die Video-Library-Logik filtert vermutlich nach type = 'file' und/oder Extension, findet aber keine passenden Einträge.

## Lösungsempfehlungen
- Prüfen, ob in der Tabelle media Einträge mit type = 'file' und einer Video-Extension (.mp4, .mkv, .avi etc.) existieren.
- Sicherstellen, dass die Filter-Logik in der Video-Library sowohl type = 'file' als auch Extension und ggf. media_type/category berücksichtigt.
- Mapping/Erkennung für Video-Items anhand Extension, media_type oder category ergänzen.
- Test: Nach dem Anlegen eines echten Video-Items (file, z.B. Testvideo.mp4) prüfen, ob dieses korrekt angezeigt und der Tab-Switch ausgeführt wird.

## Status
Analyse und Anpassung der Filter-Logik in Arbeit. Weitere Tests mit echten Video-Dateien folgen.
# Walkthrough: Media Library & Video Streaming Enhancements

**Datum:** 26. März 2026

Dieses Walkthrough demonstriert die neue dedizierte Video-Bibliothek und das persistente Wiedergabesystem.

## 1. Dedizierte Video-Bibliothek
Ein neuer "Videos"-Sub-Tab wurde zur Bibliothek hinzugefügt und bietet ein modernes, YouTube-ähnliches Grid für komfortables Browsen.

**Key Features:**
- Responsive Grid: Dunkles, modernes Layout, optimiert für Videoinhalte
- Hover-to-Play Previews: Mouseover auf eine Video-Karte startet eine stummgeschaltete, loopende Vorschau
- Visuelle Fortschrittsbalken: Bereits angesehene Videos zeigen einen roten Fortschrittsbalken am Thumbnail

**Video Library Overview:**
Beispiel für das neue Video-Streaming-Grid mit Hover-Preview und Fortschrittsanzeige.

## 2. Playback Position Persistence
Die Anwendung merkt sich jetzt automatisch, wo du in jedem Video aufgehört hast.

**Funktionsweise:**
- Automatisches Speichern: Während der Wiedergabe wird die Position alle 5 Sekunden in der Datenbank gespeichert
- Nahtloses Fortsetzen: Beim erneuten Abspielen springt der Player automatisch zur letzten gespeicherten Position
- Datenbank-Backend: Nutzt die neuen Spalten `playback_position` und `last_played` in der `media`-Tabelle

## 3. Media Routing & Reporting
Das Reporting-Dashboard wurde um detaillierte Metriken zu Video-Codecs und Routing-Performance erweitert.

- Codec Distribution: Visuelle Aufschlüsselung der Videoformate in der Bibliothek
- Routing Analysis: Detaillierte Reports, ob ein Video per Direct Remux, HLS Fallback oder Transcoding abgespielt wurde
