# Implementation Plan: VLC Interactive Embedded Stream (27.03.2026)

## Ziel
Integration eines interaktiven, VLC-basierten Streams in den Media Viewer. DVDs/ISOs können direkt im Chrome-Tab mit voller Menü-Navigation abgespielt werden.

## Proposed Changes

### 1. Restoration & Fixes (Frontend)
- **app.html:**
  - Wiederherstellung und Fix von `handleContextMenuAction`
  - Sicherstellen, dass `isVideoItem` korrekt verwendet wird

### 2. Backend Enhancements
- **main.py:**
  - Update `start_vlc_guarded`:
    - `--intf http`, `--http-port`, `--http-password` in VLC-Command für `vlc_embedded`-Modus
    - Dynamische Portvergabe für Stream & Control-Interface
    - HLS-Ausgabe für niedrige Latenz optimieren (kürzere Segmente)
  - **[NEU]** `send_vlc_command(port, command)`: Eel-exposed Funktion, um Navigation (key-up, key-down, Enter) an VLC zu senden

### 3. Frontend Integration
- **app.html:**
  - Interaktiver Hook: Bei aktivem `vlc_embedded` auf Arrow Keys/Enter hören
  - Remote Command Bridge: Tasten an `send_vlc_command` im Backend senden
  - UI-Feedback: Toast/Indicator bei gesendeten Kommandos anzeigen

## Verification Plan

### Manual Verification
- **Context Menu Restoration:** Rechtsklick auf Datei → "Resume", "VLC DVD-Folder" etc. funktionieren korrekt
- **VLC Interactive Mode:**
  - DVD-ISO im "VLC DVD-Folder"-Modus öffnen
  - Stream startet im Video-Tab
  - Pfeiltasten bewegen Menüauswahl, Enter wählt Menüpunkt
- **Latency Check:** Zeit zwischen Tastendruck und Menü-Update ist akzeptabel

**Fazit:**
Mit dieser Integration wird ein voll interaktives DVD/Blu-ray-Menü im Browser möglich – 100% Linux-kompatibel, ideal für Media-Library-Apps.
