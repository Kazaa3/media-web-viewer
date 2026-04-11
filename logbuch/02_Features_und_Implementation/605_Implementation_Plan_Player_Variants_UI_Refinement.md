# Logbuch: Implementation Plan – Player Variants & UI Refinement

**Datum:** 16. März 2026

## Ziel
Erweiterung des Video-Players um fehlende Varianten, fortgeschrittene UI-Controls und Behebung gemeldeter Bugs (ISO-Decoding, Video.js API).

---

## Wichtige Hinweise
- **Chromecast & DLNA:** Benötigt pychromecast und dlnap.
- **swyh-rs:** Benötigt swyh-rs-Binary auf dem System.
- **Batch-Remux:** Benötigt mkvmerge (MKVToolNix).

---

## Vorgeschlagene Änderungen

### Backend (`main.py`)
- **Path Decoding:** URL-Decoding von `file_path` in `open_video` und `vlc_ts_mode` (Fix für .iso mit Sonderzeichen).
- **Eel Exposure:**
  - `stream_to_mediamtx` und `mediamtx_mode` für neue Frontend-Calls verfügbar machen.
- **Casting Integration:**
  - `eel.discover_cast_devices()`: Gibt Chromecast- und DLNA-Ziele zurück.
  - `eel.start_cast(file_path, device_name, type)`: Remote-Playback starten.
- **Batch-Remux:**
  - `eel.batch_remux_to_mkv(folder_path)` mit mkvmerge implementieren.
- **swyh-rs:**
  - `eel.toggle_swyh_rs()` zum Starten/Stoppen der Audio-Bridge.

### Frontend (`app.html`)
- **Advanced UI Buttons:**
  - Stop, Shuffle, Repeat, Seek, Speed, EQ (Unicode: ■, 🔀, 🔁, ⏪, ⏩, ⏱️, 🎚️) in der Player-Control-Bar.
- **Bug Fix:**
  - `.pause()`-Aufruf auf vjsPlayer-Instanz in `startVLC` und `stopVideo`.
- **Cast Menu:**
  - UI für Geräteauswahl (Chromecast/DLNA).
- **Batch-Remux UI:**
  - Button in der Bibliotheksansicht für Ordner-Remux.

### Localization (`i18n.json`)
- Labels für neue Buttons und Cast-Features ergänzen.

---

## Verifikationsplan

### Automatisierte Tests
- `pytest tests/test_vlc_mkv_streaming.py`: Remux- und Pipe-Logik.
- `pytest tests/test_casting_stubs.py`: Mock-Hardware-Discovery.

### Manuelle Verifikation
- .iso-Playback mit Leerzeichen im Dateinamen testen (Decoding prüfen).
- "Stop"-Button für Video.js und Standalone-Player testen.
- "Casting"-Discovery-UI prüfen.

---

Weitere Details siehe implementation_plan.md und task.md.
