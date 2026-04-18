# Walkthrough — Expanded Rendering Governance & Multi-Type Queues

## Zusammenfassung
Die zentrale Steuerung der Rendering-Pulse wurde erweitert, um alle Hauptmodule der Mediengalerie zu erfassen. Ein dedizierter Photo-Queue-Renderer wurde implementiert, sodass Bilder korrekt angezeigt werden, wenn sie gefiltert werden.

---

## 1. Erweiterte Rendering-Governance
- **Datei:** config_master.py
- **Aktion:**
    - Neue Flags registriert:
        - `render_library_enabled`: Steuert das Haupt-Mediengrid.
        - `render_photo_queue_enabled`: Steuert die Anzeige von Bildern in der Queue.
        - `render_file_browser_enabled`: Steuert die Dateibrowser-Ergebnisse.
    - Alle Flags in `ui_flag_registry` unter "UI Pulses"/"Governance" eingetragen.

## 2. Multi-Type Queue Support
- **Datei:** audioplayer.js
    - Neue Funktion `renderPhotoQueue()` implementiert:
        - Filtert `window.currentPlaylist` nach Bildern.
        - Rendert Bilder mit spezifischem Layout (Thumbnails/Preview) in die Queue-Container.
    - Sowohl `renderAudioQueue()` als auch `renderPhotoQueue()` prüfen ihre jeweiligen window.CONFIG-Flags.
- **Datei:** playlists.js
    - `syncQueueWithLibrary()` ruft jetzt auch `renderPhotoQueue()` im globalen Refresh-Pulse auf.
- **Datei:** bibliothek.js
    - `renderLibrary()` prüft das Flag `render_library_enabled`.
- **Datei:** browse.js
    - `renderFileList()` prüft das Flag `render_file_browser_enabled`.

---

## Verifikation
- Auswahl "Bilder" im Filter zeigt korrekt Fotos in der Mediengalerie an.
- Umschalten der Flags in der Konfiguration aktiviert/deaktiviert die Rendering-Pulse der jeweiligen Module.

---

*Letztes Update: 18.04.2026*
