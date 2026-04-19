# Logbuch: Forensic UI Alignment & Sub-Bar Restoration

## Hintergrund
Die Analyse des Referenz-Screenshots ergab, dass das gewünschte GUI auf der konsolidierten Split-View (`player_queue.html`) basiert und nicht auf dem neuen modularen Workstation-Shell. Ziel ist die Wiederherstellung der korrekten Fragment-Registrierung, die Synchronisierung der Sub-Navigation und die Lokalisierung der Recovery-Statusanzeigen.

---

## Umsetzungsschritte

### 1. Configuration & Registry
- **config_master.py**
  - `sub_nav_registry["media"]` aktualisiert:
    - Queue → `switchPlayerView('warteschlange')`
    - Mediengalerie → `switchMainCategory('library')`
    - Visualizer → `switchPlayerView('visualizer')`
    - Video Cinema → `switchMainCategory('video')`
  - Ergebnis: Sub-Bar entspricht exakt dem Referenz-Screenshot.

### 2. Frontend Orchestration
- **app_core.js**
  - Player-Fragment-Registrierung zurück auf `fragments/player_queue.html` gesetzt.
  - Sicherstellen, dass der `onActivate`-Hook `renderAudioQueue()` und `renderPlaylist()` triggert.
- **nuclear_pulsar.js**
  - `triggerNuclearPulsar()` refaktoriert: Nicht mehr global, sondern gezielt für `#player-deck-column` und `#player-playlist-column`.

### 3. UI Fragments (Proof of Life)
- **player_queue.html**
  - Harte Status-Tags am Anfang jeder Split:
    - Links: Grüner Tag „⚡ DECK DATA ACTIVE“
    - Rechts: Oranger Tag „⚡ QUEUE DATA ACTIVE“
  - Ergebnis: Marker sind auch bei Black Screen innerhalb der Splits sichtbar.

### 4. Data Hydration Fix
- **playlists.js**
  - `syncQueueWithLibrary()` wird sofort getriggert, wenn die Queue leer ist.
  - Eel-Call an Backend, um Library-Scan zu erzwingen, falls 0 Items erkannt werden.

---

## Offene Fragen
- Sollen die Sub-Nav-Buttons „Mediengalerie“ und „Video Cinema“ das Hauptmodul wechseln (wie im Screenshot), oder innerhalb des Players bleiben? (Standard: Modulwechsel)
- Soll die pinke „NUCLEAR RECOVERY PULSE“-Bar komplett entfernt oder nur verschoben werden? (Standard: Entfernt, Proof-of-Life nur noch in Splits)

---

## Verifikation
- Sub-Nav zeigt: Queue, Mediengalerie, Visualizer, Video Cinema
- Player-Layout: Artwork links, Liste rechts
- Proof-of-Life-Marker in beiden Splits sichtbar
- Konsole zeigt `[PULSAR]`-Liveness-Logs

---

*Plan und Korrekturen gemäß Referenz-Screenshot umgesetzt. Weitere Anpassungen auf Wunsch möglich.*
