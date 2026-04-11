
# Logbuch: Abschluss Media Viewer v1.34 – UI, Pipeline & Navigation Umbau

## Zusammenfassung – Umbau erfolgreich abgeschlossen

### 1. UI-Rebranding & Navigation
- **Audio-Player:** Haupt-Tab in der Kopfzeile von "Player" zu "Audio-Player" umbenannt
- **Playlist-Tab:** Neuer, eigenständiger Tab "Playlist" für schnellen Zugriff auf Sammlungen (jetzt im Audio-Player Sub-Menü)
- **Queue:** Alle "Warteschlange"-Instanzen (Buttons, Header, Menüs) zu "Queue" geändert
- **Parser & Tools:** In den Options-Bereich verschoben, um die Top-Navigation zu verschlanken
- **Header-Fix:** Die Gesamthöhe aller Fixed Bars (Header, Subnav, Footer) wird jetzt dynamisch berechnet (72px), sodass der Content nie "abgehackt" wirkt

### 2. High-Fidelity Audio-Pipeline (Transcoding)
- **ALAC-Support:** .m4a/.alac werden automatisch erkannt und verlustfrei nach FLAC transkodiert (Browser-kompatibel)
- **OGG & WAV24:** OGG-Transkodierung und korrekte Mimetype für 24-bit WAV zentral in web/app_bottle.py implementiert; Fragmente werden gecached
- **ISO Main Track Detection:** In main.py wird per ffprobe automatisch der längste Track (Hauptfilm) in ISO/DVD-Images erkannt, sodass Transcoding und Playback immer auf den Hauptinhalt zielen (keine Menüs/Extras mehr)

### 3. Synchronisierte Player-Ansichten
- **Artwork Sync:** Alle .synced-artwork-Elemente (Footer, Main Player, Visualizer) werden synchron aktualisiert
- **Meta-Daten Sync:** Titel, Artist, Album, Codec, Bitrate, Samplerate bleiben in allen Player-Views synchron

### 4. Intelligentes Kontextmenü
- **Audio:** "Zur Queue hinzufügen", "Abspielen", "Metadaten bearbeiten"
- **Video:** "Im Video Player abspielen", "Video analysieren (FFprobe)", "Datei löschen"

### 5. Audiobook & Album Sidebar (Premium Sidebar)
- In der linken Player-Spalte werden bei Hörbüchern/Alben alle Kapitel/Tracks gelistet (Name, Nummer, Dauer)
- Klick auf Kapitel startet Wiedergabe an dieser Stelle

### 6. Navigation & Menüstruktur
- **Menu Entry Restoration:** Die fehlenden Einträge für Reporting und System Test wurden in die Top-Menüleiste und die neue dynamische Sub-Navigation (glassmorphische Pills) integriert
- **Dynamische Sub-Navigation:** Breadcrumb-Bar unter dem Header, die je nach Kategorie passende Sub-Tabs (z.B. Reporting, Tests, Media, Edit) anzeigt
- **Active-State-Tracking:** Sub-Nav-Buttons heben sich beim Wechsel automatisch hervor

### 7. Technische Details & Verifikation
- **Code Integrity:** FFmpeg-Generator-Logik für Video-Transcoding (MSE/FragMP4) in main.py wiederhergestellt, inkl. Cleanup im finally-Block
- **Diagnose-Skripte:** verify_video_transcode.py prüft Streaming-Endpunkte, Content-Type und Byte-Stream
- **Automatisierte Checks:** node --check web/js/*.js, Playwright- und DOM-Tests, Logging von DB-Initialisierung und Media-Discovery
- **Manuelle Checks:** Menüeinträge, Sub-Navigation, Hauptfilm-Erkennung bei ISOs, synchronisierte Player-Ansichten, Kontextmenüs, Sidebar, Transcoding-Playback

---

**Status:**
- Alle genannten Punkte umgesetzt und für maximale Stabilität optimiert
- App bereit für Testlauf mit ALAC, OGG, WAV24, ISO/DVD und Video-Streaming
- Details siehe Walkthrough und Implementation Plan
