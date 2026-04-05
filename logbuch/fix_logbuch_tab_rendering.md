# Logbuch: Fix Logbuch Tab Rendering (27.03.2026)

## Problem
- Der Logbuch-Tab rendert aktuell als leere/weiße Seite.
- Ursache: Die Frontend-Funktion `loadLogbuchTab` ruft `eel.read_file`, das im Backend nicht exposed ist.
- Zusätzlich: Mögliche HTML/CSS-Probleme (Layout-Bleeding, Collapse) beim Aktivieren des Tabs.

## Proposed Changes

### Backend (core/main.py)
- [ ] Implementiere und expose `read_file(filename, context)` via Eel.
- [ ] Zugriff auf erlaubte Verzeichnisse (z.B. nur `logbuch/`) beschränken (Security).
- [ ] Nutze `PROJECT_ROOT` zur sicheren Pfadauflösung.

### Frontend (web/app.html)
- [ ] Audit von `loadLogbuchTab` auf JS-Fehler (fehlende Übersetzungen, Helper).
- [ ] Überprüfe CSS/Nesting von `localized-markdown-documentation-journal-panel`, um Layout-Probleme zu vermeiden.

## Verification Plan
- App starten und "Logbuch"-Tab öffnen.
- Sidebar: Einträge werden korrekt geladen.
- Eintrag anklicken: Inhalt wird im Viewer angezeigt.
- Browser-Konsole: Keine JS-Fehler mehr.

**Fazit:**
Mit diesen Änderungen wird der Logbuch-Tab wieder zuverlässig gerendert und ist gegen Layout- und Security-Probleme abgesichert.

# Cinematic Media Player Stabilization – Final Logbuch (27.03.2026)

- **Planning and Artifact Creation**
- **Fix Startup JS Error:** `srcType` variable Bug behoben
- **Restore Cinematic Layout CSS:** `cinema-expanded` wiederhergestellt
- **Fix DOM ID Mismatch:** `video-player-container-root-wrapper` gesetzt
- **Refactor all components:** ES6 Class Syntax für Video.js 8.x-Kompatibilität
- **Resolve startup TypeError crashes:** Initialisierungsfehler beseitigt
- **Final Verification & UI Versioning:** Release v1.0.1 nach vollständigem Test
- **Fix Video Player Layout:** Restriktives Overflow/Min-Height entfernt
- **Enable Reliable MKV Seeking:** Direct Play & Remux Whitelist
- **Restore Premium Features Visibility:** CSS & Labels für Custom-Buttons
- **Implement Seeking for Remux Route:** `-ss`-Support für Remux-Streams
- **Intel Arc Scaling Support:** 0-1000 → 0-100 für GPU-Stats
- **Real-Time Stats Overlay:** Backend-Pusher + ES6-Komponente
- **Universal GPU Support:** iGPU > AMD > Arc > Nvidia
- **Fix Track Switching:** Remux/Transcode (Audio/Subtitles)
- **Implement refresh() for track components:** Audio/Subs-Buttons dynamisch
- **Fix MKV & DVD Seeking:**
    - MKV Seeking (Hot-Reload)
    - DVD/ISO Seeking (Prefixes + Buffering)
- **Premium GUI Control Panel:**
    - Glassmorphic Settings Overlay (rechte Seite)
    - Settings Gear Icon Component
    - Konsolidierte Tracks, Speed, FX, Stats im Overlay
- **Premium Player UI Polish (Video.js):**
    - Volume Slider wiederhergestellt
    - Premium Features (Tracks, CC, Subs) standardisiert
    - Glassmorphism & Icons für visuelle Exzellenz
- **Context Menu & Routing Logic:**
    - Video vs. Audio Items differenzieren
    - Item-spezifische Optionen im Kontextmenü
    - Audiobook Position Persistence (Save/Resume)
- **Research & Integration:**
    - Laufende Optimierung und Feature-Integration

# Premium Media Player Refinement Task (27.03.2026)

## Premium Video.js UI Restoration
- Re-integriere Volume Slider (nicht-inline) in die vjsPlayer-Controlbar
- Füge audioTrackButton und subsCapsButton für native Track-Auswahl hinzu
- Stelle ein responsives Premium-Layout für alle Steuerelemente sicher

## Context-Aware Menu Logic
- Implementiere bedingte Anzeige in `showContextMenu`:
  - "Video Options" nur für Video/ISO
  - "Audio Options" nur für Audio
  - "Resume" nur, wenn gespeicherte Position existiert
- Überarbeite Kontextmenü-CSS: Glassmorphism (Blur, Transparenz, Neon)
- Refaktoriere `handleContextMenuAction` für 'resume' und kontextspezifische Playbacks

## Playback Position Persistence (Resume)
- Aktualisiere `play()`, `playVideo()`, `startEmbeddedVideo()` für `startTime`-Support
- Implementiere persistentes State-Tracking für Audio:
  - `ontimeupdate`-Listener in `activeAudioPipeline`
  - Alle 10s Sync via `eel.update_playback_position`
- Stelle sicher, dass Video.js Resume-Logik `currentTime` auf `loadedmetadata` korrekt setzt

## Final Audit & Polish
- Konsolidiere `isVideoItem`-Helper
- Prüfe, dass Engine/Protocol-Labels (Transparenz) weiterhin korrekt angezeigt werden
- Finaler CSS-Check für Premium-Optik

# Premium Media Player Refinement Walkthrough (27.03.2026)

## Key Changes

### 1. Glassmorphic Context Menu
- Modern Glassmorphism: Kontextmenü mit Blur, Transparenz, Neon-Cyan-Akzenten
- Kontext-Aware Filtering:
  - "Video Options" (z.B. VLC, WebM Transcode) nur für Video/ISO
  - "Audio Options" (z.B. Audio Direct) nur für Audio
  - "Resume Playback" erscheint nur bei gespeicherter Position (>5s)

### 2. Video.js UI Restoration
- Volume Slider: Standard-Panel (nicht-inline) wieder integriert
- Track Selection: Native audioTrackButton und subsCapsButton (CC) in der Controlbar

### 3. Persistent Playback (Resume)
- Automatisches Sync: Player synchronisiert alle 10s die aktuelle Position ins Backend
- Universal: Funktioniert für Video (Video.js) und Audio (Native Pipeline)
- Audiobook-Optimierung: Lesezeichen für lange Audiofiles, Resume exakt an letzter Stelle

## Verification Steps

### Automated Testing
- DB-Schema (`db.py`): Spalten `playback_position`, `last_played` geprüft
- Backend (`main.py`): Route `update_playback_position` auditiert

### Manual Verification
- Kontextmenü: Rechtsklick auf MKV → "Video Options" sichtbar, auf MP3 → nur "Audio Options"
- Resume-Test: Video 30s abspielen, schließen, erneut öffnen → "Resume Playback" startet bei 30s
- Audio-Persistenz: Audio 15s abspielen, DB/Contextmenü prüfen → Position aktualisiert
- UI-Check: Glassmorphism im Kontextmenü, Volume Slider in Video.js sichtbar

**Tipp:**
- "Resume"-Feature gezielt mit Audiobooks testen, um 10s-Sync zu validieren.
