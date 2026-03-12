## Streaming mit Chrome – Formate & Leistungsanforderungen

### Unterstützte Formate (Chrome)
- **Video:** H.264 (AVC) 8-bit, VP9, AV1
- **Audio:** AAC, MP3, Opus
- **Container:** MP4 (empfohlen), WebM, MKV (eingeschränkt)
- **Subtitles:** SRT, WebVTT

### Leistungsanforderungen
- **4K Streaming:**
  - H.264/MP4: Direct Play möglich, benötigt Gigabit-LAN (>25 Mbps)
  - HEVC/VP9: Transcoding im Browser, höhere CPU/GPU-Anforderung
- **CPU-Last:**
  - Remux mit MKVToolNix: keine Re-Encode, null CPU-Last
  - Transcoding (FFmpeg): hohe CPU/GPU-Last
- **RAM:**
  - Für große Dateien (>10 GB): Browser benötigt ausreichend RAM für Buffering

### Streaming in deiner App (Eel/Bottle)
- Nutzt HTML5 `<video>`-Tag, identisch mit Chrome-Standards
- Fokussiere H.264/AAC in MP4 für Direct Play
- CORS beachten (`crossorigin="anonymous"`), besonders bei NAS/Synology
- Codecs explizit angeben für Browser-Kompatibilität

### Beispiel-Code
```xml
<video id="player" controls crossorigin="anonymous">
  <source src="/stream/mp4/film.mp4" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'>
</video>
```

### Tipps & Fallbacks
- Remux zu MP4/H.264/AAC maximiert Direct Play
- ffprobe prüfen: `ffprobe -show_streams film.mp4`
- Fallback: HLS via FFmpeg für inkompatible Formate

### MKVToolNix vs. VLC für Streaming (4K MKV)

**MKVToolNix:**
- Ideal für Remux (MKV zu MP4/MKV) ohne Re-Encode – null CPU-Last.
- Perfekt für Direct Play: Container und Tracks bleiben unverändert, keine Qualitätsverluste.
- Batch-fähig, Docker-Image verfügbar, schnell für große Libraries.
- Kein Transcoding: Nur Container- und Track-Operationen.
- 4K MKV: Direct Play möglich, wenn Client (z. B. Chrome/Jellyfin) H.264/HEVC unterstützt und Netzwerk schnell genug (>25 Mbps).

**VLC:**
- Kann als Streaming-Server agieren (Transcoding, Live-Streams).
- Unterstützt viele Formate und Codecs, inkl. 4K MKV.
- Transcoding möglich, aber hohe CPU/GPU-Last.
- Für Direct Play weniger relevant, da meist als Player oder Server für komplexe Szenarien.

**Fazit:**
- Für Direct Play und schnelle Batch-Remux: MKVToolNix.
- Für native Wiedergabe im Chrome-Browser: Der integrierte HTML5-Player ist optimal für Direct Play (MP4/H.264/AAC), benötigt keine zusätzliche Software und nutzt Browser-Standards. Keine Transcoding-Last, volle Kompatibilität, ideal für Web-Apps und Eel/Bottle-Streaming.
 Für interaktives Streaming, Live-Transcoding oder Terminal-Steuerung: VLC bietet ein interaktives Terminal (z. B. für Live-Streams, Steuerung von Playlists, Echtzeit-Transcoding).
- 4K MKV-Streaming: MKVToolNix reicht, solange Client und Netzwerk passen.

### Direct Play mit MKVmerge

Mit MKVmerge (Teil von MKVToolNix) kannst du MKV-Dateien ohne Re-Encode remuxen und so Direct Play ermöglichen:
- Container und Tracks bleiben unverändert, keine Qualitätsverluste.
- MP4- oder MKV-Output ist direkt kompatibel mit Chrome/Jellyfin (sofern H.264/AAC oder HEVC/AAC enthalten).
- Ideal für Batch-Remux deiner Library – null CPU-Last, schnelle Verarbeitung.

**Beispiel:**
```bash
mkvmerge -o output.mp4 input.mkv
```

**Vorteile:**
- Direct Play in Browser und Jellyfin ohne Transcoding
- Maximale Performance, minimale Server-Last
- Kompatibel mit HTML5-Player

---

## Walkthrough – VLC und MKVToolNix Echtzeit-Streaming

### Backend Implementation
- Neue Funktionen in `main.py`:
  - `is_mkvtoolnix_available()`: Prüft, ob mkvmerge installiert ist.
  - `stream_to_vlc(file_path)`: Remuxed Dateien in Echtzeit und streamt direkt zu VLC (`mkvmerge <input> -o - | vlc -`).
  - `remux_mkv_batch(folder_path)`: Remuxed alle Nicht-MKV-Videos im Ordner zu MKV.
- API: Alle Funktionen via Eel für Frontend verfügbar.

### Frontend Enhancements
- UI-Update in `app.html`:
  - Modus-Auswahl Dropdown: Browser, VLC External, Direct Play.
  - "📦 Batch-Remux zu MKV"-Button im VLC Ribbon.
- Lokalisierung: Deutsche/Englische Strings in `web/i18n.json`.

### Dokumentation & Tests
- Logbuch: Eintrag `41 – VLC und MKVToolNix Echtzeit-Streaming` erstellt.
- Tests: `tests/test_vlc_mkv_streaming.py` prüft Pipeline und Batch-Logik (Mocks).

### Verification Results
- Unit Tests: 3 Tests in 0.005s, OK.

### How to use
- **Direct Play:** Modus "Direct Play (MKVmerge)" im Video Player Tab wählen, "In VLC öffnen" klicken – streamt ohne temporäre Daten.
- **Batch Remux:** Im VLC Ribbon "📦 Batch-Remux zu MKV" klicken, Ordner auswählen.

### Hinweis
- Da mkvtoolnix aktuell nicht installiert ist, erscheinen Fehler im UI, bis `sudo apt install mkvtoolnix` ausgeführt wurde.

---

### App-GUI Neustarten & Reset

**Neustart-Funktion:**
- Im UI kann ein "Neustart"-Button integriert werden, der die Eel/Bottle-App neu lädt (Frontend reload, Backend restart).
- Für einen Soft-Reset: Nur das Frontend (Browser-Tab) neu laden (`window.location.reload()`).
- Für einen Hard-Reset: Backend-Prozess neu starten (z. B. per API-Call, der `sys.exit()` auslöst und Supervisor/Script startet die App neu).

**Vorteile:**
- Behebt UI-Fehler, Session-Probleme und inkonsistente States.
- Hard-Reset setzt alle Sessions und Caches zurück.

**Implementierung:**
- Soft-Reset: JavaScript im Frontend.
- Hard-Reset: Backend-API, die den Prozess beendet und neu startet (z. B. via `os.execv` oder externes Script).

**Hinweis:**
- Nach Hard-Reset: Alle Nutzer müssen sich neu verbinden.
- Für Docker: `docker restart <container>` möglich.
