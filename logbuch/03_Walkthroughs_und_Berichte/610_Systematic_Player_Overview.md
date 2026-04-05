# Logbuch: Systematic 3-Player Overview & Integration

**Datum:** 16. März 2026

## Ziel
Integration eines flexiblen 3-Player-Systems (Chrome Native, VLC, PyPlayer) mit gruppierter Auswahl-UI und Backend-Support für 24 Wiedergabevarianten. Behebung von Reporting-Tab-Fehlern und spezifischen JS-Problemen.

---

## Änderungen

### Frontend (`app.html`)
- **Player Selection UI:**
  - Einzelnes Modus-Select ersetzt durch zwei Selects: `player-type` (Chrome, VLC, PyPlayer) und `video-mode` (dynamisch gefiltert).
  - `<optgroup>` für bessere Übersicht.
- **State Management:**
  - `playVideo()` und `orchestrateVideoPlaybackMode()` senden `player_type` und `mode` an das Backend.
- **PyPlayer Integration:**
  - Logik für `pyvidplayer2` (Desktop native) und Mini-Overlay (PiP) integriert.
- **Tab Synchronization:**
  - `tabMap` in `switchTab` um Reporting erweitert.
- **JS Error Guarding:**
  - Null-Checks für `.style`-Zugriffe, robuste Plotly-Initialisierung.

### Backend (`main.py`)
- **open_video Refactor:**
  - Neue Signatur: `open_video(file_path, player_type, mode)`.
  - Branching für chrome, vlc, pyplayer.
- **Mode Variants Implementation:**
  - Chrome Native: Direct Play, MediaMTX HLS, FragMP4 (ffmpeg).
  - VLC: cvlc Solo (TS), Embedded, External, Pipe (cvlc|ffmpeg), DVD ISO Live.
  - PyPlayer: Integration von `pyvidplayer2` für native Desktop-Wiedergabe.
  - Legacy/Extern: Platzhalter für PotPlayer, SMPlayer etc.
- **FFprobe Hook:**
  - Smart Routing/Fallback nutzt neue Player/Mode-Matrix.
- **Reporting API:**
  - `get_test_results` via `@eel.expose` bereitgestellt.
- **Requirements Logic:**
  - `_get_requirements_status` verbessert (Redirects, requirements-core.txt).

---

## Übersicht: 24 Player-Varianten (Status)

| Player-Type   | Mode                  | Status        |
|---------------|-----------------------|---------------|
| Chrome Native | Direct Play           | ✅ Implemented|
| Chrome Native | MediaMTX HLS          | ✅ Implemented|
| Chrome Native | FragMP4 (ffmpeg)      | ✅ Implemented|
| VLC           | cvlc Solo (TS)        | ✅ Implemented|
| VLC           | Embedded              | ✅ Implemented|
| VLC           | External              | ✅ Implemented|
| VLC           | Pipe (cvlc|ffmpeg)    | ✅ Implemented|
| VLC           | DVD ISO Live          | ✅ Implemented|
| PyPlayer      | pyvidplayer2          | ✅ Implemented|
| PyPlayer      | Mini-Overlay (PiP)    | ⏳ In Progress|
| Legacy        | PotPlayer             | ⏳ Placeholder|
| Legacy        | SMPlayer              | ⏳ Placeholder|
| ...           | ...                   | ...           |

(Weitere Varianten siehe Alle_Video_Player_Komplettliste.md)

---

## Verifikationsplan

### Automatisierte Tests
- `pytest tests/test_player_modes.py`: Prüft, ob jeder Modus den korrekten Backend-Befehl auslöst (Subprocess-Mocking).

### Manuelle Verifikation
- Alle Hauptmodi testen: Chrome Direct, cvlc TS Stream, Pyvidplayer2.
- Dynamisches UI-Filtering im Player-Tab prüfen.
- Logbuch-Eintrag-Formatierung kontrollieren.

---

Weitere Details siehe implementation_plan.md und vorherige Logbuch-Einträge.
