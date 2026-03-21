---

## Summary of Video Player & Diagnostic Fixes (EN)

### Key Improvements & Fixes
- Removed duplicate window.jumpToChapter declarations (conflict at line 9325, robust version at 6700 kept)
- Fixed activeAudioPipeline re-initialization/shadowing
- Restored DIV balance: 651 opening/651 closing tags (QA/Reporting tabs)
- Added global initUiTraceHooks IIFE: proxies alert/confirm/prompt, logs to backend
- Global error/unhandledrejection listeners: all JS errors now logged with stack trace
- 🐞 Simulate & Verify Failure Capture: buttons for ReferenceError, Promise Rejection, alert/confirm proxying (Startup/Integrity sub-tab)
- Integrated Video Player Test Suite in Reporting tab: Native, VLC, WebM, FFmpeg, FragMP4 modes, with videoTestHistory tracking

### Verification
- DIV balance checked (balance 0)
- Trace hooks verified in Chromium
- All backend triggers mapped to UI buttons

---

## 🚀 Finalization: Video Player Diagnostic & Stress Suite (21.03.2026)

### FFplay Bridge Completion
- open_ffplay in src/core/main.py implementiert (mit -autoexit, -sn für Performance-Tests)
- FFplay-Testbutton im Reporting → Video-UI ergänzt
- "FFmpeg"-Test im Frontend jetzt mit echtem trigger_ffmpeg_stream-Callback verbunden

### JS Error Interception & Eel Bridge
- log_js_error und toggle_swyh_rs korrekt via @eel.expose angebunden (Fehler-Reporting jetzt backend-seitig sichtbar)
- Doppel-Exposure-Bug bei @eel.expose behoben

### UI Trace & Validation
- "Simulate & Verify Failure Capture"-Panel in Tests → Startup geprüft
- initUiTraceHooks: alert/confirm/prompt-Proxy & globale Fehler-Events werden korrekt abgefangen und geloggt

### Process Sanitization
- Hintergrundprozesse (Selenium/Python) bereinigt, Startup-Performance verbessert

### 🧪 System State Check
- Video-Testmodi: Native, VLC, WebM, FFmpeg, FFplay, FragMP4 — alle verlinkt & einsatzbereit
- Fehlerpipeline: Frontend-Errors werden an log.error im Backend weitergeleitet
- DIV-Integrität: 651/651 — balanciert

**Suite ist bereit für Cross-Codec-Stresstest (MKV/H265/ISO).**

---

## 🆕 Video Player: Expanded Test Suite & MP4 Fixes (21.03.2026)

### 1. Robust Media Routing & Playback Fix
- MP4-Playback-Probleme gelöst: Backend-Routing für /direct/ gehärtet (Pfadhandling, Unquoting, explizite MIME-Typen)
- URL-Encoding: Alle Media-URLs werden jetzt mit urllib.parse.quote kodiert (Spaces/Sonderzeichen sicher)
- Seeking-Support: bottle.static_file optimiert für Range-Requests (schnelles Spulen bei großen MP4s)

### 2. Expanded Test Suite UI
- Reporting-Tab: Kompakte Button-Icons, lokalisierte Labels für alle Testmodi
- "Test-Medium"-Selector: Dynamisch mit allen abspielbaren Videos befüllt
- History/Progress: Ergebnis-Tabelle zeigt detaillierte Statusmeldungen der Backend-Prozesse

### 3. New Backend Test Bridges
- MPV & FFplay: Direkter Launch für lokale Playback-Tests
- MKVmerge: Hintergrund-Remux in cache/-Verzeichnis
- MediaMTX: RTSP-Bridge für automatisierte HLS/WebRTC-Tests
- MP4 FastStart: FFmpeg-Test für moov-Atom-Optimierung

### 4. Automated Codec Matrix
- "Generate & Run": test_media_factory erzeugt Mini-Mocks für H.264, H.265, VP9, MP3, FLAC, OPUS
- Status-Indikatoren: UI zeigt Verfügbarkeit/Erfolg (grün/rot) für alle Test-Assets

### File Modifications
- main.py: Routing gehärtet, Bridges/Subprozesse, URL-Handling verbessert
- app.html: Reporting-UI verfeinert, Testmodi/Selector-Logik ergänzt
- test_media_factory.py: MKV/OPUS-Mock-Support

**Alle Testvarianten direkt im Reporting → Video-Tab verfügbar.**

---

## ⚡ Real-time Transcoding for PAL/NTSC DVDs & Wild Formats (21.03.2026)

### 1. Real-time FFmpeg Streaming Pipeline
- Neuer /transcode/<path>-Route im Backend: On-the-fly-Transcoding mit FFmpeg in Fragmented MP4 für Chrome
- Hardware-Effizienz: libx264, ultrafast, zerolatency für minimale Startverzögerung
- Intelligentes Deinterlacing: ffprobe erkennt PAL/NTSC-Interlacing, yadif-Filter wird nur bei Bedarf aktiviert

### 2. Automatic Format Routing
- get_play_source & analyze_media priorisieren jetzt den Transcoder für .iso und "wilde" Formate (MPEG-2, HEVC/H.265, VC-1, WMV3)
- DVD-ISOs werden direkt gestreamt, keine langsame Extraktion mehr
- Fallback: Komplexe Dateien werden zuerst transkodiert, erst dann an VLC etc. übergeben

### 3. Frontend Integration & Test Suite
- Neuer "⚡ Trans"-Button im Reporting → Video-Tab: Manuelles Testen des Transcoding-Pipelines für beliebige Dateien
- Automatische Wiedergabe: DVD/Komplexformate starten sofort im Embedded Player mit Transcode-Stream

### File Modifications
- main.py: /transcode/-Route, Routing-Logik erweitert
- format_utils.py: ffprobe_suite extrahiert scan_type (interlaced/progressive)
- app.html: "Real-time Transcode"-Button & Routing-Update

**DVD-ISOs & komplexe Formate jetzt direkt im Browser abspielbar – mit Deinterlacing!**

---

## 🚀 Echtzeit-Transkodierung & Premium-Video-Player (21.03.2026)

### Echtzeit-Transkodierung (Fragmented MP4 Streaming)
- Neue /transcode/-Route in main.py: Medien werden via FFmpeg direkt als Fragmented MP4 für Chrome gestreamt
- Intelligentes Deinterlacing: ffprobe erkennt Interlaced-Material (PAL/NTSC), yadif-Filter wird selektiv angewendet
- Optimiertes Routing: ISO/DVDs & komplexe Codecs (HEVC, VC1, MPEG2, WMV3) werden bevorzugt transkodiert, um native Playback-Probleme zu vermeiden

### FFmpeg Pipeline Test Suite
- Neue Media/Pipeline-Ansicht im Dashboard (Tests-Tab)
- FFmpegTestSuite im Backend prüft Remuxing (MKV→MP4) & HLS-Segmentierung
- "Vortrag"-Testfile als Standard für sofortige Validierung

### Premium Video-Player UI
- Status/Route-Info-Bar: Zeigt live den gewählten Pfad (DIRECT, TRANSCODE) & Quality Score (1-100)
- Dynamische Codec-Tags: Player zeigt H.264, AAC, HDR etc. nach Analyse direkt an
- Erweiterte Steuerung: Timeline & Seek-Buttons für alle Player-Modi optimiert

### Test-Erweiterungen
- Test-Media-Matrix: Synthetische Test-Patterns für verschiedene Codecs generierbar
- Anforderungen aus Logbuch 019 & 044 abgedeckt: DVDs & "wilde" Formate laufen jetzt stabil im Browser

**Spezifische Datei- oder DVD-ISO-Tests können direkt über die neue Pipeline gestartet werden.**

---

## 📀 DVD-Playback, Kontextmenü & UI-Optimierung (21.03.2026)

### DVD & ISO Standard-Playback
- DVDs (ISO/Ordner) & komplexe Codecs (HEVC, MPEG2, VC1) werden jetzt standardmäßig via Chrome Native (Transkodiert) im Browser abgespielt
- open_video wählt automatisch den Transcode-Pfad, außer bei expliziter Auswahl (z.B. VLC)

### Kontextmenü (Rechtsklick) im Library-Tab
- HTML für Kontextmenü neu implementiert
- Menü-Optionen:
  - 🚀 Chrome Native (Direkt/Transkodiert/Remuxed)
  - 💿 Disc-Optionen: VLC ISO, DVD-Ordner
  - 📺 Externe Player: System-VLC, MPV, FFplay
- handleContextMenuAction erkennt neue Transcode-Modi und wechselt automatisch zum Video-Tab

### Kein Downscrolling im Video-Tab
- overflow: hidden für Video-Tab
- Höhe via calc(100vh - 60px) fixiert, Player & Controls bleiben immer sichtbar

### "Öffnen mit" & VLC-Support
- VLC-Submenü: "VLC Extern (App)" startet Video direkt in System-VLC
- Player-Engine-Bar: Neuer Button für FFmpeg Transcode (MSE) zum manuellen Umschalten
- Intelligente Pfadwahl: Standard = Transcode im Browser, aber jederzeit Umschalten auf externe Player/Protokolle möglich

---

## 🚀 Bottom-Bar & Impressum-Modal (21.03.2026)

### Untere Statusleiste (Bottom-Bar)
- "DICT": Klick öffnet Telemetry Inspector Tab (Item-Dictionaries & Debug-Daten)
- "VSNC": Status-Indikator (Standard: VSNC: OK)
- "Impressum / imprint": Rechts verlinkt, öffnet Info-Modal

### Impressum-Modal
- Modal mit Inhalten aus i18n.json verknüpft
- Enthält technische Architektur (Python, Bottle, Eel), Features & rechtliche Hinweise (Entwickler, Standort, Datenschutz)

### Interaktivität & Steuerung
- toggleImpressum() & toggleDebugDict() am Dokumentende ergänzt
- CSS für .bottom-bar (24px, fixiert) wird korrekt genutzt
- Leiste sitzt fest unter Audio-Player-Footer, bietet geforderte Infos & Verknüpfungen

---

# Video Player Fixes & UI-Trace Diagnostics (21.03.2026)

## 🛠️ Key Improvements & Fixes

### JavaScript Stability
- **Duplicate Functions Removed:** Redundant window.jumpToChapter declarations (line 9325) removed; robust version at line 6700 retained.
- **Orphaned Variables:** Fixed re-initialization/shadowing of activeAudioPipeline.
- **DIV Balance Restored:** Nesting errors in "Quality Assurance" and "Reporting" tabs fixed; now 651 opening/651 closing tags for stable rendering.

### UI-Trace Debugging Suite
- **Failure Capture Interceptors:** Global initUiTraceHooks IIFE proxies alert, confirm, prompt; all popups logged to backend via eel.log_js_error().
- **Runtime Error Hijacking:** Global listeners for error and unhandledrejection send stack traces to backend logs.

### Simulated Failure & Verification Suite
- **Startup/Integrity Sub-Tab:** New 🐞 Simulate & Verify Failure Capture section with buttons to force ReferenceError, Promise Rejection, and test alert/confirm proxying. Enables manual and automated (Selenium) verification of error pipeline.

### Media Routing Test Suite (Reporting Tab)
- **Integrated Video Player Test Suite:** Native, VLC, WebM, FFmpeg, FragMP4 playback modes testable for any library item.
- **videoTestHistory:** Tracks result trends and initialization latency.

## 🧪 Verification
- **DIV Stability:** Verified by grep/count; balance is 0.
- **Trace Hooks:** Confirmed active in Chromium.
- **Routing Logic:** All backend triggers mapped to UI buttons.

---

## 🟢 Final: DVD-Playback Fix & Transcode-Integration (21.03.2026)

### Media Routing Logic
- get_play_source in src/core/main.py erkennt jetzt explizit DVD-Strukturen (VIDEO_TS-Ordner, .iso)
- Neuer "transcode"-Modus: Frontend erhält MSE-kompatiblen MP4-Stream via internen FFmpeg-Transcoder
- analyze_media empfiehlt optimalen Modus basierend auf Codec/Container-Analyse

### Frontend Integration
- playVideo in app.html erkennt/handhabt "transcode"-Modus
- addToQueue wiederhergestellt, Toasts für Analyse-Feedback
- Video-Tab: Höhe/Overflow optimiert, kein Scrollen mehr nötig

### Automated Test Suite
- test_dvd_playback.py prüft Routing für DVD-Ordner & .iso → Transcoder
- Test wird automatisch im Reporting/Tests-Tab integriert

### Reporting Dashboard
- Reporting-Tab trackt jetzt "Transcode"-Events neben Direct/VLC
- Dashboard zeigt Routing-Verteilung für gesamte Mediathek

### UI Polish & Footer
- Bottom-Bar modernisiert (dunkles Design)
- Live DICT VSNC-Status & RTT-Tracking im Footer
- Impressum/Imprint-Link sauber im neuen Footer integriert

**Alle DVD-basierten Medien werden jetzt direkt im Browser abgespielt. Testbar via Reporting → Tests → test_dvd_playback.**

---

## 🛠️ Dispatcher-Fixes & Tab-Fokus für DVD/ISO-Playback (21.03.2026)

### Dispatcher Logic (JS)
- isVideo-Erkennung im Playback-Entry-Point erweitert: Lokalisierte Kategorien wie 'Film', 'Abbild', 'Serie' etc. werden jetzt als Video erkannt
- DVDs/ISOs landen nicht mehr im Audio-Player, sondern korrekt im Video-Container

### Forced Tab Focusing (JS)
- playVideo ruft jetzt für alle Modi (Direct, HLS, Transcode) explizit switchTab('video', ...)
- UI springt immer direkt zum Video-Tab, auch bei Fallback/Transcode

### Smart Router & Path Resolution (Python)
- open_video_smart in src/core/main.py: MPEG-1/2 (PAL/NTSC-DVDs) werden jetzt korrekt an chrome_transcode statt VLC geroutet
- get_play_source nutzt resolve_media_path für konsistente Pfadbehandlung (absolut/relativ)
- DVD-Strukturen werden zuverlässig erkannt, unabhängig vom Indexierungsmodus

### Ergebnis
- Item List (Coverflow/Grid) & Playlist starten DVD-Medien jetzt immer im Video-Tab mit nativer Transcode-Wiedergabe
- test_dvd_playback.py: Alle DVD-bezogenen Tests erfolgreich

---

## 🟢 Final: "Going Raw" & Plain ISO Playback Fixes (21.03.2026)

### Plain ISO Identification
- is_playable in format_utils.py erkennt jetzt explizit .iso, .bin, .img als abspielbare Medien
- Auch "rohe" Disc-Images ohne Metadaten werden korrekt erkannt

### Automatische 'Film'-Kategorisierung
- MediaItem in models.py: Disc-Images werden standardmäßig als 'Film' klassifiziert, wenn kein anderes Tag vorhanden ist
- Items erscheinen korrekt in Video-Player-Filtern und Grids

### Dispatcher Routing (JS)
- isVideo-Check im Frontend erweitert: Kategorien wie 'Disk-Abbild', 'Abbild' werden als Video erkannt
- "Going Raw"-Items landen immer im playVideo-Flow

### Real-time Transcoding
- Backend routet Plain ISOs über /transcode/ (FFmpeg frag_mp4), Chrome spielt nativ ab

### Verifizierte Ergebnisse
| Item Type              | Category | Action     | Result                                 |
|------------------------|----------|------------|----------------------------------------|
| DVD Folder (VIDEO_TS)  | Film     | Click Play | ✅ Tab switch + Chrome Native Transcode |
| Plain ISO (movie.iso)  | Film     | Click Play | ✅ Tab switch + Chrome Native Transcode |
| Non-Movie ISO (raw.iso)| Abbild   | Click Play | ✅ Tab switch + Chrome Native Transcode |

**Kein manuelles Refresh nötig, aber für alte Items ggf. hilfreich.**

---

## ⏩ Seeking & Accurate Duration for DVD/ISO Transcoding (22.03.2026)

### Time-Offset Seeking
- /transcode/-Backend unterstützt jetzt ss-Parameter (Start-Seek): Bei Timeline-Sprung wird FFmpeg mit -ss neu gestartet
- Nahtloses Navigieren durch lange Medien möglich

### Accurate Film Length
- ffprobe_suite & analyze_media berechnen jetzt die Gesamtdauer (Sekunden) von DVD-Ordnern & Disc-Images
- Dauer wird vor Playback an das Frontend übergeben
- Video.js überschreibt Duration für Transcode-Streams, Timeline zeigt echte Filmlänge (z.B. 1h 45m)

### DVD Folder Analysis
- ffprobe_suite erkennt und analysiert verschachtelte .iso-Dateien in DVD-Ordnern, Metadaten werden korrekt gemeldet

### Verification Results
| Test Case         | Scenario              | Expected Behavior      | Result                |
|-------------------|----------------------|-----------------------|-----------------------|
| Duration Detection| DVD Folder with ISO  | Detect total seconds  | ✅ Detected (e.g. 5448s)|
| Timeline Display  | Start Playback       | Show full movie length| ✅ Full time shown     |
| Seeking           | Click midway on slider| Restart at offset    | ✅ Seek Successful     |
| Routing           | Plain .iso file      | Open in Chrome        | ✅ Native Playback     |

### Automated Testing
- tests/test_dvd_playback.py deckt alle neuen Features ab
- Testlauf: .venv_run/bin/python tests/test_dvd_playback.py

**DVDs & ISOs jetzt mit voller Timeline-Kontrolle und exakter Dauer im Browser!**

