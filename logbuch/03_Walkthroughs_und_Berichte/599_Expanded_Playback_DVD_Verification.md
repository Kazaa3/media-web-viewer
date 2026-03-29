# Logbuch: Expanded Playback & DVD Verification

**Datum:** 16. März 2026

## Erweiterte Wiedergabe & DVD-Verifikation

### Aufgaben & Änderungen

- **Integrationstests für DVD ISO:**
  - Spezialisierter Test für echte DVD ISO-Strukturen (Going Raw - JUDITA_169_OPTION.ISO).
  - Neue Datei: `tests/integration/basic/playback/test_dvd_iso.py`.
  - Verifiziert, dass `open_video` mit `dvd_native` korrekt funktioniert.

- **Standalone Playback Modes:**
  - **FFmpeg (Browser):**
    - Transkodiert und streamt direkt über `/video-stream/` zu `<video>` im Browser.
  - **FFplay (Standalone):**
    - Startet ffplay für ein separates Videofenster.
  - **MKVMerge (Standalone):**
    - Remux im Hintergrund zu temporärem MKV, öffnet anschließend in VLC (ohne Pipe-Jitter).

- **Backend-Änderungen:**
  - `src/core/main.py`: Erweiterung von `open_video` um neue Modi (`ffmpeg_browser`, `ffplay`, `mkvmerge_standalone`).
  - Verfeinerung von `stream_to_vlc` für robustere Behandlung von `dvd://` und `bluray://` (insbesondere für die ISO-Datei).

- **Frontend-Änderungen:**
  - `web/app.html`: Neue Modi im Kontextmenü und Selector.
  - Aktualisierung der Übersetzungsschlüssel.

### Verifikationsplan

- **Automatisierte Tests:**
  - `python3 tests/integration/basic/playback/test_dvd_iso.py`
  - Aktualisierte `test_playback_modes.py`

- **Manuelle Verifikation:**
  - Rechtsklick auf ISO in der Bibliothek → "DVD / ISO (Native)" auswählen.
  - Überprüfen, ob VLC mit DVD-Menü startet.
  - Testen des neuen "FFmpeg (Browser)" Modus im integrierten Player.

---

**User Review Required**

Die "without pipe"-Modi für FFmpeg und MKVMerge werden wie oben beschrieben implementiert.

Weitere Details siehe implementation_plan.md.
