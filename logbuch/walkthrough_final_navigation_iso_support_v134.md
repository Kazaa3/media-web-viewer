# Walkthrough – v1.34 Final: Advanced Navigation & ISO Support

Die Media Viewer v1.34 ist jetzt vollständig optimiert: mit modularer Navigation und erweitertem Media-Engine-Support für professionelle Formate (ISO/Transcoding).

---

## Key Accomplishments

### 1. Navigation Restructure (Clean Header)
- **Playlist Manager:** Vom Hauptmenü in den Audio-Player-Sub-Tab verschoben
- **Parser Chain:** Aus dem Hauptmenü entfernt, jetzt als Sub-View in den Optionen (System)
- **Fixed Overlap:** Dual-Header (40px + 32px) sorgt mit 72px Offset für sauberen Content-Bereich ohne Überlappungen

### 2. Audio Player & Gallery Features
- **Item Type Filter:** Neue Filtermöglichkeit in der Mediengalerie: Audio, Video, ISO/DVD – für gezielte Asset-Ansicht
- **Playlist Accessibility:** Playlist Manager ist jetzt direkt im Sub-Nav des Players erreichbar
- **Visualizer Sync:** Alle Visualizer-Buttons (oben rechts & Sub-Nav) triggern synchron die Premium-Ansicht

### 3. Backend Engine: ISO & Audio Transcoding
- **ISO Main Track:** Streaming-Engine erkennt automatisch den längsten Titel (Main Track) in ISO-Filmen und spielt direkt den Hauptfilm ab (keine Menü-Navigation mehr nötig)
- **Audio-Only Transcoding:** FragMP4-Pipeline für Audio-only-Dateien (mp3, flac, etc.) repariert – High-Fidelity-Streaming im Browser über die einheitliche Transcode-Route

---

## Verification

### 1. Header Layout
- Alt-Menü toggeln und prüfen, dass der Content sauber nach unten verschoben wird (kein "Abhacken")

### 2. Gallery Filtering
- Audio-Player → Mediengalerie öffnen
- Dropdown nutzen, um zwischen "Alle Typen", "Audio" und "Video" zu wechseln

### 3. ISO Playback
- ISO-Datei aus der Galerie auswählen und abspielen – Backend erkennt und streamt automatisch den Hauptfilm

---

**Status:**
- v1.34 Finalisierung erfolgreich abgeschlossen. Navigation, Medienfilter und ISO-Playback sind jetzt robust und benutzerfreundlich.
