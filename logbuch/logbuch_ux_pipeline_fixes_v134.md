# Logbuch: Media Viewer v1.34 – UX & Pipeline Fixes

## Zusammenfassung der Änderungen

### 1. UI Renaming & Navigation
- "Player" im app.html-Header zu "Audio-Player" umbenannt
- "Playlist"-Tab im Header ergänzt (Kategorie playlist)
- Alle "Warteschlange"-Buttons/Überschriften in player_queue.html zu "Queue" geändert
- subNavMap['media'] in ui_nav_helpers.js auf "Queue" aktualisiert

### 2. Media Playback & Transcoding
- On-the-fly-Transcoding für ALAC, WAV24 und OGG in main.py implementiert (FFmpeg-Pipe)
- WAV24/PCM-Sample-Header für Browser-Kompatibilität gefixt
- Transcoding-Funktionalität mit FFmpeg getestet

### 3. Player Visuals
- playAudio(item) in audioplayer.js aktualisiert: Alle .synced-artwork-Elemente werden synchronisiert
- Footer-Artwork bleibt immer im Sync mit dem aktuellen Track

### 4. Context Menu Enhancement
- showContextMenu in common_helpers.js prüft jetzt isVideoItem(item)
- Menüoptionen:
  - Audio: "Zur Queue hinzufügen", "Metadaten bearbeiten"
  - Video: "Im Video Player abspielen", "Datei löschen", "Analysieren"

### 5. Audiobook Chapters & Sidebar
- player-chapters-list-Container in player_queue.html (linke Spalte) ergänzt
- renderAudiobookDetails(item) in audioplayer.js implementiert: Kapitel-/Trackliste mit Klick-zum-Abspielen

### 6. Verification
- ALAC, WAV24 und OGG-Playback mit tests/ui/playback_ erfolgreich getestet

---

**Status:**
- Alle geplanten UX- und Pipeline-Fixes umgesetzt und getestet.
- Medienwiedergabe und Navigation sind jetzt robust und benutzerfreundlich.
