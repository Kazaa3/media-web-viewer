# Implementation Plan – Media Viewer v1.34: UX Refinement & Pipeline Hardening

## Ziel
Behebung von UI-Regressions, Verbesserung der Datenpipeline für hochwertige Audioformate und smartere Kontextmenüs.

---

## Proposed Changes

### 1. UI Renaming & Navigation Refactoring
- **Ziel:**
  - "Player" → "Audio-Player"
  - "Warteschlange" → "Queue"
  - "Playlist" als Top-Level-Tab
- **Änderungen:**
  - **app.html:** Header-Button umbenennen, "Playlist"-Button ergänzen
  - **player_queue.html:** Sub-Tab-Buttons und Überschriften anpassen
  - **ui_nav_helpers.js:** subNavMap['media']-Labels auf "Queue" setzen, Playlist-Handling ergänzen

### 2. Player: Cover Art Restoration
- **Ziel:** Artwork-Sync über alle Sub-Views und Footer
- **audioplayer.js:**
  - `playAudio(item)` aktualisiert alle `.synced-artwork`-Elemente (z.B. `big-player-artwork-queue`, `footer-artwork-raster-buffer`)

### 3. Backend: ALAC & WAV24 Transcoding
- **Ziel:** Browser-Inkompatibilitäten (ALAC, WAV24) beheben
- **main.py:**
  - `/media/<file_path:path>`-Route: ALAC per FFmpeg nach FLAC/WAV transkodieren
  - WAV24: Richtigen MIME-Type setzen, PCM-Header für High-Bitrate

### 4. Smart Context Menu
- **Ziel:** Kontextabhängige Menüoptionen
- **common_helpers.js:**
  - `showContextMenu(e, item)` nutzt `isVideoItem(item)`
  - Audio: "Zur Queue hinzufügen", "Metadaten bearbeiten"
  - Video: "Im Video Player abspielen", "Analysieren", "Datei löschen"

### 5. Audiobook Chapter Sidebar
- **Ziel:** Premium-Sidebar für Kapitel-/Track-Navigation bei Hörbüchern
- **audioplayer.js:**
  - `renderAudiobookDetails(item)` füllt Detail-Pane mit Kapiteln (Titel, Dauer, Klick zum Abspielen)

---

## Open Questions
- Playlist Tab: Soll beim Öffnen automatisch die letzte Playlist geladen werden oder nur das Manager-Interface?
- Premium Sidebar: Nur für Hörbuch/Audiobook oder für alle Audio-Alben?

---

## Verification Plan
- **Automated:**
  - `tests/ui/playback_verify.py` mit ALAC/WAV24-Testfiles
  - `tests/ui/navigation_verify.py` für Kategorie-Labels
- **Manual:**
  - Rechtsklick auf MP3 vs. MKV: Unterschiedliche Menüs
  - "Playlist"-Button: Fragment lädt korrekt
  - Artwork-Update im Footer & Main-Player synchron prüfen
