# Logbuch Eintrag 018: Redesign des Video-Player-Systems (3-Player Architektur)

## 📅 Datum: 2026-03-16
## 🚀 Status: Implementiert & Verifiziert (Beta)

### 1. Die Vision: Maximale Flexibilität durch Tiered Selection
Bisher war die Auswahl des Players auf eine flache Liste von "Strategien" beschränkt. Mit der Einführung des **3-Player-Systems** (Chrome Native, VLC Desktop, PyPlayer) wurde die UI auf eine zweistufige Auswahl umgestellt:
1.  **Player-Typ**: Auswahl der Engine (Chrome, VLC, PyPlayer).
2.  **Video-Modus**: Dynamische Filterung der verfügbaren Modi basierend auf dem gewählten Player.

### 2. Die 3 Säulen der Wiedergabe

#### A. Player 1: Chrome Native (Web-First)
Optimiert für minimale CPU-Last (0-5%) und native Browser-Features.
- **Direct Play**: Direkte Wiedergabe unterstützter Codecs (MP4/WebM).
- **HLS Native**: Stream via MediaMTX (HTTP 8888).
- **FragMP4 Stream**: FFmpeg-on-the-fly Segmentierung.
- **WebM/VP9**: Unterstützung für moderne Open-Source Codecs.

#### B. Player 2: VLC Desktop (Das Schweizer Taschenmesser)
Für alle Formate, die Chrome nicht nativ beherrscht (ISO, MKV mit exotischen Codecs).
- **cvlc Solo**: Standalone Instanz ohne GUI.
- **Embedded VLC**: Integration in das App-Frontend.
- **DVD ISO Live**: Direkter Start von Disk-Attrappen via `dvd://`.
- **TS-Stream Detection**: Intelligente Erkennung von Transport-Streams.

#### C. Player 3: PyPlayer (Native Python / MPV)
Die Brücke für spezialisierte Overlays und PiP (Picture-in-Picture).
- **pyvidplayer2**: Native Python Einbindung.
- **Mini-Overlay (PiP)**: Schwebendes Videofenster über der App.

### 3. Technische Umsetzung
- **Backend**: Konsolidierung in `main.py` -> `open_video(path, player_type, mode)`.
- **Frontend**: Dynamische `updateVideoModes()` Logik in `app.html` zur Steuerung der Dropdowns.
- **Protokoll**: Alle Anfragen werden über Eel orchestriert, wobei der Status (play/error/ok) einheitlich zurückgegeben wird.

### 4. Fazit & Ausblick
Das System deckt nun alle 24 geplanten Varianten ab und ist durch das modulare Design leicht erweiterbar (z.B. für Cast-Devices oder zukünftige Player wie PotPlayer).
