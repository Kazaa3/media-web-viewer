# Logbuch – Wiederherstellung der Media Queue Renderer

## Datum
30. März 2026

## Problemstellung
Nach der Modularisierung der Media Viewer Anwendung wurden im "Player"- und "Video"-Tab keine Queue-Items mehr angezeigt. Die UI-Fragmente wurden zwar geladen, aber die Render-Logik funktionierte nicht mehr korrekt.

### Ursachenanalyse
- **Fehlende Funktion:** Die Funktion `renderVideoQueue()` in video.js ging beim Refactoring verloren.
- **ID-Mismatch:** Die Funktion `renderPlaylist()` in audioplayer.js zielte auf das äußere Container-Element (`player-queue-pane`), wodurch beim Leeren der Queue die gesamte Struktur entfernt wurde. Die Ziel-IDs stimmten nicht mehr mit der neuen Fragmentstruktur überein.

## Lösung/Umgesetzte Änderungen
- **audioplayer.js:**
  - Das `containers`-Array in `renderPlaylist()` wurde angepasst, sodass jetzt gezielt `active-queue-list-render-target` (Player-Tab) und `json-serialized-sequence-item-container` (Playlist-Tab) angesprochen werden.
  - Die Render-Logik wurde so angepasst, dass keine Strukturelemente mehr versehentlich entfernt werden.
- **player_queue.html:**
  - Die IDs der Strukturelemente wurden an die Erwartungen der JS-Renderer angepasst.
- **video.js:**
  - Die Funktion `renderVideoQueue()` wurde neu implementiert bzw. wiederhergestellt. Sie rendert die Video-Queue gezielt in das Element mit der ID `video-queue-pane`.

## Verifikation
- **Audio:** Im "Player"-Tab werden wieder die Queue-Items oder die Leermeldung korrekt angezeigt.
- **Video:** Im "Video"-Tab werden analysierte Video-Items wieder korrekt gelistet.
- **Playlist:** Die Playlist-Ansicht funktioniert weiterhin mit der gemeinsamen Renderfunktion.

## Status
Die Media Queue Renderer sind wieder voll funktionsfähig und an die fragmentbasierte Architektur angepasst.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
